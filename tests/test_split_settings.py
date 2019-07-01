# -*- coding: utf-8 -*-


def test_merge(merged):
    """Test that all values from settings are present."""
    assert hasattr(merged, 'SECRET_KEY')
    assert hasattr(merged, 'STATIC_ROOT')


def test_override(merged, monkeypatch):
    """This setting must be overridden in the testing.py."""
    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'tests.settings.merged')

    from django.conf import settings  # noqa: Z435

    assert merged.STATIC_ROOT == settings.STATIC_ROOT


def test_recursion_inclusion(recursion):
    """
    Tests `include` function for inclusion files only once.

    It protects of infinite recursion.
    """
    assert hasattr(recursion, 'RECURSION_OK')


def test_stacked_settings(stacked):
    """
    Tests `include` function for inclusion files only once.

    It protects of infinite recursion.
    """
    assert hasattr(stacked, 'STACKED_BASE_LOADED')
    assert hasattr(stacked, 'STACKED_DB_PERSISTENT')
