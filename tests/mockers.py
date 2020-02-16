import pandas

EXPECTED_CONFIG = {
    "sheet_name": "df_dropper",
    "sheet_key": "sample",
    "target_schema": "sand",
    "target_table": "bb_test_sheetload",
    "columns": [
        {"name": "col_a", "datatype": "int"},
        {"name": "col_b", "datatype": "varchar"},
        {"name": "col_one", "datatype": "varchar"},
        {"name": "renamed_col", "identifier": "long ass name", "datatype": "varchar"},
    ],
    "excluded_columns": ["to_exclude"],
}

NO_COLS_EXPECTED_CONFIG = {
    "sheet_name": "no_cols",
    "sheet_key": "sample",
    "target_schema": "sand",
    "target_table": "bb_test_sheetload",
}

DIRTY_DF = {
    "col_a": [1, 2, 32],
    "col b": ["as .    ", "b", "   c"],
    "col_numeric": [12.33, 14.44, 13.33],
    "1. col_one": ["aa", "bb", "cc"],
    "": ["q", "q", "q"],
    "long ass name": ["foo", "bar", "fizz"],
}

CLEAN_DF = {
    "col_a": {0: 1, 1: 2, 2: 32},
    "col_b": {0: "as .", 1: "b", 2: "c"},
    "col_numeric": {0: 12.33, 1: 14.44, 2: 13.33},
    "col_one": {0: "aa", 1: "bb", 2: "cc"},
    "long_ass_name": {0: "foo", 1: "bar", 2: "fizz"},
}

CASING_DF = {
    "CamelCasedCol": [1, 2, 3],
    "snake_cased_col": [1, 2, 3],
}

RENAMED_DF = {
    "col_a": {0: 1, 1: 2, 2: 32},
    "col_b": {0: "as .", 1: "b", 2: "c"},
    "col_numeric": {0: 12.33, 1: 14.44, 2: 13.33},
    "col_one": {0: "aa", 1: "bb", 2: "cc"},
    "renamed_col": {0: "foo", 1: "bar", 2: "fizz"},
}

DROP_COL_DF = {
    "col_a": [1, 2, 32],
    "col b": ["as .    ", "b", "   c"],
    "col_numeric": [12.33, 14.44, 13.33],
    "1. col_one": ["aa", "bb", "cc"],
    "": ["q", "q", "q"],
    "long ass name": ["foo", "bar", "fizz"],
    "to_exclude": ["garbage1", "garbage2", "garbage3"],
}

RENAMED_COLS = ["col_a", "col b", "col_numeric", "1. col_one", "", "renamed_col"]

EXCLUDED_DF_COLS = ["col_a", "col b", "col_numeric", "1. col_one", "", "long ass name"]

SNAKE_CASED_COLS = ['camel_cased_col', 'snake_cased_col']

CAMEL_CASED_COLS = ['CamelCasedCol', 'SnakeCasedCol']


def generate_test_df(df):
    test_df = pandas.DataFrame.from_dict(df)
    return test_df
