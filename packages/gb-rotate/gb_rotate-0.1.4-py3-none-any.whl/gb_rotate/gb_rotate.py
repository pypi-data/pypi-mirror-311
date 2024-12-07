def parse_genbank(file_path: str) -> tuple:
    """
    Parses a GenBank file into header, sequence, and features sections.

    Args:
        file_path (str): Path to the GenBank file.

    Returns:
        tuple: Tuple containing header, features section lines, and sequence.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    header = []
    features_section_lines = []
    sequence_lines = []
    inside_features_section = False
    inside_sequence_section = False

    for line in lines:
        if line.startswith("FEATURES"):
            inside_features_section = True
            inside_sequence_section = False
        elif line.startswith("ORIGIN"):
            inside_features_section = False
            inside_sequence_section = True
        elif line.startswith("//"):
            inside_sequence_section = False

        if inside_features_section:
            features_section_lines.append(line)
        elif inside_sequence_section:
            sequence_lines.append(line.strip())
        else:
            if not line.strip().startswith("//") and len(line.strip()) > 0:
                header.append(line)

    # Extract and clean the sequence
    sequence = "".join("".join(line.split()[1:]) for line in sequence_lines if line)
    return header, features_section_lines, sequence


def parse_features(features_section_lines: str) -> list:
    """
    Parses the FEATURES section to extract feature locations and metadata.

    Args:
        features_section_lines (list): List of lines from the FEATURES section.

    Returns:
        list: List of features with type, location, and qualifiers.
    """
    features = []
    current_feature = None

    for line in features_section_lines:
        if line.startswith(" " * 5) and not line.startswith(" " * 21):
            if current_feature:
                features.append(current_feature)

            parts = line.strip().split(maxsplit=1)
            feature_type = parts[0]
            feature_location = parts[1] if len(parts) > 1 else ""
            current_feature = {
                "type": feature_type,
                "location": feature_location,
                "qualifiers": {}
            }
        elif line.startswith(" " * 21):
            if "=" in line:
                key, value = line.strip().split("=", 1)
                current_feature["qualifiers"][key.strip()] = value.strip()
            else:
                if current_feature["qualifiers"]:
                    last_key = list(current_feature["qualifiers"].keys())[-1]
                    if last_key != "/translation":
                        current_feature["qualifiers"][last_key] += "\n" + (" " * 21) + line.strip()
                    else:
                        current_feature["qualifiers"][last_key] += " " + line.strip()
                else:
                    current_feature["qualifiers"]["note"] = line.strip()

    if current_feature:
        features.append(current_feature)
    return features


def transform_feature_location(og_location: str, sequence_length: int,
                               rotation_offset: int, reverse_complement: bool) -> str:
    """
    Transforms feature locations based on rotation and reverse complement while preserving the original format.
    Stores ranges in structured format before reconstructing the final string.

    Args:
        og_location (str): The original location string (e.g., "join(complement(>100..310),500..1300)").
        sequence_length (int): The length of the sequence.
        rotation_offset (int): The position to rotate around.
        reverse_complement (bool): Whether to apply reverse complement.

    Returns:
        str: Transformed location string in the original format.
    """
    def _rotate(pos: int) -> int:
        """
        Rotate a position around the sequence.

        Args:
            pos (int): The position to rotate.

        Returns:
            int: The rotated position.
        """
        if pos >= rotation_offset:
            return pos - rotation_offset
        else:
            return pos + (sequence_length - rotation_offset)


    def _parse_range(range_str: str, in_join: bool, in_complement: bool, range_pos: int) -> dict:
        """
        Parse a single range and store it in structured format.

        Args:
            range_str (str): The range string (e.g., "100..200").
            in_join (bool): Whether the range is within a join.
            in_complement (bool): Whether the range is within a complement.
            range_pos (int): The position of the range within the join or complement.

        Returns:
            dict: The structured range data.
        """
        start, end = range_str.split("..")
        start_uncertainty = start[0] if start[0] in "<>" else None
        end_uncertainty = end[0] if end[0] in "<>" else None
        start = int(start.lstrip("<>"))
        end = int(end.lstrip("<>"))
        return {
            "start": start,
            "end": end,
            "start_uncertainty": start_uncertainty if start_uncertainty else None,
            "end_uncertainty": end_uncertainty if end_uncertainty else None,
            "in_join": in_join,
            "in_complement": in_complement,
            "in_range_pos": range_pos,
        }


    def _transform_range(range_data: dict) -> dict:
        """
        Transform a range with rotation and optional reverse complement.

        Args:
            range_data (dict): The structured range data.

        Returns:
            dict: The transformed range data.
        """
        start = range_data["start"]
        end = range_data["end"]
        start = _rotate(start)
        end = _rotate(end)

        if reverse_complement:
            start, end = sequence_length - end + 1, sequence_length - start + 1
            range_data["in_complement"] = not range_data["in_complement"]

        range_data["start"] = start
        range_data["end"] = end

        return range_data


    def _recursive_bracket_parser(s: str, i: int, in_join: bool=False, in_complement: bool=False) -> tuple:
        """
        Recursively parse bracketed sections of the location string.

        Args:
            s (str): The location string.
            i (int): The current position in the string.
            in_join (bool): Whether the current section is within a join.
            in_complement (bool): Whether the current section is within a complement.

        Returns:
            tuple: The updated position and list of structured
        """
        ranges = []
        current_token = ""
        range_pos = 0

        while i < len(s):
            char = s[i]
            if char == '(':
                if current_token.strip() in {"join", "complement"}:
                    func_name = current_token.strip()
                    i, inner_ranges = _recursive_bracket_parser(
                        s,
                        i + 1,
                        in_join=(func_name == "join") or in_join,
                        in_complement=(func_name == "complement") ^ in_complement,
                    )
                    ranges.extend(inner_ranges)
                current_token = ""
            elif char == ')':
                if current_token.strip():
                    if ".." in current_token:
                        range_data = _parse_range(current_token.strip(), in_join, in_complement, range_pos)
                        ranges.append(range_data)
                        range_pos += 1
                return i + 1, ranges
            elif char == ',':
                if current_token.strip():
                    if ".." in current_token:
                        range_data = _parse_range(current_token.strip(), in_join, in_complement, range_pos)
                        ranges.append(range_data)
                        range_pos += 1
                current_token = ""
            else:
                current_token += char
            i += 1

        if current_token.strip():
            if ".." in current_token:
                range_data = _parse_range(current_token.strip(), in_join, in_complement, range_pos)
                ranges.append(range_data)

        return i, ranges


    def _format_range(r: dict) -> str:
        """
        Format a single range as a string.

        Args:
            r (dict): The structured range data.

        Returns:
            str: The formatted range string.
        """
        start = f"{r['start_uncertainty']}{r['start']}" if r[
            'start_uncertainty'] else f"{r['start']}"
        end = f"{r['end_uncertainty']}{r['end']}" if r[
            'end_uncertainty'] else f"{r['end']}"
        return f"{start}..{end}"


    def _reconstruct_location(ranges: list) -> str:
        """
        Reconstruct the location string using the structured ranges.

        Args:
            ranges (list): List of structured range data.

        Returns:
            str: The reconstructed location
        """
        ranges_str = ""
        in_complement = False
        in_join = False
        for r in ranges:
            if r["in_complement"] and not in_complement:
                ranges_str += "complement("
                in_complement = True
            if not r["in_complement"] and in_complement:
                ranges_str = ranges_str.rstrip(",")
                ranges_str += "),"
                in_complement = False
            if r["in_join"] and not in_join:
                ranges_str += "join("
                in_join = True
            if not r["in_join"] and in_join:
                ranges_str = ranges_str.rstrip(",")
                ranges_str += "),"
                in_join = False
            ranges_str += f"{_format_range(r)},"

        ranges_str = ranges_str.rstrip(",")
        ranges_str += ")" if in_join else ""
        ranges_str += ")" if in_complement else ""
        return ranges_str

    _, parsed_ranges = _recursive_bracket_parser(og_location, 0) # Parse and transform the original string
    transformed_ranges = sorted([_transform_range(r) for r in parsed_ranges], key=lambda r: r["start"]) # Transform all ranges
    new_location = _reconstruct_location(transformed_ranges) # Reconstruct the location string

    return new_location


def process_features(features: list, sequence_length: int, rotation_offset: int, reverse_complement: int) -> list:
    """
    Updates feature locations for rotation and reverse complement.

    Args:
        features (list): List of features with original locations.
        sequence_length (int): Length of the sequence.
        rotation_offset (int): Position to rotate around.
        reverse_complement (bool): Whether to apply reverse complement.

    Returns:
        list: Updated features with transformed locations.
    """
    updated_features = []
    for feature in features:
        if feature["type"] != "source":
            updated_location = transform_feature_location(
                feature["location"], sequence_length, rotation_offset, reverse_complement
            )
        else:
            updated_location = feature["location"]
        feature["location"] = updated_location
        updated_features.append(feature)
    return updated_features


def rotate_and_reverse_complement_sequence(sequence: str, rotation_offset: int, reverse_complement: bool) -> str:
    """
    Rotates and optionally reverse-complements the sequence.

    Args:
        sequence (str): The input sequence.
        rotation_offset (int): The position to rotate around.
        reverse_complement (bool): Whether to apply reverse complement.

    Returns:
        str: The rotated and/or reverse-complemented sequence.
    """
    if reverse_complement:
        complement = str.maketrans("ACGTacgt", "TGCAtgca")
        sequence = sequence.translate(complement)[::-1]
    rotated = sequence[rotation_offset:] + sequence[:rotation_offset]

    return rotated


def write_genbank(header: list, features: list, sequence: str, output_path: str) -> None:
    """
    Writes the updated GenBank file with modified features and sequence.

    Args:
        header (list): List of lines in the header.
        features (list): List of features with updated locations.
        sequence (str): The updated sequence.
        output_path (str): Path to write the output GenBank file

    Returns:
        None
    """

    def _format_translation(value: str) -> str:
        """
        Splits a translation qualifier value into lines at spaces, ensuring lines are indented.

        Args:
            value (str): The translation value.

        Returns:
            str: The formatted translation value.
        """
        max_line_length = 59
        lines = []
        while value:
            if len(value) <= max_line_length:
                lines.append(value)
                break
            split_idx = value[:max_line_length + 1].rfind(" ")
            if split_idx == -1:
                split_idx = max_line_length
            lines.append(value[:split_idx])
            value = value[split_idx + 1:]
        return "\n".join(f"{' ' * 21}/translation={line}" if i == 0
                         else f"{' ' * 21}{line}"
                         for i, line in enumerate(lines))

    with open(output_path, "w") as file:
        file.writelines(header)
        if not header[-1].strip().endswith("FEATURES"):
            file.write("FEATURES             Location/Qualifiers\n")

        for feature in features:
            file.write(f"     {feature['type']:<16}{feature['location']}\n")
            for key, value in feature["qualifiers"].items():
                if key == "/translation":
                    # Special handling for translation qualifier
                    file.write(_format_translation(value) + "\n")
                else:
                    file.write(f"                     {key}={value}\n")

        file.write("ORIGIN\n")
        for i in range(0, len(sequence), 60):
            line = f"{i + 1:<9}{' '.join(sequence[i:i+60][j:j+10] for j in range(0, 60, 10))}\n"
            file.write(line)
        file.write("//\n")


def process_genbank(file_path: str, output_path: str, rotation_offset: int, reverse_complement: bool) -> None:
    """
    Main function to process GenBank file: parse, transform, and write updated file.

    Args:
        file_path (str): Path to the input GenBank file.
        output_path (str): Path to write the output GenBank file.
        rotation_offset (int): Position to rotate around.
        reverse_complement (bool): Whether to apply reverse complement.

    Returns:
        None
    """
    header, features_section, sequence = parse_genbank(file_path)
    features = parse_features(features_section)
    sequence_length = len(sequence)

    updated_sequence = rotate_and_reverse_complement_sequence(sequence, rotation_offset, reverse_complement)
    updated_features = process_features(features, sequence_length, rotation_offset, reverse_complement)

    write_genbank(header, updated_features, updated_sequence, output_path)
