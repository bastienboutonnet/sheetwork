import logging

from pathlib import Path
from typing import Tuple

import pytest

FIXTURE_DIR = Path(__file__).resolve().parent

logger = logging.getLogger("testing logger")


@pytest.mark.datafiles(FIXTURE_DIR)
def test__override_gspread_default_creds(datafiles, monkeypatch):
    import gspread

    from sheetwork.core.clients.google import GoogleSpreadsheet
    from sheetwork.core.config.profile import Profile
    from sheetwork.core.config.project import Project
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser

    # mock check for credentials so that we don't have to have a creds file in GH actions
    def mock__check_google_creds_exist(self) -> Tuple[bool, Path]:
        return True, Path("dummy")

    monkeypatch.setattr(
        GoogleSpreadsheet, "_check_google_creds_exist", mock__check_google_creds_exist
    )

    # Patch gspread functions so they don't attempt to do stuff
    def mock_load_credentials(self) -> None:
        # noop
        pass

    def mock_store_credentials(self) -> None:
        # noop
        pass

    monkeypatch.setattr(gspread.auth, "load_credentials", mock_load_credentials)
    monkeypatch.setattr(gspread.auth, "store_credentials", mock_store_credentials)

    flags = FlagParser(parser, project_dir=str(datafiles), profile_dir=str(datafiles))
    project = Project(flags)
    profile = Profile(project, "end_user")
    gsheet = GoogleSpreadsheet(profile)

    # testing this also because who knows these might become deprecated
    assert hasattr(gspread.auth, "DEFAULT_CONFIG_DIR")
    assert hasattr(gspread.auth, "DEFAULT_CREDENTIALS_FILENAME")
    assert hasattr(gspread.auth, "DEFAULT_AUTHORIZED_USER_FILENAME")
    assert hasattr(gspread.auth, "DEFAULT_SERVICE_ACCOUNT_FILENAME")

    # now make the replacements
    gsheet._override_gspread_default_creds()
    # dry_run=True)
    g_creds_dir = profile.google_credentials_dir

    project_name = "sheetwork_test"
    assert gspread.auth.DEFAULT_CONFIG_DIR == g_creds_dir
    assert gspread.auth.DEFAULT_CREDENTIALS_FILENAME == g_creds_dir.joinpath(f"{project_name}.json")
    assert gspread.auth.DEFAULT_AUTHORIZED_USER_FILENAME == g_creds_dir.joinpath(
        f"{project_name}_authorised_user.json"
    )
    assert gspread.auth.DEFAULT_SERVICE_ACCOUNT_FILENAME == g_creds_dir.joinpath(
        f"{project_name}_service_account.json"
    )
