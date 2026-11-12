"""List the visible files and folders in a directory in sorted order."""
import glob

from tools.helper_function import is_path_safe


def ls(path="."):
    """Return the visible names in a folder in sorted order.

    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     Path(folder, "z.txt").touch()
    ...     Path(folder, "a.txt").touch()
    ...     print(ls(Path(folder).name))
    a.txt  z.txt
    >>> ls() == ls(".")
    True
    >>> ls("..")
    'Invalid path'
    """
    if not is_path_safe(path):
        return "Invalid path"

    names = glob.glob("*", root_dir=path)
    return "  ".join(sorted(names))
