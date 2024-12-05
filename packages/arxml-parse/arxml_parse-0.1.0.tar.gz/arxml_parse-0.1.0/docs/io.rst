I/O functions
-------------

This module provides utility functions to parse ARXML files conforming to
different AUTOSAR schema versions. The input can be a file path, binary data,
or a binary file-like object. Each function parses a specific AUTOSAR schema version
and returns the corresponding parsed object.

Schema Compatibility
^^^^^^^^^^^^^^^^^^^^

The schema releases match the AUTOSAR standards as follows:

.. list-table:: AUTOSAR Schema Compatibility
   :widths: 20 40
   :header-rows: 1

   * - Schema
     - AUTOSAR Standard Release
   * - AUTOSAR_00042.xsd
     - AP Release 17-03 (covers CP 4.3.0, AP 17-03)
   * - AUTOSAR_00043.xsd
     - AP Release 17-10 (covers CP 4.3.0, AP 17-10)
   * - AUTOSAR_00044.xsd
     - CP Release 4.3.1 (covers CP 4.3.1, AP 17-10)
   * - AUTOSAR_00045.xsd
     - AP Release 18-03 (covers CP 4.3.1, AP 18-03)
   * - AUTOSAR_00046.xsd
     - CP Release 4.4.0/AP Release 18-10 (covers CP 4.4.0, AP 18-10)
   * - AUTOSAR_00047.xsd
     - AP Release 19-03 (covers CP 4.4.0, AP 19-03)
   * - AUTOSAR_00048.xsd
     - CP and AP Release 19-11 (covers 4.5.0)
   * - AUTOSAR_00049.xsd
     - CP and AP Release 20-11 (covers 4.6.0)
   * - AUTOSAR_00050.xsd
     - CP and AP Release 21-11 (covers 4.7.0)
   * - AUTOSAR_00051.xsd
     - CP and AP Release 22-11 (covers 4.8.0)
   * - AUTOSAR_00052.xsd
     - CP and AP Release 23-11 (covers 4.9.0)

API
^^^

.. automodule:: arxml_parse.io
