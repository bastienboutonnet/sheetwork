from pathlib import Path

import pytest

from .mockers import EXPECTED_DEV_TEST_PROFILE

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "target_name, profile_name, profile_dir",
    [
        ("dev", "sheetwork_test", None),
        ("dev", "non_existant", "bad_dir"),
        ("dev", "non_profile", None),
        ("non_existant", "sheetwork_test", None),
    ],
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_read_profile(datafiles, target_name, profile_name, profile_dir):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.exceptions import ProfileParserError

    flags = FlagParser(parser, project_dir=str(datafiles), profile_dir=str(datafiles))
    project = Project(flags)
    print(f"TARGET_NAME {target_name}")
    print(f"PROFILE_NAME {profile_name}")
    if target_name == "non_existant" and profile_name == "sheetwork_test":
        with pytest.raises(ProfileParserError):
            profile = Profile(project, target_name)

    elif profile_name == "non_profile":
        project.project_name = profile_name
        with pytest.raises(ProfileParserError):
            profile = Profile(project, target_name)

    elif target_name == "dev" and profile_name == "sheetwork_test":
        profile = Profile(project, target_name)
        assert profile.profile_dict == EXPECTED_DEV_TEST_PROFILE

    if profile_dir == "bad_dir":
        with pytest.raises(FileNotFoundError):
            project.profile_dir = Path()
            profile = Profile(project, target_name)
