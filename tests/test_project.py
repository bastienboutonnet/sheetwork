from pathlib import Path

import pytest

from .mockers import EXPECTED_SHEETWORK_PROJECT

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_project_from_yaml(datafiles):
    from core.flags import FlagParser
    from core.config.project import Project
    from core.main import parser

    flags = FlagParser(parser, project_dir=str(datafiles))
    project = Project(flags)
    project.load_project_from_yaml()

    assert project.project_dict == EXPECTED_SHEETWORK_PROJECT
