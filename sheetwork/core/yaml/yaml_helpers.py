"""Helpers for yml stuff."""
from pathlib import Path
from typing import Any, Dict

import yaml
from cerberus import Validator

from sheetwork.core.exceptions import SheetConfigParsingError, YAMLFileEmptyError


def open_yaml(path: "Path"):
    """Yeah it opens a yml file..."""
    if path.is_file():
        with open(path, "r") as stream:
            yaml_file = yaml.safe_load(stream)  # type: ignore
            if yaml_file:
                return yaml_file
            raise YAMLFileEmptyError(f"Your yml file {path.resolve()} seems empty.")
    raise FileNotFoundError(f"File {path.resolve()} was not found.")


def validate_yaml(yaml: Dict[Any, Any], validation_schema: Dict[Any, Any]) -> bool:
    """Validates a yml based on a given schema.

    It leverages cerberus Validator. It's pretty strict and the schema dict (found in yaml_schema.py)
    takes a bit to get used to but it's super nice.

    Args:
        yaml (Dict[Any, Any]): A python dictionary from a yml file.
        validation_schema (Dict[Any, Any]): validation dictionary. Check yaml_schema.py for a idea.

    Raises:
        SheetConfigParsingError: Thrown whenever the validation has failed and prints what the errors are.

    Returns:
        bool: True if yml is valid, and false it if it's not.
    """
    v = Validator()
    is_valid_yaml: bool = v.validate(yaml, validation_schema)  # type: ignore
    if not is_valid_yaml:
        raise SheetConfigParsingError(f"scheet.yml is not formatted properly. \n {v.errors}")  # type: ignore
    return is_valid_yaml
