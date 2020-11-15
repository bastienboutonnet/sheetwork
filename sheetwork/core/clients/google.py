from pathlib import Path
from typing import Any, List

import gspread
import pandas
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import (
    GoogleCredentialsFileMissingError,
    GoogleSpreadSheetNotFound,
    NoWorkbookLoadedError,
    WorksheetNotFoundError,
)
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import green
from sheetwork.core.utils import check_dupe_cols


class GoogleSpreadsheet:
    """Gets google cloud credentials checks client from profile and handles google sheet
    interactions such as downloading a sheet or other activities permitted by the gspread lib.

    Raises:
        GoogleCredentialsFileMissingError: When the credentials file cannot be located in the expect
        location.
        GoogleSpreadSheetNotFound: When the required google sheet cannot be found.

    Returns:
        GoogleSpreadsheet: GoogleSpreadsheet object and methods.
    """

    def __init__(self, profile: Profile, workbook_key: str = str(), workbook_name: str = str()):
        self._profile = profile
        self.is_service_account = profile.profile_dict.get("is_service_account", True)
        p = Path(profile.google_credentials_dir, profile.profile_name).with_suffix(".json")
        if p.exists():
            if self.is_service_account:
                logger.debug("Using SERVICE_ACCOUNT auth")
                self.gc = gspread.service_account(p)
            else:
                logger.debug("Using END_USER auth")
                # ! This override should be temporary ideally we'll have a more long term solution in:
                # ! https://github.com/burnash/gspread/issues/826
                self._override_gspread_default_creds()
                self.gc = gspread.oauth()
        else:
            raise GoogleCredentialsFileMissingError(
                "Sheetwork could not find a credentials file for your "
                f"'{profile.profile_name}' profile in the ~/.sheetwork/google/ folder. "
                "Check installation instructions if you do not know how to set this up."
            )
        self.workbook_key = workbook_key
        self.workbook_name = workbook_name
        self.client = profile.profile_dict.get("guser")
        self._open_workbook()

    def _override_gspread_default_creds(self) -> None:
        """Temporary workaround to allow `gspread.oauth()` to look for credentials in another location
        than defaults. For more info: https://github.com/burnash/gspread/issues/826
        This will likely be removed if work on gspread #826 gets carried out.
        """
        logger.debug(
            "Overriding `gspread`'s DEFAULT_AUTHORISED_USER_FILENAME and stuff. "
            "This is temporary (hopefully) see `GoogleSpreadsheet._override_gspread_default_creds()` "
            "docstring for more info."
        )
        logger.debug(
            f"Overriding to: {self._profile.google_credentials_dir}/{self._profile.profile_name}"
        )
        gspread.auth.DEFAULT_CONFIG_DIR = Path(self._profile.google_credentials_dir)

        gspread.auth.DEFAULT_CREDENTIALS_FILENAME = gspread.auth.DEFAULT_CONFIG_DIR.joinpath(
            self._profile.profile_name
        ).with_suffix(".json")

        gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME = gspread.auth.DEFAULT_CONFIG_DIR.joinpath(
            f"{self._profile.profile_name}_authorised_user"
        ).with_suffix(".json")

        gspread.auth.DEFAULT_SERVICE_ACCOUNT_FILENAME = gspread.auth.DEFAULT_CONFIG_DIR.joinpath(
            f"{self._profile.profile_name}_service_account"
        ).with_suffix(".json")

        gspread.auth.load_credentials.__defaults__ = (
            gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME,
        )

        gspread.auth.store_credentials.__defaults__ = (
            gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME,
            "token",
        )

    def _open_workbook(self):
        try:
            if self.workbook_key:
                self.workbook = self.gc.open_by_key(self.workbook_key)
            elif self.workbook_name:
                self.workbook = self.gc.open(self.workbook_name)

        except SpreadsheetNotFound:
            raise GoogleSpreadSheetNotFound(
                "Spreadsheet not found. You either have a typo in the key or name provided "
                f"or your client {self.client} does not have read access to the sheet."
            )

    def make_df_from_worksheet(
        self, worksheet_name: str = str(), grab_header: bool = True
    ) -> pandas.DataFrame:
        if not self.workbook:
            raise NoWorkbookLoadedError(
                "Workbook object seems empty, cannot turn a None object into a dataframe"
            )
        try:
            if worksheet_name:
                worksheet = self.workbook.worksheet(worksheet_name)
            else:
                worksheet_name = "default sheet"
                worksheet = self.workbook.get_worksheet(0)
            logger.debug(green("Sheet loaded successfully"))
            if grab_header:
                values: List[Any] = worksheet.get_all_values()
                check_dupe_cols(values[0])
                df = pandas.DataFrame(values[1:], columns=values[0])
            else:
                df = pandas.DataFrame(worksheet.get_all_values())
            return df
        except WorksheetNotFound:
            raise WorksheetNotFoundError(
                f"Could not find {worksheet_name} in workbook. "
                "If 'default sheet' not found all sheets in the workbook may be empty."
            )
