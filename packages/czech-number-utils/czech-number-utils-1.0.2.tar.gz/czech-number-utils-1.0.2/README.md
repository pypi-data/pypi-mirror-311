# Czech Number Utilities

Czech Number Utilities is a Python module for converting numbers into their textual representations in Czech, both cardinal and ordinal forms. It supports grammatical cases and handles large numbers up to billions.

## Features

- Convert numbers to Czech cardinal and ordinal forms.
- Handles complex numbers like millions and billions.
- Supports grammatical rules specific to Czech.

## Installation

You can install the package directly from PyPI:

```bash
pip install czech-number-utils
```

## Usage

```python
from czech_number_utils import number_to_czech_word, number_to_czech_ordinal

# Cardinal numbers
print(number_to_czech_word(1379))  # Output: "tisíc tři sta sedmdesát devět"

# Ordinal numbers
print(number_to_czech_ordinal(23))  # Output: "dvacátý třetí"
```

## Contributing

Contributions are welcome! Please submit issues or pull requests on the [GitHub repository](https://github.com/zbyso23/czech-number-utils).

## License

This project is licensed under the MIT License. See the LICENSE file for details.