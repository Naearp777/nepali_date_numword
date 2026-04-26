from datetime import date, datetime

import pytest

from nepali_date_numword import date_to_words


def test_gregorian_date_to_words():
    assert (
        date_to_words("2024-01-15", calendar="AD")
        == "सन् दुई हजार चौबीस जनवरी पन्ध्र तारिख"
    )


def test_bs_date_to_words():
    assert (
        date_to_words("2080-10-01", calendar="BS")
        == "वि.सं. दुई हजार अस्सी माघ एक गते"
    )


def test_short_date_format():
    assert date_to_words("2024-01-15", short=True) == "१५ जनवरी २०२४"


def test_tuple_input_and_suffix_toggle():
    assert (
        date_to_words((2080, 10, 1), calendar="BS", include_suffix=False)
        == "वि.सं. दुई हजार अस्सी माघ एक"
    )


def test_datetime_input():
    value = datetime(2024, 1, 15, 10, 30, 0)
    assert date_to_words(value, calendar="AD") == "सन् दुई हजार चौबीस जनवरी पन्ध्र तारिख"


def test_date_object_input():
    assert date_to_words(date(2024, 1, 15), calendar="AD", short=True) == "१५ जनवरी २०२४"


def test_use_bs_from_gregorian_when_dependency_available():
    pytest.importorskip("bsdatetime")
    assert (
        date_to_words("2024-01-15", calendar="AD", use_bs=True)
        == "वि.सं. दुई हजार अस्सी माघ एक गते"
    )


def test_invalid_calendar_name():
    with pytest.raises(ValueError):
        date_to_words("2024-01-15", calendar="CE")


def test_use_bs_not_allowed_for_bs_input():
    with pytest.raises(ValueError):
        date_to_words("2080-10-01", calendar="BS", use_bs=True)
