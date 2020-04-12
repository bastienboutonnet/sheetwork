from core.ui.colours import COLOURS


USE_COLOURS = True
PRINTER_WIDTH = 80

CL_RED = COLOURS["red"]
CL_GREEN = COLOURS["green"]
CL_YELLOW = COLOURS["yellow"]
CL_RESET_ALL = COLOURS["reset_all"]


def colour(message: str, colour: str) -> str:
    if USE_COLOURS:
        return f"{colour}{message}{CL_RESET_ALL}"
    else:
        return message


def green(message: str):
    return colour(message, CL_GREEN)


def yellow(message: str):
    return colour(message, CL_YELLOW)


def red(message: str):
    return colour(message, CL_RED)
