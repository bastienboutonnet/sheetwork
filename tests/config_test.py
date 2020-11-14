import os

import pytest

from sheetwork.core.flags import FlagParser

from .mockers import EXPECTED_CONFIG, NO_COLS_EXPECTED_CONFIG

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_set_config(datafiles):
    from sheetwork.core.config.config import ConfigLoader

    from sheetwork.core.config.project import Project
    from sheetwork.core.main import parser

    flags = FlagParser(
        parser,
        test_sheet_name="df_dropper",
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    project = Project(flags)
    config = ConfigLoader(flags, project)

    flags2 = FlagParser(
        parser,
        test_sheet_name="no_cols",
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    project2 = Project(flags2)
    config2 = ConfigLoader(flags2, project2)

    assert config.sheet_config == EXPECTED_CONFIG
    assert config2.sheet_config == NO_COLS_EXPECTED_CONFIG


@pytest.mark.datafiles(FIXTURE_DIR)
def test__override_cli_args(datafiles):
    from sheetwork.core.config.config import ConfigLoader

    from sheetwork.core.main import parser
    from sheetwork.core.config.project import Project

    flags = FlagParser(
        parser,
        test_sheet_name="sheet_with_no_schema",
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    project = Project(flags)
    config = ConfigLoader(flags, project)
    assert config.target_schema == project.target_schema
