
import glob
import re

from tools.helper_function import is_path_safe


def grep(regex, path):
    r"""Return matching lines from the files selected by path.

    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     base = Path(folder).name
    ...     _ = Path(base, "a.txt").write_text("goal 2\nno score\n", encoding="utf-8")
    ...     _ = Path(base, "b.txt").write_text("goal 10\ngoal soon\n", encoding="utf-8")
    ...     _ = Path(base, "c.txt").write_bytes(bytes([255]))
    ...     Path(base, "folder.txt").mkdir()
    ...     Path(base, "link.txt").symlink_to(Path.cwd().parent)
    ...     print(grep(r"goal \d+", base + "/*.txt"))
    ...     grep("assist", base + "/*.txt")
    goal 2
    goal 10
    ''
    >>> grep("goal", "../*.txt")
    'Invalid path'
    >>> grep("[", "*.txt")
    'Invalid regex'
    """
    if not is_path_safe(path):
        return "Invalid path"

    try:
        pattern = re.compile(regex)
    except re.error:
        return "Invalid regex"

    matches = []
    for filename in sorted(glob.glob(path)):
        if not is_path_safe(filename):
            continue

        try:
            with open(filename, encoding="utf-8") as file:
                lines = file.read().splitlines()
        except (OSError, UnicodeDecodeError):
            continue

        for line in lines:
            if pattern.search(line):
                matches.append(line)

    return "\n".join(matches)
