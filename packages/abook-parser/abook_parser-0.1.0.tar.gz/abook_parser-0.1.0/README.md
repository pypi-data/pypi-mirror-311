# abook_parser

parser for the [abook](https://abook.sourceforge.io/) CLI

## Installation

Requires `python3.12+`

To install with pip, run:

```
pip install git+https://github.com/purarue/abook_parser
```

## Usage

This can read the addressbook, sort it by some key, and print a formatted version (either `JSON` or the `abook` addressbook format).

```
Usage: abook_parser parse [OPTIONS] FILE

  Parse the addressbook file, and sort it by the name field

Options:
  -t, --output-type [abook|json]  output format type
  -k, --sort-key TEXT             sort addressbook items by key
  -o, --output PATH               output file path
  --help                          Show this message and exit.
```

It also has commands to `add` or `edit` and item with a [`fzf`](https://github.com/junegunn/fzf)-based interactive mode.

```
Usage: abook_parser edit [OPTIONS] FILE

  Edit a field in the addressbook file

Options:
  --ignore-case / --no-ignore-case
                                  ignore case in query
  -q, --query TEXT                query string to search for
  --help                          Show this message and exit.
```

### Tests

```bash
git clone 'https://github.com/purarue/abook_parser'
cd ./abook_parser
pip install '.[testing]'
pytest
flake8 ./abook_parser
mypy ./abook_parser
```
