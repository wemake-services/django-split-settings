# -*- coding: utf-8 -*-
# pylint: disable=exec-used

"""
Organize Django settings into multiple files and directories.
Easily override and modify settings. Use wildcards and optional
settings files.
"""

import glob
import os
import sys
import types

__all__ = ['optional', 'include']


def optional(filename):
    """
    This functions is used for compatibility reasons,
    it masks the old `optional` class with the name error.
    Now `invalid-name` is removed from `pylint`.

    Args:
        filename: the filename to be optional

    Returns: new instance of :class:`_Optional`

    """
    return _Optional(filename)


class _Optional(str):
    """Wrap a file path with this class to mark it as optional.

    Optional paths don't raise an IOError if file is not found.
    """
    pass


def include(*args, **kwargs):
    """Used for including Django project settings from multiple files.

    Note: Expects to get ``scope=globals()`` as a keyword argument.

    Usage::

        from split_settings.tools import optional, include

        include(
            'components/base.py',
            'components/database.py',
            optional('local_settings.py'),

            scope=globals()
        )

    Parameters:
        *args: File paths (``glob`` - compatible wildcards can be used)
        **kwargs: The context for the settings,
            should always contain ``scope=globals()``

    Raises:
        IOError: if a required settings file is not found
    """

    scope = kwargs.pop('scope')
    including_file = scope.get('__included_file__',
                               scope['__file__'].rstrip('c'))
    conf_path = os.path.dirname(including_file)
    for conf_file in args:
        saved_included_file = scope.get('__included_file__')
        pattern = os.path.join(conf_path, conf_file)

        # find files per pattern, raise an error if not found (unless file is
        # optional)
        files_to_include = glob.glob(pattern)
        if not files_to_include and not isinstance(conf_file, _Optional):
            raise IOError('No such file: %s' % pattern)

        for included_file in files_to_include:
            scope['__included_file__'] = included_file
            with open(included_file, 'rb') as to_compile:
                exec(compile(to_compile.read(), included_file, 'exec'), scope)

            # add dummy modules to sys.modules to make runserver autoreload
            # work with settings components
            module_name = ('_split_settings.%s' %
                           conf_file[:conf_file.rfind('.')].replace('/', '.'))

            module = types.ModuleType(str(module_name))
            module.__file__ = included_file
            sys.modules[module_name] = module
        if saved_included_file:
            scope['__included_file__'] = saved_included_file
        elif '__included_file__' in scope:
            del scope['__included_file__']
