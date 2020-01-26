from sheetload.exceptions import SheetConfigParsingError, SheetloadConfigMissingError
from sheetload.flags import FlagParser, logger
from sheetload.yaml_helpers import load_yaml, validate_yaml


class ConfigLoader:
    def __init__(self, flags: FlagParser, yml_folder: str = str()):
        self.config_file = None
        self.sheet_config: dict = dict()
        self.sheet_column_rename_dict: dict = dict()
        self.sheet_columns: dict = dict()
        self.excluded_columns: list = list()
        self.flags: FlagParser = flags
        self.yml_folder: str = yml_folder
        self.columns_casing: str = str()
        self.set_config()

    def set_config(self):
        if self.flags.sheet_name:
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
        yml_is_valid = validate_yaml(self.yml_folder)
        if yml_is_valid:
            self.config = load_yaml(self.yml_folder)
        if self.config:
            self.get_sheet_config()
            self._generate_column_type_override_dict()
            self._generate_column_rename_dict()
            self._override_cli_args()
        else:
            raise SheetConfigParsingError("Your sheets.yml file seems empty.")

    @staticmethod
    def lowercase(obj):
        """ Make dictionary lowercase """
        new = dict()
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    v = lowercase(v)
                if k == "name":
                    new[k] = v.lower()
                else:
                    new[k] = v
        return new

    def get_sheet_config(self):
        if self.flags.sheet_name:
            sheets = self.config["sheets"]
            sheet_config = [
                sheet for sheet in sheets if sheet["sheet_name"] == self.flags.sheet_name
            ]
            if len(sheet_config) > 1:
                raise SheetConfigParsingError(
                    f"Found more than one config for {self.flags.sheet_name}. Check your sheets.yml file."
                )
            if not sheet_config:
                raise SheetConfigParsingError(
                    f"No configuration was found for {self.flags.sheet_name}. Check your sheets.yml file."
                )
            self.sheet_config = sheet_config[0]
            logger.debug(f"Sheet config dict: {self.sheet_config}")
            if self.sheet_config.get("columns"):
                self.sheet_config["columns"] = [
                    self.lowercase(column_dict) for column_dict in self.sheet_config.get("columns")
                ]
                logger.debug(f"Cols after casing: {self.sheet_config['columns']}")
        else:
            raise SheetloadConfigMissingError("No sheet name was provided, cannot fetch config.")

    def _generate_column_type_override_dict(self):
        """Generates a dictionary of key, value where key is the name of a column and value is the
        name of the datatype into that column should be cast on table creation.
        """

        try:
            if self.sheet_config and self.sheet_config.get("columns"):
                columns = self.sheet_config.get("columns")
                column_dict = dict()
                for column in columns:
                    # FIXME: This is a temporary fix to make the data_tools function happy.
                    # And will be removed in a future version as we will have conversion handled
                    # natively.
                    if column.get("datatype") == "numeric":
                        data_type = "numeric(38,18)"
                    else:
                        data_type = column.get("datatype")
                    column_dict.update(dict({column.get("name"): data_type}))
                if column_dict:
                    logger.debug(column_dict)
                    self.sheet_columns = column_dict
        except KeyError as e:
            logger.warning(
                f"No {str(e)} data for {self.flags.sheet_name}. But that might be intentional."
            )

    def _generate_column_rename_dict(self):
        """Generates a dictionary of key values where key is the original name in the sheet and
        value is the target name.
        """

        if self.sheet_config:
            columns = self.sheet_config.get("columns")
            if columns:
                column_rename_dict = dict()
                for column in columns:
                    if column.get("identifier"):
                        column_rename_dict.update(dict({column["identifier"]: column["name"]}))
                    if column_rename_dict:
                        logger.debug(column_rename_dict)
                        self.sheet_column_rename_dict = column_rename_dict

    def _override_cli_args(self):
        """Overrides any CLI argument that may have been passed to sheeload when it reads from a
        config yaml file, thereby giving precedence to the arguments in the .yml file.
        """

        self.sheet_key = self.sheet_config["sheet_key"]
        self.target_schema = self.sheet_config["target_schema"]
        self.target_table = self.sheet_config["target_table"]
