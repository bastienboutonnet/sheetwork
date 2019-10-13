import os

import yaml

from sheetload.exceptions import SheetloadConfigMissingError
from sheetload.flags import args, logger


class FlagParser:
    def __init__(self):
        self.fetch_yml_config = True
        self.sheet_name = args.sheet_name
        self.create_table = args.create_table
        self.sheet_key = args.sheet_key
        self.target_schema = args.schema
        self.target_table = args.table
        if args.sheet_key and args.schema and args.table:
            self.fetch_yml_config = False
        if self.fetch_yml_config is True and not args.schema or not args.table:
            raise NotImplementedError(
                """
                No target schema and or target was provided.
                You must provide one when reading not from config."
                """
            )
        if not args.sheet_key and not args.sheet_name:
            raise NotImplementedError(
                """
                No sheet selected for import. Provide a sheet_key or a sheet_name.
                See help, for hints."""
            )


class ConfigLoader(FlagParser):
    def __init__(self):
        self.config_file = None
        self.sheet_config = None
        self.sheet_columns = None
        FlagParser.__init__(self)
        self.load_config_from_file()

    def load_config_from_file(self):
        config_file_exists = os.path.isfile("sheets.yml")
        if not self.fetch_yml_config:
            logger.info("Reading config from command line arguments.")
            pass
        if config_file_exists and self.fetch_yml_config:
            with open("sheets.yml", "r") as stream:
                self.config = yaml.safe_load(stream)
            self._get_sheet_config()
            self._generate_column_dict()
            self._override_cli_args()
        elif not config_file_exists and self.fetch_yml_config:
            raise SheetloadConfigMissingError(
                "Are you in a sheetload folder? Cannot find 'sheets.yml' to import config from."
            )

    def _override_cli_args(self):
        self.sheet_key = self.sheet_config["sheet_key"]
        self.target_schema = self.sheet_config["schema"]
        self.target_table = self.sheet_config["table"]

    def _get_sheet_config(self):
        if self.fetch_yml_config:
            sheets = self.config["sheets"]
            sheet_config = [sheet for sheet in sheets if sheet["sheet_name"] == "test_sheet"]
            if len(sheet_config) > 1:
                raise AttributeError(
                    f"Found more than one config for {self.sheet_name}. Check your sheets.yml file."
                )
            self.sheet_config = sheet_config[0]

    def _generate_column_dict(self):
        if self.fetch_yml_config and self.sheet_config:
            columns = self.sheet_config.get("columns")
            column_dict = dict()
            for column in columns:
                column_dict.update(dict({column.get("name"): column.get("type")}))
            self.sheet_columns = column_dict
