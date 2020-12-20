from pathlib import Path
from sheetwork.core.exceptions import SheetConfigParsingError, SheetWorkConfigMissingError


import pytest

from sheetwork.core.flags import FlagParser

from .mockers import EXPECTED_CONFIG, NO_COLS_EXPECTED_CONFIG

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "parse_from_cli, test_sheet_name",
    [
        (True, "missing_schema_args"),
        (True, "not_missing_schema_args"),
        (False, "df_dropper"),
        (False, "no_cols"),
        (False, "non_existant_sheet"),
        (False, ""),
    ],
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_set_config(datafiles, parse_from_cli, test_sheet_name):
    from sheetwork.core.config.config import ConfigLoader

    from sheetwork.core.config.project import Project
    from sheetwork.core.main import parser

    fake_cli_args = [
        "upload",
        "--sheet-key",
        "dummy_key",
        "--schema",
        "sand",
        "--table",
        "dummy_table",
        "--profile-dir",
        str(datafiles),
        "--project-dir",
        str(datafiles),
        "--sheet-config-dir",
        str(datafiles),
    ]
    fake_cli_args_missing_schema_args = [
        "upload",
        "--sheet-key",
        "dummy_key",
        "--profile-dir",
        str(datafiles),
        "--project-dir",
        str(datafiles),
        "--sheet-config-dir",
        str(datafiles),
    ]
    expected_cli_args_sheet_config = {
        "sheet_key": "dummy_key",
        "target_schema": "sand",
        "target_table": "dummy_table",
    }
    flags = FlagParser(
        parser,
        test_sheet_name=test_sheet_name,
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    if parse_from_cli and test_sheet_name == "missing_schema_args":
        flags.consume_cli_arguments(fake_cli_args_missing_schema_args)
    if parse_from_cli and test_sheet_name == "not_missing_schema_args":
        flags.consume_cli_arguments(fake_cli_args)

    project = Project(flags)
    if parse_from_cli and test_sheet_name == "missing_schema_args":
        with pytest.raises(NotImplementedError):
            config = ConfigLoader(flags, project)
    elif parse_from_cli is False and test_sheet_name == "non_existant_sheet":
        with pytest.raises(SheetConfigParsingError):
            config = ConfigLoader(flags, project)
    elif parse_from_cli is False and test_sheet_name == "":
        with pytest.raises(SheetWorkConfigMissingError):
            config = ConfigLoader(flags, project)
    else:
        config = ConfigLoader(flags, project)

    if parse_from_cli and test_sheet_name == "not_missing_schema_args":
        assert config.sheet_config == expected_cli_args_sheet_config
    if test_sheet_name == "df_dropper" and parse_from_cli is False:
        assert config.sheet_config == EXPECTED_CONFIG
    if test_sheet_name == "no_cols" and parse_from_cli is False:
        assert config.sheet_config == NO_COLS_EXPECTED_CONFIG


@pytest.mark.datafiles(FIXTURE_DIR)
def test__override_cli_args(datafiles):
    from sheetwork.core.config.config import ConfigLoader
    from sheetwork.core.config.project import Project
    from sheetwork.core.main import parser

    flags = FlagParser(
        parser,
        test_sheet_name="sheet_with_no_schema",
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    project = Project(flags)
    config = ConfigLoader(flags, project)
    assert config.target_schema == project.target_schema
