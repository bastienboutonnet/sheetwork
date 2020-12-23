import pathlib

import numpy as np
import pytest
from pandas.testing import assert_frame_equal

from .mockers import CASING_DF, DIRTY_DF, SNAKE_CASED_COLS, generate_test_df

TESTING_PATH = pathlib.Path(__file__).parent.absolute()


def test_cleanup():
    from sheetwork.core.cleaner import SheetCleaner

    expected_df = {
        "col_a": {0: 1, 1: 2, 2: 32},
        "col_b": {0: "as .", 1: "b", 2: "c"},
        "1_col_one": {0: "aa", 1: "bb", 2: "cc"},
        "col_1": {0: 1, 1: 2, 2: 33},
        "long_ass_name": {0: "foo", 1: "bar", 2: "fizz"},
        "col_with_empty_string": {0: "1", 1: np.nan, 2: "2"},
    }

    dirty_df = generate_test_df(DIRTY_DF)
    expected_df = generate_test_df(expected_df)
    clean_df = SheetCleaner(dirty_df).cleanup()
    assert_frame_equal(clean_df, expected_df)


@pytest.mark.parametrize(
    "is_default_character_removal, is_list", [(True, True), (False, True), (False, False)]
)
def test_columns_cleanups(is_default_character_removal, is_list):
    from sheetwork.core.cleaner import SheetCleaner

    expected_df_dict = {
        "col_a": {0: 1, 1: 2, 2: 32},
        "col_b": {0: "as .    ", 1: "b", 2: "   c"},
        "1_col_one": {0: "aa", 1: "bb", 2: "cc"},
        "col_1": {0: 1, 1: 2, 2: 33},
        "long_ass_name": {0: "foo", 1: "bar", 2: "fizz"},
        "col_with_empty_string": {0: "1", 1: "", 2: "2"},
    }
    dirty_df = generate_test_df(DIRTY_DF)

    if is_default_character_removal:
        cleaned_df = SheetCleaner.columns_cleanups(dirty_df)
        expected_df = generate_test_df(expected_df_dict)

    elif is_default_character_removal is False:
        custom_char_removal = list()
        if is_list is True:
            expected_df_dict = {
                "col": {0: 1, 1: 2, 2: 32},
                "col b": {0: "as .    ", 1: "b", 2: "   c"},
                "1. _col_one": {0: "aa", 1: "bb", 2: "cc"},
                "col_1": {0: 1, 1: 2, 2: 33},
                "long _ss n_me": {0: "foo", 1: "bar", 2: "fizz"},
                "col_with_empty_string": {0: "1", 1: "", 2: "2"},
            }
            expected_df = generate_test_df(expected_df_dict)
            custom_char_removal = ["a", "?"]
        if is_list is False:
            expected_df_dict = {
                "col": {0: 1, 1: 2, 2: 32},
                "col b": {0: "as .    ", 1: "b", 2: "   c"},
                "1. ??col_one": {0: "aa", 1: "bb", 2: "cc"},
                "col_1": {0: 1, 1: 2, 2: 33},
                "long _ss n_me": {0: "foo", 1: "bar", 2: "fizz"},
                "col_with_empty_string": {0: "1", 1: "", 2: "2"},
            }

            expected_df = generate_test_df(expected_df_dict)
            custom_char_removal = "a"

        cleaned_df = SheetCleaner.columns_cleanups(
            dirty_df, characters_to_replace=custom_char_removal
        )

    assert_frame_equal(cleaned_df, expected_df)


def test_snake_to_camel():
    from sheetwork.core.cleaner import SheetCleaner

    cased_df = generate_test_df(CASING_DF)
    recased_df = SheetCleaner(cased_df, True).cleanup()

    assert recased_df.columns.tolist() == SNAKE_CASED_COLS
