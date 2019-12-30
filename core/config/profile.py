from pathlib import Path

from core.exceptions import InvalidProfileError, ProfileParserError
from core.logger import GLOBAL_LOGGER as logger
from core.yaml.yaml_helpers import open_yaml, validate_yaml
from core.yaml.yaml_schema import profiles_schema

DEFAULT_PROFILE_DIR = Path("~/.sheetload/").expanduser()


class Profile:
    """Load, validate and set profile for sheetload.

    Raises:
        FileNotFoundError: If no profiles.yml can be found in the expected location.
        InvalidProfileError: When a profile is not valid to the requirements

    Returns:
        Profile: Class holding all profiles variables necessary for clients and connections to be
        setup.
    """

    def __init__(self, profile_name: str, target_name: str, profile_dir: str = str()):
        self.profile_name = profile_name
        self.target_name = target_name
        self.profile_dict: dict = dict()
        self.cannot_be_none = {"db_type", "guser"}
        self.profile_dir: Path = DEFAULT_PROFILE_DIR
        if profile_dir:
            self.profile_dir = Path(profile_dir).expanduser().resolve()

    def read_profile(self):
        filename = Path(self.profile_dir, "profiles.yml")
        if filename.exists():
            yaml_dict = open_yaml(filename)
            logger.debug(f"YAML_PROFILE: {yaml_dict}")
            is_valid_yaml = validate_yaml(yaml_dict, profiles_schema)
            profile = yaml_dict["profiles"].get(self.profile_name)
            logger.debug(f"TARGET_PROFILE: {profile}")
            if profile.get("outputs"):
                target_profile = profile["outputs"].get(self.target_name)
            if target_profile and is_valid_yaml:
                is_valid_profile = self._validate_profile(target_profile)
                if is_valid_profile:
                    self.profile_dict = target_profile
                    logger.debug(f"PARSED_PROFILE: {self.profile_dict}")
            else:
                raise ProfileParserError(f"Error finding and entry for {self.target_name}.")
        else:
            raise FileNotFoundError(
                f"Could not open or find {filename.resolve()} check that it exists"
            )

    def _validate_profile(self, profile_dict: dict) -> bool:
        print(profile_dict)
        if isinstance(profile_dict, dict):
            keys_with_nones = {k for k, v in profile_dict.items() if not v}
            keys_with_nones.intersection_update(self.cannot_be_none)
            if keys_with_nones:
                raise InvalidProfileError(
                    f"The following fields: {keys_with_nones} cannot be empty."
                )
            return True
        raise ProfileParserError(f"Error finding and entry for {self.target_name}.")
