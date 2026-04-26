"""Utility helpers shared by the package."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Tuple

from nepali_date_numword.constants import NEPALI_DIGITS

DateInput = str | date | datetime | tuple[int, int, int]


def to_nepali_digits(value: int | str) -> str:
    """Convert Latin digits in *value* to Nepali digits."""
    return str(value).translate(NEPALI_DIGITS)


def normalize_decimal(value: int | float | Decimal | str) -> Decimal:
    """Return a Decimal built from a safe string representation."""
    return Decimal(str(value))


def parse_date_input(value: DateInput) -> Tuple[int, int, int]:
    """Parse supported date input types into a `(year, month, day)` tuple."""
    if isinstance(value, datetime):
        return value.year, value.month, value.day

    if isinstance(value, date):
        return value.year, value.month, value.day

    if isinstance(value, tuple):
        if len(value) != 3:
            raise ValueError("Date tuple must be in the form (year, month, day).")
        year, month, day = value
        return int(year), int(month), int(day)

    if isinstance(value, str):
        parts = value.split("-")
        if len(parts) != 3:
            raise ValueError("Date string must use ISO format YYYY-MM-DD.")
        year, month, day = (int(part) for part in parts)
        return year, month, day

    raise TypeError(
        "Unsupported date input. Use ISO string, datetime/date object, or (year, month, day)."
    )


def normalize_calendar_name(calendar: str) -> str:
    """Normalize the calendar label to AD or BS."""
    normalized = calendar.strip().upper()
    if normalized not in {"AD", "BS"}:
        raise ValueError("calendar must be either 'AD' or 'BS'.")
    return normalized
