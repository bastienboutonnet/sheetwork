"""Concrete database implementations for Postgres Connector."""
from typing import Any, Optional, Tuple

import pandas
import sqlalchemy
from sqlalchemy import MetaData, func, select
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import CreateSchema

from sheetwork.core.adapters.base.impl import BaseSQLAdapter
from sheetwork.core.adapters.postgres.connection import PostgresConnection
from sheetwork.core.config.config import ConfigLoader
from sheetwork.core.exceptions import (
    DatabaseError,
    NoAcquiredConnectionError,
    TableDoesNotExist,
    UploadError,
)
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import green, red, timed_message, yellow
from sheetwork.core.utils import cast_pandas_dtypes


class PostgresAdaptor(BaseSQLAdapter):
    """Concrete SQL adaptor for Postgres db."""

    def __init__(self, connection: PostgresConnection, config: ConfigLoader) -> None:
        """Constructor for PostgresAdadpor.

        Args:
            connection (PostgresConnection): connection object containing postgres credentials and
                connection engine created via SQLalchemy
            config (ConfigLoader): configuration class containing all params for sheetwork.
        """
        self._connection = connection
        self._engine = connection.engine
        self._config = config
        self._database = connection._credentials.database
        self._has_connection: bool = False

    def acquire_connection(self) -> None:
        try:
            self.con = self._engine.connect()
            self._has_connection = True
        except Exception:
            raise DatabaseError(red("Error creating Postgres connection."))

    def close_connection(self) -> None:
        try:
            self.con.close()
            self._has_connection = False
        except AttributeError:
            raise DatabaseError(
                red("Postgres adaptor did not create a connection so it cannot be closed.")
            )

    def _create_schema(self) -> None:
        if self._has_connection is False:
            raise NoAcquiredConnectionError(
                f"No acquired connection for {type(self).__name__}. "
                "Make sure `acquire_connection is ran before."
            )
        try:
            if self._config.project.object_creation_dct["create_schema"]:
                schema_exists = (
                    True
                    if self._config.target_schema in self.con.dialect.get_schema_names(self.con)
                    else False
                )
                if schema_exists is False:
                    logger.debug(
                        yellow(f"Creating schema: {self._config.target_schema} in {self._database}")
                    )
                    self.con.execute(CreateSchema(self._config.target_schema))
        except Exception as e:
            raise DatabaseError(str(e))

    # TODO: Rework the API here, I don't see a need to pass the target schema as it
    # ! THIS ACTUALLY COULD CREATE A SHITTY BUG!
    # should be accessed from the config.
    def upload(self, df: pandas.DataFrame, target_schema: str) -> None:
        df = cast_pandas_dtypes(df, overwrite_dict=self._config.sheet_columns)
        dtypes_dict = self.sqlalchemy_dtypes(self._config.sheet_columns)

        self.acquire_connection()
        self._create_schema()

        _if_schema_exists = "append"
        if self._config.project.object_creation_dct["create_table"] is True:
            if self._config.project.destructive_create_table:
                _if_schema_exists = "replace"

            if _if_schema_exists == "append":
                logger.warning(
                    yellow(
                        f"{self._database}"
                        f".{target_schema}.{self._config.target_table} already exists and was not\n"
                        "recreated because 'destructive_create_table' is set to False in your profile \n"
                        "APPENDING instead."
                    )
                )
            try:
                df.to_sql(
                    name=self._config.target_table,
                    schema=target_schema,
                    con=self.con,
                    if_exists=_if_schema_exists,
                    index=False,
                    dtype=dtypes_dict,
                )
            except Exception as e:
                raise UploadError(str(e))
            finally:
                logger.debug("Closing connection")
                self.close_connection()

    def excecute_query(self, query: str, return_results: bool = False) -> Optional[Any]:
        self.acquire_connection()
        results: Any = self.con.execute(query)
        if return_results:
            results = results.fetchall()
            self.close_connection()
            return results
        self.close_connection()
        return None

    def check_table(self, target_schema: str, target_table: str) -> Tuple[int, int]:
        self.acquire_connection()
        _qualified_table_name = f"{self._database}.{target_schema}.{target_table}"
        try:
            inspector = Inspector.from_engine(self._engine)
            columns = inspector.get_columns(target_table, target_schema)
            metadata = MetaData(self.con)
            _target_table = sqlalchemy.Table(
                target_table, metadata, autoload=True, schema=target_schema
            )
            rows = select([func.count("*")], from_obj=[_target_table])
            row_results = rows.execute()
            num_rows = row_results.first()[0]
            num_columns = len(columns)

        except NoSuchTableError:
            raise TableDoesNotExist(f"Table {_qualified_table_name} does not exist.")
        finally:
            self.close_connection()

        logger.info(
            timed_message(
                green(
                    f"Push successful for {_qualified_table_name} \n"
                    f"Found {num_columns} columns and {num_rows} rows."
                )
            )
        )
        return num_columns, num_rows
