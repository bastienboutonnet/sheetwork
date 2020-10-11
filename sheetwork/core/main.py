import argparse
from typing import Union

import sheetwork.core.sheetwork as upload_task
import sheetwork.core.task.init as init_task
from sheetwork.core._version import __version__
from sheetwork.core.config.config import ConfigLoader
from sheetwork.core.config.profile import Profile
from sheetwork.core.config.project import Project
from sheetwork.core.flags import FlagParser
from sheetwork.core.logger import log_manager
from sheetwork.core.ui.traceback_manager import SheetworkTracebackManager
from sheetwork.core.utils import check_and_compare_version

# to identify sheetwork code --we use this arg in `core.logger to shorten the traceback`
__SHEETWORK_CODE = True

parser = argparse.ArgumentParser(
    prog="sheetwork",
    formatter_class=argparse.RawTextHelpFormatter,
    description="CLI tool to load google sheets onto a DB.",
    epilog="Select one of these sub-commands to find specific help for those.",
)
parser.add_argument("-v", "--version", action="version", version=f"%(prog)s Running v{__version__}")

base_subparser = argparse.ArgumentParser(add_help=False)
base_subparser.add_argument("--log-level", help="sets the log level", type=str, default=str())
base_subparser.add_argument(
    "--profile-dir",
    help="Unusual path to the directory in which the 'profiles.yml' can be found",
    default=str(),
)
base_subparser.add_argument(
    "--project-dir",
    help="Unusual path to the directory in which the 'sheetwork_project.yml' can be found",
    default=str(),
)
base_subparser.add_argument(
    "--full-tracebacks",
    action="store_true",
    default=False,
    help="When provided full tracebacks will be printed otherwise only the nearest one only.",
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
    "-sn", "--sheet-name", help="Name of your sheet from config", type=str, default=None
)
upload_sub.add_argument("-sk", "--sheet-key", help="Google sheet Key", type=str, default=None)
upload_sub.add_argument(
    "--dry-run", help="Skips pushing to database", action="store_true", default=False
)
upload_sub.add_argument(
    "-i",
    "--interactive",
    help="Turns on interactive mode, which allows previews and cleanup choices",
    action="store_true",
    default=False,
)
upload_sub.add_argument(
    "-t",
    "--target",
    help="Specity target profile. When none provided sheetwork will use the profile default",
)
upload_sub.add_argument(
    "--sheet-config-dir",
    help="Unusual path to the directory in which the 'sheets.yml' can be found",
    default=str(),
)
upload_sub.add_argument(
    "--create-table",
    help="Creates target table before pushing.",
    action="store_true",
    default=False,
)

# Init task parser
init_sub = subs.add_parser(
    "init", parents=[base_subparser], help="Initialise your sheetwork project"
)
init_sub.set_defaults(cls=init_task.InitTask, which="init")
init_sub.add_argument("--project-name", help="Name you want to init your dbt project with")
init_sub.add_argument(
    "--force-credentials-folders",
    action="store_true",
    default=False,
    help="Forces init task to at least attempt to create credential folders.",
)


def handle(parser: argparse.ArgumentParser):
    flag_parser = FlagParser(parser)
    flag_parser.consume_cli_arguments()

    # set up traceback override
    SheetworkTracebackManager(flag_parser)

    if flag_parser.log_level == "debug":
        log_manager.set_debug()

    if flag_parser.args.command == "init":
        task: Union[init_task.InitTask, upload_task.SheetBag] = init_task.InitTask(flag_parser)
        return task.run()

    if flag_parser.args.command == "upload":
        project = Project(flag_parser)
        config = ConfigLoader(flag_parser, project)
        profile = Profile(project)
        task = upload_task.SheetBag(config, flag_parser, profile)
        return task.run()


def main(parser: argparse.ArgumentParser = parser):
    print(f"Sheetwork version: {__version__} \n")
    check_and_compare_version()
    if parser:
        handle(parser)
    else:
        raise NotImplementedError(
            """You did not parse any args to sheetwork.
            If you are not sure how to use it consult the help by doing: sheetwork --help
            """
        )


if __name__ == "__main__":
    main()
