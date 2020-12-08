from pathlib import Path

import pytest

from .mockers import (
    EXPECTED_SHEETWORK_PROJECT,
    EXPECTED_SHEETWORK_PROJECT_DEPRECATED,
    EXPECTED_SHEETWORK_PROJECT_ALL_CREATE,
)

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_project_from_yaml(datafiles):
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.config.project import Project
    from sheetwork.core.main import parser

    flags = FlagParser(parser, project_dir=str(datafiles))
    project = Project(flags)
    project.load_project_from_yaml()

    assert project.project_dict == EXPECTED_SHEETWORK_PROJECT


@pytest.mark.parametrize(
    "project_name",
    ["sheetwork_project", "sheetwork_project_all_create", "sheetwork_project_deprecated"],
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_decide_object_creation(monkeypatch, datafiles, project_name):
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.config.project import Project
    from sheetwork.core.main import parser

    monkeypatch.setattr(Project, "PROJECT_FILENAME", f"{project_name}.yml")
    monkeypatch.setattr(Project, "IS_TEST", True)

    expected_object_creation_dict = {
        "create_table": True,
        "create_schema": True,
    }

    if project_name == "sheetwork_project_all_create":
        expected_object_creation_dict = {val: True for val in expected_object_creation_dict}

    if project_name == "sheetwork_project_deprecated":
        expected_object_creation_dict.update({"create_schema": False})

    flags = FlagParser(parser, project_dir=str(datafiles))
    project = Project(flags)
    project.decide_object_creation()

    assert project.object_creation_dct == expected_object_creation_dict
    assert project.destructive_create_table is True


@pytest.mark.parametrize(
    "project_name",
    ["sheetwork_project", "sheetwork_project_all_create", "sheetwork_project_deprecated"],
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_override_object_creation_from_flags(monkeypatch, datafiles, project_name):
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.config.profile import Project
    from sheetwork.core.main import parser

    def mock_consume_cli_arguments(self):
        self.create_table = True
        self.destructive_create_table = True

    monkeypatch.setattr(FlagParser, "consume_cli_arguments", mock_consume_cli_arguments)
    flags = FlagParser(parser, project_dir=str(datafiles))
    flags.consume_cli_arguments()

    project = Project(flags)
    project.decide_object_creation()

    assert project.object_creation_dct["create_table"] is True
    assert project.object_creation_dct["create_schema"] is True
    assert project.destructive_create_table is True
