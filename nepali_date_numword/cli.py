"""Command-line interface for nepali-date-numword."""

from __future__ import annotations

import argparse
from typing import Sequence

from nepali_date_numword.converter import number_to_words
from nepali_date_numword.date_converter import date_to_words
from nepali_date_numword.text_converter import text_to_words


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="nepali-date-numword",
        description="Convert numbers and dates into Nepali words.",
    )
    parser.add_argument("value", nargs="?", help="Numeric value to convert.")
    parser.add_argument("--date", dest="date_value", help="Date in YYYY-MM-DD format.")
    parser.add_argument("--text", dest="text_value", help="Convert dates and numbers inside a sentence.")
    parser.add_argument(
        "--calendar",
        choices=["AD", "BS"],
        default="AD",
        help="Calendar system of the provided --date input.",
    )
    parser.add_argument(
        "--bs",
        action="store_true",
        help="Convert Gregorian input date to Bikram Sambat output.",
    )
    parser.add_argument(
        "--currency",
        action="store_true",
        help="Append the Nepali currency suffix.",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help="Use compact date formatting with Nepali digits.",
    )
    parser.add_argument(
        "--no-suffix",
        action="store_true",
        help="Do not append गते to word-based date output.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and print the converted result."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.date_value:
        result = date_to_words(
            args.date_value,
            calendar=args.calendar,
            use_bs=args.bs,
            include_suffix=not args.no_suffix,
            short=args.short,
        )
        print(result)
        return 0

    if args.text_value:
        result = text_to_words(
            args.text_value,
            use_bs=args.bs,
            include_suffix=not args.no_suffix,
            short_dates=args.short,
            detect_currency=True,
        )
        print(result)
        return 0

    if args.value is None:
        parser.error("Provide a numeric value, use --date, or use --text.")

    result = number_to_words(args.value, currency=args.currency)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
