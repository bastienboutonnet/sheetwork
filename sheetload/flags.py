import argparse
import logging

from data_tools.logging import LoggerFactory

from sheetload._version import __version__

parser = argparse.ArgumentParser()
parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
parser.add_argument("--mode", help="Chooses between prod or dev run", type=str, default="dev")
parser.add_argument("--log_level", help="sets the log level", type=str, default="info")
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
    "--i",
    help="Turns on interactive mode, which allows previews and cleanup choices",
    action="store_true",
    default=False,
)
args = parser.parse_args()


# set up logger levels
if args.mode == "dev":
    logger = LoggerFactory.get_logger(level=getattr(logging, "debug".upper()))
elif args.mode == "prod":
    logger = LoggerFactory.get_logger(level=getattr(logging, "info".upper()))
else:
    raise NotImplementedError("This mode is not supported.")
if args.log_level in {"debug", "warning", "info", "error"}:
    logger = LoggerFactory.get_logger(level=getattr(logging, args.log_level.upper()))
else:
    raise NotImplementedError("This level is not supported.")
