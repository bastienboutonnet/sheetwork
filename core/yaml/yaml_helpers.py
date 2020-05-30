from pathlib import Path

import yaml
from cerberus import Validator

from core.exceptions import SheetConfigParsingError, YAMLFileEmptyError


def open_yaml(path: "Path"):
    if path.is_file():
        with open(path, "r") as stream:
            yaml_file = yaml.safe_load(stream)  # type: ignore
            if yaml_file:
                return yaml_file
            raise YAMLFileEmptyError(f"Your yml file {path.resolve()} seems empty.")
    raise FileNotFoundError(f"File {path.resolve()} was not found.")


def validate_yaml(yaml: dict, validation_schema: dict) -> bool:
    v = Validator()
    valid_yaml = v.validate(yaml, validation_schema)
    if not valid_yaml:
        raise SheetConfigParsingError(f"scheet.yml is not formatted properly. \n {v.errors}")
    return valid_yaml
