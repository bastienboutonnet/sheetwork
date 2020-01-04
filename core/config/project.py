from core.yaml.yaml_helpers import open_yaml, validate_yaml
from core.yaml.yaml_schema import project_schema
from core.utils import PathFinder
from pathlib import Path
from typing import TYPE_CHECKING
from core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from core.flags import FlagParser

PROJECT_FILENAME = "sheetload_project.yml"


class Project:
    """Sets up everything there is to know about the project config.
    """

    def __init__(self, flags: "FlagParser", project_name: str = str()):
        self.project_name = project_name
        self.project_dict: dict = dict()
        self.target_schema: str = str()
        self.always_create: bool = True
        self.flags = flags

        # directories (first overwritten by flags, then by project) This may not always be able to
        # be like this we might wanna give prio to CLI but for now this removes some complication.
        self.project_file_fullpath: Path = Path("dumpy_path")
        self.profile_dir: Path = Path("~/.sheetload/").expanduser()
        self.sheet_config_dir: Path = Path.cwd()

        # override defaults
        self.override_from_flags()
        self.load_project_from_yaml()
        logger.debug(f"Project name: {self.project_name}")

    # TODO: Bake in some post loading verification and throw error if no file is loaded.
    def load_project_from_yaml(self):
        if self.project_file_fullpath == Path("dumpy_path"):
            _, self.project_file_fullpath = PathFinder().find_nearest_dir_and_file(PROJECT_FILENAME)
        project_yaml = open_yaml(self.project_file_fullpath)
        is_valid_yaml = validate_yaml(project_yaml, project_schema)
        logger.debug(f"PROJECT_YAML: {project_yaml}")
        if is_valid_yaml:
            self.project_dict = project_yaml
            self.project_name = project_yaml.get("name", self.project_name)
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
            self.always_create = project_yaml.get("always_create", self.always_create)

    def override_from_flags(self):
        if self.flags.project_dir:
            self.project_file_fullpath = Path(self.flags.project_dir, PROJECT_FILENAME)
        if self.flags.profile_dir:
            self.profile_dir = Path(self.flags.profile_dir)
        if self.flags.sheet_config_dir:
            self.sheet_config_dir = Path(self.flags.sheet_config_dir)
