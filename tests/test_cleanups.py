from .mockers import DIRTY_DF, CLEAN_DF, CASING_DF, SNAKE_CASED_COLS, generate_test_df


def test_cleanup():
    from core.cleaner import SheetCleaner

    dirty_df = generate_test_df(DIRTY_DF)
    clean_df = SheetCleaner(dirty_df).cleanup()
    expected_df = generate_test_df(CLEAN_DF)

    assert clean_df.equals(expected_df)


def test_snake_to_camel():
    from core.cleaner import SheetCleaner

    cased_df = generate_test_df(CASING_DF)
    recased_df = SheetCleaner(cased_df, True).cleanup()
    print(recased_df.columns.tolist())

    assert recased_df.columns.tolist() == SNAKE_CASED_COLS
