import argparse
import logging

import pandas
from data_tools.db.pandas import push_pandas_to_snowflake
from data_tools.google.sheets import Spreadsheet
from data_tools.logging import LoggerFactory

parser = argparse.ArgumentParser()
parser.add_argument("--log_level", help="sets the log level", type=str, default="info")
parser.add_argument("--sheet_name", help="Name of your sheet from config", type=str, default=None)
parser.add_argument("--sheet_key", help="Google sheet Key", type=str, default=None)
parser.add_argument("--schema", help="Target Schema Name", type=str, default=None)
parser.add_argument("--table", help="Target Table Name", type=str, default=None)
parser.add_argument("--create_table", action="store_true", default=False)
args = parser.parse_args()

SHEET_NAME = None
CREATE_TABLE = None
TARGET_SCHEMA = None
TARGET_TABLE = None

# set up logger levels
if args.log_level in {"debug", "warning", "info", "error"}:
    logger = LoggerFactory.get_logger(level=getattr(logging, args.log_level.upper()))
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
            "No sheet selected for import. Provide a sheet_key or a sheet_name. See help, for hints."
        )


class SheetBag:
    def __init__(self):
        self.sheet_name = SHEET_NAME
        self.sheet_key = None
        self.target_schema = None
        self.target_table = None
        self.create_table = False
        self.sheet_df = None
        self.parse_yaml()

    def parse_yaml(self):
        logger.info("Parsing yml")
        self.target_schema = "sand"
        self.target_table = "bb_sheetload_test"
        self.create_table = True
        logger.info(SHEET_NAME)
        if SHEET_NAME:
            self.sheet_key = SHEET_NAME
        else:
            self.sheet_key = "Unknown"
        logger.info(self.sheet_key)

    def load_sheet(self):
        logger.info(f"Importing data from {self.sheet_key}")
        df = Spreadsheet(self.sheet_key).worksheet_to_df()
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("import_sheet did not return a pandas DataFrame")
        self.sheet_df = df

    @staticmethod
    def cleanup(sheet_df):
        logging.info("Housekeeping...")
        pass

    def push_sheet(self):
        push_pandas_to_snowflake(
            self.sheet_df, self.target_schema, self.target_table, create=self.create_table
        )


def run():
    set_flags_from_args(args)
    sheetbag = SheetBag()
    sheetbag.load_sheet()
    sheetbag.push_sheet()


if __name__ == "__main__":
    run()
