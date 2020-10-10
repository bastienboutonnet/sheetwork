from pathlib import Path
from typing import Dict

from sheetwork.core.config.project import Project
from sheetwork.core.exceptions import InvalidProfileError, ProfileParserError
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.yaml.yaml_helpers import open_yaml, validate_yaml
from sheetwork.core.yaml.yaml_schema import profiles_schema


class Profile:
    """Load, validate and set profile for sheetwork.

    Raises:
        FileNotFoundError: If no profiles.yml can be found in the expected location.
        InvalidProfileError: When a profile is not valid to the requirements

    Returns:
        Profile: Class holding all profiles variables necessary for clients and connections to be
        setup.
    """

    def __init__(self, project: Project, target_name: str = str()):
        self.profile_name = project.project_name
        self.target_name = target_name
        self.profile_dict: Dict[str, str] = dict()
        self.cannot_be_none = {"db_type", "guser"}
        self.profile_dir: Path = project.profile_dir
        self.google_credentials_dir = Path(project.profile_dir, "google").resolve()
        self.read_profile()
        logger.debug(f"PROFILE_DIR {self.profile_dir}")
        logger.debug(f"PROFILE_NAME: {self.profile_name}")

    def read_profile(self):
        logger.debug(f"Profile Name: {self.profile_name}")
        filename = Path(self.profile_dir, "profiles.yml")
        if filename.exists():
            yaml_dict = open_yaml(filename)
            is_valid_yaml = validate_yaml(yaml_dict, profiles_schema)
            profile = yaml_dict["profiles"].get(self.profile_name)
            if profile:
                # set target name from profile unless one was given at init from flags parse.
                if not self.target_name:
                    self.target_name = profile.get("target")
                if profile.get("outputs"):
                    target_profile = profile["outputs"].get(self.target_name)
                if target_profile and is_valid_yaml:
                    is_valid_profile = self._validate_profile(target_profile)
                    if is_valid_profile:
                        self.profile_dict = target_profile
                else:
                    raise ProfileParserError(
                        f"Error finding and entry for  target: {self.target_name}, "
                        f"under the {self.profile_name} profile."
                    )
            else:
                raise ProfileParserError(
                    f"Could not find an entry for {self.profile_name} in your profile.yml"
                )
        else:
            raise FileNotFoundError(
                f"Could not open or find {filename.resolve()} check that it exists"
            )

    def _validate_profile(self, profile_dict: Dict[str, str]) -> bool:
        if isinstance(profile_dict, dict):
            keys_with_nones = {k for k, v in profile_dict.items() if not v}
            keys_with_nones.intersection_update(self.cannot_be_none)
            if keys_with_nones:
                raise InvalidProfileError(
                    f"The following fields: {keys_with_nones} cannot be empty."
                )
            return True
        raise ProfileParserError(f"Error finding and entry for {self.target_name}.")
