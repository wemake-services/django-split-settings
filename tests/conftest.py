# -*- coding: utf-8 -*-

"""
This file contains different utils and fixtures.
"""

import os

from pytest import fixture

__author__ = 'sobolevn'


class Scope(dict):
    """
    This class emulates `globals()`,
    but does not share state across all tests.
    """

    def __init__(self, *args, **kwargs):
        """
        Adding `__file__` to make things work in `tools.py`.
        """
        super(Scope, self).__init__(*args, **kwargs)
        self['__file__'] = __file__


# Different util functions:

@fixture
def scope():
    """
    This fixture just returns the new instance
    of the test Scope class.
    """
    return Scope()


@fixture
def fixture_file():
    """
    This fixture return a path to the test fixture file.
    """
    return os.path.join(
        'settings',
        'basic',
        'fixture_to_include.py'
    )


# Settings files:

@fixture
def merged():
    """
    This fixture returns basic merged settings example.
    """
    from tests import settings
    return settings


@fixture
def stacked():
    """
    This fixture returns stacked settings example.
    """
    from tests.settings import stacked as _stacked
    return _stacked


@fixture
def recursion():
    """
    This fixture returns recursion settings example.
    """
    from tests.settings import recursion as _recursion
    return _recursion
