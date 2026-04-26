"""Gregorian and Bikram Sambat date wording utilities."""

from __future__ import annotations

from datetime import date as ad_date

from nepali_date_numword.constants import BS_MONTHS_NEPALI, GREGORIAN_MONTHS_NEPALI
from nepali_date_numword.converter import number_to_words
from nepali_date_numword.utils import DateInput, normalize_calendar_name, parse_date_input, to_nepali_digits


def _validate_month_day(month: int, day: int) -> None:
    """Validate a basic month/day tuple."""
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12.")
    if not 1 <= day <= 32:
        raise ValueError("day must be between 1 and 32.")


def _convert_ad_to_bs(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a Gregorian date to a BS date using the runtime dependency."""
    try:
        import bsdatetime as bs  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "AD to BS conversion requires the 'bsdatetime' package to be installed."
        ) from exc

    return bs.ad_to_bs(ad_date(year, month, day))


def _format_words(
    year: int,
    month: int,
    day: int,
    *,
    calendar: str,
    include_suffix: bool,
) -> str:
    """Format a parsed date tuple into Nepali words."""
    month_name = (
        GREGORIAN_MONTHS_NEPALI[month]
        if calendar == "AD"
        else BS_MONTHS_NEPALI[month]
    )
    prefix = "सन्" if calendar == "AD" else "वि.सं."
    suffix_word = "तारिख" if calendar == "AD" else "गते"
    suffix = f" {suffix_word}" if include_suffix else ""
    return (
        f"{prefix} {number_to_words(year)} {month_name} "
        f"{number_to_words(day)}{suffix}"
    )


def _format_short(year: int, month: int, day: int, *, calendar: str) -> str:
    """Format a date using Nepali digits and localized month names."""
    month_name = (
        GREGORIAN_MONTHS_NEPALI[month]
        if calendar == "AD"
        else BS_MONTHS_NEPALI[month]
    )
    return f"{to_nepali_digits(day)} {month_name} {to_nepali_digits(year)}"


def date_to_words(
    value: DateInput,
    *,
    calendar: str = "AD",
    use_bs: bool = False,
    include_suffix: bool = True,
    short: bool = False,
) -> str:
    """Convert Gregorian or Bikram Sambat dates into Nepali words.

    Parameters
    ----------
    value:
        ISO string, date/datetime object, or `(year, month, day)` tuple.
    calendar:
        Input calendar type, either `"AD"` or `"BS"`.
    use_bs:
        When True, convert AD input into BS before formatting.
    include_suffix:
        Append `गते` for word output.
    short:
        Return a compact form like `१५ जनवरी २०२४`.
    """
    calendar_name = normalize_calendar_name(calendar)
    year, month, day = parse_date_input(value)
    _validate_month_day(month, day)

    if calendar_name == "AD":
        ad_date(year, month, day)
        if use_bs:
            year, month, day = _convert_ad_to_bs(year, month, day)
            calendar_name = "BS"
    elif use_bs:
        raise ValueError("use_bs=True is only valid when the input calendar is 'AD'.")

    if short:
        return _format_short(year, month, day, calendar=calendar_name)

    return _format_words(
        year,
        month,
        day,
        calendar=calendar_name,
        include_suffix=include_suffix,
    )
