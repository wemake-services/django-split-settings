# -*- coding: utf-8 -*-
# pylint: disable=no-member

"""
This file contains unit-tests.
"""

import os

import six
import pytest

from split_settings.tools import include

from .utils import Scope


FIXTURE = 'fixture_to_include.py'


def test_missing_file_error():
    """ This test covers the IOError, when file does not exist. """
    with pytest.raises(IOError):
        include(
            'does-not-exist.py',
            scope=Scope(),
        )


def test_keys_count():
    """ Scope must contain all base python attrs and a custom value. """
    scope = Scope()

    include(
        FIXTURE,
        scope=scope,
    )

    # Keys: 'FIXTURE_VALUE', '__file__', '__doc__', '__builtins__', '__included_files__'
    assert len(scope.keys()) == 5


def test_included_file_scope():
    """
    This test emulates gunicorn behaviour with `__included_file__` value.
    """
    base = os.path.dirname(__file__)
    saved_file = os.path.join(base, FIXTURE)

    scope = Scope()
    scope['__included_file__'] = saved_file

    include(
        FIXTURE,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert scope['__included_file__'] == saved_file


def test_empty_included_file():
    """
    This test simulates normal behaviour when no `__included_file__`
    is provided in the `scope`.
    """
    scope = Scope()

    include(
        FIXTURE,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert '__included_file__' not in scope


def test_unicode_passed():
    """
    Tests the `unicode` filename in `python2`.
    """
    scope = Scope()

    include(
        six.text_type(FIXTURE),  # unicode on py23, str on py35
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope


def test_caller_scope_automatically():
    """
    Tests `include` function for automatic `globals()` extraction from execution stack.
    Now you can omit positional argument `scope`.
    """

    include(
        six.text_type(FIXTURE)
    )

    assert 'FIXTURE_VALUE' in globals()


def test_recursion_inclusion():
    """
    Tests `include` function for inclusion files only once. It protects of infinite recursion.
    """

    from tests.settings import recursion

    assert hasattr(recursion, 'RECURSION_OK')

def test_stacked_settings():
    """
    Tests `include` function for inclusion files only once. It protects of infinite recursion.
    """

    from tests.settings import stacked

    assert hasattr(stacked, 'STACKED_BASE_LOADED')
    assert hasattr(stacked, 'STACKED_DB_PERSISTENT')
