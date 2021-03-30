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

ColumnNameNotFoundError (from :class:`SQLAthanorError`)
--------------------------------------------------------------------

.. autoclass:: ColumnNameNotFoundError

----------------

InvalidDataFormatError (from :class:`SQLAthanorError`)
----------------------------------------------------------

.. autoclass:: InvalidDataFormatError

----------------

InvalidLayoutError (from :class:`SQLAthanorError`)
-------------------------------------------------------

.. autoclass:: InvalidLayoutError
