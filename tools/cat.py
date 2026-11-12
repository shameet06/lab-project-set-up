"""Read and return the contents of a local text file."""
from tools.helper_function import is_path_safe


def cat(path):
    r"""Return the contents of a UTF-8 text file or an error message.

    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     base = Path(Path(folder).name)
    ...     note = base / "notes.txt"
    ...     _ = note.write_text("first line\nsecond line\n", encoding="utf-8")
    ...     cat(str(note))
    ...     cat(str(base / "missing.txt"))
    ...     binary = base / "sample.bin"
    ...     _ = binary.write_bytes(bytes([255]))
    ...     cat(str(binary))
    ...     cat(str(base))
    'first line\nsecond line\n'
    'File not found'
    'Cannot read as UTF-8'
    'Cannot open file'
    >>> cat("../notes.txt")
    'Invalid path'
    """
    if not is_path_safe(path):
        return "Invalid path"

    try:
        with open(path, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found"
    except UnicodeDecodeError:
        return "Cannot read as UTF-8"
    except OSError:
        return "Cannot open file"
