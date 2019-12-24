import logging
import sys

import pandas
from data_tools.db import odbc
from data_tools.db.pandas import push_pandas_to_snowflake
from data_tools.google.sheets import Spreadsheet

from sheetload._version import __version__
from sheetload.cleaner import SheetCleaner
from sheetload.config import ConfigLoader
from sheetload.exceptions import ColumnNotFoundInDataFrame, external_errors_to_catch
from sheetload.flags import FlagParser, logger


class SheetBag:
    def __init__(self, config: ConfigLoader, flags: FlagParser):
        self.sheet_df: pandas.DataFrame = pandas.DataFrame()
        self.flags: FlagParser = flags
        self.config: ConfigLoader = config
        self.target_schema: str = str()
        self.consume_config()

    def consume_config(self):
        """Sets up overriding of config when needed.
        """
        logger.info("Reading configuration...")

        # overrides target schema
        if self.flags.mode == "dev" and not self.flags.force:
            self.target_schema = "sand"

        logger.info(
            f"Running in {self.flags.mode.upper()} mode."
            f"Log level: {self.flags.log_level.upper()}. Writing to: {self.target_schema.upper()}"
        )

    def _obtain_googlesheet(self):
        df = Spreadsheet(self.config.sheet_key).worksheet_to_df()
        return df

    def load_sheet(self):
        """Loads a google sheet, and calls clean up steps if applicable.
        Sheet must have been shared with account admin email address used in storage.

        Raises:
            TypeError: When loader does not return results that can be converted into a pandas
            DataFrame a type error will be raised.
        """

        logger.info(f"Importing data from {self.config.sheet_key}")
        df = self._obtain_googlesheet()
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("import_sheet did not return a pandas DataFrame")
        logger.debug(f"Loaded DF Cols: {df.columns.tolist()}")
        df = self.rename_columns(df)
        df = self.run_cleanup(df)
        logger.debug(f"Cols should be: {df.columns}")
        self.sheet_df = df

    def rename_columns(self, df):
        if self.config.sheet_column_rename_dict:
            for column in self.config.sheet_column_rename_dict.keys():
                if column not in df.columns:
                    raise ColumnNotFoundInDataFrame(
                        f"The column: '{column}' was not found in the sheet, make sure you spelled "
                        "it correctly in 'identifier' field. If it contains special chars you "
                        "should wrap it between double quotes."
                    )
            df = df.rename(columns=self.config.sheet_column_rename_dict)
        return df

    @staticmethod
    def _collect_and_check_answer():
        acceptable_answers = ["y", "n", "a"]
        user_input = str()
        while user_input not in acceptable_answers:
            if user_input is not None:
                logger.info(
                    "Your response cannot be interpreted.Choose 'y':yes, 'n':no, 'a':abort'"
                )
            user_input = input("Would you like to perform cleanup? (y/n/a): ")
        if user_input.lower() == "y":
            return True
        if user_input.lower() == "n":
            return False
        if user_input.lower() == "a":
            logger.info("User aborted.")
            sys.exit(1)

    @staticmethod
    def _show_dry_run_preview(sheet_df):

        print("\nDataFrame DataTypes: \n\n" + str(sheet_df.dtypes))
        print("\nDataFrame Preview: \n\n" + str(sheet_df.head(10)))

    def run_cleanup(self, df):
        clean_up = True
        # check for interactive mode
        if self.flags.interactive:
            logger.info("PRE-CLEANING PREVIEW: This is what you would push to the database.")
            self._show_dry_run_preview(df)
            clean_up = self._collect_and_check_answer()

        if clean_up is True:
            logger.info("Housekeeping...")
            clean_df = SheetCleaner(df).cleanup()
            if self.flags.dry_run or self.flags.interactive:
                logger.info("POST-CLEANING PREVIEW: This is what you would push to the database:")
                self._show_dry_run_preview(clean_df)

            return clean_df
        return df

    def _check_table(self):
        columns_query = f"""
                        select count(*)
                        from dwh.information_schema.columns
                        where table_catalog = 'DWH'
                        and table_schema = '{self.target_schema.upper()}'
                        and table_name = '{self.config.target_table.upper()}'
                        ;
                        """
        rows_query = f"select count(*) from {self.target_schema}.{self.config.target_table}"
        columns = odbc.run_query(odbc.SNOWFLAKE_DSN, columns_query)
        rows = odbc.run_query(odbc.SNOWFLAKE_DSN, rows_query)
        return columns[0][0], rows[0][0]

    def push_sheet(self):
        if not self.flags.dry_run:
            logger.info("Pushing sheet to Snowflake...")
            logger.debug(f"Column override dict is a {type(self.config.sheet_columns)}")
            try:
                logger.debug(f"Sheet Columns: {self.config.sheet_columns}")
                logger.debug(f"Df col list: {self.sheet_df.columns.tolist()}")
                push_pandas_to_snowflake(
                    self.sheet_df,
                    self.target_schema,
                    self.config.target_table,
                    create=self.flags.create_table,
                    overwrite_defaults=self.config.sheet_columns,
                )
            except ValueError as e:
                if str(e) == external_errors_to_catch["overwrite_cols_data_tools_error"]:
                    logging.error(
                        """
                        Column names in df to be imported seem to differ from the ones provided in
                        your config. You can check the data frame you're about to upload by doing a
                        dry run (--dry_run) or using the interactive (--i) mode. This is often due to
                        cleaning steps that have been skipped.
                        """
                    )
                    logger.warning("Push aborted.")
                else:
                    logging.error(e)
                sys.exit(1)
            try:
                logger.info("Checking table existence...")
                columns, rows = self._check_table()
            except Exception as e:
                raise RuntimeError(e)
            logger.info(
                f"Push successful for"
                f"{self.target_schema.upper()}.{self.config.target_table.upper()}.\n"
                f"Columns: {columns}, Rows: {rows}."
            )
        else:
            logger.info("Nothing pushed since you were in --dry_run mode.")


def run():
    print(f"Sheetload version: {__version__} \n")
    flags = FlagParser()
    flags.consume_cli_arguments()
    config = ConfigLoader(flags)
    sheetbag = SheetBag(config, flags)
    sheetbag.load_sheet()
    sheetbag.push_sheet()


if __name__ == "__main__":
    run()
