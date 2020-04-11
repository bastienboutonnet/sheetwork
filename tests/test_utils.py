from .mockers import TO_CAST_DF, CAST_DF, generate_test_df


CASTING_DICT = {
    "col_int": "int",
    "col_varchar": "varchar",
    "created_date": "date",
}


def test_cast_pandas_dtypes():
    from core.utils import cast_pandas_dtypes

    to_cast = generate_test_df(TO_CAST_DF)
    cast_df = cast_pandas_dtypes(to_cast, CASTING_DICT)
    expected_cast = generate_test_df(CAST_DF)

    assert cast_df.to_dict() == expected_cast.to_dict()


def test_check_columns_in_df():
    from core.utils import check_columns_in_df

    cols = ["column_that_is_not_in_df", "col_int"]

    to_check = generate_test_df(TO_CAST_DF)
    is_subset, columns = check_columns_in_df(to_check, cols, suppress_warning=True)

    assert is_subset is False
    assert columns == [cols[1]]


def test_check_dupe_cols():
    from core.utils import check_dupe_cols

    list_with_dupe = ["a", "a", "b"]
    dupes = check_dupe_cols(list_with_dupe, suppress_warning=True)

    assert dupes == ["a"]
