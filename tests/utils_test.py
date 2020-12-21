from pathlib import Path
from sheetwork.core.main import handle

import pytest
from pandas.testing import assert_frame_equal
from .mockers import CAST_DF, TO_CAST_DF, generate_test_df

CASTING_DICT = {
    "col_int": "int",
    "col_varchar": "varchar",
    "created_date": "date",
    "col_bool": "boolean",
    "col_numeric": "numeric",
}

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "col_is_list, warn_only", [(True, False), (True, True), (False, True), (False, False)]
)
def test_check_columns_in_df(col_is_list, warn_only):
    from sheetwork.core.utils import check_columns_in_df
    from sheetwork.core.exceptions import ColumnNotFoundInDataFrame

    if col_is_list:
        cols = ["column_that_is_not_in_df", "col_int"]
    else:
        cols = "col_int"

    to_check = generate_test_df(TO_CAST_DF)
    is_subset = None
    if warn_only and col_is_list:
        is_subset, columns = check_columns_in_df(to_check, cols, warn_only=warn_only)
        assert is_subset is False
        assert columns == [cols[1]]
    elif warn_only and col_is_list is False:
        is_subset, columns = check_columns_in_df(to_check, cols, warn_only=warn_only)
        assert is_subset is True
        assert columns == ["col_int"]
    elif (
        col_is_list is True
        and warn_only is False  # this is because in this configuration I have an exta column
    ):
        with pytest.raises(ColumnNotFoundInDataFrame):
            is_subset, columns = check_columns_in_df(to_check, cols, warn_only=warn_only)


def test_check_dupe_cols():
    from sheetwork.core.utils import check_dupe_cols
    from sheetwork.core.exceptions import DuplicatedColumnsInSheet

    list_with_dupe = ["a", "a", "b"]
    with pytest.raises(DuplicatedColumnsInSheet):
        dupes = check_dupe_cols(list_with_dupe)


def test_check_and_compare_version(mocker):
    from sheetwork.core.utils import check_and_compare_version

    # mock the call to pypi
    mocker.patch("luddite.get_version_pypi", return_value="1.0.0")
    dummy_version = "0.0.0"
    needs_update, pypi_version = check_and_compare_version(dummy_version)
    assert needs_update is True
    assert pypi_version == "1.0.0"


@pytest.mark.parametrize("scenario", ["normal", "unsupported_dtypes", "column_not_in_df"])
def test_cast_pandas_dtypes(scenario):
    from sheetwork.core.utils import cast_pandas_dtypes
    from sheetwork.core.exceptions import UnsupportedDataTypeError, ColumnNotFoundInDataFrame

    to_cast = generate_test_df(TO_CAST_DF)

    if scenario == "normal":
        casting_dict = CASTING_DICT
        cast_df = cast_pandas_dtypes(to_cast, casting_dict)
        expected_cast = generate_test_df(CAST_DF)
        assert cast_df.to_dict() == expected_cast.to_dict()

    elif scenario == "unsupported_dtypes":
        casting_dict = {"col_int": "not_allowes_dtype"}
        with pytest.raises(UnsupportedDataTypeError):
            cast_df = cast_pandas_dtypes(to_cast, casting_dict)

    elif scenario == "column_not_in_df":
        casting_dict = {"illegal_column": "int"}
        with pytest.raises(ColumnNotFoundInDataFrame):
            cast_df = cast_pandas_dtypes(to_cast, casting_dict)


@pytest.mark.parametrize("has_good_booleans", [True, False])
def test_handle_booleans(has_good_booleans):
    from sheetwork.core.utils import handle_booleans
    from sheetwork.core.exceptions import ColumnNotBooleanCompatibleError

    illegal_booleans_df = {"col_a": [False, "True"], "col_b": ["bad", "food"]}
    good_booleans_df = {"col_a": [False, True], "col_b": [True, "False"]}
    col_casting_dict = {"col_a": "boolean", "col_b": "boolean"}
    if has_good_booleans:
        df = generate_test_df(good_booleans_df)
        df = handle_booleans(df, col_casting_dict)
    else:
        with pytest.raises(ColumnNotBooleanCompatibleError):
            df = generate_test_df(illegal_booleans_df)
            df = handle_booleans(df, col_casting_dict)


@pytest.mark.parametrize("is_good_dir", [True, False])
@pytest.mark.datafiles(FIXTURE_DIR)
def test_find_nearest_dir_and_file(datafiles, is_good_dir):
    from sheetwork.core.utils import PathFinder
    from sheetwork.core.exceptions import NearestFileNotFound

    if is_good_dir:
        _, _, is_found = PathFinder().find_nearest_dir_and_file(str(datafiles))
        assert is_found is True
    else:
        with pytest.raises(NearestFileNotFound):
            _, _, is_found = PathFinder().find_nearest_dir_and_file("bad_filepath")


@pytest.mark.parametrize("colour", ["yellow", "red", None, "black"])
def test_deprecate(colour):
    from sheetwork.core.utils import deprecate

    message = "test_message"
    with pytest.warns(DeprecationWarning):
        deprecate(message, colour)
