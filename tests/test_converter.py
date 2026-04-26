from decimal import Decimal

import pytest

from nepali_date_numword import number_to_words, text_to_words


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, "शून्य"),
        (1, "एक"),
        (15, "पन्ध्र"),
        (23, "तेइस"),
        (99, "उनान्सय"),
        (100, "एक सय"),
        (123, "एक सय तेइस"),
        (1000, "एक हजार"),
        (100000, "एक लाख"),
        (123456, "एक लाख तेइस हजार चार सय छप्पन्न"),
        (10000000, "एक करोड"),
        (1000000000, "एक अरब"),
        (-12, "माइनस बाह्र"),
    ],
)
def test_number_to_words(value, expected):
    assert number_to_words(value) == expected


def test_float_conversion():
    assert number_to_words(12.5) == "बाह्र दशमलव पाँच"


def test_decimal_string_conversion():
    assert number_to_words("1001.05") == "एक हजार एक दशमलव शून्य पाँच"


def test_currency_suffix():
    assert number_to_words(123, currency=True) == "एक सय तेइस रुपैयाँ"


def test_decimal_input():
    assert number_to_words(Decimal("50.25")) == "पचास दशमलव दुई पाँच"


def test_text_to_words_with_number():
    assert text_to_words("Room 12 is ready.") == "Room बाह्र is ready."


def test_text_to_words_with_currency_prefix():
    assert (
        text_to_words("I paid Rs. 123 yesterday.")
        == "I paid एक सय तेइस रुपैयाँ yesterday."
    )


def test_text_to_words_with_currency_suffix():
    assert (
        text_to_words("Total due is 500 रुपैयाँ.")
        == "Total due is पाँच सय रुपैयाँ."
    )


def test_text_to_words_with_date_and_number():
    assert (
        text_to_words("Meeting on 2024-01-15 at room 12.")
        == "Meeting on सन् दुई हजार चौबीस जनवरी पन्ध्र तारिख at room बाह्र."
    )


def test_text_to_words_with_bs_context():
    assert (
        text_to_words("BS date 2080-10-01 is official.")
        == "BS date वि.सं. दुई हजार अस्सी माघ एक गते is official."
    )


def test_text_to_words_with_ad_to_bs_conversion():
    assert (
        text_to_words("Due date is 2024-01-15.", use_bs=True)
        == "Due date is वि.सं. दुई हजार अस्सी माघ एक गते."
    )


def test_text_to_words_with_mixed_ad_and_bs_dates():
    assert (
        text_to_words("Meeting on 2024-01-15 and BS date 2080-10-01.")
        == "Meeting on सन् दुई हजार चौबीस जनवरी पन्ध्र तारिख and BS date वि.सं. दुई हजार अस्सी माघ एक गते."
    )
