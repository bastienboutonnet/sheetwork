import uuid
from pathlib import Path
from sheetwork.core.adapters.postgres.impl import PostgresAdaptor

import pandas
import pytest
import sqlalchemy

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize("is_valid_postgres_profile", [True, False])
@pytest.mark.datafiles(FIXTURE_DIR)
def test_parse_and_validate_credentials(datafiles, is_valid_postgres_profile):
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.exceptions import CredentialsParsingError
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser

    target_name = "invalid_profile_test"
    if is_valid_postgres_profile:
        target_name = "postgres_test"

    flags = FlagParser(parser, profile_dir=str(datafiles), project_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, target_name=target_name)

    credentials = PostgresCredentials(profile)
    if is_valid_postgres_profile is False:
        with pytest.raises(CredentialsParsingError):
            credentials.parse_and_validate_credentials()
    else:
        credentials.parse_and_validate_credentials()
        assert credentials.are_valid_credentials is True
        assert credentials.user == "sheetwork_user"
        assert credentials.password == "magical_password"
        assert credentials.host == "localhost"
        assert credentials.port == "5432"
        assert credentials.database == "sheetwork_test"
        assert credentials.target_schema == "sheetwork_test_schema"
        assert credentials._db_type == "postgres"


@pytest.mark.datafiles(FIXTURE_DIR)
def test_generate_engine(datafiles):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials
    from sheetwork.core.adapters.postgres.connection import PostgresConnection

    flags = FlagParser(parser, profile_dir=str(datafiles), project_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, target_name="postgres_test")

    credentials = PostgresCredentials(profile)
    credentials.parse_and_validate_credentials()

    connection = PostgresConnection(credentials)

    assert isinstance(connection.engine, sqlalchemy.engine.Engine)
    assert (
        connection._engine_str
        == "postgresql+psycopg2://sheetwork_user:magical_password@localhost:5432/sheetwork_test"
    )


@pytest.mark.parametrize("is_valid_table", [True, False])
@pytest.mark.datafiles(FIXTURE_DIR)
def test_check_table(datafiles, is_valid_table):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials
    from sheetwork.core.adapters.postgres.connection import PostgresConnection
    from sheetwork.core.exceptions import TableDoesNotExist

    flags = FlagParser(parser, profile_dir=str(datafiles), project_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, target_name="postgres_test")

    credentials = PostgresCredentials(profile)
    credentials.parse_and_validate_credentials()

    connection = PostgresConnection(credentials)

    a = PostgresAdaptor(connection, config=str())
    target_table = "non_existant"
    if is_valid_table:
        target_table = "test"
        columns, rows = a.check_table(
            target_schema="sheetwork_test_schema", target_table=target_table
        )
        assert rows == 2
        assert columns == 3
    else:
        with pytest.raises(TableDoesNotExist):
            columns, rows = a.check_table(
                target_schema="sheetwork_test_schema", target_table=target_table
            )


@pytest.mark.parametrize(
    "schema_exists, destructive", [(True, True), (False, True), (False, False)]
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_upload(datafiles, schema_exists, destructive):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.config.config import ConfigLoader
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials
    from sheetwork.core.adapters.postgres.connection import PostgresConnection

    df = pandas.DataFrame({"col_a": [1, 2, 3], "col_b": ["unicorn", "rainbow", "sparkles"]})

    flags = FlagParser(parser)
    if schema_exists:
        target_schema = "sheetwork_test_schema"
        flags.consume_cli_arguments(
            [
                "upload",
                "--sheet-key",
                "test_sheet",
                "--project-dir",
                str(datafiles),
                "--profile-dir",
                str(datafiles),
                "--sheet-config-dir",
                str(datafiles),
                "--schema",
                target_schema,
                "--table",
                "magical_table",
            ]
        )
    else:
        target_schema = f"unicorn_{str(uuid.uuid4())[:8]}"
        flags.consume_cli_arguments(
            [
                "upload",
                "--sheet-key",
                "test_sheet",
                "--project-dir",
                str(datafiles),
                "--profile-dir",
                str(datafiles),
                "--sheet-config-dir",
                str(datafiles),
                "--schema",
                target_schema,
                "--table",
                "magical_table",
            ]
        )

    project = Project(flags)
    config = ConfigLoader(flags, project)
    profile = Profile(project, target_name="postgres_test")

    credentials = PostgresCredentials(profile)
    credentials.parse_and_validate_credentials()

    connection = PostgresConnection(credentials)
    a = PostgresAdaptor(connection=connection, config=config)
    # this triggers a forced append to test appending rather than replace logic
    # we call upload twice to make it really append
    if destructive is False:
        a._config.project.destructive_create_table = False
        a.upload(df, target_schema)
        a.upload(df, target_schema)
        columns, rows = a.check_table(target_schema, config.target_table)
        assert columns == 2
        assert rows == 6
    else:
        a.upload(df, target_schema)
        # this is not strictly testing upload but it helps us get results to asser agsinst.
        columns, rows = a.check_table(target_schema, config.target_table)
        assert columns == 2
        assert rows == 3


@pytest.mark.datafiles(FIXTURE_DIR)
def test_execute_query(datafiles):
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.config.config import ConfigLoader
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser
    from sheetwork.core.adapters.postgres.connection import PostgresCredentials
    from sheetwork.core.adapters.postgres.connection import PostgresConnection

    expectation = [(1, 11, "hello hello world"), (2, 42, "what is the meaning of life?")]

    flags = FlagParser(parser)
    flags.consume_cli_arguments(
        [
            "upload",
            "--sheet-key",
            "test_sheet",
            "--project-dir",
            str(datafiles),
            "--profile-dir",
            str(datafiles),
            "--sheet-config-dir",
            str(datafiles),
            "--schema",
            "sheetwork_test_schema",
            "--table",
            "magical_table",
        ]
    )

    project = Project(flags)
    config = ConfigLoader(flags, project)
    profile = Profile(project, target_name="postgres_test")

    credentials = PostgresCredentials(profile)
    credentials.parse_and_validate_credentials()

    connection = PostgresConnection(credentials)
    a = PostgresAdaptor(connection=connection, config=config)
    results = a.excecute_query("select * from sheetwork_test_schema.test", return_results=True)
    assert results == expectation
