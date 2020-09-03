import numpy as np
import pandas
from pandas import Timestamp

EXPECTED_CONFIG = {
    "sheet_name": "df_dropper",
    "sheet_key": "sample",
    "target_schema": "sand",
    "target_table": "bb_test_sheetwork",
    "columns": [
        {"name": "col_a", "datatype": "int"},
        {"name": "col_b", "datatype": "varchar"},
        {"name": "col_one", "datatype": "varchar"},
        {"name": "renamed_col", "identifier": "long ass name", "datatype": "varchar"},
    ],
    "excluded_columns": ["to_exclude"],
}

EXPECTED_DEV_TEST_PROFILE = {
    "db_type": "snowflake",
    "account": "a",
    "user": "b",
    "password": "c",
    "role": "d",
    "database": "e",
    "warehouse": "f",
    "schema": "g",
    "guser": "sheetwork_test@blahh.iam.gserviceaccount.com",
}

NO_COLS_EXPECTED_CONFIG = {
    "sheet_name": "no_cols",
    "sheet_key": "sample",
    "target_schema": "sand",
    "target_table": "bb_test_sheetwork",
}

EXPECTED_SHEETWORK_PROJECT = {
    "name": "sheetwork_test",
    "target_schema": "sand",
    "always_create": True,
}

DIRTY_DF = {
    "col_a": [1, 2, 32],
    "col b": ["as .    ", "b", "   c"],
    "1. col_one": ["aa", "bb", "cc"],
    "": ["q", "q", "q"],
    "col_1": [1, 2, 33],
    "long ass name": ["foo", "bar", "fizz"],
    "col_with_empty_string": ["1", "", "2"],
}

TO_CAST_DF = {
    "col_int": ["1", "2", "32"],
    "col_varchar": ["foo", "bar", "fizz"],
    "created_date": ["2019/01/01", "2019/01/02", "2019/01/03"],
}

CAST_DF = {
    "col_int": {0: 1, 1: 2, 2: 32},
    "col_varchar": {0: "foo", 1: "bar", 2: "fizz"},
    "created_date": {
        0: Timestamp("2019-01-01 00:00:00"),
        1: Timestamp("2019-01-02 00:00:00"),
        2: Timestamp("2019-01-03 00:00:00"),
    },
}

CASING_DF = {
    "CamelCasedCol": [1, 2, 3],
    "snake_cased_col": [1, 2, 3],
}

SNAKE_CASED_COLS = ["camel_cased_col", "snake_cased_col"]

CAMEL_CASED_COLS = ["CamelCasedCol", "SnakeCasedCol"]

CLEAN_DF = {
    "col_a": {0: 1, 1: 2, 2: 32},
    "col_b": {0: "as .", 1: "b", 2: "c"},
    "col_one": {0: "aa", 1: "bb", 2: "cc"},
    "col_1": {0: 1, 1: 2, 2: 33},
    "long_ass_name": {0: "foo", 1: "bar", 2: "fizz"},
    "col_with_empty_string": {0: "1", 1: "", 2: "2"},
}

RENAMED_DF = {
    "col_a": {0: 1, 1: 2, 2: 32},
    "col_b": {0: "as .", 1: "b", 2: "c"},
    "col_one": {0: "aa", 1: "bb", 2: "cc"},
    "col_1": {0: 1, 1: 2, 2: 33},
    "renamed_col": {0: "foo", 1: "bar", 2: "fizz"},
}

DROP_COL_DF = {
    "col_a": [1, 2, 32],
    "col b": ["as .    ", "b", "   c"],
    "1. col_one": ["aa", "bb", "cc"],
    "": ["q", "q", "q"],
    "long ass name": ["foo", "bar", "fizz"],
    "to_exclude": ["garbage1", "garbage2", "garbage3"],
}

RENAMED_COLS = ["col_a", "col b", "1. col_one", "", "col_1", "renamed_col", "col_with_empty_string"]

EXCLUDED_DF_COLS = ["col_a", "col b", "1. col_one", "", "long ass name"]


def generate_test_df(df):
    test_df = pandas.DataFrame.from_dict(df)
    return test_df
