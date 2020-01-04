import os

import pytest

from core.flags import FlagParser

from .mockers import EXPECTED_CONFIG

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_set_config(datafiles):
    from core.config.config import ConfigLoader
    from core.config.project import Project
    from core.main import parser

    flags = FlagParser(
        parser,
        test_sheet_name="df_dropper",
        project_dir=str(datafiles),
        sheet_config_dir=str(datafiles),
    )
    project = Project(flags)
    config = ConfigLoader(flags, project)

    assert config.sheet_config == EXPECTED_CONFIG
