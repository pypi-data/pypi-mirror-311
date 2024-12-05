# arxml-parse

[![PyPI - Version](https://img.shields.io/pypi/v/arxml-parse.svg)](https://pypi.org/project/arxml-parse)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arxml-parse.svg)](https://pypi.org/project/arxml-parse)

The dataclasses in this library are created from xml schema files with the help
of the [xsdata](https://github.com/tefra/xsdata/) code generator.
As such, the library is fully compliant with `mypy --strict` type checking.

The `arxml_parse.io` module contains functions to parse arxml files and return
the xml root object (e.g. `arxml_parse.autosar_00042.autosar_00042.Autosar`).

## Installation

Install the library via `pip`::

```shell
   pip install arxml-parse
```


## Example

```python
from pathlib import Path

import arxml_parse.io

# parse arxml file
arxml_path = Path("random.arxml")
arxml_root_obj = arxml_parse.io.parse_arxml(arxml_path)

# serialize arxml
arxml_string = arxml_parse.io.serialize_arxml(arxml_root_obj)
```
