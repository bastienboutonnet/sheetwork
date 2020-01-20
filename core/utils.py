from pathlib import Path
from typing import Tuple

import pandas

from core.exceptions import (
    ColumnNotFoundInDataFrame,
    DatabaseError,
    NearestFileNotFound,
    UnsupportedDataTypeError,
)
from core.logger import GLOBAL_LOGGER as logger


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


def cast_pandas_dtypes(df: pandas.DataFrame, overwrite_dict: dict = dict()) -> pandas.DataFrame:
    overwrite_dict = overwrite_dict.copy()
    dtypes_map = dict(
        varchar="object",
        int="int64",
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
    logger.debug(f"Head of cast DF:\n {df.head()}")
    return df
