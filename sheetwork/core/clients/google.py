"""Houses classes and methods to help interacting with Google Spreasheet API. Uses `gspread` mainly."""
from pathlib import Path
from typing import Any, List, Tuple

import gspread
import pandas
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import (
    GoogleClientNotAuthenticatedError,
    GoogleCredentialsFileMissingError,
    GoogleSpreadSheetNotFound,
    NoWorkbookLoadedError,
    WorksheetNotFoundError,
)
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import green
from sheetwork.core.utils import check_dupe_cols


class GoogleSpreadsheet:
    """Takes care of the interaction with a Google Sheet like you've never seen before!

    Gets google cloud credentials checks client from profile and handles google sheet
    interactions such as downloading a sheet or other activities permitted by the gspread lib.

    Raises:
        GoogleCredentialsFileMissingError: When the credentials file cannot be located in the expect
        location.
        GoogleSpreadSheetNotFound: When the required google sheet cannot be found.

    Returns:
        GoogleSpreadsheet: GoogleSpreadsheet object and methods.
    """

    CREDS_EXT = ".json"

    def __init__(self, profile: Profile, workbook_key: str = str(), workbook_name: str = str()):
        """Constructor of GoogleSpreadsheet.

        Mainly just sets up auth.

        Args:
            profile (Profile): Initialised profile class containing parsed credentials and
                other goodness.
            workbook_key (str, optional): Unique google sheet key (found in URL). Defaults to str().
            workbook_name (str, optional): Name of the workbook in your drive. Defaults to str().
        """
        self._profile = profile
        self.is_service_account = profile.profile_dict.get("is_service_account", True)
        self.credential_file_exists, self.creds_path = self._check_google_creds_exist()
        self.workbook_key = workbook_key
        self.workbook_name = workbook_name
        self.client = profile.profile_dict.get("guser")
        self.is_authenticated: bool = False

    def _check_google_creds_exist(self) -> Tuple[bool, Path]:
        creds_path = Path(
            self._profile.google_credentials_dir, self._profile.profile_name
        ).with_suffix(self.CREDS_EXT)
        if creds_path.exists():
            return True, creds_path
        raise GoogleCredentialsFileMissingError(
            "Sheetwork could not find a credentials file for your "
            f"'{self._profile.profile_name}' profile in the {self._profile.profile_dir} folder. "
            "Check installation instructions if you do not know how to set this up."
        )

    def authenticate(self) -> None:
        if self.is_service_account:
            logger.debug("Using SERVICE_ACCOUNT auth")
            self.google_client = gspread.service_account(self.creds_path)
        else:
            logger.debug("Using END_USER auth")
            # ! This override should be temporary ideally we'll have a more long term solution in:
            # ! https://github.com/burnash/gspread/issues/826
            self._override_gspread_default_creds()
            self.google_client = gspread.oauth()
        self.is_authenticated = True

    def _override_gspread_default_creds(self) -> None:
        """Temporary workaround to allow `gspread.oauth()` to look for credentials in another location.

        For more info: https://github.com/burnash/gspread/issues/826
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
        ).with_suffix(self.CREDS_EXT)

        gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME = gspread.auth.DEFAULT_CONFIG_DIR.joinpath(
            f"{self._profile.profile_name}_authorised_user"
        ).with_suffix(self.CREDS_EXT)

        gspread.auth.DEFAULT_SERVICE_ACCOUNT_FILENAME = gspread.auth.DEFAULT_CONFIG_DIR.joinpath(
            f"{self._profile.profile_name}_service_account"
        ).with_suffix(self.CREDS_EXT)

        # doing this skipping for when I'm testing this function
        gspread.auth.load_credentials.__defaults__ = (
            gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME,
        )

        gspread.auth.store_credentials.__defaults__ = (
            gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME,
            "token",
        )

    def open_workbook(self):
        if self.is_authenticated:
            try:
                if self.workbook_key:
                    self.workbook = self.google_client.open_by_key(self.workbook_key)
                elif self.workbook_name:
                    self.workbook = self.google_client.open(self.workbook_name)

            except SpreadsheetNotFound:
                raise GoogleSpreadSheetNotFound(
                    "Spreadsheet not found. You either have a typo in the key or name provided "
                    f"or your client {self.client} does not have read access to the sheet."
                )
        else:
            raise GoogleClientNotAuthenticatedError(
                "You are not authenticated yet. Make sure you run `authenticate()` successfully"
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
