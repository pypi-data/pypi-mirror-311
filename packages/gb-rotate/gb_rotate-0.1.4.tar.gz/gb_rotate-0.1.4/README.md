# gb_rotate
[![](https://img.shields.io/pypi/v/gb_rotate.svg)](https://pypi.org/project/typer/)
[![](https://img.shields.io/pypi/pyversions/gb_rotate.svg)](https://pypi.org/project/typer/)
[![](https://img.shields.io/pypi/l/gb_rotate.svg)](https://pypi.org/project/typer/)

A basic Python for rotating and reverse complementing GenBank files based on a numerical offset. This tool updates feature annotations to ensure consistency with the transformed sequence. Intended for personal use and originally developed for rotating plastid genomes.

### Features
- Rotate GenBank sequences around a specified offset.
- Reverse complement sequences and update annotations accordingly.
- Compatible with GenBank formatting, preserving header and feature details.

## Installation
### From PyPI
```
pip install gb_rotate
```

### From repository
1. Clone the repository:
```
git clone https://github.com/kherronism/gb_rotate.git
```
2. Build and install locally:
```
cd gb_rotate
pip install .
```

## Usage
### Basic usage
After installation, use the `gb_rotate` command:
```
gb_rotate -i <input_file> -o <output_file> -r <rotation_offset> -c
```
### Options
| Option | Description |
| ------ | ----------- |
| -i, --input-file  | Path to the input GenBank file (required). |
| -o, --output-file | Path to the output GenBank file (required). |
| -r, --rotation-offset | Rotation offset position (default: 0). |
| -rc, --reverse-complement	| Reverse complement the sequence (optional). |
### Examples
#### Rotate only
Rotations should be in the range of 0 to the sequence length. With a rotation_offset of 1000, the first position in the sequence will be the 1001st position in the output.

Rotate a sequence around offset 50000 and save the result:
```
gb_rotate -i example.gb -o example_rotated.gb -r 50000
```
#### Reverse Complement only
Reverse complement a sequence and save the result:
```
gb_rotate -i example.gb -o example_rc.gb -rc
```
### Combine both
When combining, the reverse complement operation takes place first, followed by the rotation, therefore the offset is applied to the reverse complemented sequence.

Combine both operations:
```
gb_rotate -i example.gb -o example_modified.gb -r 50000 -rc
```

