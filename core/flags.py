from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import parser


class FlagParser:
    """Holds flags from args or sets up default ones that are mainly used to testing and delaying
    argument parsing from CLI so that pytest doesn't steal them and thinks they're for him and
    ultimately complain. It's one way to do it... There are probably other but I feel ok with it.
    """

    def __init__(
        self,
        parser: "parser.ArgumentParser",
        test_sheet_name: str = str(),
        sheet_config_dir: str = str(),
        profile_dir: str = str(),
        project_dir: str = str(),
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

    def consume_cli_arguments(self):
        self.args = self.parser.parse_args()
        self.sheet_name = self.args.sheet_name
        self.create_table = self.args.create_table
        self.sheet_key = self.args.sheet_key
        self.target_schema = self.args.schema
        self.target_table = self.args.table
        self.log_level = self.args.log_level
        self.interactive = self.args.interactive
        self.dry_run = self.args.dry_run
        self.sheet_config_dir = self.args.sheet_config_dir
        self.profile_dir = self.args.profile_dir
        self.project_dir = self.args.project_dir
        self.target = self.args.target
