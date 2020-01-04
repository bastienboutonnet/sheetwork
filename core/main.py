import argparse

import core.sheetload as upload_task
from core._version import __version__
from core.config.config import ConfigLoader
from core.config.profile import Profile
from core.config.project import Project
from core.flags import FlagParser
from core.logger import log_manager

parser = argparse.ArgumentParser(
    prog="sheetload: a handy tool to load google sheets into your DB.",
    formatter_class=argparse.RawTextHelpFormatter,
    description="CLI tool to load google sheets onto a DB.",
    epilog="Select one of these sub-commands to find specific help for those.",
)
parser.add_argument("--version", action="version", version=f"%(prog)s Running v{__version__}")

base_subparser = argparse.ArgumentParser(add_help=False)
base_subparser.add_argument(
    "--mode", help="Chooses between prod or dev run", type=str, default="dev"
)
base_subparser.add_argument(
    "-sn", "--sheet_name", help="Name of your sheet from config", type=str, default=None
)
base_subparser.add_argument("-sk", "--sheet_key", help="Google sheet Key", type=str, default=None)
base_subparser.add_argument("--log_level", help="sets the log level", type=str, default=str())
base_subparser.add_argument(
    "-f",
    "--force",
    help="Forces target schema to be followed. Even when in DEV mode.",
    action="store_true",
    default=False,
)
base_subparser.add_argument(
    "--dry_run", help="Skips pushing to database", action="store_true", default=False
)
base_subparser.add_argument(
    "-i",
    "--interactive",
    help="Turns on interactive mode, which allows previews and cleanup choices",
    action="store_true",
    default=False,
)
base_subparser.add_argument(
    "--sheet_config_dir",
    help="Unusual path to the directory in which the 'sheets.yml' can be found",
    default=str(),
)
base_subparser.add_argument(
    "--profile_dir",
    help="Unusual path to the directory in which the 'profiles.yml' can be found",
    default=str(),
)
base_subparser.add_argument(
    "--project_dir",
    help="Unusual path to the directory in which the 'sheetload_project.yml' can be found",
    default=str(),
)

# Adds sub task parsers
subs = parser.add_subparsers(title="Available sub commands", dest="command")

# Upload task parser
upload_sub = subs.add_parser(
    "upload", parents=[base_subparser], help="Pull, sanitize and upload a google sheet."
)
upload_sub.set_defaults(cls=upload_task.SheetBag, which="upload")
upload_sub.add_argument("--schema", help="Target Schema Name", type=str, default=None)
upload_sub.add_argument("--table", help="Target Table Name", type=str, default=None)
upload_sub.add_argument(
    "--create_table",
    help="Creates target table before pushing.",
    action="store_true",
    default=False,
)


def handle(parser: argparse.ArgumentParser):
    flag_parser = FlagParser(parser)
    flag_parser.consume_cli_arguments()

    if flag_parser.log_level == "debug":
        log_manager.set_debug()

    if flag_parser.args.command == "upload":
        project = Project(flag_parser)
        config = ConfigLoader(flag_parser, project)
        # TODO: Add target handling and remove this hardcode.
        profile = Profile(project, "dev")
        task = upload_task.SheetBag(config, flag_parser, profile)
        return task.run()


def main(parser: argparse.ArgumentParser = parser):
    print(f"Sheetload version: {__version__} \n")
    if parser:
        handle(parser)
    else:
        NotImplementedError(
            """You did not parse any args to sheetload.
            If you are not sure how to use it consult the help by doing: sheetload --help
            """
        )


if __name__ == "__main__":
    main()