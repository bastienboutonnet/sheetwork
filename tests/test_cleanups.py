from .mockers import DIRTY_DF, CLEAN_DF, generate_test_df


def test_cleanup():
    from sheetload.cleaner import SheetCleaner

    dirty_df = generate_test_df(DIRTY_DF)
    clean_df = SheetCleaner(dirty_df).cleanup()
    expected_df = generate_test_df(CLEAN_DF)

    assert clean_df.equals(expected_df)
