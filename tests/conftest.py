# -*- coding: utf-8 -*-

"""This file contains different utils and fixtures."""

import os

import pytest


class Scope(dict):  # noqa: WPS600
    """This class emulates `globals()`, but does not share state in tests."""

    def __init__(self, *args, **kwargs):
        """Adding `__file__` to make things work in `tools.py`."""
        super().__init__(*args, **kwargs)
        self['__file__'] = __file__


# Different util functions:

@pytest.fixture()
def scope():
    """This fixture just returns the new instance of the test Scope class."""
    return Scope()


@pytest.fixture()
def fixture_file():
    """This fixture return a path to the test fixture file."""
    return os.path.join(
        'settings',
        'basic',
        'fixture_to_include.py',
    )


# Settings files:

@pytest.fixture()
def merged():
    """This fixture returns basic merged settings example."""
    from tests.settings import merged as _merged  # noqa: WPS433
    return _merged

@pytest.fixture()
def alt_ext():
    """This fixture returns basic merged settings example."""
    from tests.settings import alt_ext as _alt_ext  # noqa: WPS433
    return _alt_ext

@pytest.fixture()
def stacked():
    """This fixture returns stacked settings example."""
    from tests.settings import stacked as _stacked  # noqa: WPS433
    return _stacked


@pytest.fixture()
def recursion():
    """This fixture returns recursion settings example."""
    from tests.settings import recursion as _recursion  # noqa: WPS433
    return _recursion
