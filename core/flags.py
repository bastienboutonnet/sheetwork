from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import parser


class FlagParser:
    def __init__(self, parser: "parser.ArgumentParser", test_sheet_name: str = str()):
        self.sheet_name = test_sheet_name
        self.create_table = False
        self.sheet_key = str()
        self.target_schema = str()
        self.target_table = str()
        self.mode = "dev"
        self.log_level = str()
        self.force = False
        self.interactive = False
        self.dry_run = False
        self.parser = parser

    def consume_cli_arguments(self):
        self.args = self.parser.parse_args()
        self.sheet_name = self.args.sheet_name
        self.create_table = self.args.create_table
        self.sheet_key = self.args.sheet_key
        self.target_schema = self.args.schema
        self.target_table = self.args.table
        self.mode = self.args.mode
        self.log_level = self.args.log_level
        self.force = self.args.force
        self.interactive = self.args.interactive
        self.dry_run = self.args.dry_run
