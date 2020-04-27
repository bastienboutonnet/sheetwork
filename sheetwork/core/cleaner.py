"""Cleaning module. Holds SheetCleaner which holds df kinds of cleanings."""
import re

import inflection
import numpy as np
import pandas
from typing import List, Union


class SheetCleaner:
    """Class containing all sheet cleaning related methods and ochestrators for such cleaning."""

    def __init__(self, df: pandas.DataFrame, casing: bool = False) -> None:
        """Constructor for SheetCleaner.

        Args:
            df (pandas.DataFrame): dataframe to clean up
            casing (bool, optional): When true case-related operations (see self.cleanup()) are
                performed. Defaults to False.
        """
        self.df = df
        self.casing = casing
        assert isinstance(
            self.df, pandas.DataFrame
        ), f"SheetCleaner can only process a pandas.DataFrame. You are feeding a {type(self.df)}."

    def cleanup(self) -> pandas.DataFrame:
        clean_df = self.df.copy(deep=True)

        if self.casing:
            clean_df = self.camel_to_snake(clean_df)
        clean_df = self.columns_cleanups(clean_df)
        clean_df = self.fields_cleanups(clean_df)

        return clean_df

    @staticmethod
    def columns_cleanups(
        df: pandas.DataFrame,
        default_replacement: str = "_",
        characters_to_replace: Union[List[str], str] = list(),
    ):
        # when provided, ensure characters_to_replace is a list
        if isinstance(characters_to_replace, str):
            characters_to_replace = [characters_to_replace]

        # only keep alphanumeric by default
        regex_string = "[^a-zA-Z0-9]+"

        # or, replace a given list of characters when specified
        if characters_to_replace:
            escaped_slash = "\\"
            if len(characters_to_replace) > 1:
                characters_to_replace = escaped_slash.join(characters_to_replace)
            else:
                characters_to_replace = characters_to_replace[0]
            regex_string = r"[{0}{1}]+".format(escaped_slash, characters_to_replace)

        # replace specified characters with the default_replacement and remove consecutive and
        # trailing whitespace and default_replacement
        df.columns = [
            re.sub(regex_string, default_replacement, col).strip(default_replacement).strip()
            for col in df.columns
        ]

        # remove empty cols
        if "" in df.columns:
            df = df.drop([""], axis=1)

        # make all columns lowercase
        df.columns = list(map(str.lower, df.columns))
        return df

    @staticmethod
    def fields_cleanups(df: pandas.DataFrame) -> pandas.DataFrame:
        # convert empty strings with missing value
        df = df.replace("", np.nan)  # type: ignore

        # clean trailing spaces in fields
        for col in df.columns:  # type: ignore
            if df[col].dtype == "object":  # type: ignore
                df[col] = df[col].str.strip()  # type: ignore

        return df

    @staticmethod
    def camel_to_snake(df: pandas.DataFrame) -> pandas.DataFrame:
        df.columns = [inflection.underscore(col) for col in df.columns]  # type: ignore
        return df
