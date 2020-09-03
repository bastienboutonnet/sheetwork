import pathlib
from pathlib import Path

import numpy as np
import pandas

from .mockers import CASING_DF, DIRTY_DF, SNAKE_CASED_COLS, generate_test_df

TESTING_PATH = pathlib.Path(__file__).parent.absolute()


def test_cleanup():
    from core.cleaner import SheetCleaner

    clean_df_path = Path(TESTING_PATH, "clean_df.json")
    dirty_df = generate_test_df(DIRTY_DF)
    clean_df = SheetCleaner(dirty_df).cleanup()
    expected_df = pandas.read_json(
        clean_df_path,
        dtype={"col_with_empty_string": "object"},
    )
    expected_df = expected_df.fillna(np.nan)

    assert clean_df.equals(expected_df)


def test_snake_to_camel():
    from core.cleaner import SheetCleaner

    cased_df = generate_test_df(CASING_DF)
    recased_df = SheetCleaner(cased_df, True).cleanup()

    assert recased_df.columns.tolist() == SNAKE_CASED_COLS
