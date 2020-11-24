"""You need colours now and then. Sets up some colorama shortcuts."""

from typing import Dict

import colorama

COLOURS: Dict[str, str] = {
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "yellow": colorama.Fore.YELLOW,
    "reset_all": colorama.Style.RESET_ALL,
}
