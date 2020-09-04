import tempfile
from typing import TYPE_CHECKING

import pandas
from sqlalchemy.types import BOOLEAN, DATE, INTEGER, TIMESTAMP, VARCHAR, Numeric

from core.config.config import ConfigLoader
from core.exceptions import DatabaseError, TableDoesNotExist
from core.logger import GLOBAL_LOGGER as logger
from core.ui.printer import green, timed_message

if TYPE_CHECKING:
    from core.adapters.connection import Connection


class SnowflakeAdapter:
    """Interacts with snowflake via SQLAlchemy"""

    def __init__(self, connection: "Connection", config: ConfigLoader):
        self.connection = connection
        self.engine = connection.engine
        self.config = config

    def acquire_connection(self):
        self.con = self.engine.connect()

    def close_connection(self):
        self.con.close()

    @staticmethod
    def sqlalchemy_dtypes(dtypes_dict) -> dict:
        dtypes_dict = dtypes_dict.copy()
        dtypes_map = dict(
            varchar=VARCHAR,
            int=INTEGER,
            numeric=Numeric(38, 18),
            boolean=BOOLEAN,
            timestamp_ntz=TIMESTAMP,
            date=DATE,
        )

        for col, data_type in dtypes_dict.items():
            dtypes_dict.update({col: dtypes_map[data_type]})
        return dtypes_dict

    def upload(self, df: pandas.DataFrame, override_schema: str = str()):
        # cast columns
        # ! temporarily deactivatiing df casting in pandas related to #205 & #204
        dtypes_dict = self.sqlalchemy_dtypes(self.config.sheet_columns)

        # potenfially override target schema from config.
        if override_schema:
            schema = override_schema
        else:
            schema = self.config.target_schema

        # write to csv and try to talk to db
        temp = tempfile.NamedTemporaryFile()
        df.to_csv(temp.name, index=False, header=False, sep="|")

        try:
            self.acquire_connection()
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
            raise DatabaseError(e)
        finally:
            temp.close()
            self.close_connection()

    def execute(self, query: str, return_results: bool = False):
        self.acquire_connection()
        results = self.con.execute(query)
        if return_results:
            result_set = results.fetchall()
            self.close_connection()
            return result_set
        self.close_connection()
        return None

    def check_table(self, target_schema: str, target_table: str):
        columns_query = f"""
                select count(*)
                from dwh.information_schema.columns
                where table_catalog = 'DWH'
                and table_schema = '{target_schema.upper()}'
                and table_name = '{target_table.upper()}'
                ;
                """
        rows_query = rows_query = f"select count(*) from {target_schema}.{target_table}"
        columns = self.execute(columns_query, return_results=True)
        rows = self.execute(rows_query, return_results=True)
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
