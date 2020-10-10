import sys
from typing import TYPE_CHECKING
from sheetwork.core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from pathlib import Path


def open_dir_cmd() -> str:
    # https://docs.python.org/2/library/sys.html#sys.platform
    if sys.platform == "win32":
        return "start"

    if sys.platform == "darwin":
        return "open"

    return "xdg-open"


def make_dir(path: "Path"):
    logger.debug(f"Making folder: {path}")
    path.mkdir()


def make_file(path: "Path", contents: str = str()):
    logger.debug(f"Making file: {path}")
    path.touch()
    if contents:
        with path.open("w", encoding="utf-8") as f:
            f.write(contents)
