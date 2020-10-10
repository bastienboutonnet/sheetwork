import sys
from typing import List, Optional, Tuple, Union

import pandas

from sheetwork.core.adapters.base.connection import BaseConnection, BaseCredentials
from sheetwork.core.adapters.base.impl import BaseSQLAdapter
from sheetwork.core.adapters.factory import AdapterContainer
from sheetwork.core.cleaner import SheetCleaner
from sheetwork.core.clients.google import GoogleSpreadsheet
from sheetwork.core.config.config import ConfigLoader
from sheetwork.core.config.profile import Profile
from sheetwork.core.flags import FlagParser
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import red, timed_message, yellow
from sheetwork.core.utils import check_columns_in_df


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

    def __init__(self, config: ConfigLoader, flags: FlagParser, profile: Profile):
        self.sheet_df: pandas.DataFrame = pandas.DataFrame()
        self.flags = flags
        self.config = config
        self.target_schema = config.target_schema
        self.target_table = config.target_table
        self.profile = profile
        self.push_anyway = False
        self.sheet_key: str = str(config.sheet_config.get("sheet_key", str()))
        self.credentials_adapter: Optional[BaseCredentials] = None
        self.connection_adapter: Optional[BaseConnection] = None
        self.sql_adapter: Optional[BaseSQLAdapter] = None
        self.init_adapters()

    def init_adapters(self) -> None:
        adapter_container = self._get_adapter_modules()
        self.credentials_adapter = adapter_container.credentials_adapter(  # type:ignore
            self.profile
        )
        self.connection_adapter = adapter_container.connection_adapter(  # type:ignore
            self.credentials_adapter
        )
        self.sql_adapter = adapter_container.sql_adapter(  # type:ignore
            self.connection_adapter, self.config
        )

    def _get_adapter_modules(self) -> AdapterContainer:
        adapters = AdapterContainer()
        adapters.register_adapter(self.profile)
        adapters.load_plugins()
        return adapters

    def _obtain_googlesheet(self):
        worksheet = str(self.config.sheet_config.get("worksheet", str()))
        df = GoogleSpreadsheet(self.profile, self.sheet_key).make_df_from_worksheet(
            worksheet_name=worksheet
        )
        return df

    def load_sheet(self):
        """Loads a google sheet, and calls clean up steps if applicable.
        Sheet must have been shared with account admin email address used in storage.

        Raises:
            TypeError: When loader does not return results that can be converted into a pandas
            DataFrame a type error will be raised.
        """

        if self.flags.sheet_name:
            logger.info(timed_message(f"Importing: {self.flags.sheet_name}"))
            logger.debug(f"Importing data from: {self.config.sheet_config['sheet_key']}")
        else:
            logger.info(
                timed_message(f"Importing data from: {self.config.sheet_config.get('sheet_key')}")
            )
        df = self._obtain_googlesheet()
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("import_sheet did not return a pandas DataFrame")
        logger.debug(f"Columns imported from sheet: {df.columns.tolist()}")

        # Perform exclusions, renamings and cleanups before releasing the sheet.
        df = self.exclude_columns(df)
        df = self.rename_columns(df)
        self.push_anyway, df = self.run_cleanup(df)
        logger.debug(f"Columns after cleanups and exclusions: {df.columns}")
        self.sheet_df = df

    def rename_columns(self, df: pandas.DataFrame):
        if self.config.sheet_column_rename_dict:
            _, _ = check_columns_in_df(df, list(self.config.sheet_column_rename_dict.keys()))
            df = df.rename(columns=self.config.sheet_column_rename_dict)  # type: ignore
        return df

    def exclude_columns(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """Drops columns referred to by their identifier (the exact string in the google sheet) when
        a list is provided in the "excluded_columns" field of a sheet yml file.

        Args:
            df (pandas.DataFrame): DataFrame downloaded from google sheet.

        Returns:
            pandas.DataFrame: Either the same dataframe as originally provided or one with dropped
            columns as required.
        """

        cols_to_exclude: Union[str, List[str]] = self.config.sheet_config.get(  # type: ignore
            "excluded_columns", list(str())
        )
        if cols_to_exclude:
            _, filtered_columns = check_columns_in_df(df, cols_to_exclude, warn_only=True)
            if filtered_columns:
                df = df.drop(filtered_columns, axis=1)
            return df
        return df

    @staticmethod
    def _collect_and_check_answer(post_cleanup: bool = False):
        acceptable_answers = ["y", "n", "a"]
        user_input = str()
        while user_input not in acceptable_answers:
            if user_input is not None:
                logger.info("Choose 'y':yes, 'n':no, 'a':abort'")
            if post_cleanup:
                user_input = input("Would you like to push to db? (y/n):")
            else:
                user_input = input("Would you like to perform cleanup? (y/n/a): ")
        if user_input.lower() == "y":
            return True
        if user_input.lower() == "n":
            return False
        if user_input.lower() == "a":
            logger.info(red("User aborted."))
            sys.exit(1)

    @staticmethod
    def _show_dry_run_preview(sheet_df: pandas.DataFrame):

        print("\nDataFrame DataTypes: \n\n" + str(sheet_df.dtypes))
        print("\nDataFrame Header: \n\n" + str(sheet_df.head(10)))

    def run_cleanup(self, df: pandas.DataFrame) -> Tuple[bool, pandas.DataFrame]:
        clean_up = True
        # check for interactive mode
        if self.flags.interactive:
            logger.info(
                yellow(
                    "PRE-CLEANING PREVIEW: The DataFrame you would push to the database would look like this:"
                )
            )
            self._show_dry_run_preview(df)
            clean_up = self._collect_and_check_answer()

        if clean_up is True:
            logger.debug("Performing clean ups")
            clean_df = SheetCleaner(
                df, bool(self.config.sheet_config.get("snake_case_camel", False))
            ).cleanup()
            if self.flags.dry_run or self.flags.interactive:
                logger.info(yellow("\nPOST-CLEANING PREVIEW:"))
                self._show_dry_run_preview(clean_df)
                carry_on = self._collect_and_check_answer(post_cleanup=True)
                if not carry_on:
                    logger.info(timed_message(red("User Aborted.")))
                    sys.exit(1)
            return True, clean_df
        return True, df

    def push_sheet(self):
        logger.info(timed_message("Pushing sheet to database..."))
        logger.debug(f"Column override dict is a {type(self.config.sheet_columns)}")
        logger.debug(f"Sheet columns: {self.config.sheet_columns}")
        logger.debug(f"Columns in final df: {self.sheet_df.columns.tolist()}")
        self.sql_adapter.upload(self.sheet_df, self.target_schema)

    def check_table(self):
        self.sql_adapter.check_table(self.target_schema, self.target_table)

    def run(self):
        self.load_sheet()
        if self.push_anyway:
            self.push_sheet()
            self.check_table()
        else:
            logger.info(yellow("Nothing pushed since you were in --dry_run mode."))
