import sys
import traceback
from sheetwork.core.flags import FlagParser


class SheetworkTracebackManager:
    """Consumes from flags whether user wants full tracebacks and sets up approproate skipping for
    all tracebacks that are not part of the sheetwork code as identified by the __SHEETWORK_CODE
    gobal which resides in main.py
    """

    def __init__(self, flags: FlagParser) -> None:
        if flags.full_tracebacks:
            # noop
            pass

        else:

            def is_mycode(tb):
                globs = tb.tb_frame.f_globals
                return globs.__contains__("__sheetwork_code")

            def mycode_traceback_levels(tb):
                length = 0
                while tb and is_mycode(tb):
                    tb = tb.tb_next
                length += 1
                return length

            def handle_exception(type, value, tb):
                # 1. skip custom assert code, e.g.
                # while tb and is_custom_assert_code(tb):
                #   tb = tb.tb_next
                # 2. only display your code
                length = mycode_traceback_levels(tb)
                print("".join(traceback.format_exception(type, value, tb, length)))

            sys.excepthook = handle_exception
