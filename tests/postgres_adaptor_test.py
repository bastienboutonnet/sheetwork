from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.datafiles(FIXTURE_DIR)
def test_parse_and_validate_credentials(datafiles):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials

    flags = FlagParser(parser, profile_dir=str(datafiles), project_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, target_name="postgres_test")

    credentials = PostgresCredentials(profile)
    credentials.parse_and_validate_credentials()

    assert credentials.are_valid_credentials is True
    assert credentials.user == "sheetwork_user"
    assert credentials.password == "magical_password"
    assert credentials.host == "localhost"
    assert credentials.port == "5432"
    assert credentials.database == "sheetwork_test"
    assert credentials.schema == "sheetwork_test_schema"
    assert credentials._db_type == "postgres"
