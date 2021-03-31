**********************************
Using the SPSS Converter
**********************************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

.. _introduction:

Introduction
==========================================================

The **SPSS Converter** library is a simple wrapper around the
`Pyreadstat <https://github.com/Roche/pyreadstat>`_ and
`Pandas <https://pandas.pydata.org>`_ libraries that provides a clean and simple API for
reading data files in a variety of formats and converting them to a variety of formats.
The semantics are super simple, and should be as simple as: ``spss_converter.to_csv('my-spss-file.sav')``
or ``spss_converter.from_json('my-json-file.json')``.

-----------

Converting Data from SPSS
============================================================

To read from SPSS files and convert them to a different format you can use functions whose
names start with ``spss_converter.to_*``. The examples below provide specifics:

Converting to Pandas DataFrame
--------------------------------

To convert from an SPSS file to a `Pandas <https://pandas.pydata.org>`_
:class:`DataFrame <pandas:pandas.DataFrame>`, simply call the
:func:`to_dataframe() <spss_converter.read.to_dataframe>` function:

.. code-block:: python

  import spss_converter

  df, metadata = spss_converter.to_dataframe('my-spss-file.sav')

The code above will read your data from the file ``my-spss-file.sav``, convert it into a
`Pandas <https://pandas.pydata.org>`_ :class:`DataFrame <pandas:pandas.DataFrame>`, and
generate an :class:`spss_converter.Metadata` representation of the SPSS file's meta-data,
which includes its data map, labeling, etc.

.. seealso::

  * :func:`to_dataframe() <spss_converter.read.to_dataframe>`

Converting to CSV
-----------------------

To read data from an SPSS file and convert it into a CSV file, simply call the
:func:`to_csv() <spss_converter.read.to_csv>` function:

.. code-block:: python

  import spss_converter

  as_csv = spss_converter.to_csv('my-spss-file.sav')
  # Will store the contents of the CSV as a string in as_csv.

  spss_converter.to_csv('my-spss-file.sav', target = 'my-csv-file.csv')
  # Will save the CSV data to the file my-csv-file.csv.

Both lines of code above will read the SPSS data from ``my-spss-file.sav``, but the first
line will store it in the :class:`str <python:str>` variable ``as_csv``. The second will
instead write it to the file ``my-csv-file.csv``.

.. seealso::

  * :func:`to_csv() <spss_converter.read.to_csv>`

Converting to JSON
-----------------------

To read data from an SPSS file and convert it into a JSON object, simply call the
:func:`to_json() <spss_converter.read.to_json>` function:

.. tabs::

  .. tab:: As Records (default)

    .. code-block:: python

      import spss_converter

      as_json = spss_converter.to_json('my-spss-file.sav', layout = 'records')
      # Stores the JSON data as a string in the variable as_json.

      spss_converter.to_json('my-spss-file.sav',
                             target = 'my-json-file.json',
                             layout = 'records')
      # Stores the JSON data in the file "my-json-file.json".

  .. tab:: As Table

    .. code-block:: python

      import spss_converter

      as_json = spss_converter.to_json('my-spss-file.sav', layout = 'table')
      # Stores the JSON data as a string in the variable as_json.

      spss_converter.to_json('my-spss-file.sav',
                             target = 'my-json-file.json',
                             layout = 'table')
      # Stores the JSON data in the file "my-json-file.json".

The **SPSS Converter** supports two different layouts for JSON representation of data:

  * **Records**. This layout returns a JSON collection (array) of JSON objects. Each
    object in the collection represents one record from the SPSS file. The object is a
    a set of key/value pairs where each key represents a variable/column in the SPSS file
    and its value represents the value of that variable/column for that respondent. This
    is the default layout.
  * **Table**. This layout returns a JSON object that includes a ``schema`` with the data
    map, and a separate ``data`` key which contains a collection (array) of objects where
    each object represents a single record from the SPSS data file.

.. note::

  If no ``target`` is supplied, then the JSON representation is stored in-memory in the
  return value. If a ``target`` is supplied, then the JSON representation will be written
  to this file.

.. seealso::

  * :func:`to_json() <spss_converter.read.to_json>`

Converting to YAML
-----------------------

To read data from an SPSS file and convert it into a YAML object, simply call the
:func:`to_yaml() <spss_converter.read.to_yaml>` function:

.. tabs::

  .. tab:: As Records (default)

    .. code-block:: python

      import spss_converter

      as_yaml = spss_converter.to_yaml('my-spss-file.sav', layout = 'records')
      # Stores the YAML data as a string in the variable as_yaml.

      spss_converter.to_yaml('my-spss-file.sav',
                             target = 'my-yaml-file.yaml',
                             layout = 'records')
      # Stores the YAML data in the file "my-yaml-file.yaml".

  .. tab:: As Table

    .. code-block:: python

      import spss_converter

      as_yaml = spss_converter.to_yaml('my-spss-file.sav', layout = 'table')
      # Stores the YAML data as a string in the variable as_yaml.

      spss_converter.to_yaml('my-spss-file.sav',
                             target = 'my-yaml-file.yaml',
                             layout = 'table')
      # Stores the YAML data in the file "my-yaml-file.yaml".

The **SPSS Converter** supports two different layouts for YAML representation of data:

  * **Records**. This layout returns a YAML collection (array) of YAML objects. Each
    object in the collection represents one record from the SPSS file. The object is a
    a set of key/value pairs where each key represents a variable/column in the SPSS file
    and its value represents the value of that variable/column for that respondent. This
    is the default layout.
  * **Table**. This layout returns a YAML object that includes a ``schema`` with the data
    map, and a separate ``data`` key which contains a collection (array) of objects where
    each object represents a single record from the SPSS data file.

.. note::

  If no ``target`` is supplied, then the YAML representation is stored in-memory in the
  return value. If a ``target`` is supplied, then the JSON representation will be written
  to this file.

.. seealso::

  * :func:`to_yaml() <spss_converter.read.to_yaml>`


Converting to Excel
-----------------------

To read data from an SPSS file and convert it into a Microsoft Excel file, simply call the
:func:`to_excel() <spss_converter.read.to_excel>` function:

.. code-block:: python

  import spss_converter

  as_excel = spss_converter.to_excel('my-spss-file.sav')
  # Will store the contents of the Excel file as a binary object in as_excel.

  spss_converter.to_excel('my-spss-file.sav', target = 'my-excel-file.xlsx')
  # Will save the Excel data to the file my-excel-file.xlsx.

Both lines of code above will read the SPSS data from ``my-spss-file.sav``, but the first
line will store it in the :class:`bytes <python:bytes>` variable ``as_excel``. The second
will instead write it to the file ``my-excel-file.xlsx``.

.. seealso::

  * :func:`to_excel() <spss_converter.read.to_excel>`

Converting to ``dict``
-------------------------

To read data from an SPSS file and convert it into a :class:`dict <python:dict>` object,
simply call the :func:`to_dict() <spss_converter.read.to_dict>` function:

.. tabs::

  .. tab:: As Records (default)

    .. code-block:: python

      import spss_converter

      as_dict = spss_converter.to_dict('my-spss-file.sav', layout = 'records')
      # Stores the data as a dict or list of dict in the variable as_dict.

  .. tab:: As Table

    .. code-block:: python

      import spss_converter

      as_dict = spss_converter.to_dict('my-spss-file.sav', layout = 'table')
      # Stores the data as a dict or list of dict in the variable as_dict.

The **SPSS Converter** supports two different layouts for :class:`dict <python:dict>`
representation of data:

  * **Records**. This layout returns a :class:`list <python:list>` of
    :class:`dict <python:dict>` objects. Each object in the list represents one record
    from the SPSS file. The object is a :class:`dict <python:dict>` whose keys each
    represent a variable/column in the SPSS file and whose values represent the value of
    that variable/column for that respondent. This is the default layout.
  * **Table**. This layout returns a :class:`dict <python:dict>` object that includes a
    ``schema`` key with the data map, and a separate ``data`` key which contains a
    :class:`list <python:list>` of objects where each object represents a single record
    from the SPSS data file.

.. seealso::

  * :func:`to_dict() <spss_converter.read.to_dict>`

------------------------

Converting Data to SPSS
============================

To convert other sources of data to SPSS format, you can simply use any function whose
names start with ``spss_converter.from_*``. The examples below provide specifics:

Converting from Pandas ``DataFrame``
----------------------------------------

To generate an SPSS file from a `Pandas <https://pandas.pydata.org>`_
:class:`DataFrame <pandas:pandas.DataFrame>`, simply call the
:func:`from_dataframe() <spss_converter.read.from_dataframe>` function:

.. note::

  The examples below all assume that the variable ``df`` contains the
  :class:`DataFrame <pandas:pandas.DataFrame>` whose data will be converted to SPSS
  format and the variable ``meta`` contains the
  :class:`Metadata <spss_converter.Metadata>` that describes that data frame.

.. code-block:: python

  import spss_converter

  as_spss = spss_converter.from_dataframe(df, metadata = meta)
  # Will store the SPSS data in-memory in a binary bytes object named as_spss.

  spss_converter.from_dataframe(df, target = 'my-spss-file.sav', metadata = meta)
  # Will store the SPSS data to the hard drive in the file named "my-spss-file.sav".

The code above will convert the data in the :class:`DataFrame <pandas:pandas.DataFrame>`
named ``df``, and generate it in SPSS format either in-memory or on the hard drive.

.. seealso::

  * :func:`from_dataframe() <spss_converter.write.from_dataframe>`

Converting from CSV
-----------------------

To read data from a CSV file and convert it into SPSS format, simply call the
:func:`from_csv() <spss_converter.write.from_csv>` function:

.. code-block:: python

  import spss_converter

  as_spss = spss_converter.from_csv('my-csv-file.csv')
  # Will store the contents of the CSV file as an in-memory binary object called as_spss.

  spss_converter.from_csv('my-csv-file.csv', target = 'my-spss-file.sav')
  # Will save the CSV data to the file my-spss-file.sav.

Both lines of code above will read the data from ``my-csv-file.csv``, but the first
line will store it in the :class:`bytesIO <python:io.BytesIO>` variable ``as_spss``. The
second will instead write it to the file ``my-spss-file.sav``.

.. seealso::

  * :func:`from_csv() <spss_converter.write.from_csv>`

Converting from ``dict``
-------------------------

To read data from a :class:`dict <python:dict>` and convert it into an SPSS format, simply
call the :func:`from_dict() <spss_converter.write.from_dict>` function:

.. code-block:: python

  import spss_converter

  as_spss = spss_converter.from_dict(as_dict)
  # Stores the data in-memory in the variable as_spss.

  spss_converter.from_dict(as_dict, target = 'my-spss-file.sav')
  # Stores the data on the hard drive in the file named "my-spss-file.sav".

.. seealso::

  * :func:`from_dict() <spss_converter.write.from_dict>`

Converting from JSON
-----------------------

To read data from a JSON file and convert it into SPSS format, simply call the
:func:`from_json() <spss_converter.write.from_json>` function:

.. tabs::

  .. tab:: As Records (default)

    .. code-block:: python

      import spss_converter

      as_spss = spss_converter.from_json('my-json-file.json', layout = 'records')
      # Stores the SPSS data in-memory in the variable as_spss.

      spss_converter.from_json('my-json-file.json',
                               target = 'my-spss-file.sav',
                               layout = 'records')
      # Stores the SPSS data in the file "my-spss-file.sav".

  .. tab:: As Table

    .. code-block:: python

      import spss_converter

      as_spss = spss_converter.from_json('my-json-file.json', layout = 'table')
      # Stores the SPSS data in-memory in the variable as_spss.

      spss_converter.from_json('my-json-file.json',
                               target = 'my-spss-file.sav',
                               layout = 'table')
      # Stores the SPSS data in the file "my-spss-file.sav".

The **SPSS Converter** supports two different layouts for JSON representation of data:

  * **Records**. This layout expects a JSON collection (array) of JSON objects. Each
    object in the collection represents one record in the SPSS file. The object is a
    a set of key/value pairs where each key represents a variable/column in the SPSS file
    and its value represents the value of that variable/column for that respondent. This
    is the default layout.
  * **Table**. This layout returns a JSON object that includes a ``schema`` with the data
    map, and a separate ``data`` key which contains a collection (array) of objects where
    each object represents a single record in the SPSS data file.

.. note::

  If no ``target`` is supplied, then the SPSS representation is stored in-memory in the
  return value. If a ``target`` is supplied, then the SPSS representation will be written
  to this file.

.. tip::

  The :func:`from_json() <spss_converter.write.from_json>` function can accept either a
  filename or a string with JSON data.

.. seealso::

  * :func:`from_json() <spss_converter.write.from_json>`

Converting from YAML
-----------------------

To read data from a YAML file and convert it into SPSS format, simply call the
:func:`from_yaml() <spss_converter.write.from_yaml>` function:

.. tabs::

  .. tab:: As Records (default)

    .. code-block:: python

      import spss_converter

      as_spss = spss_converter.from_yaml('my-yaml-file.yaml', layout = 'records')
      # Stores the SPSS data in-memory in the variable as_spss.

      spss_converter.from_yaml('my-yaml-file.yaml',
                               target = 'my-spss-file.sav',
                               layout = 'records')
      # Stores the SPSS data in the file "my-spss-file.sav".

  .. tab:: As Table

    .. code-block:: python

      import spss_converter

      as_spss = spss_converter.from_yaml('my-yaml-file.yaml', layout = 'table')
      # Stores the SPSS data in-memory in the variable as_spss.

      spss_converter.from_yaml('my-yaml-file.yaml',
                               target = 'my-spss-file.sav',
                               layout = 'table')
      # Stores the SPSS data in the file "my-spss-file.sav".

The **SPSS Converter** supports two different layouts for YAML representation of data:

  * **Records**. This layout expects a YAML collection (array) of YAML objects. Each
    object in the collection represents one record in the SPSS file. The object is a
    a set of key/value pairs where each key represents a variable/column in the SPSS file
    and its value represents the value of that variable/column for that respondent. This
    is the default layout.
  * **Table**. This layout returns a YAML object that includes a ``schema`` with the data
    map, and a separate ``data`` key which contains a collection (array) of objects where
    each object represents a single record in the SPSS data file.

.. note::

  If no ``target`` is supplied, then the SPSS representation is stored in-memory in the
  return value. If a ``target`` is supplied, then the SPSS representation will be written
  to this file.

.. tip::

  The :func:`from_yaml() <spss_converter.write.from_yaml>` function can accept either a
  filename or a string with YAML data.

.. seealso::

  * :func:`from_yaml() <spss_converter.write.from_yaml>`

Converting to Excel
-----------------------

To read data from an Excel file and convert it into SPSS format, simply call the
:func:`from_excel() <spss_converter.write.from_excel>` function:

.. code-block:: python

  import spss_converter

  as_excel = spss_converter.from_excel('my-excel-file.xlsx')
  # Will store the contents of the SPSS data as a binary object in-memory in as_excel.

  spss_converter.from_excel('my-excel-file.xlsx', target = 'my-spss-file.sav')
  # Will save the SPSS data to the file my-spss-file.xlsx.

Both lines of code above will read the data from ``my-excel-file.xlsx``, but the first
line will store it in the :class:`bytes <python:bytes>` variable ``as_excel``. The second
will instead write it to the file ``my-spss-file.sav``.

.. seealso::

  * :func:`from_excel() <spss_converter.write.from_excel>`

-------------------

Working with Metadata
==========================

Key to working with SPSS data is understanding the distinction between the raw data's
storage format and the metadata that describes that data. Fundamentally, think of
metadata as the map of how a value stored in the raw data (such as a numerical value
``1``) can actually represent a human-readable labeled value (such as the labeled value
``"Female"``).

The metadata for an SPSS file can itself be quite verbose and define various rules for what
can and should be expected when analyzing the records in the SPSS file. Within the
**SPSS Converter**, this meta-data is represented using the
:class:`Metadata <spss_converter.Metadata.Metadata>` class.

Various functions that read SPSS data produce
:class:`Metadata <spss_converter.Metadata.Metadata>` instances, and these instances can be
manipulated to restate and adjust the human-readable labels applied to your SPSS data.

.. seealso::

  * :class:`Metadata <spss_converter.Metadata.Metadata>`
  * :func:`get_metadata() <spss_converter.read.get_metadata>`
  * :func:`apply_metadata() <spss_converter.write.apply_metadata>`
  * :class:`ColumnMetadata <spss_converter.Metadata.ColumnMetadata>`
