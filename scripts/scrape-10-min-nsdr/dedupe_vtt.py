# Cleans a VTT file into line-by-line text, removing duplicate lines
# Source https://stackoverflow.com/a/67253885
# Modified to take inout file path & output file path as args $1 and $2
# Example usage:
# python3 dedupe_vtt.py "path_to_your_input_file.vtt" "path_to_your_output_file.deduped.txt"

from pathlib import Path
from typing import Generator
import webvtt
import argparse

def vtt_lines(src) -> Generator[str, None, None]:
    """
    Extracts all text lines from a vtt file which may contain duplicates

    :param src: File path or file like object
    :return: Generator for lines as strings
    """
    vtt = webvtt.read(src)

    for caption in vtt:  # type: webvtt.structures.Caption
        # A caption which may contain multiple lines
        for line in caption.text.strip().splitlines():  # type: str
            # Process each one of them
            yield line

def deduplicated_lines(lines) -> Generator[str, None, None]:
    """
    Filters all duplicated lines from list or generator

    :param lines: iterable or generator of strings
    :return: Generator for lines as strings without duplicates
    """
    last_line = ""
    for line in lines:
        if line == last_line:
            continue

        last_line = line
        yield line

def vtt_to_linear_text(input_file, output_file, line_end="\n"):
    """
    Converts a vtt caption file to linear text.

    :param input_file: Path to an existing vtt file
    :param output_file: Path to save content in
    :param line_end: Default to line break. May be set to a space for a single line output.
    """
    with output_file.open("w") as writer:
        for line in deduplicated_lines(vtt_lines(str(input_file))):
            writer.write(line.replace("&nbsp;", " ").strip() + line_end)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert VTT file to linear text and remove duplicate lines.")
    parser.add_argument("input_file", type=Path, help="Input VTT file path")
    parser.add_argument("output_file", type=Path, help="Output file path")
    args = parser.parse_args()
    print('\n\n')
    print('input file: ', args.input_file)
    print('input file: ', type(args.input_file))
    print('output file: ', args.output_file)
    print('output file: ', type(args.output_file))
    print('\n\n')
    vtt_to_linear_text(args.input_file, args.output_file)

