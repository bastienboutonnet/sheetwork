import logging
import sys

import pandas
from data_tools.db import odbc
from data_tools.db.pandas import push_pandas_to_snowflake
from data_tools.google.sheets import Spreadsheet

from sheetload.config import ConfigLoader
from sheetload.exceptions import external_errors_to_catch
from sheetload.flags import args, logger
from sheetload.yaml_helpers import validate_yaml


class SheetBag(ConfigLoader):
    def __init__(self):
        ConfigLoader.__init__(self)
        self.sheet_df = None
        self.consume_config()

    def consume_config(self):
        """Sets up overriding of config when needed.
        """
        logger.info("Reading configuration...")

        # overrides target schema
        if args.mode == "dev" and not args.force:
            self.target_schema = "sand"

        logger.info(
            f"Running in {args.mode.upper()} mode."
            f"Log level: {args.log_level.upper()}. Writing to: {self.target_schema.upper()}"
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

    @staticmethod
    def _collect_and_check_answer():
        acceptable_answers = ["y", "n", "a"]
        user_input = None
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

    def cleanup(self, df):
        clean_up = True
        # check for interactive mode
        if args.i:
            logger.info("PRE-CLEANING PREVIEW: This is what you would push to the database.")
            self._show_dry_run_preview(df)
            clean_up = self._collect_and_check_answer()

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

            try:
                push_pandas_to_snowflake(
                    self.sheet_df,
                    self.target_schema,
                    self.target_table,
                    create=self.create_table,
                    overwrite_defaults=self.sheet_columns,
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
                f"Push successful for {self.target_schema.upper()}.{self.target_table.upper()}.\n"
                f"Columns: {columns}, Rows: {rows}."
            )
        else:
            logger.info("Nothing pushed since you were in --dry_run mode.")


def run():
    validate_yaml()
    sheetbag = SheetBag()
    sheetbag.load_sheet()
    sheetbag.push_sheet()


if __name__ == "__main__":
    run()
