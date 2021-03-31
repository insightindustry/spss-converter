"""
***********************************
tests.test_write
***********************************

Tests for the functions which write data to an SPSS file when converted from a different
format.

"""
import pytest
import tempfile
import os

from validator_collection import checkers, errors

from spss_converter import read, write
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
def test_from_dataframe(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        df, metadata = read.to_dataframe(data)
        result = write.from_dataframe(df, metadata = metadata)
        assert result is not None

    else:
        with pytest.raises(error):
            df, metadata = read.to_dataframe(data)
            result = write.from_dataframe(df, metadata = metadata)


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
def test_from_csv(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        with tempfile.NamedTemporaryFile(delete = False) as temp_file:
            temp_file_name = temp_file.name

        as_csv = read.to_csv(data,
                             target = temp_file_name,
                             limit = 1)
        assert as_csv is None

        result = write.from_csv(temp_file_name, delimiter = '|')
        assert result is not None

        os.remove(temp_file_name)

    else:
        with tempfile.NamedTemporaryFile(delete = False) as temp_file:
            temp_file_name = temp_file.name

        with pytest.raises(error):

            as_csv = read.to_csv(data,
                                 target = temp_file_name,
                                 limit = 1)
            assert as_csv is None

            result = write.from_csv(temp_file_name, delimiter = '|')
            assert result is not None

        os.remove(temp_file_name)


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
def test_from_dict(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        as_dict = read.to_dict(data, limit = 1)
        assert as_dict is not None

        result = write.from_dict(as_dict)
        assert result is not None

    else:
        with pytest.raises(error):
            as_dict = read.to_dict(data, limit = 1)
            assert as_dict is not None

            result = write.from_dict(as_dict)


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
def test_from_json(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        as_json = read.to_json(data, limit = 1)
        assert as_json is not None

        result = write.from_json(as_json)
        assert result is not None

    else:
        with pytest.raises(error):
            as_json = read.to_json(data, limit = 1)
            assert as_json is not None

            result = write.from_json(as_json)


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
def test_from_yaml(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        as_yaml = read.to_yaml(data, limit = 1)
        assert as_yaml is not None

        result = write.from_yaml(as_yaml)
        assert result is not None

    else:
        with pytest.raises(error):
            as_yaml = read.to_yaml(data, limit = 1)
            assert as_yaml is not None

            result = write.from_yaml(as_yaml)


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
def test_from_excel(input_files, filename, as_file, error):
    input_data = check_input_file(input_files, filename)
    if not as_file:
        with open(input_data, 'rb') as file_:
            data = file_.read()
    else:
        data = input_data

    if not error:
        as_excel = read.to_excel(data, limit = 1)
        assert as_excel is not None

        result = write.from_excel(as_excel)
        assert result is not None

    else:
        with pytest.raises(error):
            as_excel = read.to_excel(data, limit = 1)
            result = write.from_excel(as_excel)
