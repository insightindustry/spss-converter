from typing import Union, List, Optional, Any
import tempfile

import os
from io import BytesIO, StringIO
import simplejson as json
import yaml
import pyreadstat
from validator_collection import validators, checkers
from spss_converter import errors
from spss_converter.Metadata import Metadata
from pandas import ExcelWriter


def _read_spss(data: Union[bytes, BytesIO, 'os.PathLike[Any]'],
               limit: Optional[int] = None,
               offset: int = 0,
               exclude_variables: Optional[List[str]] = None,
               include_variables: Optional[List[str]] = None,
               metadata_only: bool = False,
               apply_labels: bool = False,
               labels_as_categories: bool = True,
               missing_as_NaN: bool = False,
               convert_datetimes: bool = True,
               dates_as_datetime64: bool = False,
               **kwargs):
    """Internal function that reads an SPSS (.sav or .zsav) file and returns a
    :class:`tuple <python:tuple>` with a Pandas
    :class:`DataFrame <pandas:pandas.DataFrame>` object and a metadata
    :class:`dict <python:dict>`.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete metadata
      :class:`dict <python:dict>`. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: A :class:`DataFrame <pandas:DataFrame>` representation of the SPSS data (or
      :obj:`None <python:None>`) and a :class:`Metadata` representation of the dataset's
      metadata / data map.
    :rtype: :class:`pandas.DataFrame <pandas:DataFrame>`/:obj:`None <python:None>` and
      :class:`Metadata`

    """
    if not any([checkers.is_file(data),
                checkers.is_bytesIO(data),
                checkers.is_type(data, bytes)]):
        raise errors.InvalidDataFormatError('data must be a filename, BytesIO, or bytes '
                                            f'object. Was: {data.__class__.__name__}')

    limit = validators.integer(limit, allow_empty = True, minimum = 0)
    offset = validators.integer(offset, minimum = 0)

    exclude_variables = validators.iterable(exclude_variables, allow_empty = True)
    if exclude_variables:
        exclude_variables = [validators.string(x) for x in exclude_variables]

    include_variables = validators.iterable(include_variables, allow_empty = True)
    if include_variables:
        include_variables = [validators.string(x) for x in include_variables]

    if not checkers.is_file(data):
        with tempfile.NamedTemporaryFile(delete = False) as temp_file:
            temp_file.write(data)
            temp_file_name = temp_file.name

        df, meta = pyreadstat.read_sav(temp_file_name,
                                       metadataonly = metadata_only,
                                       dates_as_pandas_datetime = dates_as_datetime64,
                                       apply_value_formats = apply_labels,
                                       formats_as_category = labels_as_categories,
                                       usecols = include_variables,
                                       user_missing = not missing_as_NaN,
                                       disable_datetime_conversion = not convert_datetimes,
                                       row_limit = limit or 0,
                                       row_offset = offset,
                                       **kwargs)
        os.remove(temp_file_name)
    else:
        df, meta = pyreadstat.read_sav(data,
                                       metadataonly = metadata_only,
                                       dates_as_pandas_datetime = dates_as_datetime64,
                                       apply_value_formats = apply_labels,
                                       formats_as_category = labels_as_categories,
                                       usecols = include_variables,
                                       user_missing = not missing_as_NaN,
                                       disable_datetime_conversion = not convert_datetimes,
                                       row_limit = limit or 0,
                                       row_offset = offset,
                                       **kwargs)

    metadata = Metadata.from_pyreadstat(meta)

    if exclude_variables:
        df = df.drop(exclude_variables, axis = 1)
        if metadata.column_metadata:
            for variable in exclude_variables:
                metadata.column_metadata.pop(variable, None)

    return df, metadata


def get_metadata(data):
    """Retrieve the metadata that describes the coded representation of the data,
    corresponding formatting information, and their related human-readable labels.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :returns: The metadata that describes the raw data and its corresponding labels.
    :rtype: :class:`Metadata`
    """
    return _read_spss(data, metadata_only = True)[1]


def to_dataframe(data: Union[bytes, BytesIO, 'os.PathLike[Any]'],
                 limit: Optional[int] = None,
                 offset: int = 0,
                 exclude_variables: Optional[List[str]] = None,
                 include_variables: Optional[List[str]] = None,
                 metadata_only: bool = False,
                 apply_labels: bool = False,
                 labels_as_categories: bool = True,
                 missing_as_NaN: bool = False,
                 convert_datetimes: bool = True,
                 dates_as_datetime64: bool = False,
                 **kwargs):
    """Reads SPSS data and returns a :class:`tuple <python:tuple>` with a Pandas
    :class:`DataFrame <pandas:pandas.DataFrame>` object and relevant :class:`Metadata`.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: A :class:`DataFrame <pandas:DataFrame>` representation of the SPSS data (or
      :obj:`None <python:None>`) and a :class:`Metadata <Metadata>` representation of the
      data's meta-data (value and labels / data map).
    :rtype: :class:`pandas.DataFrame <pandas:DataFrame>`/:obj:`None <python:None>` and
      :class:`Metadata <Metadata>`

    """
    return _read_spss(data,
                      limit = limit,
                      offset = offset,
                      exclude_variables = exclude_variables,
                      include_variables = include_variables,
                      metadata_only = metadata_only,
                      apply_labels = apply_labels,
                      labels_as_categories = labels_as_categories,
                      missing_as_NaN = missing_as_NaN,
                      convert_datetimes = convert_datetimes,
                      dates_as_datetime64 = dates_as_datetime64,
                      **kwargs)


def to_csv(data: Union['os.PathLike[Any]', BytesIO, bytes],
           target: Optional[Union['os.PathLike[Any]', StringIO]] = None,
           include_header: bool = True,
           delimter: str = '|',
           null_text: str = 'NaN',
           wrapper_character: str = "'",
           escape_character: str = "\\",
           line_terminator: str = '\r\n',
           decimal: str = '.',
           limit: Optional[int] = None,
           offset: int = 0,
           exclude_variables: Optional[List[str]] = None,
           include_variables: Optional[List[str]] = None,
           metadata_only: bool = False,
           apply_labels: bool = False,
           labels_as_categories: bool = True,
           missing_as_NaN: bool = False,
           convert_datetimes: bool = True,
           dates_as_datetime64: bool = False,
           **kwargs):
    r"""Convert the SPSS ``data`` into a CSV string where each row represents a record of
    SPSS data.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param target: The destination where the CSV representation should be stored. Accepts
      either a filename, file-pointer or a :class:`StringIO <python:io.StringIO>`, or
      :obj:`None <python:None>`. If :obj:`None <python:None>`, will return a
      :class:`str <python:str>` object stored in-memory. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`StringIO <python:io.StringIO>` /
      :class:`str <python:str>` / :obj:`None <python:None>`

    :param include_header: If ``True``, will include a header row with column
      labels. If ``False``, will not include a header row. Defaults to ``True``.
    :type include_header: :class:`bool <python:bool>`

    :param delimiter: The delimiter used between columns. Defaults to ``|``.
    :type delimiter: :class:`str <python:str>`

    :param null_text: The text value to use in place of empty values. Only
      applies if ``wrap_empty_values`` is ``True``. Defaults to ``'NaN'``.
    :type null_text: :class:`str <python:str>`

    :param wrapper_character: The string used to wrap string values when
      wrapping is necessary. Defaults to ``'``.
    :type wrapper_character: :class:`str <python:str>`

    :param escape_character: The character to use when escaping nested wrapper
      characters. Defaults to ``\``.
    :type escape_character: :class:`str <python:str>`

    :param line_terminator: The character used to mark the end of a line.
      Defaults to ``\r\n``.
    :type line_terminator: :class:`str <python:str>`

    :param decimal: The character used to indicate a decimal place in a numerical value.
      Defaults to ``.``.
    :type decimal: :class:`str <python:str>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>` if ``target`` was not :obj:`None <python:None>`,
      otherwise a :class:`str <python:str>` representation of the CSV file.
    :rtype: :obj:`None <python:None>` or :class:`str <python:str>`

    """
    if target and not checkers.is_pathlike(target) and not checkers.is_stringIO(target):
        raise errors.InvalidDataFormatError('target must be a filename, StringIO object, '
                                            f'or None. Was: {data.__class__.__name__}')

    df, metadata = _read_spss(data,
                              limit = limit,
                              offset = offset,
                              exclude_variables = exclude_variables,
                              include_variables = include_variables,
                              metadata_only = metadata_only,
                              apply_labels = apply_labels,
                              labels_as_categories = labels_as_categories,
                              missing_as_NaN = missing_as_NaN,
                              convert_datetimes = convert_datetimes,
                              dates_as_datetime64 = dates_as_datetime64,
                              **kwargs)

    result = df.to_csv(target,
                       sep = delimter,
                       na_rep = null_text,
                       header = include_header,
                       quotechar = wrapper_character,
                       line_terminator = line_terminator,
                       escapechar = escape_character,
                       decimal = decimal)

    if target is not None:
        return None

    return result


def to_json(data: Union['os.PathLike[Any]', BytesIO, bytes],
            target: Optional[Union['os.PathLike[Any]', StringIO]] = None,
            layout: str = 'records',
            double_precision: int = 10,
            limit: Optional[int] = None,
            offset: int = 0,
            exclude_variables: Optional[List[str]] = None,
            include_variables: Optional[List[str]] = None,
            metadata_only: bool = False,
            apply_labels: bool = False,
            labels_as_categories: bool = True,
            missing_as_NaN: bool = False,
            convert_datetimes: bool = True,
            dates_as_datetime64: bool = False,
            **kwargs):
    r"""Convert the SPSS ``data`` into a JSON string.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param target: The destination where the JSON representation should be stored. Accepts
      either a filename, file-pointer or :class:`StringIO <python:io.StringIO>`, or
      :obj:`None <python:None>`. If :obj:`None <python:None>`, will return a
      :class:`str <python:str>` object stored in-memory. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`StringIO <python:io.StringIO>` /
      :class:`str <python:str>` / :obj:`None <python:None>`

    :param layout: Indicates the layout schema to use for the JSON representation of the
      data. Accepts:

        * ``records``, where the resulting JSON object represents an array of objects
          where each object corresponds to a single record, with key/value pairs for each
          column and that record's corresponding value
        * ``table``, where the resulting JSON object contains a metadata (data map)
          describing the data schema along with the resulting collection of record objects

      Defaults to ``records``.
    :type layout: :class:`str <python:str>`

    :param double_precision: Indicates the precision (places beyond the decimal point) to
      apply for floating point values. Defaults to ``10``.
    :type double_precision: class:`int <python:int>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>` if ``target`` was not :obj:`None <python:None>`,
      otherwise a :class:`str <python:str>` representation of the JSON output.
    :rtype: :obj:`None <python:None>` or :class:`str <python:str>`

    """
    if target and not checkers.is_pathlike(target) and not checkers.is_stringIO(target):
        raise errors.InvalidDataFormatError('target must be a filename, StringIO object, '
                                            f'or None. Was: {data.__class__.__name__}')

    if layout not in ['records', 'table']:
        raise errors.InvalidLayoutError('layout must be either "records" or "table". '
                                        f'Was: "{layout}"')

    df, metadata = _read_spss(data,
                              limit = limit,
                              offset = offset,
                              exclude_variables = exclude_variables,
                              include_variables = include_variables,
                              metadata_only = metadata_only,
                              apply_labels = apply_labels,
                              labels_as_categories = labels_as_categories,
                              missing_as_NaN = missing_as_NaN,
                              convert_datetimes = convert_datetimes,
                              dates_as_datetime64 = dates_as_datetime64,
                              **kwargs)

    result = df.to_json(target,
                        orient = layout,
                        double_precision = double_precision)

    if target is not None:
        return None

    return result


def to_yaml(data: Union['os.PathLike[Any]', BytesIO, bytes],
            target: Optional[Union['os.PathLike[Any]', StringIO]] = None,
            layout: str = 'records',
            double_precision: int = 10,
            limit: Optional[int] = None,
            offset: int = 0,
            exclude_variables: Optional[List[str]] = None,
            include_variables: Optional[List[str]] = None,
            metadata_only: bool = False,
            apply_labels: bool = False,
            labels_as_categories: bool = True,
            missing_as_NaN: bool = False,
            convert_datetimes: bool = True,
            dates_as_datetime64: bool = False,
            **kwargs):
    r"""Convert the SPSS ``data`` into a YAML string.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param target: The destination where the YAML representation should be stored. Accepts
      either a filename, file-pointer or :class:`StringIO <python:io.StringIO>`, or
      :obj:`None <python:None>`. If :obj:`None <python:None>`, will return a
      :class:`str <python:str>` object stored in-memory. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`StringIO <python:io.StringIO>` /
      :class:`str <python:str>` / :obj:`None <python:None>`

    :param layout: Indicates the layout schema to use for the JSON representation of the
      data. Accepts:

        * ``records``, where the resulting YAML object represents an array of objects
          where each object corresponds to a single record, with key/value pairs for each
          column and that record's corresponding value
        * ``table``, where the resulting JSON object contains a metadata (data map)
          describing the data schema along with the resulting collection of record objects

      Defaults to ``records``.
    :type layout: :class:`str <python:str>`

    :param double_precision: Indicates the precision (places beyond the decimal point) to
      apply for floating point values. Defaults to ``10``.
    :type double_precision: class:`int <python:int>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>` if ``target`` was not :obj:`None <python:None>`,
      otherwise a :class:`str <python:str>` representation of the YAML output.
    :rtype: :obj:`None <python:None>` or :class:`str <python:str>`

    """
    if target and not checkers.is_pathlike(target) and not checkers.is_stringIO(target):
        raise errors.InvalidDataFormatError('target must be a filename, StringIO object, '
                                            f'or None. Was: {data.__class__.__name__}')

    if layout not in ['records', 'table']:
        raise errors.InvalidLayoutError('layout must be either "records" or "table". '
                                        f'Was: "{layout}"')

    df, metadata = _read_spss(data,
                              limit = limit,
                              offset = offset,
                              exclude_variables = exclude_variables,
                              include_variables = include_variables,
                              metadata_only = metadata_only,
                              apply_labels = apply_labels,
                              labels_as_categories = labels_as_categories,
                              missing_as_NaN = missing_as_NaN,
                              convert_datetimes = convert_datetimes,
                              dates_as_datetime64 = dates_as_datetime64,
                              **kwargs)

    as_json = df.to_json(None,
                         orient = layout,
                         double_precision = double_precision)

    as_dict = json.loads(as_json)

    as_yaml = yaml.dump(as_dict)

    if target is None:
        return as_yaml

    with open(target, 'wb') as target_file:
        target_file.write(as_yaml)


def to_dict(data: Union['os.PathLike[Any]', BytesIO, bytes],
            layout: str = 'records',
            double_precision: int = 10,
            limit: Optional[int] = None,
            offset: int = 0,
            exclude_variables: Optional[List[str]] = None,
            include_variables: Optional[List[str]] = None,
            metadata_only: bool = False,
            apply_labels: bool = False,
            labels_as_categories: bool = True,
            missing_as_NaN: bool = False,
            convert_datetimes: bool = True,
            dates_as_datetime64: bool = False,
            **kwargs):
    r"""Convert the SPSS ``data`` into a Python :class:`dict <python:dict>`.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param layout: Indicates the layout schema to use for the JSON representation of the
      data. Accepts:

        * ``records``, where the resulting YAML object represents an array of objects
          where each object corresponds to a single record, with key/value pairs for each
          column and that record's corresponding value
        * ``table``, where the resulting JSON object contains a metadata (data map)
          describing the data schema along with the resulting collection of record objects

      Defaults to ``records``.
    :type layout: :class:`str <python:str>`

    :param double_precision: Indicates the precision (places beyond the decimal point) to
      apply for floating point values. Defaults to ``10``.
    :type double_precision: class:`int <python:int>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>` if ``target`` was not :obj:`None <python:None>`,
      otherwise a :class:`list <python:list>` of :class:`dict <python:dict>` if ``layout``
      is ``records``, or a :class:`dict <python:dict>` if ``layout`` is ``table``.
    :rtype: :obj:`None <python:None>` or :class:`str <python:str>`

    """
    if layout not in ['records', 'table']:
        raise errors.InvalidLayoutError('layout must be either "records" or "table". '
                                        f'Was: "{layout}"')

    as_json = to_json(data,
                      layout = layout,
                      double_precision = double_precision,
                      limit = limit,
                      offset = offset,
                      exclude_variables = exclude_variables,
                      include_variables = include_variables,
                      metadata_only = metadata_only,
                      apply_labels = apply_labels,
                      labels_as_categories = labels_as_categories,
                      missing_as_NaN = missing_as_NaN,
                      convert_datetimes = convert_datetimes,
                      dates_as_datetime64 = dates_as_datetime64,
                      **kwargs)

    as_dict = json.loads(as_json)

    return as_dict


def to_excel(data: Union['os.PathLike[Any]', BytesIO, bytes],
             target: Optional[Union['os.PathLike[Any]', BytesIO, ExcelWriter]] = None,
             sheet_name: str = 'Sheet1',
             start_row: int = 0,
             start_column: int = 0,
             null_text: str = 'NaN',
             include_header: bool = True,
             limit: Optional[int] = None,
             offset: int = 0,
             exclude_variables: Optional[List[str]] = None,
             include_variables: Optional[List[str]] = None,
             metadata_only: bool = False,
             apply_labels: bool = False,
             labels_as_categories: bool = True,
             missing_as_NaN: bool = False,
             convert_datetimes: bool = True,
             dates_as_datetime64: bool = False,
             **kwargs):
    r"""Convert the SPSS ``data`` into an Excel file where each row represents a record of
    SPSS data.

    :param data: The SPSS data to load. Accepts either a series of bytes or a filename.
    :type data: Path-like filename, :class:`bytes <python:bytes>` or
      :class:`BytesIO <python:io.bytesIO>`

    :param target: The destination where the Excel file should be stored. Accepts
      either a filename, file-pointer or a :class:`BytesIO <python:io.BytesIO>`, or
      an :class:`ExcelWriter <pandas:pandas.ExcelWriter>` instance.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :class:`ExcelWriter <pandas:pandas.ExcelWriter>`

    :param sheet_name: The worksheet on which the SPSS data should be written. Defaults to
      ``'Sheet1'``.
    :type sheet_name: :class:`str <python:str>`

    :param start_row: The row number (starting at 0) where the SPSS data should begin.
      Defaults to ``0``.
    :type start_row: :class:`int <python:int>`

    :param start_column: The column number (starting at 0) where the SPSS data should
      begin. Defaults to ``0``.
    :type start_column: :class:`int <python:int>`

    :param null_text: The way that missing values should be represented in the Excel
      file. Defaults to ``''`` (an empty string).
    :type null_text: :class:`str <python:str>`

    :param include_header: If ``True``, will include a header row with column
      labels. If ``False``, will not include a header row. Defaults to ``True``.
    :type include_header: :class:`bool <python:bool>`

    :param limit: The number of records to read from the data. If
      :obj:`None <python:None>` will return all records. Defaults to
      :obj:`None <python:None>`.
    :type limit: :class:`int <python:int>` or :obj:`None <python:None>`

    :param offset: The record at which to start reading the data. Defaults to 0 (first
      record).
    :type offset: :class:`int <python:int>`

    :param exclude_variables: A list of the variables that should be ignored when reading
      data. Defaults to :obj:`None <python:None>`.
    :type exclude_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param include_variables: A list of the variables that should be explicitly included
      when reading data. Defaults to :obj:`None <python:None>`.
    :type include_variables: iterable of :class:`str <python:str>` or
      :obj:`None <python:None>`

    :param metadata_only: If ``True``, will return no data records in the resulting
      :class:`DataFrame <pandas:pandas.DataFrame>` but will return a complete
      :class:`Metadata` instance. Defaults to ``False``.
    :type metadata_only: :class:`bool <python:bool>`

    :param apply_labels: If ``True``, converts the numerically-coded values in the raw
      data to their human-readable labels. Defaults to ``False``.
    :type apply_labels: :class:`bool <python:bool>`

    :param labels_as_categories: If ``True``, will convert labeled or formatted values to
      Pandas :term:`categories <pandas:category>`. Defaults to ``True``.

      .. caution::

        This parameter will only have an effect if the ``apply_labels`` parameter is
        ``True``.

    :type labels_as_categories: :class:`bool <python:bool>`

    :param missing_as_NaN: If ``True``, will return any missing values as
      :class:`NaN <pandas:NaN>`. Otherwise will return missing values as per the
      configuration of missing value representation stored in the underlying SPSS data.
      Defaults to ``False``, which applies the missing value representation configured in
      the SPSS data itself.
    :type missing_as_NaN: :class:`bool <python:bool>`

    :param convert_datetimes: if ``True``, will convert the native integer representation
      of datetime values in the SPSS data to Pythonic
      :class:`datetime <python:datetime.datetime>`, or
      :class:`date <python:datetime.date>`, etc. representations (or Pandas
      :class:`datetime64 <pandas:datetime64>`, depending on the ``dates_as_datetime64``
      parameter). If ``False``, will leave the original integer representation. Defaults
      to ``True``.
    :type convert_datetimes: :class:`bool <python:bool>`

    :param dates_as_datetime64: If ``True``, will return any date values as Pandas
      :class:`datetime64 <pandas.datetime64>` types. Defaults to ``False``.

      .. caution::

        This parameter is only applied if ``convert_datetimes`` is set to ``True``.

    :type dates_as_datetime64: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>` if ``target`` was not :obj:`None <python:None>`,
      otherwise a :class:`BytesIO <python:BytesIO>` representation of the Excel file.
    :rtype: :obj:`None <python:None>` or :class:`str <python:str>`

    """
    if target and \
       not checkers.is_pathlike(target) and \
       not checkers.is_bytesIO(target) and \
       not checkers.is_type(target, 'ExcelWriter'):
        raise errors.InvalidDataFormatError('target must be a filename, BytesIO, '
                                            f'ExcelWriter, or None. '
                                            f'Was: {data.__class__.__name__}')

    df, metadata = _read_spss(data,
                              limit = limit,
                              offset = offset,
                              exclude_variables = exclude_variables,
                              include_variables = include_variables,
                              metadata_only = metadata_only,
                              apply_labels = apply_labels,
                              labels_as_categories = labels_as_categories,
                              missing_as_NaN = missing_as_NaN,
                              convert_datetimes = convert_datetimes,
                              dates_as_datetime64 = dates_as_datetime64,
                              **kwargs)

    return_target = False
    if not target or checkers.is_bytesIO(target):
        return_target = True
        target = BytesIO()

    df.to_excel(target,
                sheet_name = sheet_name,
                na_rep = null_text,
                header = include_header,
                startrow = start_row,
                startcol = start_column)

    if return_target:
        return target
