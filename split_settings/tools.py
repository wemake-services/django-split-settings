# -*- coding: utf-8 -*-
# pylint: disable=exec-used

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

if sys.platform == 'win32':
    try:
        import win32file
        import msvcrt
    except ImportError: # pragma: no cover
        pass


__all__ = ['optional', 'include']


class FileObjWrapper(object):
    """
    This class used to implement only read() method on file object
    basically for compatibility reasons with I/O API

    Args:
        file: file to read from
        *args: used as dummy to accept build-in open() function args which further ignored

    Returns:
        new instance of :class:`FileObjWrapper`

    Raises:
        IOError: if a required file is not found
    """

    def __init__(self, file, *args, **kwargs):
        try:
            file_descriptor = os.open(file, os.O_RDONLY|os.O_BINARY)
            self.full_size = os.fstat(file_descriptor).st_size
            self.handler = msvcrt.get_osfhandle(file_descriptor)
        except os.error as err:
            exc = IOError(err.strerror)
            err.__suppress_context__ = True
            err.__traceback__ = None
            raise exc

    def read(self, size=None):
        """
        Reads from file some quantity of data and returns it as a string

        Args:
            n: bytes size to read

        Returns: string
        """
        if not size:
            size = self.full_size
        win32file.SetFilePointer(self.handler, 0, win32file.FILE_BEGIN)
        data = win32file.ReadFile(self.handler, size, None)[1]
        return data

    def close(self):
        """
        Close file handler to free resources
        """
        win32file.CloseHandle(self.handler)
        del self.handler


class FastOpen(object):
    """
    This class used as replacement of build-in open() function.

    The main purpose - increase file read speed on Windows-based platforms.
    If f_open instance running on Windows and win32file module (from pywin32)
    loaded then file open/read operations is done by this instance.
    Otherwise build-in open() function invokes.

    Usage::

        with f_open('file') as file:
            data = file.read()

    Parameters:
        name: file to open
        *args: arguments for build-in open() function
    """

    def __init__(self, name, *args, **kwargs):
        if (sys.platform == 'win32') and ('win32file' in sys.modules):
            self._opener = FileObjWrapper
        else:
            self._opener = open

        self._handler_obj = self._opener(name, *args, **kwargs)

    def __enter__(self):
        return self._handler_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._handler_obj.close()


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

    Optional paths don't raise an :class:`IOError` if file is not found.
    """
    pass


def include(*args, **kwargs):
    """
    Used for including Django project settings from multiple files.

    Usage::

        from split_settings.tools import optional, include

        include(
            'components/base.py',
            'components/database.py',
            optional('local_settings.py'),

            scope=globals()  # optional scope
        )

    Parameters:
        *args: File paths (``glob`` - compatible wildcards can be used)
        **kwargs: The context for the settings,
            may contain ``scope=globals()`` or be empty

    Raises:
        IOError: if a required settings file is not found
    """

    if 'scope' not in kwargs:
        # we are getting globals() from previous frame
        # globals - it is caller's globals()
        scope = inspect.stack()[1][0].f_globals
    else:
        scope = kwargs.pop('scope')

    scope.setdefault('__included_files__', [])
    included_files = scope.get('__included_files__')

    including_file = scope.get(
        '__included_file__',
        scope['__file__'].rstrip('c')
    )
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
            if included_file in included_files:
                continue

            included_files.append(included_file)

            scope['__included_file__'] = included_file
            with FastOpen(included_file, 'rb') as to_compile:
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
