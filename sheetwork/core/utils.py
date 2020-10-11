import collections
from pathlib import Path
from typing import List, Optional, Tuple, Union
from urllib.error import URLError

import luddite
import pandas
from packaging.version import parse as semver_parse

from sheetwork.core._version import __version__
from sheetwork.core.exceptions import (
    ColumnNotFoundInDataFrame,
    DuplicatedColumnsInSheet,
    NearestFileNotFound,
    UnsupportedDataTypeError,
)
from sheetwork.core.logger import GLOBAL_LOGGER as logger
from sheetwork.core.ui.printer import yellow


class PathFinder:
    """Finds paths of files by going up a number of parent folders. That's it really. It's a class
    mainly to be able to limit the number of iterations otherwise we could end up going up and
    up and up and up...

    Raises:
        NearestFileNotFound: When the required file in find_nearest_dir_and_file() cannot be found
        within the maximum number of allowed iterations upwards.

    Returns:
        PathFinder: Yeah nothing much more, real returns come from the class methods.
    """

    def __init__(self, max_iter: int = 4):
        self.max_iter = max_iter
        self.iteration = 0

    def find_nearest_dir_and_file(
        self, yaml_file: str, current: Path = Path.cwd()
    ) -> Tuple[Path, Path]:
        """Looks for the yaml_file you ask for starting from the current directory and going up with
        recursion while the iteration number is still within the max allowed.

        Args:
            yaml_file (str): Name and extension of the file to find.
            current (Path, optional): Path() objects from which to start. Defaults to Path.cwd().

        Raises:
            NearestFileNotFound: When no file that matches the required name can be found.

        Returns:
            Tuple[Path, Path]: The directory up to the file name, and the full path to the filename,
            respectively. Maybe we'll end up deprecating one of these returns down the line but for
            now it's handy.
        """
        filename = Path(current, yaml_file)
        while self.iteration < self.max_iter:
            logger.debug(f"Looking for {filename}")
            if filename.exists():
                project_dir = filename.parent
                logger.debug(f"{filename} exists and was returned")
                return project_dir, filename
            current = current.parent
            filename = Path(current, yaml_file)
            self.iteration += 1
        else:
            raise NearestFileNotFound(
                f"Unable to find {yaml_file} in the nearby directories after {self.max_iter} "
                "iterations upwards."
            )


def check_columns_in_df(
    df: pandas.DataFrame,
    columns: Union[List[str], str],
    warn_only: bool = False,
    suppress_warning: bool = False,
) -> Tuple[bool, List[str]]:
    if isinstance(columns, str):
        columns = [columns]
    is_subset = set(columns).issubset(df.columns)
    if is_subset:
        return True, columns
    # else reduce columms, provide filtered list set bool to false and warn or raise
    cols_not_in_df = [x for x in columns if x not in df.columns.tolist()]
    reduced_cols = [x for x in columns if x in df.columns.tolist()]
    message = f"The following columns were not found in the sheet: {cols_not_in_df} "
    if warn_only and not suppress_warning:
        logger.warning(
            yellow(message + "they were ignored. Consider cleaning your sheets.yml file")
        )
    elif not warn_only and not suppress_warning:
        raise ColumnNotFoundInDataFrame(message + "Google Sheet or sheets.yml needs to be cleaned")
    return False, reduced_cols


def check_dupe_cols(columns: List[str], suppress_warning: bool = False) -> Optional[List[str]]:
    """checks dupes in a list"""
    columns_without_empty_strings = list(filter(None, columns))
    dupes = [
        item
        for item, count in collections.Counter(columns_without_empty_strings).items()
        if count > 1
    ]
    if dupes and not suppress_warning:
        raise DuplicatedColumnsInSheet(
            f"Duplicate column names found in Google Sheet: {dupes}. Aborting. Fix your sheet."
        )
    return dupes


def check_and_compare_version(external_version: Optional[str] = str()) -> bool:
    try:
        pypi_version: str = luddite.get_version_pypi("sheetwork")
        if external_version:
            installed_version = external_version
        else:
            installed_version = __version__

        needs_update = semver_parse(pypi_version) > semver_parse(installed_version)
        if needs_update:
            logger.warning(
                yellow(
                    f"Looks like you're a bit behind. A newer version of Sheetwork v{pypi_version} is available."
                )
            )
        return needs_update

    except URLError:
        return False


def cast_pandas_dtypes(df: pandas.DataFrame, overwrite_dict: dict = dict()) -> pandas.DataFrame:
    overwrite_dict = overwrite_dict.copy()
    dtypes_map = dict(
        varchar="object",
        # this is intentional in case of nulls. currently pandas doesn't play well with converting mixed types
        # see https://github.com/bastienboutonnet/sheetwork/issues/204 for more details
        int="object",
        numeric="float64",
        boolean="bool",
        timestamp_ntz="datetime64[ns]",
        date="datetime64[ns]",  # this intentional pandas doesn't really have just dates.
    )

    # Check for type support
    unsupported_dtypes = set(overwrite_dict.values()).difference(dtypes_map.keys())
    if unsupported_dtypes:
        raise UnsupportedDataTypeError(f"{unsupported_dtypes} are currently not supported")

    # check overwrite col is in df
    invalid_columns = set(overwrite_dict.keys()).difference(set(df.columns.tolist()))
    if invalid_columns:
        raise ColumnNotFoundInDataFrame(f"{invalid_columns} not in DataFrame. Check spelling?")

    # recode dict in pandas terms
    for col, data_type in overwrite_dict.items():
        overwrite_dict.update({col: dtypes_map[data_type]})

    # cast
    df = df.astype(overwrite_dict)
    logger.debug(f"Head of cast dataframe:\n {df.head()}")
    return df
