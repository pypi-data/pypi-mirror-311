import argparse
from .core import FIXParser


def main():
    parser = argparse.ArgumentParser(description="Parse FIX messages and export to text and CSV formats.")
    parser.add_argument("--input", required=True, help="Path to the input file containing FIX messages.")
    parser.add_argument("--output", required=True, help="Path to the human-readable output text file.")
    parser.add_argument("--csv_output", required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    # Initialize the parser and run
    fix_parser = FIXParser(input_file=args.input, output_file=args.output, csv_output=args.csv_output)
    fix_parser.parse_and_export()