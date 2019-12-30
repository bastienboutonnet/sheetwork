import os

import mock
import pytest

from core.config.config import ConfigLoader
from core.config.profile import Profile
from core.flags import FlagParser
from tests.mockers import (
    DIRTY_DF,
    DROP_COL_DF,
    EXCLUDED_DF_COLS,
    RENAMED_COLS,
    RENAMED_DF,
    generate_test_df,
)

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_rename_columns(datafiles):
    from core.sheetload import SheetBag
    from core.main import parser

    flags = FlagParser(parser, test_sheet_name="df_renamer")
    config = ConfigLoader(flags, yml_folder=str(datafiles))
    profile = Profile("sheetload_test", "dev")
    df = generate_test_df(DIRTY_DF)
    renamed_df = SheetBag(config, flags, profile).rename_columns(df)

    assert renamed_df.columns.tolist() == RENAMED_COLS


@pytest.mark.datafiles(FIXTURE_DIR)
def test_exclude_columns(datafiles):
    from core.sheetload import SheetBag
    from core.main import parser

    flags = FlagParser(parser, test_sheet_name="df_dropper")
    config = ConfigLoader(flags, yml_folder=str(datafiles))
    profile = Profile("sheetload_test", "dev")
    df = generate_test_df(DROP_COL_DF)
    excluded_df = SheetBag(config, flags, profile).exclude_columns(df)

    assert excluded_df.columns.tolist() == EXCLUDED_DF_COLS


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_sheet(datafiles):
    from core.sheetload import SheetBag
    from core.main import parser

    flags = FlagParser(parser, test_sheet_name="df_renamer")
    config = ConfigLoader(flags, yml_folder=str(datafiles))
    profile = Profile("sheetload_test", "dev")
    with mock.patch.object(
        SheetBag, "_obtain_googlesheet", return_value=generate_test_df(DIRTY_DF)
    ):
        sheetbag = SheetBag(config, flags, profile)
        sheetbag.load_sheet()
        target_df = generate_test_df(RENAMED_DF)
        assert target_df.equals(sheetbag.sheet_df)
