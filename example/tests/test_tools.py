# -*- coding: utf-8 -*-
# pylint: disable=no-member

"""
This file contains unit-tests.
"""

import pytest
import os

from split_settings.tools import include


def test_missing_file_error():
    """ This test covers the IOError, when file does not exist. """
    with pytest.raises(IOError):
        include(
            'does-not-exist.py',
            scope=globals(),
        )


def test_included_file_scope():
    """
    This test emulates gunicorn behaviour with `__included_file__` value.
    """
    base = os.path.dirname(__file__)
    to_include = 'fixture_to_include.py'
    saved_file = os.path.join(base, to_include)

    scope = globals()
    scope['__included_file__'] = saved_file

    include(
        to_include,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert scope['__included_file__'] == saved_file


def test_empty_included_file():
    scope = globals()
    del scope['__included_file__']

    include(
        'fixture_to_include.py',
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
    assert '__included_file__' not in scope
