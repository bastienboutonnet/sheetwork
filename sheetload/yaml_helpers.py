import os

import yaml
from cerberus import Validator

from sheetload.exceptions import SheetConfigParsingError, SheetloadConfigMissingError
from sheetload.yaml_schema import validation_schema


def load_yaml():
    yml_exists = os.path.isfile("sheets.yml")
    if yml_exists:
        with open("sheets.yml", "r") as stream:
            yaml_file = yaml.safe_load(stream)
            if yaml_file:
                return yaml_file
            raise SheetConfigParsingError("Your sheets.yml file seems empty.")
    else:
        raise SheetloadConfigMissingError(
            "Are you in a sheetload folder? Cannot find 'sheets.yml' to import config from."
        )


def validate_yaml():
    v = Validator()
    doc = load_yaml()
    valid_yaml = v.validate(doc, validation_schema)
    if not valid_yaml:
        raise SheetConfigParsingError(f"scheet.yml is not formatted properly. \n {v.errors}")
