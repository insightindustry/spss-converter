####################################################
SPSS Converter
####################################################

**Simple format converter utility for SPSS data files**

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

   * - `v.0.2 <https://github.com/insightindustry/spss-converter/tree/v.0.2.0>`_
     -
       .. image:: https://travis-ci.com/insightindustry/spss-converter.svg?branch=v.0.2.0
          :target: https://travis-ci.com/insightindustry/spss-converter
          :alt: Build Status (Travis CI)

       .. image:: https://codecov.io/gh/insightindustry/spss-converter/branch/v.0.2.0/graph/badge.svg
          :target: https://codecov.io/gh/insightindustry/spss-converter
          :alt: Code Coverage Status (Codecov)

       .. image:: https://readthedocs.org/projects/spss-converter/badge/?version=v.0.2.0
          :target: http://spss-converter.readthedocs.io/en/latest/?badge=v.0.2.0
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

The **SPSS Converter** is a simple utility that facilitates the easy conversion of SPSS
data to / from a variety of formats, including:

  * CSV
  * JSON
  * YAML
  * Excel
  * Pandas ``DataFrame``

**COMPLETE DOCUMENTATION:** http://spss-converter.readthedocs.org/en/latest/index.html

.. contents::
 :depth: 3
 :backlinks: entry

-----------------

***************
Installation
***************

To install the **SPSS Converter** via Pip just execute:

.. code:: bash

 $ pip install spss-converter

Dependencies
==============

.. list-table::
   :widths: 100
   :header-rows: 1

   * - Python 3.x
   * - | * `Pandas v0.24 <https://pandas.pydata.org/docs/>`_ or higher
       | * `Pyreadstat v1.0 <https://github.com/Roche/pyreadstat>`_ or higher
       | * `OpenPyXL v.3.0.7 <https://openpyxl.readthedocs.io/en/stable/>`_ or higher
       | * `PyYAML v3.10 <https://github.com/yaml/pyyaml>`_ or higher
       | * `simplejson v3.0 <https://simplejson.readthedocs.io/en/latest/>`_ or higher
       | * `Validator-Collection v1.5.0 <https://github.com/insightindustry/validator-collection>`_ or higher

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

  * a `Pandas <https://pandas.pydata.org>`_ ``DataFrame``
  * CSV
  * JSON
  * YAML
  * Excel
  * a ``dict``

* With one function call, create an SPSS data file from data in:

  * a `Pandas <https://pandas.pydata.org>`_ ``DataFrame``
  * CSV
  * JSON
  * YAML
  * Excel
  * a ``dict``

* With one function call, generate a Pythonic data map or meta-data collection from your
  SPSS data file.
* Decide which variables (columns) you want to include / exclude when doing your
  conversion.

**SPSS Converter** vs Alternatives
=========================================

For a comparison of the **SPSS Converter** to various alternative
conversion approaches, please see full documentation:
https://spss-converter.readthedocs.io/en/latest/index.html#spss-converter-vs-alternatives

***********************************
Complete Documentation
***********************************

The **SPSS Converter** is a simple library, but its functions are comprehensively
documented at:

  https://spss-converter.readthedocs.org/en/latest/index.html

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
`Contributor Guide <http://spss-converter.readthedocs.org/en/latest/contributing.html>`_

-------------------

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation,
`Codecov.io <http://codecov.io>`_ for our test coverage, and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our
`Testing Reference <http://spss-converter.readthedocs.org/en/latest/testing.html>`_.

--------------------

**********************
License
**********************

The **SPSS Converter** is made available under an
`MIT License <http://spss-converter.readthedocs.org/en/latest/license.html>`_.
