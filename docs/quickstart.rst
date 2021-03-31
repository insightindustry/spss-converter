******************************************
Quickstart: Patterns and Best Practices
******************************************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Installation
===============

.. include:: _installation.rst

-----------

Convert between SPSS and CSV
================================

.. tabs::

  .. tab:: SPSS --> CSV

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to "my-csv-file.csv".
      spss_converter.to_csv('my-spss-file.sav', target = 'my-csv-file.csv')


  .. tab:: CSV --> SPSS

    .. code-block:: python
      :linenos:

      # Convert "my-csv-file.csv" to "my-spss-file.sav"
      spss_converter.from_csv('my-csv-file.csv', target = 'my-spss-file.sav')

-------------------------

Convert between SPSS and JSON
================================

.. tabs::

  .. tab:: SPSS --> JSON

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to "my-json-file.json" using a "records" layout
      spss_converter.to_json('my-spss-file.sav',
                             target = 'my-json-file.json',
                             layout = 'records')

      # Convert "my-spss-file.sav" to "my-json-file.json" using a "table" layout
      spss_converter.to_json('my-spss-file.sav',
                             target = 'my-json-file.json',
                             layout = 'table')


  .. tab:: JSON --> SPSS

    .. code-block:: python
      :linenos:

      # Convert "my-json-file.json" to "my-spss-file.sav" using a "records" layout
      spss_converter.from_json('my-json-file.json',
                               target = 'my-spss-file.sav',
                               layout = 'records')

      # Convert "my-json-file.sav" to "my-spss-file.json" using a "table" layout
      spss_converter.from_json('my-json-file.json',
                               target = 'my-spss-file.sav',
                               layout = 'table')

------------------------

Convert between SPSS and YAML
================================

.. tabs::

  .. tab:: SPSS --> YAML

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to "my-yaml-file.yaml" using a "records" layout
      spss_converter.to_yaml('my-spss-file.sav',
                             target = 'my-yaml-file.yaml',
                             layout = 'records')

      # Convert "my-spss-file.sav" to "my-yaml-file.yaml" using a "table" layout
      spss_converter.to_yaml('my-spss-file.sav',
                             target = 'my-yaml-file.yaml',
                             layout = 'table')


  .. tab:: YAML --> SPSS

    .. code-block:: python
      :linenos:

      # Convert "my-yaml-file.yaml" to "my-spss-file.sav" using a "records" layout
      spss_converter.from_yaml('my-yaml-file.yaml',
                               target = 'my-spss-file.sav',
                               layout = 'records')

      # Convert "my-yaml-file.sav" to "my-spss-file.yaml" using a "table" layout
      spss_converter.from_yaml('my-yaml-file.yaml',
                               target = 'my-spss-file.sav',
                               layout = 'table')

---------------------

Convert between SPSS and Pandas ``DataFrame``
==================================================

.. tabs::

  .. tab:: SPSS --> ``DataFrame``

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to df
      df, meta = spss_converter.to_dataframe('my-spss-file.sav')


  .. tab:: ``DataFrame`` --> SPSS

    .. code-block:: python
      :linenos:

      # Convert the Pandas DataFrame df to "my-spss-file.sav"
      spss_converter.from_dataframe(df, target = 'my-spss-file.sav', metadata = meta)

-------------------------

Convert between SPSS and ``dict``
======================================

.. tabs::

  .. tab:: SPSS --> ``dict``

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to a dict using a "records" layout
      as_dict = spss_converter.to_dict('my-spss-file.sav',
                                       layout = 'records')

      # Convert "my-spss-file.sav" to a dict using a "table" layout
      as_dict = spss_converter.to_dict('my-spss-file.sav',
                                       layout = 'table')


  .. tab:: ``dict`` --> SPSS

    .. code-block:: python
      :linenos:

      # Convert as_dict to "my-spss-file.sav"
      spss_converter.from_dict(as_dict,
                               target = 'my-spss-file.sav')

------------------------

Convert between SPSS and Excel
================================

.. tabs::

  .. tab:: SPSS --> Excel

    .. code-block:: python
      :linenos:

      # Convert "my-spss-file.sav" to "my-excel-file.xlsx".
      spss_converter.to_excel('my-spss-file.sav', target = 'my-excel-file.xlsx')


  .. tab:: Excel --> SPSS

    .. code-block:: python
      :linenos:

      # Convert "my-csv-file.csv" to "my-spss-file.sav"
      spss_converter.from_excel('my-excel-file.xlsx', target = 'my-spss-file.sav')

---------------------

Get the Metadata from an SPSS File
======================================

.. code-block:: python
  :linenos:

  # Retrieve Metadata from the SPSS file "my-spss-file.sav"
  meta = spss_converter.get_metadata('my-spss-file.sav')

------------------------

Change the Metadata for a Given ``DataFrame``
================================================

.. code-block:: python
  :linenos:

  # Apply the metadata in updated_meta to the dataframe in df.
  spss_converter.apply_metadata(df, updated_meta)
