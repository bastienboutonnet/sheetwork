from pathlib import Path

import pytest

from .mockers import EXPECTED_DEV_TEST_PROFILE

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_read_profile(datafiles):
    from core.config.profile import Profile

    print(FIXTURE_DIR)
    profile = Profile("sheetload_test", "dev", datafiles)
    profile.read_profile()

    assert profile.profile_dict == EXPECTED_DEV_TEST_PROFILE
