"""This file contains different utils and fixtures."""

from compileall import compile_file
import os
from pathlib import Path

import pytest


class Scope(dict):  # noqa: WPS600
    """This class emulates `globals()`, but does not share state in tests."""

    def __init__(self, *args, **kwargs):
        """Adding `__file__` to make things work in `tools.py`."""
        super().__init__(*args, **kwargs)
        self['__file__'] = __file__


# Different util functions:

@pytest.fixture
def scope():
    """This fixture just returns the new instance of the test Scope class."""
    return Scope()


@pytest.fixture
def fixture_file():
    """This fixture return a path to the test fixture file."""
    return os.path.join(
        'settings',
        'basic',
        'fixture_to_include.py',
    )


@pytest.fixture
def fixture_file_bad_pyc():
    """This fixture return a path to the test fixture file."""

    return os.path.join(
        'settings',
        'basic',
        'fixture_bad_pyc.pyc',
    )


# Settings files:

@pytest.fixture
def merged():
    """This fixture returns basic merged settings example."""

    rel_path = os.path.join('settings', 'merged', 'components', 'database.py')
    py_file = Path(__file__).parent.absolute() /  rel_path

    # Compile the Python file to a .pyc file.
    pyc_file = py_file.with_suffix('.pyc')
    compile_file(py_file, legacy=True)

    # Back up the Python file to a .bak file.
    bak_file = py_file.with_suffix('.bak')
    py_file.rename(bak_file)

    from tests.settings import merged as _merged  # noqa: WPS433
    yield _merged

    # Delete the .pyc file after it has served its purpose.
    pyc_file.unlink()

    # Restore the .py file from backup.
    bak_file.rename(py_file)


@pytest.fixture
def stacked():
    """This fixture returns stacked settings example."""
    from tests.settings import stacked as _stacked  # noqa: WPS433
    return _stacked


@pytest.fixture
def recursion():
    """This fixture returns recursion settings example."""
    from tests.settings import recursion as _recursion  # noqa: WPS433
    return _recursion
