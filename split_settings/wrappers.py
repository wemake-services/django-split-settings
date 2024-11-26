import contextlib
import glob
import os
import typing


class Entry:
    """
    Wrap a file path with this class.

    This class provides the additional functionality required for
    handling paths to settings files.
    """

    def __init__(self, inner: str):
        """Create a new object of class :class:`Entry`."""
        self.inner = inner

    def get_files_to_include(self, conf_path: str) -> list[str]:
        """
        Get the Python source file names that match the inner pattern.

        Args:
            conf_path: the path to prepend to the pattern.

        Raises:
            ValueError: if the pattern matches a Python compiled file.

        Returns:
            The list of Python source file names that match the pattern.
        """
        files = self._get_files_matching_pattern(conf_path)

        if any(match_file.endswith('.pyc') for match_file in files):
            raise ValueError(
                'A Python compiled file matched the pattern: {0}'.format(
                    self.inner,
                ),
            )

        return files

    def _get_files_matching_pattern(self, conf_path: str) -> list[str]:
        """
        Get the file names that match the inner pattern.

        Args:
            conf_path: the path to prepend to the pattern.

        Raises:
            OSError: if the no files match the given pattern.

        Returns:
            The list of file names that match the pattern.
        """
        pattern = os.path.join(conf_path, self.inner)
        files = glob.glob(pattern)

        if not files:
            raise OSError('No such file: {0}'.format(self.inner))

        return files


def entry(filename: str) -> Entry:
    """
    This function is used to get a regular (non-compiled) file path.

    Args:
        filename: the filename of the Python file.

    Returns:
        New instance of :class:`Entry`.

    Raises:
        ValueError: if the name ends with `.pyc`.
    """
    if filename.endswith('.pyc'):
        raise ValueError(
            'Expected a Python source file: {0}'.format(filename),
        )

    return Entry(filename)


class Compiled(Entry):  # noqa: WPS600
    """
    Wrap a file path with this class to mark it as compiled.

    A compiled instance is expected to be a Python compiled file
    (``.pyc``) and will raise :class:`ValueError` if it isn't.
    """

    def get_files_to_include(self, conf_path: str) -> list[str]:
        """
        Get the Python compiled file names that match the inner pattern.

        Args:
            conf_path: the path to prepend to the pattern.

        Raises:
            ValueError: if the pattern matches a Python source file.

        Returns:
            The list of Python compiled file names that match the
            pattern.
        """
        files = self._get_files_matching_pattern(conf_path)

        if any(match_file.endswith('.py') for match_file in files):
            raise ValueError(
                'A Python source file matched the pattern: {0}'.format(
                    self.inner,
                ),
            )

        return files


def compiled(filename: str) -> Compiled:
    """
    This function is used to get a compiled file path.

    Args:
        filename: the filename to be compiled.

    Returns:
        New instance of :class:`Compiled`.

    Raises:
        ValueError: if the name is not a compiled file.
    """
    if filename.endswith('.py'):
        raise ValueError(
            'Expected a Python compiled file: {0}'.format(filename),
        )

    return Compiled(filename)


class OneOf:
    """
    Wrap a list of file paths where the first found path will be used.

    A one-of instance needs at least one argument and will raise a
    :class:`ValueError` if no arguments are provided.

    This raises an :class:`OSError` if none of the files are found.
    """

    def __init__(self, inner: tuple[Entry, ...]):
        """Create a new object of class :class:`OneOf`."""
        self.inner = inner

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return '({0})'.format(
            ', '.join(inner_item.inner for inner_item in self.inner),
        )

    def get_files_to_include(self, conf_path: str) -> list[str]:
        """
        Get the file names that match the wrapped patterns.

        This absorbs the :class:`OSError` from each individual item's
        match but raises the error if in the end, no files are found.

        Raises:
            OSError: if the no files match all the wrapped patterns.
        """
        files_to_include = []
        for inner_item in self.inner:
            # We want to ignore errors from individual items.
            with contextlib.suppress(OSError):
                files_to_include.extend(
                    inner_item.get_files_to_include(conf_path),
                )

        if not files_to_include:
            # We want to raise an error if all items failed to match.
            raise OSError('No such file: {0}'.format(self))

        return files_to_include


def one_of(*args: typing.Union[str, Entry]) -> OneOf:
    """
    Wrap a list of file paths where the first found path will be used.

    Args:
        *args: the file paths to collect.

    Returns:
        New instance of :class:`OneOf`.
    """
    if not args:
        raise ValueError('Expected at least 1 argument but received 0.')

    out: tuple[Entry, ...] = tuple(
        entry(arg) if isinstance(arg, str) else arg
        for arg in args
    )

    return OneOf(out)


class Optional:
    """
    Wrap a value with this class to mark it as optional.

    This wrapper can wrap a file path (`str`), a :class:`Compiled`
    instance or a :class:`OneOf` instance.

    Optional paths don't raise an :class:`OSError` if file is not found.
    """

    def __init__(self, inner: typing.Union[Entry, OneOf]):
        """Create a new object of class :class:`Optional`."""
        self.inner = inner

    def get_files_to_include(self, conf_path: str) -> list[str]:
        """
        Get the file names that match the wrapped patterns.

        This absorbs the :class:`OSError` that would be raised if no
        file was found, effectively making the wrapped value optional.
        """
        try:
            return self.inner.get_files_to_include(conf_path)
        except OSError:
            return []


def optional(
    inner: typing.Optional[typing.Union[str, Entry, OneOf]],
) -> Optional:
    """
    This function is used for compatibility reasons.

    It masks the old `optional` class with the name error.
    Now `invalid-name` is removed from `pylint`.

    Args:
        inner: the file name or instance of `Compiled`/`OneOf`.

    Returns:
        New instance of :class:`Optional`.
    """
    if inner is None:
        inner = entry('')
    elif isinstance(inner, str):
        inner = entry(inner)

    return Optional(inner)
