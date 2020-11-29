"""Holds some fun stuff to allow for quantity of traceback printed to stout. Nothing too magical."""
import pretty_errors

from sheetwork.core.flags import FlagParser


class SheetworkTracebackManager:
    """Consumes from flags whether user wants full tracebacks and sets up approproate skipping.

    This class now uses `pretty_errors` to manage traceback length, look and feel.
    """

    def __init__(self, flags: FlagParser) -> None:
        """Traceback manager constructor.

        Needs flags to know some things like whether you want full or not full tracebacks. That's
        about it.

        Args:
            flags (FlagParser): Initialised flags object.
        """
        self._stack_depth: int = 4
        if flags.full_tracebacks:
            self._stack_depth = int()

        self.configure_pretty_errors()

    def configure_pretty_errors(self) -> None:
        pretty_errors.configure(
            separator_character="*",
            line_number_first=False,
            display_link=True,
            lines_before=5,
            lines_after=2,
            line_color=pretty_errors.RED + "> " + pretty_errors.default_config.line_color,
            code_color="  " + pretty_errors.default_config.line_color,
            truncate_code=True,
            display_locals=True,
            stack_depth=self._stack_depth,
            trace_lines_before=4,
            trace_lines_after=0,
            display_arrow=True,
        )
