import os

import yaml

from sheetload.exceptions import SheetloadConfigMissingError, SheetConfigParsingError
from sheetload.flags import args, logger
from sheetload.yaml_helpers import load_yaml


class FlagParser:
    def __init__(self):
        self.sheet_name = args.sheet_name
        self.create_table = args.create_table
        self.sheet_key = args.sheet_key
        self.target_schema = args.schema
        self.target_table = args.table


class ConfigLoader(FlagParser):
    def __init__(self):
        self.config_file = None
        self.sheet_config = None
        self.sheet_columns = None
        FlagParser.__init__(self)
        self.set_config()

    def set_config(self):
        if self.sheet_name:
            self.load_config_from_file()
        elif self.sheet_key and self.target_schema and self.target_table:
            logger.info("Reading config from command line.")
        else:
            raise NotImplementedError(
                """
                No target schema and or target was provided.
                You must provide one when not reading from config file.
                """
            )

    def load_config_from_file(self):
        logger.info("Reading config from config file.")
        self.config = load_yaml()
        if self.config:
            self._get_sheet_config()
            self._generate_column_dict()
            self._override_cli_args()
        else:
            raise SheetConfigParsingError("Your sheets.yml file seems empty.")

    def _get_sheet_config(self):
        if self.sheet_name:
            sheets = self.config["sheets"]
            sheet_config = [sheet for sheet in sheets if sheet["sheet_name"] == self.sheet_name]
            if len(sheet_config) > 1:
                raise SheetConfigParsingError(
                    f"Found more than one config for {self.sheet_name}. Check your sheets.yml file."
                )
            if not sheet_config:
                raise SheetConfigParsingError(
                    f"No configuration was found for {self.sheet_name}. Check your sheets.yml file."
                )
            self.sheet_config = sheet_config[0]
        else:
            raise SheetloadConfigMissingError("No sheet name was provided, cannot fetch config.")

    def _generate_column_dict(self):
        try:
            if self.sheet_config:
                columns = self.sheet_config["columns"]
                column_dict = dict()
                for column in columns:
                    column_dict.update(dict({column["name"]: column["datatype"]}))
                self.sheet_columns = column_dict
        except KeyError as e:
            logger.warning(
                f"No {str(e)} data for {self.sheet_name}. But that might be intentional."
            )

    def _override_cli_args(self):
        self.sheet_key = self.sheet_config["sheet_key"]
        self.target_schema = self.sheet_config["target_schema"]
        self.target_table = self.sheet_config["target_table"]
