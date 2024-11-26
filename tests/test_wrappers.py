import os
from pathlib import Path

import pytest

from split_settings.tools import compiled, entry, one_of, optional

_TESTS_DIR = str(Path(__file__).parent)


def test_entry_raises_error_when_no_files():
    """This test checks that entry() raises an error when no files are found."""
    entry_obj = entry('non_existent.py')

    with pytest.raises(OSError, match='No such file'):
        entry_obj.get_files_to_include(_TESTS_DIR)


def test_entry_disallows_pyc():
    """This test checks that entry() disallows .pyc files."""
    with pytest.raises(
        ValueError,
        match='Expected a Python source file: fixture_file.pyc',
    ):
        entry('fixture_file.pyc')


def test_entry_disallows_pyc_matches(fixture_file, fixture_file_pyc):
    """This test checks that entry() disallows .pyc files in glob."""
    entry_obj = entry('{0}*'.format(fixture_file))

    with pytest.raises(
        ValueError,
        match=r'A Python compiled file matched the pattern: {0}\*'.format(
            fixture_file,
        ),
    ):
        entry_obj.get_files_to_include(_TESTS_DIR)


def test_compiled_disallows_py():
    """This test checks that compiled() disallows .py files."""
    with pytest.raises(
        ValueError,
        match='Expected a Python compiled file: fixture_file.py',
    ):
        compiled('fixture_file.py')


def test_compiled_disallows_py_matches(fixture_file_pyc, fixture_file):
    """This test checks that compiled() disallows .py files in glob."""
    compiled_obj = compiled('{0}*'.format(fixture_file))

    with pytest.raises(
        ValueError,
        match=r'A Python source file matched the pattern: {0}\*'.format(
            fixture_file,
        ),
    ):
        compiled_obj.get_files_to_include(_TESTS_DIR)


def test_one_of_requires_arguments():
    """Tests that `one_of` requires at least 1 argument."""
    with pytest.raises(
        ValueError,
        match='Expected at least 1 argument but received 0.',
    ):
        one_of()


def test_one_of_iterates_till_first_present_file(fixture_file):
    """This test checks that `one_of` iterates till the first present file."""
    one_of_obj = one_of('non_existent.py', fixture_file)
    assert one_of_obj.get_files_to_include(_TESTS_DIR) == [
        os.path.join(_TESTS_DIR, fixture_file),
    ]


def test_one_of_raises_error_when_no_files():
    """This test checks that `one_of` raises `OSError` if no files are found."""
    one_of_obj = one_of('non_existent.py', 'also_non_existent.py')

    with pytest.raises(OSError, match='No such file'):
        one_of_obj.get_files_to_include(_TESTS_DIR)


def test_optional_requires_arguments():
    """This test checks that `optional` requires at least 1 argument."""
    with pytest.raises(TypeError):
        optional()


def test_optional_can_handle_blank():
    """This text checks that `optional` can handle a blank string or `None`."""
    assert not optional('').inner.inner
    assert not optional(None).inner.inner


def test_nesting_compiled_in_optional():
    """This test checks that `compiled` can be nested in `optional`."""
    optional_obj = optional(compiled('non_existent.pyc'))
    assert not optional_obj.get_files_to_include(_TESTS_DIR)


def test_nesting_one_of_in_optional():
    """This test checks that `one_of` can be nested in `optional`."""
    optional_obj = optional(one_of('non_existent.py', 'also_non_existent.py'))
    assert not optional_obj.get_files_to_include(_TESTS_DIR)


def test_nesting_compiled_in_one_of(fixture_file_pyc):
    """This test checks that `compiled` can be nested in `one_of`."""
    one_of_obj = one_of(
        compiled('non_existent.pyc'),
        compiled(fixture_file_pyc),
    )
    assert one_of_obj.get_files_to_include(_TESTS_DIR) == [
        os.path.join(_TESTS_DIR, fixture_file_pyc),
    ]
