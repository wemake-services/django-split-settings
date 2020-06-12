# -*- coding: utf-8 -*-

from split_settings.tools import __all__


def test_wildcard_import():
    """Imports all from all modules."""
    assert 'optional' in __all__
    assert 'include' in __all__
    assert 'resource' in __all__


def test_class_import(merged):
    """This test case covers #7 issue."""
    from tests.settings.merged.components import testing  # noqa: WPS433

    path = testing.TestingConfiguration('').get_path()
    assert merged.STATIC_ROOT == path
