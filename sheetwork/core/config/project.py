"""Houses Project parsing class from sheetwork_project.yml."""
import time
from pathlib import Path
from typing import Dict, Union

from sheetwork.core.exceptions import ProjectFileParserError
from sheetwork.core.flags import FlagParser
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import yellow
from sheetwork.core.utils import PathFinder, deprecate
from sheetwork.core.yaml.yaml_helpers import open_yaml, validate_yaml
from sheetwork.core.yaml.yaml_schema import project_schema


class Project:
    """Sets up everything there is to know about the project config.

    Will give precedence to CLI Args --see override functions.
    """

    PROJECT_FILENAME = "sheetwork_project.yml"
    # this is some garbage to make sure we don't sleep when we test the deprecation handling
    # ! DEPRECATION "always_create"
    IS_TEST = False

    def __init__(self, flags: FlagParser) -> None:
        """Constructs project object.

        Args:
            flags (FlagParser): Inited flags object.
        """
        self.project_dict: Dict[str, Union[str, bool]] = dict()
        self.target_schema: str = str()
        self.object_creation_dct: Dict[str, bool] = dict()
        self.destructive_create_table: bool = False
        self.flags = flags

        # directories (first overwritten by flags, then by project) This may not always be able to
        # be like this we might wanna give prio to CLI but for now this removes some complication.
        self.project_file_fullpath: Path = Path("dumpy_path")
        self.profile_dir: Path = Path("~/.sheetwork/").expanduser()
        self.sheet_config_dir: Path = Path.cwd()

        # override defaults
        self.override_paths_from_flags()
        self.load_project_from_yaml()
        self.decide_object_creation()
        self.override_object_creation_from_flags()
        logger.debug(f"Project name: {self.project_name}")

    def load_project_from_yaml(self):
        if self.project_file_fullpath == Path("dumpy_path"):
            _, self.project_file_fullpath = PathFinder().find_nearest_dir_and_file(
                type(self).PROJECT_FILENAME
            )
        project_yaml = open_yaml(self.project_file_fullpath)
        is_valid_yaml = validate_yaml(project_yaml, project_schema)
        if project_yaml and is_valid_yaml:
            self.project_dict = project_yaml
            self.project_name = project_yaml.get("name")
            self.target_schema = project_yaml.get("target_schema", self.target_schema)
            if project_yaml.get("paths"):
                self.profile_dir = (
                    Path(project_yaml["paths"].get("profile_dir", self.profile_dir))
                    .expanduser()
                    .resolve()
                )
                self.sheet_config_dir = (
                    Path(project_yaml["paths"].get("sheet_config_dir", self.sheet_config_dir))
                    .expanduser()
                    .resolve()
                )
        else:
            raise ProjectFileParserError(
                f"Error trying to load project config from {self.project_file_fullpath}. "
                "Check it exists or that it is valid."
            )

    # ! DEPRECATION "always_create"
    def handle_deprecations(self, colour: str = "red") -> None:
        if self.project_dict.get("always_create"):
            msg = (
                "'always_create' will be deprecated in a future major release "
                "'always_create' now means 'always_create_table'. "
                "Prefer using 'always_create_table' instead or 'always_create_all_objects' if you "
                "want to make sheetwork create all objects (database, schemas and tables)."
            )

            deprecate(message=msg, colour=colour)
            if type(self).IS_TEST is False:
                time.sleep(4)

    def decide_object_creation(self) -> None:
        self.handle_deprecations()
        create_everything_label = "always_create_objects"
        object_creation_mapping = {
            # ! DEPRECATE "always_create"
            "create_table": ["always_create_table", "always_create"],
            "create_schema": ["always_create_schema"],
        }
        for object_type, rule in object_creation_mapping.items():
            if self.project_dict.get(create_everything_label):
                create = [True]
            else:
                create = [True for x in rule if self.project_dict.get(x) is True]
            self.object_creation_dct.update({object_type: True in create})
        self.destructive_create_table = (
            True
            if self.project_dict.get("destructive_create_table", self.destructive_create_table)
            is True
            else False
        )
        logger.debug(yellow(f"Object creation dict:\n {self.object_creation_dct}"))
        logger.debug(yellow(str(self.project_dict)))

    def override_paths_from_flags(self):
        if self.flags.project_dir:
            self.project_file_fullpath = Path(self.flags.project_dir, type(self).PROJECT_FILENAME)

        if self.flags.profile_dir:
            self.profile_dir = Path(self.flags.profile_dir)

        if self.flags.sheet_config_dir:
            self.sheet_config_dir = Path(self.flags.sheet_config_dir)

    def override_object_creation_from_flags(self) -> None:
        if self.flags.create_table:
            logger.debug(yellow("going to create table"))
            self.object_creation_dct.update({"create_table": True})

        if self.flags.create_schema:
            logger.debug(yellow("going to create schema"))
            self.object_creation_dct.update({"create_schema": True})
        logger.debug(yellow(f"Object creation dict after override\n {self.object_creation_dct}"))

        if self.flags.destructive_create_table:
            logger.debug(yellow("going to perform destuctive table creation"))
            self.destructive_create_table = True
