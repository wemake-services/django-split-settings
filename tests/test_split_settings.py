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


def test_resources(resources):  # noqa: WPS218
    """Test that all values from settings are present."""
    assert resources.APPS_MIDDLEWARE_INCLUDED
    assert resources.BASE_INCLUDED
    assert resources.DATABASE_INCLUDED
    assert resources.LOCALE_INCLUDED
    assert resources.LOGGING_INCLUDED
    assert resources.STATIC_SETTINGS_INCLUDED
    assert resources.TEMPLATES_INCLUDED
    assert resources.OVERRIDE_WORKS
    assert resources.UNFOUND_RESOURCE_IS_IOERROR
    assert resources.UNFOUND_PACKAGE_IS_MODULE_ERROR


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
