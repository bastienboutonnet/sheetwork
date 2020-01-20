import logging
import sys
from typing import TYPE_CHECKING, Tuple

import pandas

from core.adapters.connection import Connection, Credentials
from core.adapters.impl import SnowflakeAdapter
from core.cleaner import SheetCleaner
from core.clients.google import GoogleSpreadsheet
from core.config.config import ConfigLoader
from core.config.profile import Profile
from core.exceptions import ColumnNotFoundInDataFrame, TableDoesNotExist
from core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from core.flags import FlagParser


class SheetBag:
    """Main object orchestrates sheet loading, cleaning, and db pushing by calling the relevant
    submodules.

    Raises:
        TypeError: [description]
        ColumnNotFoundInDataFrame: If a column on which a rename or casting is asked for cannot be
        found in the DataFrame resulting from the obtained sheet.
        RuntimeError: [description]

    Returns:
        SheetBag: Loaded, and possibly cleaned sheet object with db interaction methods.
    """

    def __init__(self, config: "ConfigLoader", flags: "FlagParser", profile: "Profile"):
        self.sheet_df: pandas.DataFrame = pandas.DataFrame()
        self.flags = flags
        self.config = config
        self.target_schema: str = str()
        self.profile = profile
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
        worksheet = self.config.sheet_config.get("worksheet", str())
        df = GoogleSpreadsheet(
            self.profile, self.config.sheet_config["sheet_key"]
        ).make_df_from_worksheet(worksheet_name=worksheet)
        return df

    def load_sheet(self):
        """Loads a google sheet, and calls clean up steps if applicable.
        Sheet must have been shared with account admin email address used in storage.

        Raises:
            TypeError: When loader does not return results that can be converted into a pandas
            DataFrame a type error will be raised.
        """

        logger.info(f"Importing data from {self.config.sheet_config['sheet_key']}")
        df = self._obtain_googlesheet()
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("import_sheet did not return a pandas DataFrame")
        logger.debug(f"Loaded DF Cols: {df.columns.tolist()}")

        # Perform exclusions, renamings and cleanups before releasing the sheet.
        df = self.exclude_columns(df)
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

    def exclude_columns(self, df) -> pandas.DataFrame:
        """Drops columns referred to by their identifier (the exact string in the google sheet) when
        a list is provided in the "excluded_columns" field of a sheet yml file.

        Args:
            df (pandas.DataFrame): DataFrame downloaded from google sheet.

        Returns:
            pandas.DataFrame: Either the same dataframe as originally provided or one with dropped
            columns as required.
        """

        if self.config.sheet_config.get("excluded_columns", str()):
            df = df.drop(self.config.sheet_config["excluded_columns"], axis=1)
            return df
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

    def push_sheet(self):
        logger.info("Pushing sheet to Snowflake...")
        logger.debug(f"Column override dict is a {type(self.config.sheet_columns)}")
        logger.debug(f"Sheet Columns: {self.config.sheet_columns}")
        logger.debug(f"Df col list: {self.sheet_df.columns.tolist()}")
        credentials = Credentials(self.profile)
        connection = Connection(credentials)
        adapter = SnowflakeAdapter(connection, self.config)
        adapter.upload(self.sheet_df, self.target_schema)

    def check_table(self):
        credentials = Credentials(self.profile)
        connection = Connection(credentials)
        adapter = SnowflakeAdapter(connection, self.config)
        columns_query = f"""
                select count(*)
                from dwh.information_schema.columns
                where table_catalog = 'DWH'
                and table_schema = '{self.target_schema.upper()}'
                and table_name = '{self.config.sheet_config['target_table'].upper()}'
                ;
                """
        rows_query = (
            f"select count(*) from {self.target_schema}.{self.config.sheet_config['target_table']}"
        )
        columns = adapter.execute(columns_query, return_results=True)
        rows = adapter.execute(rows_query, return_results=True)
        if columns and rows:
            logger.info(
                f"Push successful for "
                f"{self.target_schema}.{self.config.sheet_config['target_table']}"
                f"\nColumns: {columns[0][0]}, Rows: {rows[0][0]}."
            )
        else:
            raise TableDoesNotExist(
                f"Table {self.target_schema}.{self.config.sheet_config['target_table']} seems empty"
            )

    def run(self):
        self.load_sheet()
        if not self.flags.dry_run:
            self.push_sheet_adaptor()
            self.check_table_adaptor()
        else:
            logger.info("Nothing pushed since you were in --dry_run mode.")
