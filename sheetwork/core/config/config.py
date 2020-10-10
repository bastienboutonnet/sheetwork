from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Union

from sheetwork.core.config.project import Project
from sheetwork.core.exceptions import (
    SheetConfigParsingError,
    SheetWorkConfigMissingError,
    TargetSchemaMissing,
)
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import yellow
from sheetwork.core.yaml.yaml_helpers import open_yaml, validate_yaml
from sheetwork.core.yaml.yaml_schema import config_schema

if TYPE_CHECKING:
    from core.flags import FlagParser


class ConfigLoader:
    def __init__(self, flags: "FlagParser", project: Project):
        self.config: Dict[str, List[Dict[str, Any]]] = dict()
        self.sheet_config: Dict[str, Union[str, bool, List[Union[str, Dict[str, str]]]]] = dict(
            sheet_key=flags.sheet_key,
            target_schema=flags.target_schema,
            target_table=flags.target_table,
        )
        self.target_schema: str = flags.target_schema
        self.target_table: str = flags.target_table
        self.sheet_column_rename_dict: Dict[str, str] = dict()
        self.sheet_columns: Dict[str, str] = dict()
        self.excluded_columns: Dict = dict()
        self.flags = flags
        self.project = project
        self.yml_folder: Path = project.sheet_config_dir
        logger.debug(f"SHEET_FOLDER: {project.sheet_config_dir}")
        self.set_config()

    def set_config(self):
        if self.flags.sheet_name:
            self.load_config_from_file()
        elif self.flags.sheet_key and self.flags.target_schema and self.flags.target_table:
            logger.debug("Reading config from command line.")
        else:
            raise NotImplementedError(
                """
                No target schema and or target was provided.
                You must provide one when not reading from config file.
                """
            )

    def load_config_from_file(self):
        logger.debug("Reading config from config file.")
        filename = Path(self.yml_folder, "sheets.yml")
        logger.debug(f"SHEET FILENAME: {filename}")
        if filename.exists():
            config_yaml = open_yaml(filename)
        else:
            raise SheetWorkConfigMissingError(
                """
                Are you in a sheetwork folder? Cannot find 'sheets.yml' to import config from.
                If you plan to run sheetwork from a different folder than current you'll have to
                provide a custom path to the config files. See --help for arguments."""
            )
        if config_yaml:
            is_valid_yaml = validate_yaml(config_yaml, config_schema)
        if is_valid_yaml:
            self.config = config_yaml
            self.get_sheet_config()
            self._generate_column_type_override_dict()
            self._generate_column_rename_dict()
            self._override_cli_args()

    @staticmethod
    def lowercase(obj: Dict[str, str]) -> Dict[str, str]:
        """ Make dictionary lowercase """
        new: Dict[str, str] = dict()
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    v = lowercase(v)  # type: ignore # noqa
                if k == "name":
                    new[k] = v.lower()  # type: ignore
                else:
                    new[k] = v
        return new

    def get_sheet_config(self):
        if self.flags.sheet_name:
            sheets = self.config["sheets"]
            sheet_config = [
                sheet for sheet in sheets if sheet.get("sheet_name") == self.flags.sheet_name
            ]
            if len(sheet_config) > 1:
                raise SheetConfigParsingError(
                    f"Found more than one config for {self.flags.sheet_name}. "
                    "Check your sheets.yml file."
                )
            if not sheet_config:
                raise SheetConfigParsingError(
                    f"No configuration was found for {self.flags.sheet_name}. "
                    "Check your sheets.yml file."
                )
            self.sheet_config = sheet_config[0]
            logger.debug(f"Sheet config dict: {self.sheet_config}")
            if self.sheet_config.get("columns"):
                self.sheet_config["columns"] = [
                    self.lowercase(column_dict) for column_dict in self.sheet_config.get("columns")  # type: ignore
                ]
                logger.debug(f"Cols after lowercasing: {self.sheet_config.get('columns')}")
        else:
            raise SheetWorkConfigMissingError("No sheet name was provided, cannot fetch config.")

    def _generate_column_type_override_dict(self):
        """Generates a dictionary of key, value where key is the name of a column and value is the
        name of the datatype into that column should be cast on table creation.
        """

        try:
            if self.sheet_config and self.sheet_config.get("columns"):
                columns: List[Dict[str, str]] = self.sheet_config.get("columns", list())  # type: ignore
                column_dict: Dict[str, str] = dict()
                for column in columns:
                    column_dict.update({column.get("name", str()): column.get("datatype", str())})
                if column_dict:
                    logger.debug(f"colums operations dict: {column_dict}")
                    self.sheet_columns = column_dict
        except KeyError as e:
            logger.warning(
                yellow(
                    f"No {str(e)} data for {self.flags.sheet_name}. But that might be intentional."
                )
            )

    def _generate_column_rename_dict(self):
        """Generates a dictionary of key values where key is the original name in the sheet and
        value is the target name.
        """

        if self.sheet_config:
            columns: List[Dict[str, str]] = self.sheet_config.get("columns", list())  # type: ignore
            if columns:
                column_rename_dict: Dict[str, str] = dict()
                for column in columns:
                    if column.get("identifier"):
                        column_rename_dict.update(dict({column["identifier"]: column["name"]}))
                    if column_rename_dict:
                        logger.debug(f"column renaming dict {column_rename_dict}")
                        self.sheet_column_rename_dict = column_rename_dict

    def _override_cli_args(self):
        """Overrides any CLI argument that may have been passed to sheeload when it reads from a
        config yaml file, thereby giving precedence to the arguments in the .yml file.
        """

        self.sheet_key = self.sheet_config["sheet_key"]
        if not self.target_table:
            self.target_table = str(self.sheet_config.get("target_table", str()))
        if not self.target_schema:
            self.target_schema = str(
                self.sheet_config.get("target_schema", self.project.target_schema)
            )
        if not self.target_schema:
            raise TargetSchemaMissing(
                "No target schema found. You must provide one either in the project, sheet or CLI"
            )
