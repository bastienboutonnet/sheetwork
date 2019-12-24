import argparse
import logging

from data_tools.logging import LoggerFactory

from sheetload._version import __version__

parser = argparse.ArgumentParser()
parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
parser.add_argument("--mode", help="Chooses between prod or dev run", type=str, default="dev")
parser.add_argument("--log_level", help="sets the log level", type=str, default=str())
parser.add_argument("--sheet_name", help="Name of your sheet from config", type=str, default=None)
parser.add_argument("--sheet_key", help="Google sheet Key", type=str, default=None)
parser.add_argument("--schema", help="Target Schema Name", type=str, default=None)
parser.add_argument("--table", help="Target Table Name", type=str, default=None)
parser.add_argument(
    "--create_table",
    help="Creates target table before pushing.",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--force",
    help="Forces target schema to be followed. Even when in DEV mode.",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--dry_run", help="Skips pushing to database", action="store_true", default=False
)
parser.add_argument(
    "--interactive",
    help="Turns on interactive mode, which allows previews and cleanup choices",
    action="store_true",
    default=False,
)


class FlagParser:
    def __init__(self, test_sheet_name: str = str()):
        self.sheet_name = test_sheet_name
        self.create_table = False
        self.sheet_key = parser.get_default("sheet_key")
        self.target_schema = parser.get_default("schema")
        self.target_table = parser.get_default("table")
        self.mode = parser.get_default("mode")
        self.log_level = parser.get_default("log_level")
        self.force = parser.get_default("force")
        self.interactive = parser.get_default("interactive")
        self.dry_run = parser.get_default("dry_run")

    def consume_cli_arguments(self):
        args = parser.parse_args()
        self.sheet_name = args.sheet_name
        self.create_table = args.create_table
        self.sheet_key = args.sheet_key
        self.target_schema = args.schema
        self.target_table = args.table
        self.mode = args.mode
        self.log_level = args.log_level
        self.force = args.force
        self.interactive = args.interactive
        self.dry_run = args.dry_run

    def set_logger(self):
        if self.mode == "dev":
            logger = LoggerFactory.get_logger(level=getattr(logging, "debug".upper()))
        elif self.mode == "prod":
            logger = LoggerFactory.get_logger(level=getattr(logging, "info".upper()))
        else:
            raise NotImplementedError(f"Mode {self.mode} is not supported.")

        # Override mode if an explicit log level is passed to the command line
        if self.log_level:
            if self.log_level in {"debug", "warning", "info", "error"}:
                logger = LoggerFactory.get_logger(level=getattr(logging, self.log_level.upper()))
            else:
                raise NotImplementedError(f"Level: {self.log_level} is not supported.")
        else:
            self.log_level = "debug"
        return logger


logger = FlagParser().set_logger()
