"""Command-line interface for the Prompt File Format Formatter."""

import sys
from pathlib import Path

import rich_click as click


@click.command(
    help=(
        "Prompt File Format Formatter takes care of outputting your file's "
        "content so that they can easily be prompted to a LLM"
    )
)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def main(files):
    """Process and print the contents of the given files."""
    for file in (Path(f) for f in files):
        # We're using sys.stdout.write() instead of print() to avoid the T201 error
        # while still outputting the desired content
        sys.stdout.write(f"`{file}`\n\n")
        sys.stdout.write("```\n")
        sys.stdout.write(file.read_text().rstrip("\n") + "\n")
        sys.stdout.write("```\n\n")
