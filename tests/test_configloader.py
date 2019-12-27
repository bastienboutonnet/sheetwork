import os

import pytest

from core.flags import FlagParser

from .mockers import EXPECTED_CONFIG

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_set_config(datafiles):
    from core.config import ConfigLoader
    from core.main import parser

    flags = FlagParser(parser, test_sheet_name="df_dropper")
    config = ConfigLoader(flags, yml_folder=str(datafiles))

    assert config.sheet_config == EXPECTED_CONFIG
