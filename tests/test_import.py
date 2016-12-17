# -*- coding: utf-8 -*-
# pylint: disable=no-member

"""
This module tests imports of django-split-setting.
"""

import types


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


def test_module_import():
    """
    Imports base functionality.
    """
    from split_settings import __version__
    from split_settings.tools import include
    from split_settings.tools import optional

    _assert_types(__version__, include, optional)


def test_wildcard_import():
    """
    Imports all from all modules.
    """
    from split_settings.tools import __all__

    assert 'optional' in __all__
    assert 'include' in  __all__


def test_class_import(merged):
    """
    This test case covers #7 issue.
    """
    from tests.settings.components import testing as _testing

    path = _testing.TestingConfiguration('').get_path()
    assert merged.STATIC_ROOT == path
