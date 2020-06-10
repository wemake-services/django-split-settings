# -*- coding: utf-8 -*-


def test_merge(merged):
    """Test that all values from settings are present."""
    assert merged.SECRET_KEY
    assert merged.STATIC_ROOT


def test_alt_ext(alt_ext):
    """Test that all values from settings are present."""
    assert alt_ext.NO_EXT_INCLUDED
    assert alt_ext.DOT_CONF_INCLUDED
    assert alt_ext.DOUBLE_EXT_INCLUDED
    assert alt_ext.OPTIONAL_INCLUDED


def test_override(merged, monkeypatch):
    """This setting must be overridden in the testing.py."""
    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'tests.settings.merged')

    from django.conf import settings  # noqa: WPS433

    assert merged.STATIC_ROOT == settings.STATIC_ROOT


def test_recursion_inclusion(recursion):
    """
    Tests `include` function for inclusion files only once.

    It protects of infinite recursion.
    """
    assert recursion.RECURSION_OK


def test_stacked_settings(stacked):
    """
    Tests `include` function for inclusion files only once.

    It protects of infinite recursion.
    """
    assert stacked.STACKED_BASE_LOADED
    assert stacked.STACKED_DB_PERSISTENT
