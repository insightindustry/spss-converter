####################################################
SPSS Converter
####################################################

**Simple utility for converting data to/from SPSS data files**

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Branch
     - Unit Tests
   * - `latest <https://github.com/insightindustry/spss-converter/tree/master>`_
     -
       .. image:: https://travis-ci.com/insightindustry/spss-converter.svg?branch=master
         :target: https://travis-ci.com/insightindustry/spss-converter
         :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/spss-converter/branch/master/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/spss-converter
         :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/spss-converter/badge/?version=latest
         :target: http://spss-converter.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status (ReadTheDocs)

   * - `v.0.1 <https://github.com/insightindustry/spss-converter/tree/v.0.1.0>`_
     -
       .. image:: https://travis-ci.com/insightindustry/spss-converter.svg?branch=v.0.1.0
         :target: https://travis-ci.com/insightindustry/spss-converter
         :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/spss-converter/branch/v.0.1.0/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/spss-converter
         :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/spss-converter/badge/?version=v.0.1.0
         :target: http://spss-converter.readthedocs.io/en/latest/?badge=v.0.1.0
         :alt: Documentation Status (ReadTheDocs)

.. toctree::
 :hidden:
 :maxdepth: 3
 :caption: Contents:

 Home <self>
 Quickstart: Patterns and Best Practices <quickstart>
 Using the SPSS Converter <using>
 API Reference <api>
 Error Reference <errors>
 Contributor Guide <contributing>
 Testing Reference <testing>
 Release History <history>
 Glossary <glossary>
 License <license>

The **SPSS Converter** is a simple utility that facilitates the easy conversion of SPSS
data to / from a variety of formats, including:

  * CSV
  * JSON
  * YAML
  * Excel
  * `Pandas <https://pandas.pydata.org/>`_ :class:`DataFrame <pandas:pandas.DataFrame>`

.. contents::
 :depth: 3
 :backlinks: entry

-----------------

***************
Installation
***************

.. include:: _installation.rst

Dependencies
==============

.. include:: _dependencies.rst

-------------

************************************
Why the SPSS Converter?
************************************

If you work with SPSS data in the Python ecosystem, you probably use a combination of
two or three key libraries: `Pandas <https://pandas.pydata.org>`_,
`Pyreadstat <https://github.com/Roche/pyreadstat>`_, and
`savReaderWriter <https://pythonhosted.org/savReaderWriter/>`_. All three libraries are
vital tools, incredibly well-constructed, designed, and managed. But over the years, I
have found that converting from SPSS to other file formats using these libraries requires
some fairly repetitive boilerplate code. So why not make it easier?

The **SPSS Converter** library is a simple wrapper around the
`Pyreadstat <https://github.com/Roche/pyreadstat>`_ and
`Pandas <https://pandas.pydata.org>`_ libraries that provides a clean and simple API for
reading data files in a variety of formats and converting them to a variety of formats.
The semantics are super simple, and should be as simple as: ``spss_converter.to_csv('my-spss-file.sav')``
or ``spss_converter.from_json('my-json-file.json')``.

Key **SPSS Converter** Features
====================================

* With one function call, convert an SPSS file into:

  * a `Pandas <https://pandas.pydata.org/>`_ :class:`DataFrame <pandas:pandas.DataFrame>`
  * CSV
  * JSON
  * YAML
  * Excel
  * a :class:`dict <python:dict>`

* With one function call, create an SPSS data file from data in:

  * a `Pandas <https://pandas.pydata.org/>`_ :class:`DataFrame <pandas:pandas.DataFrame>`
  * CSV
  * JSON
  * YAML
  * Excel
  * a :class:`dict <python:dict>`

* With one function call, generate a Pythonic data map or meta-data collection from your
  SPSS data file.
* Decide which variables (columns) you want to include / exclude when doing your
  conversion.

**SPSS Converter** vs Alternatives
=========================================

The **SPSS Converter** library is a simple wrapper around the
`Pyreadstat <https://github.com/Roche/pyreadstat>`_ and
`Pandas <https://pandas.pydata.org>`_ libraries that simplifies the syntax for converting
between different file formats.

While I am (I think understandably) biased in favor of the **SPSS Converter**, there some
perfectly reasonable alternatives:

.. tabs::

  .. tab:: Pyreadstat + Pandas

    Obviously, since the **SPSS Converter** is just a wrapper around
    `Pyreadstat <https://github.com/Roche/pyreadstat>`_ and
    `Pandas <https://pandas.pydata.org>`_, you can simply call their functions directly.

    Both libraries are excellent, stable, and use fairly straightforward syntax. However:

      * using those libraries directly does double the number of function calls you need
        to make to convert between different data formats, and
      * those libraries (and `Pyreadstat <https://github.com/Roche/pyreadstat>`_ in
        particular) provide limited validation or Pythonic object representation (less
        "batteries included" in its syntactical approach).

    Of course, these differences are largely stylistic in nature.

    .. tip::

      **When to use it?**

      Honestly, since initially building this wrapper I rarely use
      `Pyreadstat <https://github.com/Roche/pyreadstat>`_ and
      `Pandas <https://pandas.pydata.org>`_ directly. Mostly, this is a matter of
      syntactical taste and personal preference.

      However, I would definitely look to those libraries directly if I were:

        * writing this kind of wrapper
        * working in older versions of Python (< 3.7)
        * working with other formats of data than SPSS

    .. tabs::

      .. tab:: Using SPSS Converter

        .. code-block:: python
          :linenos:

          from spss_converter import read, write

          # SPSS File to CSV
          read.to_csv('my-spss-file.sav',
                      target = 'my-csv-file.csv')

          # CSV to SPSS File
          write.from_csv('my-csv-file.csv',
                         target = 'my-spss-file.sav')

          # SPSS File to Excel file
          read.to_excel('my-spss-file.sav',
                        target = 'my-excel-file.xlsx')

          # Excel to SPSS file
          write.from_excel('my-excel-file.xlsx',
                           target = 'my-spss-file.sav')

          # ... similar pattern for other formats

      .. tab:: Using Pyreadstat and Pandas

        .. code-block:: python
          :linenos:

          import pyreadstat
          import pandas

          # SPSS File to CSV
          df, metadata = pyreadstat.read_sav('my-spss-file.sav')
          csv_file = df.to_csv('my-csv-file.csv')

          # CSV to SPSS file
          df = pandas.read_csv('my-csv-file.csv')
          spss_file = pyreadstat.write_sav(df,
                                           'my-spss-file.sav')

          # SPSS File to Excel File
          df, metadata = pyreadstat.read_sav('my-spss-file.sav')
          excel_file = df.to_excel('my-excel-file.xlsx')

          # Excel file to SPSS file
          df = pandas.read_excel('my-excel-file.xlsx')
          spss_file = pyreadstat.write_sav(df,
                                           'my-spss-file.sav')

          # .. similar pattern for other formats

  .. tab:: savReaderWriter

    The `savReaderWriter <https://pythonhosted.org/savReaderWriter/>`_ library is a
    powerful library for converting SPSS data to/from different formats. Its core strength
    is its ability to get very granular metadata about the SPSS data and to sequentially
    iterate through its records.

    However, the library has three significant limitations when it comes to format
    conversion:

      * The library only provides read and write access for SPSS data, and this means that
        you would have to write the actual "conversion" logic yourself. This can get quite
        complicated, particularly when dealing with data serialization challenges.
      * The library depends on the SPSS I/O module, which is packaged with the library.
        This module has both licensing implications and is a "heavy" module for
        distribution.
      * The library's most-recent commits date back to 2017, and it would seem that it is
        no longer being actively maintained.

    .. tip::

      **When to use it?**

      * When you actually need to dive into the data at the level of particular cases
        or values.
      * When your data has :term:`Multiple Response Sets <Multiple Response Set>`, which
        are not (yet) supported by either
        `Pyreadstat <https://github.com/Roche/pyreadstat>`_ or the **SPSS Converter**.


--------------

*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/insightindustry/spss-converter/issues>`_

-----------------

*********************
Contributing
*********************

We welcome contributions and pull requests! For more information, please see the
:doc:`Contributor Guide <contributing>`.

-------------------

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation,
`Codecov.io <http://codecov.io>`_ for our test coverage, and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our :doc:`Testing Reference <testing>`.

--------------------

**********************
License
**********************

The **SPSS Converter** is made available under an
:doc:`MIT License <license>`.
