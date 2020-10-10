from pathlib import Path

import pytest

from .mockers import EXPECTED_DEV_TEST_PROFILE

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_read_profile(datafiles):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser

    flags = FlagParser(parser, project_dir=str(datafiles), profile_dir=str(datafiles))
    project = Project(flags, "sheetwork_test")
    profile = Profile(project, "dev")
    profile.read_profile()

    assert profile.profile_dict == EXPECTED_DEV_TEST_PROFILE
