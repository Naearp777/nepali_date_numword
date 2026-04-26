# nepali-date-numword

`nepali-date-numword` converts numbers and dates into grammatically correct Nepali words.
It supports Nepali number wording, Gregorian date wording, Bikram Sambat date wording,
currency suffixes, negative values, floats, and a small CLI for everyday use.

## Features

- Convert integers using the Nepali numbering system: `सय`, `हजार`, `लाख`, `करोड`, `अरब`
- Handle irregular Nepali values from `0` to `100`
- Support negative numbers and floating-point values
- Add currency suffixes like `रुपैयाँ`
- Convert Gregorian dates into Nepali words
- Convert Bikram Sambat dates into Nepali words
- Convert AD dates to BS output with `use_bs=True`
- Provide CLI support for numbers and dates

## Installation

```bash
pip install nepali-date-numword
```

Python 3.10 or newer is required.

For local development:

```bash
pip install -e .[dev]
```

## Quick Usage

```python
from datetime import date

from nepali_date_numword import date_to_words, number_to_words, text_to_words

print(number_to_words(123))
# एक सय तेइस

print(number_to_words(-12.5))
# माइनस बाह्र दशमलव पाँच

print(number_to_words(123, currency=True))
# एक सय तेइस रुपैयाँ

print(date_to_words("2024-01-15", calendar="AD"))
# सन् दुई हजार चौबीस जनवरी पन्ध्र गते

print(date_to_words("2080-10-01", calendar="BS"))
# वि.सं. दुई हजार अस्सी माघ एक गते

print(date_to_words(date(2024, 1, 15), calendar="AD", use_bs=True))
# वि.सं. दुई हजार अस्सी माघ एक गते

print(date_to_words("2024-01-15", short=True))
# १५ जनवरी २०२४

print(text_to_words("I paid Rs. 123 on 2024-01-15."))
# I paid एक सय तेइस रुपैयाँ on सन् दुई हजार चौबीस जनवरी पन्ध्र गते.
```

## API

### `number_to_words(number, currency=False)`

Convert an integer or floating-point value into Nepali words.

Examples:

```python
number_to_words(0)
number_to_words(100000)
number_to_words(12.5)
number_to_words(123, currency=True)
```

### `date_to_words(value, calendar="AD", use_bs=False, short=False)`

Convert a Gregorian or Bikram Sambat date into Nepali words.

Accepted input forms:

- ISO string: `"2024-01-15"`
- `datetime.date` or `datetime.datetime`
- Tuple: `(2024, 1, 15)`

Examples:

```python
date_to_words("2024-01-15", calendar="AD")
date_to_words("2080-10-01", calendar="BS")
date_to_words((2024, 1, 15), calendar="AD", use_bs=True)
```

### `text_to_words(text, use_bs=False, include_suffix=True, short_dates=False)`

Convert mixed sentences by detecting:

- ISO dates such as `2024-01-15`
- plain numbers such as `123` or `12.5`
- currency patterns such as `Rs. 500`, `NPR 500`, or `500 रुपैयाँ`

Example:

```python
text_to_words("Invoice total is Rs. 123 and due on 2024-01-15.")
```

## CLI

```bash
nepali-date-numword 123
nepali-date-numword --currency 123
nepali-date-numword --date 2024-01-15
nepali-date-numword --date 2024-01-15 --bs
nepali-date-numword --date 2080-10-01 --calendar BS
nepali-date-numword --date 2024-01-15 --short
nepali-date-numword --text "I paid Rs. 123 on 2024-01-15."
```

## Development

Run tests with:

```bash
pytest
```

## Notes

- `use_bs=True` converts Gregorian input into Bikram Sambat output.
- BS formatting works directly for explicit BS input such as `2080-10-01`.
- The package keeps `bsdatetime` as a runtime dependency so installed distributions can do AD-to-BS conversion accurately.

## License

MIT
