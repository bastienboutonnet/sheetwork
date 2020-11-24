"""System related interaction methods."""
import sys
from typing import TYPE_CHECKING

from sheetwork.core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from pathlib import Path


def open_dir_cmd() -> str:
    """Generates the system appropriate terminal command to open a file.

    Returns:
        str: open command string depending on the syste,
    """
    # https://docs.python.org/2/library/sys.html#sys.platform
    if sys.platform == "win32":
        return "start"

    if sys.platform == "darwin":
        return "open"

    return "xdg-open"


def make_dir(path: "Path"):
    """Creates a directory.

    Args:
        path (Path): Where you want it to be.
    """
    logger.debug(f"Making folder: {path}")
    path.mkdir()


def make_file(path: "Path", contents: str = str()):
    """Creates a text file with potential things in it. WOW!

    Args:
        path (Path): Where you want it to be
        contents (str, optional): What you want to put in that text file. Defaults to str().
    """
    logger.debug(f"Making file: {path}")
    path.touch()
    if contents:
        with path.open("w", encoding="utf-8") as f:
            f.write(contents)
