"""Sets up some easy colour shortcuts to make sure we can easily colour logs and prints."""
import time

from sheetwork.core.ui.colours import COLOURS

USE_COLOURS = True
PRINTER_WIDTH = 80

CL_RED = COLOURS["red"]
CL_GREEN = COLOURS["green"]
CL_YELLOW = COLOURS["yellow"]
CL_RESET_ALL = COLOURS["reset_all"]


def colour(message: str, colour: str) -> str:  # noqa D103
    if USE_COLOURS:
        return f"{colour}{message}{CL_RESET_ALL}"
    return message


def green(message: str):  # noqa D103
    return colour(message, CL_GREEN)


def yellow(message: str):  # noqa D103
    return colour(message, CL_YELLOW)


def red(message: str):  # noqa D103
    return colour(message, CL_RED)


def timed_message(message: str) -> str:
    """Adds time information before a message string.

    Args:
        message (str): Message string to print and wrap in time

    Returns:
        str: A time preceeded version of the message.
    """
    t = time.localtime()
    now = time.strftime("%H:%M:%S", t)
    return f"{now} ---- {message}"
