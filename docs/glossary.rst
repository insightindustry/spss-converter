**********
Glossary
**********

.. glossary::

  Metadata
    A collection of information that allows a human being to understand what raw data
    represents. Think of it as a "data map" that tells you a) what to expect within the
    raw data stored in a given format, b) what that data actually means / signifies.

    .. seealso::

      * :class:`Metadata <spss_converter.Metadata.Metadata>`
      * :class:`ColumnMetadata <spss_converter.Metadata.ColumnMetadata>`

  Multiple Response Set
    A way of representing "select all answers that apply" survey questions in SPSS data, where
    each answer maps to its own variable/column in the raw data, but the set of
    variables/columns should be grouped within the multiple response set.

    .. warning::

      Because `Pyreadstat <https://github.com/Roche/pyreadstat>`_ does not yet support
      Multiple Response Sets, the **SPSS Converter** also does not support them.
