import os
from pathlib import Path

import yaml
from cerberus import Validator

from core.exceptions import SheetConfigParsingError, SheetloadConfigMissingError, YAMLFileEmptyError
from core.logger import GLOBAL_LOGGER as logger


def open_yaml(path: "Path"):
    if path.is_file():
        with open(path, "r") as stream:
            yaml_file = yaml.safe_load(stream)
            if yaml_file:
                return yaml_file
            raise YAMLFileEmptyError(f"Your yml file {path.resolve()} seems empty.")
    raise FileNotFoundError(f"File {path.resolve()} was not found.")


# TODO: Make this be more tied to a sheet config method and genericise or so.
def load_yaml(path: Path) -> dict:
    if path:
        yml_file = os.path.join(path, "sheets.yml")
    else:
        yml_file = "sheets.yml"
    yml_exists = os.path.isfile(yml_file)
    logger.info(path)
    if yml_exists:
        with open(yml_file, "r") as stream:
            yaml_file = yaml.safe_load(stream)
            if yaml_file:
                return yaml_file
            raise SheetConfigParsingError("Your sheets.yml file seems empty.")
    else:
        raise SheetloadConfigMissingError(
            "Are you in a sheetload folder? Cannot find 'sheets.yml' to import config from."
        )


def validate_yaml(yaml: dict, validation_schema: dict) -> bool:
    v = Validator()
    valid_yaml = v.validate(yaml, validation_schema)
    if not valid_yaml:
        raise SheetConfigParsingError(f"scheet.yml is not formatted properly. \n {v.errors}")
    return valid_yaml
