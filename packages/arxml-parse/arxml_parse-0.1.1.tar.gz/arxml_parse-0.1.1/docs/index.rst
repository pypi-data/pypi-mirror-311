arxml-parse documentation
=========================

The dataclasses in this library are created from xml schema files with the help
of the `xsdata <https://github.com/tefra/xsdata/>`__ code generator.
As such, the library is fully compliant with `mypy --strict` type checking.

The `arxml_parse.io` module contains functions to parse arxml files and return
the xml root object (e.g. :class:`~arxml_parse.autosar_00042.Autosar`).

Installation
------------

Install the library via `pip`::

    $ pip install arxml-parse

Example
-------

    >>> from pathlib import Path
    >>> import arxml_parse
    ...
    >>> arxml_path = Path("random.arxml")
    >>> root = arxml_parse.io.parse_arxml(arxml_path)


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   io
   autosar_00042
   autosar_00043
   autosar_00044
   autosar_00045
   autosar_00046
   autosar_00047
   autosar_00048
   autosar_00049
   autosar_00050
   autosar_00051
   autosar_00052
