import tempfile
from typing import Any, Optional

import pandas

# ! temporarily deactivatiing df casting in pandas related to #205 & #204
from sheetwork.core.utils import cast_pandas_dtypes
from sheetwork.core.adapters.base.impl import BaseSQLAdapter
from sheetwork.core.adapters.connection import SnowflakeConnection
from sheetwork.core.config.config import ConfigLoader
from sheetwork.core.exceptions import DatabaseError, TableDoesNotExist
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import green, timed_message, red


class SnowflakeAdapter(BaseSQLAdapter):
    """Interacts with snowflake via SQLAlchemy"""

    def __init__(self, connection: SnowflakeConnection, config: ConfigLoader):
        self.connection = connection
        self.engine = connection.engine
        self.config = config

    def acquire_connection(self) -> None:
        try:
            self.con = self.engine.connect()
        except Exception:
            raise DatabaseError(red(f"Error creating Snowflake connection."))

    def close_connection(self) -> None:
        try:
            self.con.close()
        except AttributeError:
            raise DatabaseError(
                red("SnowflakeAdaport did not create a connection so it cannot be closed")
            )

    def upload(self, df: pandas.DataFrame, override_schema: str = str()) -> None:
        # cast columns
        # !: note integer conversion doesn't actually happen it is left as a str see #204, #205
        df = cast_pandas_dtypes(df, overwrite_dict=self.config.sheet_columns)
        dtypes_dict = self.sqlalchemy_dtypes(self.config.sheet_columns)

        # potenfially override target schema from config.
        if override_schema:
            schema = override_schema
        else:
            schema = self.config.target_schema

        # write to csv and try to talk to db
        temp = tempfile.NamedTemporaryFile()
        df.to_csv(temp.name, index=False, header=False, sep="|")

        self.acquire_connection()
        try:
            df.head(0).to_sql(
                name=self.config.target_table,
                schema=schema,
                con=self.con,
                if_exists="replace",
                index=False,
                dtype=dtypes_dict,
            )

            qualified_table = f"{self.config.target_schema}.{self.config.target_table}"
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
                from dwh.information_schema.columns
                where table_catalog = 'DWH'
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
                        f"{target_schema}.{target_table} \n"
                        f"Found {columns[0][0]} columns and {rows[0][0]} rows."
                    )
                )
            )
        else:
            raise TableDoesNotExist(f"Table {target_schema}.{target_table} seems empty")
