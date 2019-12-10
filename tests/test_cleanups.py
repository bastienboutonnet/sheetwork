import pandas

DIRTY_DF = {
    "col_a": [1, 2, 32],
    "col b": ["as .    ", "b", "   c"],
    "1. col_one": ["aa", "bb", "cc"],
    "": ["q", "q", "q"],
}

CLEAN_DF = {
    "col_a": {0: 1, 1: 2, 2: 32},
    "col_b": {0: "as .", 1: "b", 2: "c"},
    "col_one": {0: "aa", 1: "bb", 2: "cc"},
}

RENAME_CANDIDATE = dict(DIRTY_DF, **{"long ass name": ["foo", "bar", "fizz"]})
RENAMED_COLS = ["col_a", "col b", "1. col_one", "", "renamed_col"]


def generate_test_df(df):
    test_df = pandas.DataFrame.from_dict(df)
    return test_df


def test_cleanup():
    from sheetload.cleaner import SheetCleaner

    dirty_df = generate_test_df(DIRTY_DF)
    clean_df = SheetCleaner(dirty_df).cleanup()
    expected_df = generate_test_df(CLEAN_DF)

    assert clean_df.equals(expected_df)


def test_rename_columns():
    from sheetload.sheetload import SheetBag
    from sheetload.config import FlagParser

    dirty_df = generate_test_df(RENAME_CANDIDATE)
    renamed_df = SheetBag(test=True).rename_columns(dirty_df)

    assert renamed_df.columns.tolist() == RENAMED_COLS
