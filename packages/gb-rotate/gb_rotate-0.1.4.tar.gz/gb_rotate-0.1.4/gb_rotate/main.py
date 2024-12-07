import typer
from .gb_rotate import process_genbank


def main(
    input_file: str = typer.Option(..., "-i", "--input-file", help="Path to the input GenBank file."),
    output_file: str = typer.Option(..., "-o", "--output-file", help="Path to the output GenBank file."),
    rotation_offset: int = typer.Option(0, "-r", "--rotation-offset", help="Position to rotate around (0 for no rotation)."),
    reverse_complement: bool = typer.Option(False, "-c", "--reverse-complement", help="Whether to apply reverse complement."),
) -> None:
    """
    Basic utility for rotating and reverse complementing GenBank files. Sequence is reverse complemented, if specified, and then rotated.

    Example:
        gb_rotate -i input.gb -o output.gb -r 100 -r
    """
    typer.echo(f"Processing GenBank file: {input_file}")
    process_genbank(input_file, output_file, rotation_offset, reverse_complement)
    typer.echo(f"Output written to: {output_file}")

def cli():
    typer.run(main)

if __name__ == "__main__":
    cli()