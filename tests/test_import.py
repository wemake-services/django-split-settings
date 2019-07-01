# -*- coding: utf-8 -*-

import types

from split_settings.tools import __all__, include, optional


def _assert_types(version, include, optional):
    """
    This helper function tests all parameters.

    :param version: version string.
    :param include: include function.
    :param optional: optional class.
    """
    assert isinstance(version, str)
    assert isinstance(include, types.FunctionType)
    assert isinstance(optional, types.FunctionType)


def test_wildcard_import():
    """Imports all from all modules."""
    assert 'optional' in __all__
    assert 'include' in __all__


def test_class_import(merged):
    """This test case covers #7 issue."""
    from tests.settings.merged.components import testing  # noqa: Z435

    path = testing.TestingConfiguration('').get_path()
    assert merged.STATIC_ROOT == path
