import os

import pytest

from split_settings.tools import include, optional

_FIXTURE_VALUE = 'FIXTURE_VALUE'


def test_missing_file_error(scope):
    """This test covers the OSError, when file does not exist."""
    with pytest.raises(OSError, match='does-not-exist.py'):
        include('does-not-exist.py', scope=scope)


def test_keys_count(scope, fixture_file):
    """Scope must contain all base python attrs and a custom value."""
    include(fixture_file, scope=scope)

    # Keys:
    # 'FIXTURE_VALUE', '__file__', '__doc__',
    # '__builtins__', '__included_files__'
    assert len(scope.keys()) == 5


def test_included_file_scope(scope, fixture_file):
    """Test emulates gunicorn behavior with `__included_file__` value."""
    base = os.path.dirname(__file__)
    saved_file = os.path.join(base, 'basic')
    scope['__included_file__'] = saved_file

    include(fixture_file, scope=scope)

    assert _FIXTURE_VALUE in scope
    assert scope['__included_file__'] == saved_file


def test_empty_included_file(scope, fixture_file):
    """Test when there's no `__included_file__`."""
    include(fixture_file, scope=scope)

    assert _FIXTURE_VALUE in scope
    assert '__included_file__' not in scope


def test_unicode_passed(scope, fixture_file):
    """Tests the `unicode` filename in `python2`."""
    include(fixture_file, scope=scope)
    assert _FIXTURE_VALUE in scope


def test_caller_scope_automatically(fixture_file):
    """
    Tests `include` function for automatic `globals()` extraction.

    Now you can omit positional argument `scope`.
    """
    include(fixture_file)

    assert _FIXTURE_VALUE in globals()  # noqa: WPS421


def test_optional_none(fixture_file):
    """
    Tests that calling optional on `None` and including the result is fine.

    Previously it used to raise an error.
    """
    include(optional(None))  # should not fail


def test_bad_pyc_file(scope, fixture_file_bad_pyc):
    """
    Tests that a bad `.pyc` file raises a `ValueError`.
    """

    with pytest.raises(ValueError, match=fixture_file_bad_pyc):
        include(fixture_file_bad_pyc, scope=scope)


def test_unsupported_file(scope, fixture_file_unsupported):
    """
    Tests that an unsupported file extension raises a `ValueError`.
    """

    with pytest.raises(ValueError, match=fixture_file_unsupported):
        include(fixture_file_unsupported, scope=scope)
