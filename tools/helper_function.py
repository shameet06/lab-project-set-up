"""Check paths before docchat tools read local files."""

from pathlib import Path


def is_path_safe(path):
    """Return True if a relative path stays inside the current folder.

    >>> is_path_safe(".")
    True
    >>> is_path_safe("tools/calculate.py")
    True
    >>> is_path_safe("*.txt")
    True
    >>> is_path_safe("/etc/hosts")
    False
    >>> is_path_safe("tools/../chat.py")
    False
    >>> is_path_safe("notes..txt")
    True
    """
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False

    try:
        candidate.resolve().relative_to(Path.cwd())
    except (ValueError, RuntimeError):
        return False

    return True
