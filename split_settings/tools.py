"""
Organize Django settings into multiple files and directories.

Easily override and modify settings. Use wildcards and optional
settings files.
"""

from __future__ import annotations

import os
import sys
import typing
from importlib.util import module_from_spec, spec_from_file_location

from split_settings.loaders import load_py, load_pyc
from split_settings.wrappers import (
    Entry,
    OneOf,
    Optional,
    compiled,
    entry,
    one_of,
    optional,
)

__all__ = ('compiled', 'entry', 'include', 'optional', 'one_of')  # noqa: WPS410

#: Special magic attribute that is sometimes set by `uwsgi` / `gunicorn`.
_INCLUDED_FILE = '__included_file__'


def include(  # noqa: WPS210, WPS231, C901
    *args: typing.Union[str, Entry, OneOf, Optional],
    scope: dict[str, typing.Any] | None = None,
) -> None:
    """
    Used for including Django project settings from multiple files.

    Args:
        *args: File paths (``glob`` - compatible wildcards can be used).
        scope: Settings context (``globals()`` or ``None``).

    Raises:
        OSError: if a required settings file is not found.
        ValueError: if a Python compiled file could not be loaded.

    Usage example:

    .. code:: python

        from split_settings.tools import optional, include

        include(
            'components/base.py',
            'components/database.py',
            optional('local_settings.py'),

            scope=globals(),  # optional scope
        )

    """
    # we are getting globals() from previous frame
    # globals - it is caller's globals()
    scope = scope or sys._getframe(1).f_globals  # noqa: WPS437

    scope.setdefault('__included_files__', [])
    included_files = scope.get('__included_files__', [])

    including_file = scope.get(
        _INCLUDED_FILE,
        scope['__file__'].rstrip('c'),
    )
    conf_path = os.path.dirname(including_file)

    for conf_file in args:
        # If the argument is a simple `str`, we wrap it with `Entry`.
        if isinstance(conf_file, str):
            conf_file = entry(conf_file)

        if isinstance(conf_file, Optional) and not conf_file.inner.inner:
            continue  # skip empty optional values

        saved_included_file = scope.get(_INCLUDED_FILE)
        files_to_include = conf_file.get_files_to_include(conf_path)

        for included_file in files_to_include:
            included_file = os.path.abspath(included_file)  # noqa: WPS440
            if included_file in included_files:
                continue

            included_files.append(included_file)

            scope[_INCLUDED_FILE] = included_file
            if included_file.endswith('.pyc'):
                compiled_code = load_pyc(included_file)
            else:
                compiled_code = load_py(included_file)
            exec(compiled_code, scope)  # noqa: S102, WPS421

            # Adds dummy modules to sys.modules to make runserver autoreload
            # work with settings components:
            rel_path = os.path.relpath(included_file)
            module_name = '_split_settings.{0}'.format(
                rel_path[:rel_path.rfind('.')].replace('/', '.'),
            )

            spec = spec_from_file_location(module_name, included_file)
            # This is only needed for mypy:
            assert spec is not None  # noqa: S101
            module = module_from_spec(spec)
            sys.modules[module_name] = module
        if saved_included_file:
            scope[_INCLUDED_FILE] = saved_included_file
        elif _INCLUDED_FILE in scope:
            scope.pop(_INCLUDED_FILE)
