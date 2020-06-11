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
from importlib import import_module
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from typing import Union

try:
    from importlib import resources as pkg_resources  # noqa: WPS433
except ImportError:
    # Use backport to PY<3.7 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore # noqa: WPS433, WPS440, E501

__all__ = ('optional', 'include', 'resource')  # noqa: WPS410

#: Special magic attribute that is sometimes set by `uwsgi` / `gunicord`.
_INCLUDED_FILE = '__included_file__'


def optional(filename: str) -> str:
    """
    This functions is used for compatibility reasons.

    It masks the old `optional` class with the name error.
    Now `invalid-name` is removed from `pylint`.

    Args:
        filename: the filename to be optional.

    Returns:
        New instance of :class:`_Optional`.

    """
    return _Optional(filename)


class _Optional(str):  # noqa: WPS600
    """
    Wrap a file path with this class to mark it as optional.

    Optional paths don't raise an :class:`IOError` if file is not found.
    """


def resource(package: Union[str, types.ModuleType], filename: str) -> str:
    """
    Include a packaged resource as a settings file.

    Args:
        package: the package as either an imported module, or a string
        filename: the filename of the resource to include.

    Returns:
        New instance of :class:`_Resource`.

    """
    return _Resource(package, filename)


class _Resource(str):  # noqa: WPS600
    """
    Wrap an included package resource as a str.

    Resource includes may also be wrapped as Optional and record if the
    package was found or not.
    """

    module_not_found = False

    def __new__(
        cls,
        package: Union[str, types.ModuleType],
        filename: str,
    ) -> '_Resource':

        # the type ignores workaround a known mypy bug
        # https://github.com/python/mypy/issues/1021

        if isinstance(package, str):
            try:
                package = import_module(package)
            except ModuleNotFoundError:
                rsrc = super().__new__(cls, package)  # type: ignore
                rsrc.module_not_found = True
                return rsrc
        try:
            with pkg_resources.path(package, filename) as pth:
                return super().__new__(cls, str(pth))  # type: ignore
        except FileNotFoundError:
            # even if it doesnt exist - return what the path would be
            return super().__new__(  # type: ignore
                cls,
                os.path.join(
                    os.path.dirname(package.__file__),  # noqa: WPS609
                    filename,
                ),
            )


def include(*args: str, **kwargs) -> None:  # noqa: WPS210, WPS231, C901
    """
    Used for including Django project settings from multiple files.

    Usage:

    .. code:: python

        from split_settings.tools import optional, include, resource
        from . import components

        include(
            'components/base.py',
            'components/database.py',
            resource(components, settings.conf),  # package resource
            optional('local_settings.py'),

            scope=globals(),  # optional scope
        )

    Args:
        *args: File paths (``glob`` - compatible wildcards can be used).
        **kwargs: Settings context: ``scope=globals()`` or ``None``.

    Raises:
        IOError: if a required settings file is not found.
        ModuleNotFoundError: if a required resource package is not found.

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

        # check if this include is a resource with an unfound module
        # before we glob it - avoid the small chance there is a file
        # with the same name as the package in cwd
        if isinstance(conf_file, _Resource) and conf_file.module_not_found:
            raise ModuleNotFoundError(
                'No module named {0}'.format(conf_file),
            )

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

            spec = spec_from_loader(
                module_name,
                SourceFileLoader(
                    os.path.basename(included_file).split('.')[0],
                    included_file,
                ),
            )
            module = module_from_spec(spec)
            sys.modules[module_name] = module
        if saved_included_file:
            scope[_INCLUDED_FILE] = saved_included_file
        elif _INCLUDED_FILE in scope:
            scope.pop(_INCLUDED_FILE)
