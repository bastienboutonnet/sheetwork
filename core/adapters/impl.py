from core.adapters.connection import Connection
from core.config.config import ConfigLoader
from core.exceptions import UnsupportedDataTypeError, ColumnNotFoundInDataFrame, DatabaseError
import tempfile
import pandas
from itertools import chain


class SnowflakeAdapter:
    """Interacts with snowflake via SQLAlchemy
    """

    def __init__(self, connection: Connection, config: ConfigLoader):
        self.connection = connection
        self.engine = connection.engine
        self.config = config

    def acquire_connection(self):
        self.con = self.engine.connect()

    def close_connection(self):
        self.con.close()

    # TODO: Check about making things TZ-less with Tedy.
    def cast_dtypes(self, df: pandas.DataFrame, overwrite_dict: dict = dict()) -> pandas.DataFrame:
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
        return df

    def upload(self, df: pandas.DataFrame):
        temp = tempfile.NamedTemporaryFile()
        df.to_csv(temp.name, index=False, header=False)

        try:
            self.acquire_connection()
            df.head(0).to_sql(
                name=self.config.target_table,
                schema=self.config.target_schema,
                con=self.con,
                if_exists="replace",
                index=False,
            )
            qualified_table = f"{self.config.target_schema}.{self.config.target_table}"
            self.con.execute(f"put file://{temp.name}* @%{self.config.target_table}")
            self.con.execute(f"copy into {qualified_table} from @%{self.config.target_table}")
        except Exception as e:
            raise DatabaseError(e)
        finally:
            temp.close()
            self.close_connection()

    def execute(self, query: str):
        self.acquire_connection()
        self.con.execute(query)
        self.close_connection()
