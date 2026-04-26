"""Sentence-level conversion for embedded dates, numbers, and currency amounts."""

from __future__ import annotations

import re

from nepali_date_numword.converter import number_to_words
from nepali_date_numword.date_converter import date_to_words

_DATE_PATTERN = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")
_CURRENCY_PREFIX_PATTERN = re.compile(
    r"(?<!\w)(?P<prefix>Rs\.?|NPR|रु\.?|रु)\s*(?P<amount>-?\d[\d,]*(?:\.\d+)?)"
)
_CURRENCY_SUFFIX_PATTERN = re.compile(
    r"(?<!\w)(?P<amount>-?\d[\d,]*(?:\.\d+)?)\s*(?P<suffix>रुपैयाँ|रुपैया|rupees?)\b",
    flags=re.IGNORECASE,
)
_NUMBER_PATTERN = re.compile(r"(?<![\w.-])(-?\d[\d,]*(?:\.\d+)?)(?![\w-])")
_BS_CONTEXT_PATTERN = re.compile(r"(BS|B\.S\.|Bikram Sambat|वि\.सं\.)", flags=re.IGNORECASE)
_AD_CONTEXT_PATTERN = re.compile(r"(AD|A\.D\.|Gregorian|सन्)", flags=re.IGNORECASE)


def _normalize_numeric_token(value: str) -> str:
    """Normalize comma-separated numeric tokens before conversion."""
    return value.replace(",", "")


def _detect_calendar_for_date(text: str, start: int, end: int) -> str:
    """Infer whether a matched ISO date token should be treated as AD or BS."""
    year = int(text[start:end].split("-", maxsplit=1)[0])
    context_before = text[max(0, start - 24):start]
    context_after = text[end:min(len(text), end + 24)]
    context = f"{context_before} {context_after}"

    if _BS_CONTEXT_PATTERN.search(context):
        return "BS"
    if _AD_CONTEXT_PATTERN.search(context):
        return "AD"
    if year > 2100:
        return "BS"
    return "AD"


def text_to_words(
    text: str,
    *,
    use_bs: bool = False,
    include_suffix: bool = True,
    short_dates: bool = False,
    detect_currency: bool = True,
) -> str:
    """Convert dates, numbers, and currency amounts embedded in free-form text."""
    converted = text

    if detect_currency:
        converted = _CURRENCY_PREFIX_PATTERN.sub(
            lambda match: number_to_words(
                _normalize_numeric_token(match.group("amount")),
                currency=True,
            ),
            converted,
        )
        converted = _CURRENCY_SUFFIX_PATTERN.sub(
            lambda match: number_to_words(
                _normalize_numeric_token(match.group("amount")),
                currency=True,
            ),
            converted,
        )

    date_replacements: list[tuple[str, str]] = []
    for index, match in enumerate(_DATE_PATTERN.finditer(converted)):
        token = match.group(1)
        calendar = _detect_calendar_for_date(converted, match.start(1), match.end(1))
        replacement = date_to_words(
            token,
            calendar=calendar,
            use_bs=use_bs if calendar == "AD" else False,
            include_suffix=include_suffix,
            short=short_dates,
        )
        placeholder = f"__NDATE_{index}__"
        date_replacements.append((placeholder, replacement))
        converted = converted.replace(token, placeholder, 1)

    converted = _NUMBER_PATTERN.sub(
        lambda match: number_to_words(_normalize_numeric_token(match.group(1))),
        converted,
    )

    for placeholder, replacement in date_replacements:
        converted = converted.replace(placeholder, replacement)

    return converted
