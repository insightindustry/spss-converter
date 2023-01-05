from typing import Union, Optional, Any
from os import PathLike
import tempfile

from io import BytesIO
import yaml
import simplejson as json
import pyreadstat
from validator_collection import validators, checkers
from spss_converter.Metadata import Metadata
import pandas

DataFrame = pandas.DataFrame


def from_dataframe(df: DataFrame,
                   target: Optional[Union['PathLike[Any]', BytesIO]] = None,
                   metadata: Optional[Metadata] = None,
                   compress: bool = False):
    """Create an SPSS dataset from a `Pandas <https://pandas.pydata.org/>`_
    :class:`DataFrame <pandas:DataFrame>`.

    :param df: The :class:`DataFrame` to serialize to an SPSS dataset.
    :type df: :class:`pandas.DataFrame <pandas:DataFrame>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param metadata: The :class:`Metadata` associated with the dataset. If
      :obj:`None <python:None>`, will attempt to derive it form ``df``. Defaults to
      :obj:`None <python:None>`.
    :type metadata: :class:`Metadata` / :obj:`None <python:None>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    :raises ValueError: if ``df`` is not a :class:`pandas.DataFrame <pandas:DataFrame>`
    :raises ValueError: if ``metadata`` is not a :class:`Metadata`

    """
    if not checkers.is_type(df, 'DataFrame'):
        raise ValueError(f'df must be a pandas.DataFrame. Was: {df.__class__.__name__}')
    if metadata and not checkers.is_type(metadata, ('Metadata',
                                                    'metadata_container',
                                                    'dict')):
        raise ValueError(f'metadata must be a Metadata instance or compatible object. '
                         f'Was: {metadata.__class__.__name__}')
    elif metadata and checkers.is_type(metadata, 'metadata_container'):
        metadata = Metadata.from_pyreadstat(metadata)
    elif metadata and checkers.is_type(metadata, 'dict'):
        metadata = Metadata.from_dict(metadata)

    is_file = False
    if target and checkers.is_pathlike(target):
        is_file = True
    elif target:
        target = validators.bytesIO(target, allow_empty = False)

    if metadata:
        as_pyreadstat = metadata.to_pyreadstat()
    else:
        as_pyreadstat = None

    if target and is_file:
        if as_pyreadstat:
            pyreadstat.write_sav(
                df = df,
                dst_path = target,
                file_label = as_pyreadstat.file_label,
                column_labels = as_pyreadstat.column_labels,
                compress = compress,
                note = as_pyreadstat.notes,
                variable_value_labels = as_pyreadstat.variable_value_labels,
                missing_ranges = as_pyreadstat.missing_ranges,
                variable_display_width = as_pyreadstat.variable_display_width,
                variable_measure = as_pyreadstat.variable_measure
            )
        else:
            pyreadstat.write_sav(df = df,
                                 dst_path = target,
                                 compress = compress)

    else:
        with tempfile.NamedTemporaryFile() as temp_file:
            if as_pyreadstat:
                pyreadstat.write_sav(
                    df = df,
                    dst_path = temp_file.name,
                    file_label = as_pyreadstat.file_label,
                    column_labels = as_pyreadstat.column_labels,
                    compress = compress,
                    note = as_pyreadstat.notes,
                    variable_value_labels = as_pyreadstat.variable_value_labels,
                    missing_ranges = as_pyreadstat.missing_ranges,
                    variable_display_width = as_pyreadstat.variable_display_width,
                    variable_measure = as_pyreadstat.variable_measure
                )
            else:
                pyreadstat.write_sav(df = df,
                                     dst_path = temp_file.name,
                                     compress = compress)

            if target:
                target.write(temp_file.read())
            else:
                target = BytesIO(temp_file.read())

            return target


def from_csv(as_csv: Union[str, 'PathLike[Any]', BytesIO],
             target: Optional[Union['PathLike[Any]', BytesIO]] = None,
             compress: bool = False,
             delimiter = '|',
             **kwargs):
    """Convert a CSV file into an SPSS dataset.

    .. tip::

      If you pass any additional keyword arguments, those keyword arguments will be passed
      onto the :func:`pandas.read_csv() <pandas:pandas.read_csv>` function.

    :param as_csv: The CSV data that you wish to convert into an SPSS dataset.
    :type as_csv: :class:`str <python:str>` / File-location /
      :class:`BytesIO <python:io.BytesIO>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :param delimiter: The delimiter used between columns. Defaults to ``|``.
    :type delimiter: :class:`str <python:str>`

    :param kwargs: Additional keyword arguments which will be passed onto the
      :func:`pandas.read_csv() <pandas:pandas.read_csv>` function.
    :type kwargs: :class:`dict <python:dict>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    """
    df = pandas.read_csv(as_csv,
                         delimiter = delimiter,
                         **kwargs)
    if 'Unnamed: 0' in df:
        df = df.drop(['Unnamed: 0'], axis = 1)

    result = from_dataframe(df,
                            target = target,
                            compress = compress)

    return result


def from_dict(as_dict: dict,
              target: Optional[Union['PathLike[Any]', BytesIO]] = None,
              compress: bool = False,
              **kwargs):
    """Convert a :class:`dict <python:dict>` object into an SPSS dataset.

    .. tip::

      If you pass any additional keyword arguments, those keyword arguments will be passed
      onto the :meth:`DataFrame.from_dict() <pandas:pandas.DataFrame.from_dict>` method.

    :param as_dict: The :class:`dict <python:dict>` data that you wish to convert into an
      SPSS dataset.
    :type as_dict: :class:`dict <python:dict>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :param kwargs: Additional keyword arguments which will be passed onto the
      :meth:`DataFrame.from_dict() <pandas:pandas.DataFrame.from_dict>` method.
    :type kwargs: :class:`dict <python:dict>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    """
    df = DataFrame.from_dict(as_dict, **kwargs)

    result = from_dataframe(df,
                            target = target,
                            compress = compress)

    return result


def from_json(as_json: Union[str, 'PathLike[Any]', BytesIO],
              target: Optional[Union['PathLike[Any]', BytesIO]] = None,
              layout: str = 'records',
              compress: bool = False,
              **kwargs):
    """Convert JSON data into an SPSS dataset.

    .. tip::

      If you pass any additional keyword arguments, those keyword arguments will be passed
      onto the :func:`pandas.read_json() <pandas:pandas.read_json>` function.

    :param as_json: The JSON data that you wish to convert into an SPSS dataset.
    :type as_json: :class:`str <python:str>` / File-location /
      :class:`BytesIO <python:io.BytesIO>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param layout: Indicates the layout schema to use for the JSON representation of the
      data. Accepts:

        * ``records``, where the resulting JSON object represents an array of objects
          where each object corresponds to a single record, with key/value pairs for each
          column and that record's corresponding value
        * ``table``, where the resulting JSON object contains a metadata (data map)
          describing the data schema along with the resulting collection of record objects

      Defaults to ``records``.

    :type layout: :class:`str <python:str>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :param kwargs: Additional keyword arguments which will be passed onto the
      :func:`pandas.read_json() <pandas:pandas.read_json>` function.

      .. warning::

        If you supply an ``orient`` keyword argument (which is supported by
        :func:`pandas.read_json() <pandas:pandas.read_json>`), the ``orient``
        value will *override* the value supplied for ``layout``. This is an
        advanced use case, so use with caution.

    :type kwargs: :class:`dict <python:dict>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    """
    if layout not in ['records', 'table']:
        raise errors.InvalidLayoutError('layout must be either "records" or "table". '
                                        f'Was: "{layout}"')

    orient = kwargs.pop('orient', layout)

    df = pandas.read_json(as_json,
                          orient = orient,
                          **kwargs)

    result = from_dataframe(df,
                            target = target,
                            compress = compress)

    return result


def from_yaml(as_yaml: Union[str, 'PathLike[Any]', BytesIO],
              target: Optional[Union['PathLike[Any]', BytesIO]] = None,
              layout: str = 'records',
              compress: bool = False,
              **kwargs):
    """Convert YAML data into an SPSS dataset.

    .. tip::

      If you pass any additional keyword arguments, those keyword arguments will be passed
      onto the :meth:`DataFrame.from_dict() <pandas:pandas.DataFrame.from_dict>` method.

    :param as_yaml: The YAML data that you wish to convert into an SPSS dataset.
    :type as_yaml: :class:`str <python:str>` / File-location /
      :class:`BytesIO <python:io.BytesIO>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param layout: Indicates the layout schema to expect for the YAML representation of the
      data. Accepts:

        * ``records``, where the resulting JSON object represents an array of objects
          where each object corresponds to a single record, with key/value pairs for each
          column and that record's corresponding value
        * ``table``, where the resulting JSON object contains a metadata (data map)
          describing the data schema along with the resulting collection of record objects

      Defaults to ``records``.
    :type layout: :class:`str <python:str>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :param kwargs: Additional keyword arguments which will be passed onto the
      :meth:`pandas.from_json() <pandas:pandas.from_json>` function.

    :param kwargs: Additional keyword arguments which will be passed onto the
      :func:`pandas.read_json() <pandas:pandas.read_json>` function.

      .. warning::

        If you supply an ``orient`` keyword argument (which is supported by
        :func:`pandas.read_json() <pandas:pandas.read_json>`), the ``orient``
        value will *override* the value supplied for ``layout``. This is an
        advanced use case, so use with caution.

    :type kwargs: :class:`dict <python:dict>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    """
    if checkers.is_file(as_yaml) or checkers.is_bytesIO(as_yaml):
        file_path = as_yaml
        with open(file_path, 'rb') as yaml_file:
            as_dict = yaml.safe_load(yaml_file)
    else:
        as_yaml = validators.string(as_yaml, allow_empty = False)
        as_dict = yaml.safe_load(as_yaml)
        as_json = json.dumps(as_dict)

    return from_json(as_json,
                     target = target,
                     layout = layout,
                     compress = compress,
                     **kwargs)


def from_excel(as_excel,
               target: Optional[Union['PathLike[Any]', BytesIO]] = None,
               compress: bool = False,
               **kwargs):
    """Convert Excel data into an SPSS dataset.

    .. tip::

      If you pass any additional keyword arguments, those keyword arguments will be passed
      onto the :func:`pandas.read_excel() <pandas:pandas.read_excel>` function.

    :param as_excel: The Excel data that you wish to convert into an SPSS dataset.
    :type as_excel: :class:`str <python:str>` / File-location /
      :class:`BytesIO <python:io.BytesIO>` / :class:`bytes <python:bytes>` /
      :class:`ExcelFile <pandas.ExcelFile>`

    :param target: The target to which the SPSS dataset should be written. Accepts either
      a filename/path, a :class:`BytesIO <python:io.BytesIO>` object, or
      :obj:`None <python:None>`. If :obj:`None <python:None>` will return a
      :class:`BytesIO <python:io.BytesIO>` object containing the SPSS dataset. Defaults to
      :obj:`None <python:None>`.
    :type target: Path-like / :class:`BytesIO <python:io.BytesIO>` /
      :obj:`None <python:None>`

    :param compress: If ``True``, will return data in the compressed ZSAV format. If
      ``False``, will return data in the standards SAV format. Defaults to ``False``.
    :type compress: :class:`bool <python:bool>`

    :param kwargs: Additional keyword arguments which will be passed onto the
      :func:`pandas.read_excel() <pandas:pandas.read_excel>` function.
    :type kwargs: :class:`dict <python:dict>`

    :returns: A :class:`BytesIO <python:io.BytesIO>` object containing the SPSS data if
      ``target`` is :obj:`None <python:None>` or not a filename, otherwise
      :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` or :obj:`None <python:None>`

    """
    df = pandas.read_excel(as_excel, **kwargs)
    if 'Unnamed: 0' in df:
        df = df.drop(['Unnamed: 0'], axis = 1)

    result = from_dataframe(df,
                            target = target,
                            compress = compress)

    return result


def apply_metadata(df: DataFrame,
                   metadata: Union[Metadata, dict, pyreadstat.metadata_container],
                   as_category: bool = True):
    """Updates the :class:`DataFrame <pandas:DataFrame>` ``df`` based on the ``metadata``.

    :param df: The :class:`DataFrame <pandas:pandas.DataFrame>` to update.
    :type df: :class:`pandas.DataFrame <pandas:pandas.DataFrame>`

    :param metadata: The :class:`Metadata` to apply to ``df``.
    :type metadata: :class:`Metadata`, :class:`pyreadstat.metadata_container`, or
      compatible :class:`dict <python:dict>`

    :param as_category: if ``True``, will variables with formats will be transformed into
      categories in the :class:`DataFrame <pandas:pandas.DataFrame>`. Defaults to
      ``True``.
    :type as_category: :class:`bool <python:bool>`

    :returns: A copy of ``df`` updated to reflect ``metadata``.
    :rtype: :class:`DataFrame <pandas:pandas.DataFrame>`
    """
    if not checkers.is_type(df, 'DataFrame'):
        raise ValueError(f'df must be a pandas.DataFrame. Was: {df.__class__.__name__}')
    if not checkers.is_type(metadata, ('Metadata', 'metadata_container', 'dict')):
        raise ValueError(f'metadata must be a Metadata instance or compatible object. '
                         f'Was: {metadata.__class__.__name__}')
    elif checkers.is_type(metadata, 'metadata_container'):
        metadata = Metadata.from_pyreadstat(metadata)
    elif checkers.is_type(metadata, 'dict'):
        metadata = Metadata.from_dict(metadata)

    as_pyreadstat = metadata.to_pyreadstat()

    return pyreadstat.set_value_labels(df,
                                       metadata = as_pyreadstat,
                                       formats_as_category = as_category)
