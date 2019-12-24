import os

import mock
import pytest

from sheetload.config import ConfigLoader
from sheetload.flags import FlagParser

from .mockers import DIRTY_DF, RENAMED_COLS, RENAMED_DF, generate_test_df

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_rename_columns(datafiles):
    from sheetload.sheetload import SheetBag

    flags = FlagParser()
    config = ConfigLoader(flags, yml_folder=str(datafiles))
    df = generate_test_df(DIRTY_DF)
    renamed_df = SheetBag(config, flags).rename_columns(df)

    assert renamed_df.columns.tolist() == RENAMED_COLS


@pytest.mark.datafiles(FIXTURE_DIR)
def test_load_sheet(datafiles):
    from sheetload.sheetload import SheetBag

    flags = FlagParser()
    config = ConfigLoader(flags, yml_folder=str(datafiles))
    with mock.patch.object(
        SheetBag, "_obtain_googlesheet", return_value=generate_test_df(DIRTY_DF)
    ):
        sheetbag = SheetBag(config, flags)
        sheetbag.load_sheet()
        target_df = generate_test_df(RENAMED_DF)
        assert target_df.equals(sheetbag.sheet_df)
