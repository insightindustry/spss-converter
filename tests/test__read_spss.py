"""
***********************************
tests.test__read_spss
***********************************

Tests for the ``_read_spss()`` internal function defined in the ``spss_converter/read``
module.

"""
import pytest

from validator_collection import checkers, errors

from spss_converter import read
from tests.fixtures import input_files, check_input_file


@pytest.mark.parametrize('filename, as_file, error', [
    ('sample.sav', True, None),
    ('sample.zsav', True, None),
    ('sample_large.sav', True, None),
    ('sample_missing.sav', True, None),
    ('ordered_category.sav', True, None),
    ('tegulu.sav', True, None),
    ('test_width.sav', True, None),

    ('sample.sav', False, None),
    ('sample.zsav', False, None),
    ('sample_large.sav', False, None),
    ('sample_missing.sav', False, None),
    ('ordered_category.sav', False, None),
    ('tegulu.sav', False, None),
    ('test_width.sav', False, None),

    ('hebrews.sav', True, errors.InvalidVariableNameError),
])
def test_default_params(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read._read_spss(data)
        assert result is not None
        assert isinstance(result, tuple) is True
        assert len(result) == 2
        assert result[0] is not None
        assert result[1] is not None
        assert checkers.is_type(result[0], 'DataFrame') is True
        assert checkers.is_type(result[1], 'Metadata') is True

        assert len(result[0]) == result[1].rows

    else:
        with pytest.raises(error):
            result = read._read_spss(data)


@pytest.mark.parametrize('filename, as_file, limit, offset, error', [
    ('sample.sav', True, 1, 0, None),
    ('sample.zsav', True, 1, 0, None),
    ('sample_large.sav', True, 1, 0, None),
    ('sample_missing.sav', True, 1, 0, None),
    ('ordered_category.sav', True, 1, 0, None),
    ('tegulu.sav', True, 1, 0, None),
    ('test_width.sav', True, 1, 0, None),

    ('sample.sav', False, 1, 0, None),
    ('sample.zsav', False, 1, 0, None),
    ('sample_large.sav', False, 1, 0, None),
    ('sample_missing.sav', False, 1, 0, None),
    ('ordered_category.sav', False, 1, 0, None),
    ('tegulu.sav', False, 1, 0, None),
    ('test_width.sav', False, 1, 0, None),

    ('sample.sav', True, 4, 0, None),
    ('sample.zsav', True, 4, 0, None),
    ('sample_large.sav', True, 4, 0, None),
    ('sample_missing.sav', True, 4, 0, None),
    ('ordered_category.sav', True, 4, 0, None),
    ('tegulu.sav', True, 1, 0, None),
    ('test_width.sav', True, 4, 0, None),

    ('sample.sav', False, 4, 0, None),
    ('sample.zsav', False, 4, 0, None),
    ('sample_large.sav', False, 4, 0, None),
    ('sample_missing.sav', False, 4, 0, None),
    ('ordered_category.sav', False, 4, 0, None),
    ('tegulu.sav', False, 1, 0, None),
    ('test_width.sav', False, 4, 0, None),

    ('hebrews.sav', True, 0, 0, errors.InvalidVariableNameError),

    ('sample.sav', True, 1, 2, None),
    ('sample.zsav', True, 1, 2, None),
    ('sample_large.sav', True, 1, 2, None),
    ('sample_missing.sav', True, 1, 2, None),
    ('ordered_category.sav', True, 1, 2, None),
    ('tegulu.sav', True, 1, 2, None),
    ('test_width.sav', True, 1, 2, None),

    ('sample.sav', False, 1, 2, None),
    ('sample.zsav', False, 1, 2, None),
    ('sample_large.sav', False, 1, 2, None),
    ('sample_missing.sav', False, 1, 2, None),
    ('ordered_category.sav', False, 1, 2, None),
    ('tegulu.sav', False, 1, 2, None),
    ('test_width.sav', False, 1, 0, None),

    ('sample.sav', True, 4, 2, None),
    ('sample.zsav', True, 4, 2, None),
    ('sample_large.sav', True, 4, 2, None),
    ('sample_missing.sav', True, 4, 2, None),
    ('ordered_category.sav', True, 4, 2, None),
    ('tegulu.sav', True, 1, 2, None),
    ('test_width.sav', True, 4, 2, None),

    ('sample.sav', False, 4, 2, None),
    ('sample.zsav', False, 4, 2, None),
    ('sample_large.sav', False, 4, 2, None),
    ('sample_missing.sav', False, 4, 2, None),
    ('ordered_category.sav', False, 4, 2, None),
    ('tegulu.sav', False, 1, 2, None),
    ('test_width.sav', False, 4, 2, None),

    ('hebrews.sav', True, 0, 2, errors.InvalidVariableNameError),
])
def test_limit_offset(input_files, filename, as_file, limit, offset, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read._read_spss(data, limit = limit)
        assert result is not None
        assert isinstance(result, tuple) is True
        assert len(result) == 2
        assert result[0] is not None
        assert result[1] is not None
        assert checkers.is_type(result[0], 'DataFrame') is True
        assert checkers.is_type(result[1], 'Metadata') is True

        if limit is None:
            assert len(result[0]) == result[1].rows
        else:
            assert len(result[0]) == max((limit - offset), limit)

    else:
        with pytest.raises(error):
            result = read._read_spss(data)


@pytest.mark.parametrize('filename, as_file, exclude_variables, error', [
    ('sample.sav', True, ['mychar'], None),
    ('sample.zsav', True, ['mychar'], None),
    ('sample_large.sav', True, ['mychar'], None),
    ('sample_missing.sav', True, ['mychar'], None),
    ('ordered_category.sav', True, ['Col1'], None),
    ('tegulu.sav', True, ['record'], None),
    ('test_width.sav', True, ['StartDate'], None),

    ('sample.sav', False, ['mychar'], None),
    ('sample.zsav', False, ['mychar'], None),
    ('sample_large.sav', False, ['mychar'], None),
    ('sample_missing.sav', False, ['mychar'], None),
    ('ordered_category.sav', False, ['Col1'], None),
    ('tegulu.sav', False, ['record'], None),
    ('test_width.sav', False, ['StartDate'], None),

    ('hebrews.sav', True, ['mychar'], errors.InvalidVariableNameError),
])
def test_exclude_variables(input_files, filename, as_file, exclude_variables, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read._read_spss(data, exclude_variables = exclude_variables)
        assert result is not None
        assert isinstance(result, tuple) is True
        assert len(result) == 2
        assert result[0] is not None
        assert result[1] is not None
        assert checkers.is_type(result[0], 'DataFrame') is True
        assert checkers.is_type(result[1], 'Metadata') is True

        assert len(result[0]) == result[1].rows
        for variable in exclude_variables:
            metadata = result[1]
            assert variable not in metadata.column_metadata
            assert variable not in result[0]

    else:
        with pytest.raises(error):
            result = read._read_spss(data)


@pytest.mark.parametrize('filename, as_file, error', [
    ('sample.sav', True, None),
    ('sample.zsav', True, None),
    ('sample_large.sav', True, None),
    ('sample_missing.sav', True, None),
    ('ordered_category.sav', True, None),
    ('tegulu.sav', True, None),
    ('test_width.sav', True, None),

    ('sample.sav', False, None),
    ('sample.zsav', False, None),
    ('sample_large.sav', False, None),
    ('sample_missing.sav', False, None),
    ('ordered_category.sav', False, None),
    ('tegulu.sav', False, None),
    ('test_width.sav', False, None),

    ('hebrews.sav', True, errors.InvalidVariableNameError),
])
def test_metadata_only(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read._read_spss(data, metadata_only = True)
        assert result is not None
        assert isinstance(result, tuple) is True
        assert len(result) == 2
        assert result[0] is not None
        assert result[1] is not None
        assert checkers.is_type(result[0], 'DataFrame') is True
        assert checkers.is_type(result[1], 'Metadata') is True

        assert len(result[0]) == 0
        assert result[1].rows > 0

    else:
        with pytest.raises(error):
            result = read._read_spss(data)
