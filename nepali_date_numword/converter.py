"""Number to Nepali words conversion."""

from __future__ import annotations

from decimal import Decimal

from nepali_date_numword.constants import NEPALI_NUMBERS, NUMBER_SCALES
from nepali_date_numword.utils import normalize_decimal


def _integer_to_words(number: int) -> str:
    """Convert a non-negative integer into Nepali words."""
    if number in NEPALI_NUMBERS:
        return NEPALI_NUMBERS[number]

    if number < 1000:
        hundreds, remainder = divmod(number, 100)
        parts = [f"{_integer_to_words(hundreds)} सय"]
        if remainder:
            parts.append(_integer_to_words(remainder))
        return " ".join(parts)

    for scale_value, scale_name in NUMBER_SCALES:
        if number >= scale_value:
            quotient, remainder = divmod(number, scale_value)
            parts = [f"{_integer_to_words(quotient)} {scale_name}"]
            if remainder:
                parts.append(_integer_to_words(remainder))
            return " ".join(parts)

    raise ValueError("Unable to convert the provided number.")


def _decimal_to_words(number: Decimal) -> str:
    """Convert a Decimal into Nepali words without scientific notation."""
    normalized = format(number, "f")
    if "." not in normalized:
        return _integer_to_words(int(normalized))

    integer_part_text, fractional_text = normalized.split(".", maxsplit=1)
    fractional_text = fractional_text.rstrip("0")

    if not fractional_text:
        return _integer_to_words(int(integer_part_text))

    integer_words = _integer_to_words(int(integer_part_text))
    fractional_words = " ".join(_integer_to_words(int(digit)) for digit in fractional_text)
    return f"{integer_words} दशमलव {fractional_words}"


def number_to_words(
    number: int | float | Decimal | str,
    *,
    currency: bool = False,
    currency_word: str = "रुपैयाँ",
) -> str:
    """Convert a number into grammatically correct Nepali words.

    Parameters
    ----------
    number:
        Integer, float, Decimal, or numeric string to convert.
    currency:
        Append the given currency word when True.
    currency_word:
        Suffix appended when `currency=True`.
    """
    decimal_value = normalize_decimal(number)
    is_negative = decimal_value < 0
    if is_negative:
        decimal_value = abs(decimal_value)

    if decimal_value == decimal_value.to_integral_value():
        words = _integer_to_words(int(decimal_value))
    else:
        words = _decimal_to_words(decimal_value)

    if is_negative:
        words = f"माइनस {words}"

    if currency:
        words = f"{words} {currency_word}"

    return words
