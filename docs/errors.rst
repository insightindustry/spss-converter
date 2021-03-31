**********************************
Error Reference
**********************************

.. module:: spss_converter.errors

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Handling Errors
=================

Stack Traces
--------------

Because the **SPSS Converter** produces exceptions which inherit from the
standard library, it leverages the same API for handling stack trace information.
This means that it will be handled just like a normal exception in unit test
frameworks, logging solutions, and other tools that might need that information.

------------------

SPSS Converter Errors
========================

SPSSConverterError (from :class:`ValueError <python:ValueError>`)
--------------------------------------------------------------------

.. autoclass:: SPSSConverterError

----------------

ColumnNameNotFoundError (from :class:`SPSSConverterError`)
--------------------------------------------------------------------

.. autoclass:: ColumnNameNotFoundError

----------------

InvalidDataFormatError (from :class:`SPSSConverterError`)
----------------------------------------------------------

.. autoclass:: InvalidDataFormatError

----------------

InvalidLayoutError (from :class:`SPSSConverterError`)
-------------------------------------------------------

.. autoclass:: InvalidLayoutError
