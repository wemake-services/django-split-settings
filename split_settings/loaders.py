import marshal
import types

_PYC_HEADER_SIZE = 16


def load_py(included_file: str) -> types.CodeType:
    """
    Compile the given file into a Python AST.

    This AST can then be passed to `exec`.

    Args:
        included_file: the file to be compiled.

    Returns:
        The compiled code.
    """
    with open(included_file, 'rb') as to_compile:
        return compile(  # noqa: WPS421
            to_compile.read(), included_file, 'exec',
        )


def load_pyc(included_file: str) -> types.CodeType:
    """
    Load a Python compiled file that can be unmarshalled to an AST.

    This AST can then be passed to `exec`.

    Args:
        included_file: the file to be loaded and unmarshalled.

    Returns:
        The compiled code.
    """
    # Python compiled files have a header before the marshalled code.
    # This header can be different sizes in different Python versions,
    # but it is 16 bytes in all versions supported by this package.

    with open(included_file, 'rb') as to_compile:
        to_compile.seek(_PYC_HEADER_SIZE)  # Skip .pyc header.
        try:
            compiled_code = marshal.load(to_compile)  # noqa: S302
        except (EOFError, ValueError, TypeError) as exc:
            raise ValueError(
                'Could not load Python compiled file: {0}'.format(
                    included_file,
                ),
            ) from exc

    # This is only needed for mypy:
    assert isinstance(compiled_code, types.CodeType)  # noqa: S101
    return compiled_code
