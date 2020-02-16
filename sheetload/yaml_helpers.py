import os

import yaml
from cerberus import Validator

from sheetload.exceptions import SheetConfigParsingError, SheetloadConfigMissingError
from sheetload.flags import logger
from sheetload.yaml_schema import validation_schema


def load_yaml(override_folder: str = str()) -> dict:
    if override_folder:
        yml_file = os.path.join(override_folder, "sheets.yml")
    else:
        yml_file = "sheets.yml"
    yml_exists = os.path.isfile(yml_file)
    logger.info(override_folder)
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


def validate_yaml(override_folder: str = str()):
    v = Validator()
    doc = load_yaml(override_folder)
    valid_yaml = v.validate(doc, validation_schema)
    if not valid_yaml:
        raise SheetConfigParsingError(f"scheet.yml is not formatted properly. \n {v.errors}")
    return valid_yaml
