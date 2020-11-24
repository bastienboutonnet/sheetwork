"""Flags module containing the FlagParser.

This class which will instanciate CLI args default and/or
consume CLI arguments.
"""
from argparse import ArgumentParser

from sheetwork.core.exceptions import InvalidOrMissingCommandError


class FlagParser:
    """Sets flags from defaults or by parsing CLI arguments.

    Defaults for each flag must be provided. This is a bit strict but for now it saves us from
    too many surprises.
    """

    def __init__(
        self,
        parser: ArgumentParser,
        test_sheet_name: str = str(),
        sheet_config_dir: str = str(),
        profile_dir: str = str(),
        project_dir: str = str(),
        project_name: str = str(),
    ):
        """Constructor for FlagsParser.

        Args:
            parser (ArgumentParser): CLI parser class
            test_sheet_name (str, optional): This here is purely for unit testing.
                It's should be the name of the sheet. We might reworkd this as it's a bit ugly but
                for now it helps us moving forward. Defaults to str().
            sheet_config_dir (str, optional): Path to where the sheet.yml resides.
                Again this arg is mainly for testing purposes. Defaults to str().
            profile_dir (str, optional): Path to the profiles.yml. Again for testing purposes.
                Defaults to str().
            project_dir (str, optional): Path to project directory. For testing purposes.
                Defaults to str().
            project_name (str, optional): Name of the project. Again for unit testing purposes.
                Defaults to str().
        """
        self.sheet_name = test_sheet_name
        self.create_table: bool = False
        self.create_schema: bool = False
        self.destructive_create_table: bool = False
        self.sheet_key = str()
        self.target_schema = str()
        self.target_table = str()
        self.log_level = str()
        self.interactive = False
        self.dry_run = False
        self.parser = parser
        self.sheet_config_dir = sheet_config_dir
        self.profile_dir = profile_dir
        self.project_dir = project_dir
        self.target = "test"
        self.project_name = project_name
        self.force_credentials = False
        self.full_tracebacks = False

    def consume_cli_arguments(self):
        self.args = self.parser.parse_args()
        self.task = self.args.command

        # these only come into the flags if task is upload so we have to jump over.
        # there might be a more clever way to do this but we'll see when we add some other tasks.
        if self.task == "upload":
            self.sheet_name = self.args.sheet_name
            self.create_table = self.args.create_table
            self.create_schema = self.args.create_schema
            self.destructive_create_table = self.args.destructive_create_table
            self.sheet_key = self.args.sheet_key
            self.target_schema = self.args.schema
            self.target_table = self.args.table
            self.interactive = self.args.interactive
            self.dry_run = self.args.dry_run
            self.sheet_config_dir = self.args.sheet_config_dir
            self.target = self.args.target
        elif self.task == "init":
            self.project_name = self.args.project_name
            self.force_credentials = self.args.force_credentials_folders
        else:
            raise InvalidOrMissingCommandError(
                "No task or invalid task was provided. Run `sheetwork --help` to learn how to use sheetwork."
            )
        # put these out cos they apply to both tasks or would be escaped by error.
        self.log_level = self.args.log_level
        self.profile_dir = self.args.profile_dir
        self.project_dir = self.args.project_dir
        self.full_tracebacks = self.args.full_tracebacks
