import os

import pytest

from sheetload.flags import FlagParser

from .mockers import EXPECTED_CONFIG

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_set_config(datafiles):
    from sheetload.config import ConfigLoader

    flags = FlagParser()
    config = ConfigLoader(flags, yml_folder=str(datafiles))

    assert config.sheet_config == EXPECTED_CONFIG
