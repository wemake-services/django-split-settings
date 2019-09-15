# -*- coding: utf-8 -*-

"""
Organize Django settings into multiple files and directories.

Easily override and modify settings. Use wildcards and optional
settings files.
"""

import glob
import inspect
import os
import sys
import types

__all__ = ('optional', 'include')  # noqa: WPS410

#: Special magic attribute that is sometimes set by `uwsgi` / `gunicord`.
_INCLUDED_FILE = '__included_file__'


def optional(filename: str) -> str:
    """
    This functions is used for compatibility reasons.

    It masks the old `optional` class with the name error.
    Now `invalid-name` is removed from `pylint`.

    Args:
        filename: the filename to be optional

    Returns: new instance of :class:`_Optional`

    """
    return _Optional(filename)


class _Optional(str):  # noqa: WPS600
    """
    Wrap a file path with this class to mark it as optional.

    Optional paths don't raise an :class:`IOError` if file is not found.
    """


def include(*args: str, **kwargs) -> None:  # noqa: WPS210, C901
    """
    Used for including Django project settings from multiple files.

    Usage:

    .. code:: python

        from split_settings.tools import optional, include

        include(
            'components/base.py',
            'components/database.py',
            optional('local_settings.py'),

            scope=globals(),  # optional scope
        )

    Args:
        args: File paths (``glob`` - compatible wildcards can be used).
        kwargs: Settings context, may contain ``scope=globals()`` or be empty.

    Raises:
        IOError: if a required settings file is not found.

    """
    # we are getting globals() from previous frame
    # globals - it is caller's globals()
    scope = kwargs.pop('scope', inspect.stack()[1][0].f_globals)

    scope.setdefault('__included_files__', [])
    included_files = scope.get('__included_files__')

    including_file = scope.get(
        _INCLUDED_FILE,
        scope['__file__'].rstrip('c'),
    )
    conf_path = os.path.dirname(including_file)

    for conf_file in args:
        saved_included_file = scope.get(_INCLUDED_FILE)
        pattern = os.path.join(conf_path, conf_file)

        # find files per pattern, raise an error if not found
        # (unless file is optional)
        files_to_include = glob.glob(pattern)
        if not files_to_include and not isinstance(conf_file, _Optional):
            raise IOError('No such file: {0}'.format(pattern))

        for included_file in files_to_include:
            included_file = os.path.abspath(included_file)  # noqa: WPS440
            if included_file in included_files:
                continue

            included_files.append(included_file)

            scope[_INCLUDED_FILE] = included_file
            with open(included_file, 'rb') as to_compile:
                compiled_code = compile(  # noqa: WPS421
                    to_compile.read(), included_file, 'exec',
                )
                exec(compiled_code, scope)  # noqa: S102, WPS421

            # Adds dummy modules to sys.modules to make runserver autoreload
            # work with settings components:
            rel_path = os.path.relpath(included_file)
            module_name = '_split_settings.{0}'.format(
                rel_path[:rel_path.rfind('.')].replace('/', '.'),
            )

            module = types.ModuleType(str(module_name))
            module.__file__ = included_file  # noqa: WPS609
            sys.modules[module_name] = module
        if saved_included_file:
            scope[_INCLUDED_FILE] = saved_included_file
        elif _INCLUDED_FILE in scope:
            scope.pop(_INCLUDED_FILE)
