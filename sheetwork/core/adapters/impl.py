"""Module containing all Database Specific classes."""
import tempfile
from typing import Any, Optional

import pandas
from sqlalchemy.schema import CreateSchema

from sheetwork.core.adapters.base.impl import BaseSQLAdapter
from sheetwork.core.adapters.connection import SnowflakeConnection
from sheetwork.core.config.config import ConfigLoader
from sheetwork.core.exceptions import DatabaseError, NoAcquiredConnectionError, TableDoesNotExist
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import green, red, timed_message, yellow
from sheetwork.core.utils import cast_pandas_dtypes


class SnowflakeAdapter(BaseSQLAdapter):
    """Interacts with snowflake via SQLAlchemy."""

    def __init__(self, connection: SnowflakeConnection, config: ConfigLoader):
        """Contstructs the Snowflake DB Adaptor.

        Args:
            connection (SnowflakeConnection): connection object containing credentials and
                connection variables needed for Snowflake.
            config (ConfigLoader): configuration class containing all params for sheetwork general
                operation
        """
        self.connection = connection
        self.engine = connection.engine
        self.config = config
        self._database: str = self.connection.credentials.credentials.get("database", str())
        self._has_connection: bool = False

    def acquire_connection(self) -> None:
        try:
            self.con = self.engine.connect()
            self._has_connection = True
        except Exception:
            raise DatabaseError(red("Error creating Snowflake connection."))

    def close_connection(self) -> None:
        try:
            self.con.close()
            self._has_connection = False
        except AttributeError:
            raise DatabaseError(
                red("SnowflakeAdaptor did not create a connection so it cannot be closed")
            )

    def _create_schema(self) -> None:
        if self._has_connection is False:
            raise NoAcquiredConnectionError(
                f"No acquired connection for {type(self).__name__}. Make sure you call `acquire_connection` before."
            )
        try:
            if self.config.project.object_creation_dct["create_schema"]:
                schema_exists = (
                    True
                    if self.config.target_schema in self.con.dialect.get_schema_names(self.con)
                    else False
                )
                if schema_exists is False:
                    logger.debug(
                        yellow(f"Creating schema: {self.config.target_schema} in {self._database}")
                    )
                    self.con.execute(CreateSchema(self.config.target_schema))
        except Exception as e:
            raise DatabaseError(str(e))

    def upload(self, df: pandas.DataFrame, override_schema: str = str()) -> None:
        # cast columns
        # !: note integer conversion doesn't actually happen it is left as a str see #204, #205
        df = cast_pandas_dtypes(df, overwrite_dict=self.config.sheet_columns)
        dtypes_dict = self.sqlalchemy_dtypes(self.config.sheet_columns)

        # potentially override target schema from config.
        if override_schema:
            schema = override_schema
        else:
            schema = self.config.target_schema

        # write to csv and try to talk to db
        temp = tempfile.NamedTemporaryFile()
        df.to_csv(temp.name, index=False, header=False, sep="|")

        self.acquire_connection()

        # set up schema creation
        self._create_schema()

        try:
            # set the table creation behaviour
            _if_exists = "fail"
            if self.config.project.object_creation_dct["create_table"] is True:
                if self.config.project.destructive_create_table:
                    _if_exists = "replace"

                # perform the create ops
                try:
                    df.head(0).to_sql(
                        name=self.config.target_table,
                        schema=schema,
                        con=self.con,
                        if_exists=_if_exists,
                        index=False,
                        dtype=dtypes_dict,
                    )

                # if _if_exists is fail pandas will throw a ValueError which we want to escape when
                # destructive_create_table is set to False (or not provided) and throw a warning instead.
                except ValueError as e:
                    if _if_exists == "fail":
                        logger.warning(
                            yellow(
                                f"{self._database}"
                                f".{schema}.{self.config.target_table} already exists and was not\n"
                                "recreated because 'destructive_create_table' is set to False in your profile \n"
                                "APPENDING instead."
                            )
                        )
                    else:
                        raise DatabaseError(str(e))

            # Now push the actual data --the pandas create above is only for creation the logic below
            # is actually faster as pandas does it row by row
            qualified_table = (
                f"{self._database}.{self.config.target_schema}.{self.config.target_table}"
            )
            self.con.execute(
                f"""
                create or replace temporary stage {self.config.target_table}_stg
                file_format = (type = 'CSV' field_delimiter = '|'
                skip_header = 0 field_optionally_enclosed_by = '"')
                """
            )
            self.con.execute(f"put file://{temp.name} @{self.config.target_table}_stg")
            self.con.execute(f"copy into {qualified_table} from @{self.config.target_table}_stg")
            self.con.execute(f"drop stage {self.config.target_table}_stg")
        except Exception as e:
            raise DatabaseError(str(e))
        finally:
            logger.debug("CLOSING CONNECTION & CLEANING TMP FILE")
            temp.close()
            self.close_connection()

    def excecute_query(self, query: str, return_results: bool = False) -> Optional[Any]:
        self.acquire_connection()
        results: Any = self.con.execute(query)
        if return_results:
            result_set: Any = results.fetchall()
            self.close_connection()
            return result_set
        self.close_connection()
        return None

    def check_table(self, target_schema: str, target_table: str) -> None:
        columns_query = f"""
                select count(*)
                from {self._database}.information_schema.columns
                where table_catalog = '{self._database.upper()}'
                and table_schema = '{target_schema.upper()}'
                and table_name = '{target_table.upper()}'
                ;
                """
        rows_query = rows_query = f"select count(*) from {target_schema}.{target_table}"
        columns = self.excecute_query(columns_query, return_results=True)
        rows = self.excecute_query(rows_query, return_results=True)
        if columns and rows:
            logger.info(
                timed_message(
                    green(
                        f"Push successful for "
                        f"{self._database}.{target_schema}.{target_table} \n"
                        f"Found {columns[0][0]} columns and {rows[0][0]} rows."
                    )
                )
            )
        else:
            raise TableDoesNotExist(
                f"Table {self._database}.{target_schema}.{target_table} seems empty"
            )
