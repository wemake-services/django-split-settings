"""
Organize Django settings into multiple files and directories.

Easily override and modify settings. Use wildcards and optional
settings files.
"""

from __future__ import annotations

import glob
import marshal
import os
import sys
import types
import typing
from importlib.util import module_from_spec, spec_from_file_location

__all__ = ('optional', 'include')  # noqa: WPS410

#: Special magic attribute that is sometimes set by `uwsgi` / `gunicorn`.
_INCLUDED_FILE = '__included_file__'


def optional(filename: typing.Optional[str]) -> str:
    """
    This function is used for compatibility reasons.

    It masks the old `optional` class with the name error.
    Now `invalid-name` is removed from `pylint`.

    Args:
        filename: the filename to be optional.

    Returns:
        New instance of :class:`_Optional`.

    """
    return _Optional(filename or '')


class _Optional(str):  # noqa: WPS600
    """
    Wrap a file path with this class to mark it as optional.

    Optional paths don't raise an :class:`OSError` if file is not found.
    """

def compiled(filename: str) -> _Compiled:
    """
    This function is used to get a compiled file path.

    Args:
        filename: the filename to be compiled.

    Returns:
        New instance of :class:`Compiled`.

    Raises:
        ValueError: if the name is not a compiled file.
    """
    if not filename.endswith('.pyc'):
        raise ValueError('Expected a Python compiled file: {0}'.format(filename))

    return _Compiled(filename)


class _Compiled(str):  # noqa: WPS600
    """
    Wrap a file path with this class to mark it as compiled.

    A compiled instance is expected to be a Python compiled file
    (``.pyc``) and will raise :class:`ValueError` if it isn't.
    """


def _load_py(included_file: str) -> types.CodeType:
    """
    Compile the given file into a Python AST that can then be passed to `exec`.

    Args:
        included_file: the file to be compiled.

    Returns:
        The compiled code.
    """
    with open(included_file, 'rb') as to_compile:
        return compile(  # noqa: WPS421
            to_compile.read(), included_file, 'exec',
        )


def _load_pyc(included_file: str):
    """
    Load a compiled Python code file. By unmarshalling it, one can recover the
    AST that can then be passed to `exec`.

    Args:
        included_file: the file to be loaded.

    Returns:
        The compiled code.
    """
    with open(included_file, 'rb') as to_compile:
        to_compile.seek(16)  # Skip .pyc header.
        try:
            compiled_code = marshal.load(to_compile)
        except (EOFError, ValueError, TypeError) as exc:
            raise ValueError('Could not load Python compiled file: {0}'.format(included_file)) from exc

    return compiled_code


def include(  # noqa: WPS210, WPS231, C901
    *args: str,
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
        if isinstance(conf_file, _Optional) and not conf_file:
            continue  # skip empty optional values

        saved_included_file = scope.get(_INCLUDED_FILE)
        pattern = os.path.join(conf_path, conf_file)

        # find files per pattern, raise an error if not found
        # (unless file is optional)
        files_to_include = glob.glob(pattern)
        if not files_to_include and not isinstance(conf_file, _Optional):
            raise OSError('No such file: {0}'.format(pattern))

        for included_file in files_to_include:
            included_file = os.path.abspath(included_file)  # noqa: WPS440
            if included_file in included_files:
                continue

            included_files.append(included_file)

            scope[_INCLUDED_FILE] = included_file
            if isinstance(conf_file, _Compiled):
                compiled_code = _load_pyc(included_file)
            else:
                compiled_code = _load_py(included_file)
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
