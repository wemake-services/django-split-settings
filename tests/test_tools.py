# -*- coding: utf-8 -*-

import os

import pytest
import six

from split_settings.tools import include

_FIXTURE_VALUE = 'FIXTURE_VALUE'


def test_missing_file_error(scope):
    """This test covers the IOError, when file does not exist."""
    with pytest.raises(IOError):
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
    include(
        six.text_type(fixture_file),  # unicode on py2, str on py3
        scope=scope,
    )
    assert _FIXTURE_VALUE in scope


def test_caller_scope_automatically(fixture_file):
    """
    Tests `include` function for automatic `globals()` extraction.

    Now you can omit positional argument `scope`.
    """
    include(fixture_file)

    assert _FIXTURE_VALUE in globals()  # noqa: WPS421
