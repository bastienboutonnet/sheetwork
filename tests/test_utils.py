from .mockers import TO_CAST_DF, generate_test_df

CASTING_DICT = {
    "col_int": "int",
    "col_varchar": "varchar",
    "created_date": "date",
}


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


def test_check_and_compare_version(mocker):
    from core.utils import check_and_compare_version

    # mock the call to pypi
    mocker.patch("luddite.get_version_pypi", return_value="1.0.0")
    dummy_version = "0.0.0"
    needs_update = check_and_compare_version(dummy_version)
    assert needs_update is True
