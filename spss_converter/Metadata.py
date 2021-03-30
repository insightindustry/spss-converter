from enum import Enum
from typing import Union

from validator_collection import validators, checkers
from spss_converter import errors
from pyreadstat._readstat_parser import metadata_container


class VariableAlignmentEnum(str, Enum):
    UNKNOWN = 'unknown'
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class VariableMeasureEnum(str, Enum):
    UNKNOWN = 'unknown'
    NOMINAL = 'nominal'
    ORDINAL = 'ordinal'
    SCALE = 'scale'


class ColumnMetadata(object):
    """Object representation of the :term:`metadata <Metadata>` that describes a column or
    variable form an SPSS file."""

    def __init__(self, **kwargs):
        self._name = None
        self._label = None
        self._value_metadata = None
        self._missing_range_metadata = None
        self._missing_value_metadata = None
        self._alignment = VariableAlignmentEnum.UNKNOWN
        self._measure = VariableMeasureEnum.UNKNOWN
        self._display_width = None
        self._storage_width = None

        for key in kwargs:
            value = kwargs.get(key)
            setattr(self, key, value)

    @property
    def name(self):
        """The name of the column/variable.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validators.variable_name(value, allow_empty = True)

    @property
    def label(self):
        """The label applied ot the column/variable.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._label

    @label.setter
    def label(self, value):
        self._label = validators.string(value, allow_empty = True)

    @property
    def alignment(self):
        """The alignment to apply to values from this column/variable when displaying
        data. Defaults to ``'unknown'``.

        Accepts either ``'unknown'``, ``'left'``, ``'center'``, or ``'right'`` as
        either a case-insensitive :class:`str <python:str>` or a
        :class:`VariableAlignmentEnum`.

        :rtype: :class:`VariableAlignmentEnum`
        """
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        value = validators.string(value, allow_empty = False)
        value = value.lower()
        if value not in [member.value
                         for name, member in VariableAlignmentEnum.__members__.items()]:
            raise ValueError(f'value ({value}) is not a recognized alignment')

        self._alignment = value

    @property
    def measure(self):
        """A classification of the type of measure (or value type) represented by the
        variable. Defaults to ``'unknown'``.

        Accepts either ``'unknown'``, ``'nominal'``, ``'ordinal'``, or ``'scale'``.

        :rtype: :class:`VariableMeasureEnum`
        """
        return self._measure

    @measure.setter
    def measure(self, value):
        value = validators.string(value, allow_empty = False)
        value = value.lower()
        if value not in [member.value
                         for name, member in VariableMeasureEnum.__members__.items()]:
            raise ValueError(f'value ({value}) is not a recognized measure')

        self._measure = value

    @property
    def display_width(self):
        """The maximum width at which the value is displayed. Defaults to 0.

        :rtype: :class:`int <python:int>`
        """
        return self._display_width

    @display_width.setter
    def display_width(self, value):
        self._display_width = validators.integer(value,
                                                 allow_empty = False,
                                                 minimum = 0,
                                                 coerce_value = True)

    @property
    def storage_width(self):
        """The width of data to store in the data file for the value. Defaults to 0.

        :rytpe: :class:`int <python:int>`
        """
        return self._storage_width

    @storage_width.setter
    def storage_width(self, value):
        self._storage_width = validators.integer(value,
                                                 allow_empty = False,
                                                 minimum = 0,
                                                 coerce_value = True)

    @property
    def value_metadata(self):
        """Collection of values possible for the column/variable, with corresponding
        labels for each value.

        :returns: :class:`dict <python:dict>` whose keys are the values in the raw data
          and whose values are the labels for each value. May be :obj:`None <python:None>`
          for variables whose value is not coded.
        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        return self._value_metadata

    @value_metadata.setter
    def value_metadata(self, value):
        value = validators.dict(value, allow_empty = True)
        if not value:
            self._value_metadata = None
        else:
            self._value_metadata = {
                key: validators.string(value[key], allow_empty = True) for key in value
            }

    @property
    def missing_range_metadata(self):
        """Collection of meta data that defines the numerical ranges that are to be
        considered missing in the underlying data.

        :returns: :class:`list <python:list>` of :class:`dict <python:dict>` with keys
          ``'low'`` and ``'high'`` for the low/high values of the range to apply when
          raw values are missing (:obj:`None <python:None>`).
        :rtype: :class:`list <python:list>` of :class:`dict <python:dict>` or
          :obj:`None <python:None>`

        """
        return self._missing_range_metadata

    @missing_range_metadata.setter
    def missing_range_metadata(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._missing_range_metadata = None
        else:
            ranges = [validators.dict(x, allow_empty = False) for x in value]
            validated_ranges = []
            for range in ranges:
                if 'high' not in range or 'low' not in range:
                    raise ValueError('missing_range_metadata requires a "high" and "low"'
                                     ' boundary to be defined.')

                validated_range = {
                    'high': validators.numeric(range.get('high'), allow_empty = False),
                    'low': validators.numeric(range.get('low'), allow_empty = False)
                }

                validated_ranges.append(validated_range)

            self._missing_range_metadata = validated_ranges

    @property
    def missing_value_metadata(self):
        """Value used to represent misisng values in the raw data. Defaults to
        :obj:`None <python:None>`.

        .. note::

          This is not actually relevant for SPSS data, but is an artifact for SAS and SATA
          data.

        :rtype: :class:`list <python:list>` of :class:`int <python:int>` or
          :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._missing_value_metadata

    @missing_value_metadata.setter
    def missing_value_metadata(self, value):
        if not value:
            self._missing_value_metadata = None
            return
        elif checkers.is_string(value):
            value = [value]
        elif checkers.is_numeric(value):
            value = [value]

        validated_values = []
        for item in value:
            try:
                validated_item = validators.string(item, allow_empty = False)
            except (ValueError, TypeError):
                validated_item = validators.int(item, allow_empty = False)

            validated_values.append(validated_item)

        self._missing_value_metadata = validated_values

    @classmethod
    def from_dict(cls, as_dict: dict):
        """Create a new :class:`ColumnMetadata` instance from a
        :class:`dict <python:dict>` representation.

        :param as_dict: The :class:`dict <python:dict>` representation of the
          :class:`ColumnMetadata`.
        :type as_dict: :class:`dict <python:dict>`

        :returns: The :class:`ColumnMetadata` instance.
        :rtype: :class:`ColumnMetadata`

        """
        instance = cls()
        instance.name = as_dict.pop('name', instance.name)
        instance.label = as_dict.pop('label', instance.label)
        instance.alignment = as_dict.pop('alignment', instance.alignment)
        instance.measure = as_dict.pop('measure', instance.measure)
        instance.display_width = as_dict.pop('display_width', instance.display_width)
        instance.storage_width = as_dict.pop('storage_width', instance.storage_width)
        instance.value_metadata = as_dict.pop('value_metadata', instance.value_metadata)
        instance.missing_range_metadata = as_dict.pop('missing_range_metadata',
                                                      instance.missing_range_metadata)
        instance.missing_value_metadata = as_dict.pop('missing_value_metadata',
                                                      instance.missing_value_metadata)

        return instance

    @classmethod
    def from_pyreadstat_metadata(cls,
                                 name: str,
                                 as_metadata):
        """Create a new :class:`ColumnMetadata` instance from a
        `Pyreadstat <https://github.com/Roche/pyreadstat/>`_ metadata object.

        :param name: The name of the variable for which a :class:`ColumnMetadata`
          instance should be created.
        :type name: :class:`str <python:str>`

        :param as_metadata: The `Pyreadstat <https://github.com/Roche/pyreadstat/>`_
          metadata object from which the column's metadata should be extracted.
        :type as_metadata: :class:`Pyreadstat.metadata_container <pyreadstat:_readstat_parser.metadata_container>`

        :returns: The :class:`ColumnMetadata` instance.
        :rtype: :class:`ColumnMetadata`

        """
        name = validators.variable_name(name, allow_empty = False)
        if name not in as_metadata.column_names:
            raise errors.ColumnNameNotFoundError(f'column name ({name}) not found in '
                                                 'as_metadata')
        instance = cls(name = name)
        instance.label = as_metadata.column_names_to_labels.get(name, None)
        instance.alignment = as_metadata.variable_alignment.get(name, instance.alignment)
        instance.measure = as_metadata.variable_measure.get(name, instance.measure)
        instance.display_width = as_metadata.variable_display_width.get(name,
                                                                        instance.display_width)
        instance.storage_width = as_metadata.variable_storage_width.get(name,
                                                                        instance.storage_width)
        instance.value_metadata = as_metadata.variable_value_labels.get(name,
                                                                        instance.value_metadata)

        missing_ranges = as_metadata.missing_ranges.get(name, [])
        instance.missing_range_metadata = [
            {
                'low': x.get('lo'),
                'high': x.get('hi')
            } for x in missing_ranges
        ]

        instance.missing_value_metadata = as_metadata.missing_user_values.get(name, None)

        return instance

    def to_dict(self) -> dict:
        """Generate a :class:`dict <python:dict>` representation of the instance.

        :rtype: :class:`dict <python:dict>`
        """
        return {
            'name': self.name,
            'label': self.label,
            'alignment': self.alignment,
            'measure': self.measure,
            'display_width': self.display_width,
            'storage_width': self.storage_width,
            'value_metadata': self.value_metadata,
            'missing_range_metadata': self.missing_range_metadata,
            'missing_value_metadata': self.missing_value_metadata
        }

    def add_to_pyreadstat(self, pyreadstat):
        """Update ``pyreadstat`` to include the metadata for this column/variable.

        :param pyreadstat: The `Pyreadstat <https://github.com/Roche/pyreadstat/>`_
          metadata object where the :class:`ColumnMetadata` data should be updated.
        :type pyreadstat: :class:`metadata_container <pyreadstat:_readstat_parser.metadata_container`

        :returns: The `Pyreadstat <https://github.com/Roche/pyreadstat/>`_ metadata.
        :rtype: :class:`metadata_container <pyreadstat:_readstat_parser.metadata_container`
        """
        pyreadstat.column_names_to_labels[self.name] = self.label
        pyreadstat.variable_alignment[self.name] = str(self.alignment)
        pyreadstat.variable_measure[self.name] = str(self.measure)
        pyreadstat.variable_display_width[self.name] = self.display_width
        pyreadstat.variable_storage_width[self.name] = self.storage_width
        if self.value_metadata is not None:
            pyreadstat.variable_value_labels[self.name] = self.value_metadata
            pyreadstat.value_labels[self.label] = self.value_metadata
        pyreadstat.variable_to_label[self.name] = self.label

        if self.missing_range_metadata:
            pyreadstat.missing_ranges[self.name] = [
                {
                    'lo': x.get('low'),
                    'hi': x.get('high')
                } for x in self.missing_range_metadata
            ]
        if self.missing_value_metadata:
            pyreadstat.missing_user_values[self.name] = [x for x in self.missing_value_metadata]

        if self.name not in pyreadstat.column_names:
            pyreadstat.column_names.append(self.name)
            pyreadstat.column_labels.append(self.label)
        else:
            index = pyreadstat.column_names.index(self.name)
            pyreadstat.column_names[index] = self.name
            pyreadstat.column_labels[index] = self.label

        return pyreadstat


class Metadata(object):
    """Object representation of :term:`metadata <Metadata>` retrieved from an SPSS file.
    """

    def __init__(self, **kwargs):
        self._column_metadata = None
        self._notes = None
        self._file_encoding = None
        self._rows = 0
        self._table_name = None
        self._file_label = None

        for key in kwargs:
            setattr(self, key, kwargs.get(key))

    @property
    def column_metadata(self):
        """Collection of metadata that describes each column or variable within the
        dataset.

        :returns: A :class:`dict <python:dict>` where the key is the name of the
          column/variable and the value is a :class:`ColumnMetadata` object or compatible
          :class:`dict <python:dict>`.
        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`

        """
        return self._column_metadata

    @column_metadata.setter
    def column_metadata(self, value):
        value = validators.dict(value, allow_empty = True)
        if not value:
            self._column_metadata = None
        else:
            result = {}
            for key in value:
                key = validators.variable_name(key, allow_empty = False)
                if checkers.is_type(value[key], 'ColumnMetadata'):
                    result[key] = value[key]
                else:
                    result[key] = ColumnMetadata.from_dict(result[key])

            self._column_metadata = result

    @property
    def file_encoding(self) -> str:
        """The file encoding for the dataset.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._file_encoding

    @file_encoding.setter
    def file_encoding(self, value):
        self._file_encoding = validators.string(value, allow_empty = True)

    @property
    def notes(self) -> str:
        """Set of notes related to the file.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._notes

    @notes.setter
    def notes(self, value):
        if checkers.is_iterable(value):
            value = '\n'.join(value)
        self._notes = validators.string(value, allow_empty = True)

    @property
    def table_name(self) -> Union[str, None]:
        """The name of the data table.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        self._table_name = validators.variable_name(value, allow_empty = True)

    @property
    def file_label(self) -> Union[str, None]:
        """The file label.

        .. note::

          This property is irrelevant for SPSS, but is relevant for SAS data.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._file_label

    @file_label.setter
    def file_label(self, value):
        self._file_label = validators.string(value, allow_empty = True)

    @property
    def columns(self):
        """The number of columns/variables in the dataset.

        :rtype: :class:`int <python:int>`
        """
        if not self.column_metadata:
            return 0

        return len(self.column_metadata)

    @property
    def rows(self):
        """The number of cases or rows in the dataset.

        :rtype: :class:`int <python:int>`
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = validators.integer(value,
                                        allow_empty = False,
                                        coerce_value = False,
                                        minimum = 0)

    @classmethod
    def from_dict(cls, as_dict: dict):
        """Create a :class:`Metadata` instance from a :class:`dict <python:dict>`
        representation.

        :param as_dict: A :class:`dict <python:dict>` representation of the
          :class:`Metadata`.
        :type as_dict: :class:`dict <python:dict>`

        :returns: A :class:`Metadata` instance
        :rtype: :class:`Metadata`

        """
        instance = cls()
        instance.notes = as_dict.get('notes', instance.notes)
        instance.table_name = as_dict.get('table_name', instance.table_name)
        instance.file_label = as_dict.get('file_label', instance.file_label)
        instance.rows = as_dict.get('rows', instance.rows)
        instance.file_encoding = as_dict.get('file_encoding', instance.file_encoding)
        instance.column_metadata = as_dict.get('column_metadata',
                                               instance.column_metadata)

        return instance

    def to_dict(self) -> dict:
        """Return a :class:`dict <python:dict>` representation of the instance.

        :rtype: :class:`dict <python:dict>`
        """
        return {
            'table_name': self.table_name,
            'file_label': self.file_label,
            'file_encoding': self.file_encoding,
            'columns': self.columns,
            'rows': self.rows,
            'column_metadata': self.column_metadata,
            'notes': self.notes
        }

    @classmethod
    def from_pyreadstat(cls, as_metadata):
        """Create a :class:`Metadata` instance from a
        `Pyreadstat <https://github.com/Roche/pyreadstat/>`_ metadata object.

        :param as_metadata: The `Pyreadstat <https://github.com/Roche/pyreadstat/>`_
          metadata object from which the :class:`Metadata` instance should be created.
        :type as_metadata: :class:`Pyreadstat.metadata_container <pyreadstat:_readstat_parser.metadata_container>`

        :returns: The :class:`Metadata` instance.
        :rtype: :class:`Metadata`
        """
        instance = cls()
        instance.notes = as_metadata.notes
        instance.table_name = as_metadata.table_name
        instance.file_label = as_metadata.file_label
        instance.rows = as_metadata.number_rows
        instance.file_encoding = as_metadata.file_encoding

        column_metadata = {}
        for x in as_metadata.column_names:
            column_metadata[x] = ColumnMetadata.from_pyreadstat_metadata(x, as_metadata)

        instance.column_metadata = {
            x: ColumnMetadata.from_pyreadstat_metadata(x, as_metadata)
            for x in as_metadata.column_names
        }

        return instance

    def to_pyreadstat(self):
        """Create a `Pyreadstat <https://github.com/Roche/pyreadstat/>`_ metadata
        representation of the :class:`Metadata` instance.

        :returns: The `Pyreadstat <https://github.com/Roche/pyreadstat/>`_ metadata.
        :rtype: :class:`metadata_container <pyreadstat:_readstat_parser.metadata_container`
        """
        as_metadata = metadata_container()
        as_metadata.table_name = self.table_name
        as_metadata.file_label = self.file_label
        as_metadata.file_encoding = self.file_encoding
        if self.notes and len(self.notes.split('\n')) > 1:
            notes = self.notes[0]
        else:
            notes = self.notes
        as_metadata.notes = notes
        as_metadata.rows = self.rows

        for column in self.column_metadata:
            as_metadata = self.column_metadata[column].add_to_pyreadstat(as_metadata)

        return as_metadata
