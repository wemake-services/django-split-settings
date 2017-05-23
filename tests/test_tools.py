# -*- coding: utf-8 -*-
# pylint: disable=no-member

"""
This file contains unit-tests.
"""

import os
import sys
import six
import pytest

from split_settings.tools import include
from split_settings.tools import FastOpen, FileObjWrapper


def test_fast_open_ok():
    """
    This test simulate file read using FastOpen class
    instead of build-in open()
    """
    if sys.platform == 'win32':
        try:
            import win32file
            import msvcrt
            import ctypes
        except ImportError:
            pass

    base = os.path.dirname(__file__)
    file_path = os.path.join(base, 'settings/components/logging.py')

    with FastOpen(file_path, mode='rb') as file:
        data = file.read()

    assert isinstance(data, bytes)
    assert len(data) > 0


def test_fast_open_error():
    """
    This test covers the IOError in FastOpener, when file does not exist
    or can't be opened
    """
    if sys.platform == 'win32':
        try:
            import win32file
            import msvcrt
            import ctypes
        except ImportError:
            pass

    base = os.path.dirname(__file__)
    file_path = os.path.join(base, 'settings\\components\\logging_error.py')

    with pytest.raises(IOError):
        file = FastOpen(file_path, mode='rb')


def test_fast_open_buildin_usage():
    """
    Simulates absence of win32file module and so rollback
    to using build-in open() function instead of FileObjWrapper
    """
    base = os.path.dirname(__file__)
    file_path = os.path.join(base, 'settings/components/logging.py')

    if 'win32file' in sys.modules:
        del sys.modules['win32file']

    with FastOpen(file_path, mode='rb') as file:
        assert not isinstance(file, FileObjWrapper)


def test_missing_file_error(scope):
    """
    This test covers the IOError, when file does not exist.
    """
    with pytest.raises(IOError):
        include(
            'does-not-exist.py',
            scope=scope,
        )


def test_keys_count(scope, fixture_file):
    """
    Scope must contain all base python attrs and a custom value.
    """
    include(
        fixture_file,
        scope=scope,
    )

    # Keys:
    # 'FIXTURE_VALUE', '__file__', '__doc__',
    # '__builtins__', '__included_files__'
    assert len(scope.keys()) == 5


def test_included_file_scope(scope, fixture_file):
    """
    This test emulates gunicorn behaviour with `__included_file__` value.
    """
    base = os.path.dirname(__file__)

    saved_file = os.path.join(
        base,
        'basic'
    )

    scope['__included_file__'] = saved_file

    include(
        fixture_file,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert scope['__included_file__'] == saved_file


def test_empty_included_file(scope, fixture_file):
    """
    This test simulates normal behaviour when no `__included_file__`
    is provided in the `scope`.
    """
    include(
        fixture_file,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert '__included_file__' not in scope


def test_unicode_passed(scope, fixture_file):
    """
    Tests the `unicode` filename in `python2`.
    """
    include(
        six.text_type(fixture_file),  # unicode on py2, str on py3
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope


def test_caller_scope_automatically(fixture_file):
    """
    Tests `include` function for automatic `globals()`
    extraction from execution stack.
    Now you can omit positional argument `scope`.
    """
    include(
        fixture_file
    )

    assert 'FIXTURE_VALUE' in globals()
