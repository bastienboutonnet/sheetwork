import tempfile
from typing import TYPE_CHECKING

import pandas
from sqlalchemy.types import BOOLEAN, INTEGER, TIMESTAMP, VARCHAR, Numeric

from core.config.config import ConfigLoader
from core.exceptions import ColumnNotFoundInDataFrame, DatabaseError, UnsupportedDataTypeError
from core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from core.adapters.connection import Connection


class SnowflakeAdapter:
    """Interacts with snowflake via SQLAlchemy
    """

    def __init__(self, connection: "Connection", config: ConfigLoader):
        self.connection = connection
        self.engine = connection.engine
        self.config = config

    def acquire_connection(self):
        self.con = self.engine.connect()

    def close_connection(self):
        self.con.close()

    def cast_dtypes(self, df: pandas.DataFrame, overwrite_dict: dict = dict()) -> pandas.DataFrame:
        overwrite_dict = overwrite_dict.copy()
        dtypes_map = dict(
            varchar="object",
            int="int64",
            numeric="float64",
            boolean="bool",
            timestamp_ntz="datetime64[ns]",
        )

        # Check for type support
        unsupported_dtypes = set(overwrite_dict.values()).difference(dtypes_map.keys())
        if unsupported_dtypes:
            raise UnsupportedDataTypeError(
                f"{unsupported_dtypes} are currently not supported for {self.connection.db_type}"
            )

        # check overwrite col is in df
        invalid_columns = set(overwrite_dict.keys()).difference(set(df.columns.tolist()))
        if invalid_columns:
            raise ColumnNotFoundInDataFrame(f"{invalid_columns} not in DataFrame. Check spelling?")

        # recode dict in pandas terms
        for col, data_type in overwrite_dict.items():
            overwrite_dict.update({col: dtypes_map[data_type]})

        # cast
        df = df.astype(overwrite_dict)
        logger.debug(f"Head of cast DF:\n {df.head()}")
        return df

    def sqlalchemy_dtypes(self, dtypes_dict) -> dict:
        dtypes_dict = dtypes_dict.copy()
        dtypes_map = dict(
            varchar=VARCHAR,
            int=INTEGER,
            numeric=Numeric(38, 18),
            boolean=BOOLEAN,
            timestamp_ntz=TIMESTAMP,
        )

        for col, data_type in dtypes_dict.items():
            dtypes_dict.update({col: dtypes_map[data_type]})
        return dtypes_dict

    def upload(self, df: pandas.DataFrame, override_schema: str = str()):
        # cast columns
        df = self.cast_dtypes(df, overwrite_dict=self.config.sheet_columns)
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
