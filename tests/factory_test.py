from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_plugins(datafiles):
    from sheetwork.core.adapters.base.connection import BaseConnection, BaseCredentials
    from sheetwork.core.adapters.base.impl import BaseSQLAdapter
    from sheetwork.core.adapters.factory import AdapterContainer
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser

    flags = FlagParser(parser, project_dir=str(datafiles), profile_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, "dev")
    profile.read_profile()

    a_c = AdapterContainer()
    a_c.register_adapter(profile)
    a_c.load_plugins()
    allowed_adaptors = {
        "sql_adapter": BaseSQLAdapter,
        "connection_adapter": BaseConnection,
        "credentials_adapter": BaseCredentials,
    }
    for plugin_type, plugin_class in allowed_adaptors.items():
        c_ada = getattr(a_c, plugin_type)
        assert issubclass(c_ada, plugin_class)
