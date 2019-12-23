from .mockers import CLEAN_DF, RENAMED_COLS, DIRTY_DF, RENAMED_DF, generate_test_df
import mock


def test_rename_columns():
    from sheetload.sheetload import SheetBag

    df = generate_test_df(DIRTY_DF)
    renamed_df = SheetBag(test=True).rename_columns(df)

    assert renamed_df.columns.tolist() == RENAMED_COLS


def test_load_sheet():
    from sheetload.sheetload import SheetBag

    with mock.patch.object(
        SheetBag, "_obtain_googlesheet", return_value=generate_test_df(DIRTY_DF)
    ):
        sheetbag = SheetBag(test=True)
        sheetbag.load_sheet()
        target_df = generate_test_df(RENAMED_DF)
        assert target_df.equals(sheetbag.sheet_df)
