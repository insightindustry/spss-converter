"""
***********************************
tests.test_read
***********************************

Tests for the functions which read data from an SPSS file and convert it to a different
format.

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
def test_get_metadata(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read.get_metadata(data)
        assert result is not None
        assert checkers.is_type(result, 'Metadata') is True
        assert result.column_metadata is not None
    else:
        with pytest.raises(error):
            result = read.get_metadata(data)


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
def test_to_dataframe(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read.to_dataframe(data)
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
            result = read.to_dataframe(data)


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
def test_to_csv(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result = read.to_csv(data, limit = 1)
        assert result is not None
        assert isinstance(result, str) is True

    else:
        with pytest.raises(error):
            result = read.to_csv(data)


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
def test_to_json(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result_as_records = read.to_json(data, limit = 1, layout = 'records')
        result_as_table = read.to_json(data, limit = 1, layout = 'table')
        assert result_as_records is not None
        assert result_as_table is not None
        assert isinstance(result_as_records, str) is True
        assert isinstance(result_as_table, str) is True

    else:
        with pytest.raises(error):
            result_as_records = read.to_json(data, limit = 1, layout = 'records')
            result_as_table = read.to_json(data, limit = 1, layout = 'table')


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
def test_to_yaml(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result_as_records = read.to_yaml(data, limit = 1, layout = 'records')
        result_as_table = read.to_yaml(data, limit = 1, layout = 'table')
        assert result_as_records is not None
        assert result_as_table is not None
        assert isinstance(result_as_records, str) is True
        assert isinstance(result_as_table, str) is True

    else:
        with pytest.raises(error):
            result_as_records = read.to_yaml(data, limit = 1, layout = 'records')
            result_as_table = read.to_yaml(data, limit = 1, layout = 'table')

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
def test_to_dict(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result_as_records = read.to_dict(data, limit = 1, layout = 'records')
        result_as_table = read.to_dict(data, limit = 1, layout = 'table')
        assert result_as_records is not None
        assert result_as_table is not None
        assert isinstance(result_as_records, list) is True
        assert isinstance(result_as_table, dict) is True

    else:
        with pytest.raises(error):
            result_as_records = read.to_dict(data, limit = 1, layout = 'records')
            result_as_table = read.to_dict(data, limit = 1, layout = 'table')


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
def test_to_excel(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        result_as_records = read.to_excel(data, limit = 1)
        assert result_as_records is not None

    else:
        with pytest.raises(error):
            result_as_records = read.to_excel(data, limit = 1)
