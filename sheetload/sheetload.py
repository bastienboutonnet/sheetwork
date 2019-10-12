import logging
import sys

import pandas
from data_tools.db import odbc
from data_tools.db.pandas import push_pandas_to_snowflake
from data_tools.google.sheets import Spreadsheet
from data_tools.logging import LoggerFactory

from sheetload.flags import args

SHEET_NAME = None
CREATE_TABLE = None
TARGET_SCHEMA = None
TARGET_TABLE = None

# set up logger levels
if args.log_level in {"debug", "warning", "info", "error"}:
    logger = LoggerFactory.get_logger(level=getattr(logging, args.log_level.upper()))
if args.mode == "dev":
    args.log_level = "debug"
    logger = LoggerFactory.get_logger(level=getattr(logging, "debug".upper()))
else:
    raise NotImplementedError("This level is not supported.")


def set_flags_from_args(flags):
    """SChecks arguments and sets flags

    Args:
        flags (argparse arguments): Arguments class from argparse
    """

    global SHEET_NAME, CREATE_TABLE, TARGET_SCHEMA, TARGET_TABLE
    CREATE_TABLE = flags.create_table
    if flags.sheet_key:
        SHEET_NAME = flags.sheet_key
        if not flags.schema or not flags.table:
            raise NotImplementedError(
                """
                No target schema and or target was provided.
                You must provide one when reading not from config."
                """
            )
    if not flags.sheet_key and not flags.sheet_name:
        raise NotImplementedError(
            """
            No sheet selected for import. Provide a sheet_key or a sheet_name.
            See help, for hints."""
        )


class SheetBag:
    def __init__(self):
        self.sheet_name = SHEET_NAME
        self.sheet_key = None
        self.target_schema = None
        self.target_table = None
        self.create_table = False
        self.sheet_df = None
        self.parse_config()

    def parse_config(self):
        logger.info("Parsing configuration...")
        self.target_schema = args.schema

        # override target schema for dev.
        if args.mode == "dev" and not args.force:
            self.target_schema = "sand"

        self.target_table = "bb_sheetload_test"
        self.create_table = True

        if SHEET_NAME:
            self.sheet_key = SHEET_NAME
        else:
            self.sheet_key = "Unknown"
        logger.info(self.sheet_key)
        logger.info(
            f"Running in {args.mode.upper()} mode."
            f"Log level: {args.log_level.upper()}. Writing to: {self.target_schema.upper()}"
        )

    @staticmethod
    def check_answer(user_input):
        acceptable_answers = ["y", "n", "a"]
        if user_input in acceptable_answers:
            if user_input.lower() == "y":
                return True
            if user_input.lower() == "n":
                return False
            if user_input.lower() == "a":
                logger.info("User aborted.")
                sys.exit(1)
        raise NotImplementedError(
            "Your response cannot be interpreted. Choose 'y':yes, 'n':no, 'a':abort"
        )

    def load_sheet(self):
        """Loads a google sheet, and calls clean up steps if applicable.
        Sheet must have been shared with account admin email address used in storage.

        Raises:
            TypeError: When loader does not return results that can be converted into a pandas
            DataFrame a type error will be raised.
        """

        logger.info(f"Importing data from {self.sheet_key}")
        df = Spreadsheet(self.sheet_key).worksheet_to_df()
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("import_sheet did not return a pandas DataFrame")
        df = self.cleanup(df)
        self.sheet_df = df

    def cleanup(self, df):
        clean_up = True
        # check for interactive mode
        if args.i:
            logger.info("PRE-CLEANING PREVIEW: This is what you would push to the database.")
            self._show_dry_run_preview(df)
            clean_up_answer = input("Would you like to perform cleanup? (y/n/a): ")
            clean_up = self.check_answer(clean_up_answer)

        if clean_up is True:
            logger.info("Housekeeping...")
            # clean column names (slashes and spaces to understore), remove trailing whitespace
            df.columns = [col.replace(" ", "_").replace("/", "_").strip() for col in df.columns]
            # remove empty cols
            if "" in df.columns:
                df = df.drop([""], axis=1)

            # clean trailing spaces in fields
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].str.strip()
            clean_df = df
            if args.dry_run or args.i:
                logger.info("This is what you would push to the database:")
            self._show_dry_run_preview(clean_df)

            return clean_df

    @staticmethod
    def _show_dry_run_preview(sheet_df):
        logger.info("\nDataFrame DataTypes: \n\n" + str(sheet_df.dtypes))
        logger.info("\nDataFrame Preview: \n\n" + str(sheet_df.head(10)))

    def _check_table(self):
        columns_query = f"""
                        select count(*)
                        from dwh.information_schema.columns
                        where table_catalog = 'DWH'
                        and table_schema = '{self.target_schema.upper()}'
                        and table_name = '{self.target_table.upper()}'
                        ;
                        """
        rows_query = f"select count(*) from {self.target_schema}.{self.target_table}"
        columns = odbc.run_query(odbc.SNOWFLAKE_DSN, columns_query)
        rows = odbc.run_query(odbc.SNOWFLAKE_DSN, rows_query)
        return columns[0][0], rows[0][0]

    def push_sheet(self):
        if not args.dry_run:
            logger.info("Pushing sheet to Snowflake...")
            push_pandas_to_snowflake(
                self.sheet_df, self.target_schema, self.target_table, create=self.create_table
            )
            try:
                logger.info("Checking table existance...")
                columns, rows = self._check_table()
            except Exception as e:
                raise RuntimeError(e)
            logger.info(f"Push successful. Columns {columns}, Rows: {rows}")


def run():
    set_flags_from_args(args)
    sheetbag = SheetBag()
    sheetbag.load_sheet()
    sheetbag.push_sheet()


if __name__ == "__main__":
    run()
