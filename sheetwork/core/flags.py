from argparse import ArgumentParser

from sheetwork.core.exceptions import InvalidOrMissingCommandError


class FlagParser:
    """Holds flags from args or sets up default ones that are mainly used to testing and delaying
    argument parsing from CLI so that pytest doesn't steal them and thinks they're for him and
    ultimately complain. It's one way to do it... There are probably other but I feel ok with it.
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
        self.sheet_name = test_sheet_name
        self.create_table = False
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
