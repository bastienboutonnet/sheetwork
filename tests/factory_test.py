import abc
from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_plugins(datafiles):
    from core.adapters.factory import AdapterContainer
    from core.flags import FlagParser
    from core.config.profile import Profile
    from core.config.project import Project
    from core.main import parser

    flags = FlagParser(parser, project_dir=str(datafiles), profile_dir=str(datafiles))
    project = Project(flags, "sheetwork_test")
    profile = Profile(project, "dev")
    profile.read_profile()

    a_c = AdapterContainer()
    a_c.register_adapter(profile)
    plugins_dict = a_c.load_plugins()
    allowed_adaptors = ["db_adapter", "connection", "credentials"]

    for plugin_type, plugin in plugins_dict.items():
        assert plugin_type in allowed_adaptors
        assert isinstance(plugin, abc.ABCMeta)
