"""Cleaning module. Holds SheetCleaner which holds df kinds of cleanings."""
import re

import inflection
import numpy as np
import pandas


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
    def columns_cleanups(df: pandas.DataFrame) -> pandas.DataFrame:

        # clean column names (slashes and spaces to understore), remove trailing whitespace
        df.columns = [re.sub(r"^\d+", "", col) for col in df.columns]  # type: ignore
        df.columns = [
            col.replace(" ", "_")
            .replace("/", "_")
            .replace(".", "_")
            .replace("?", "_")
            .replace("__", "_")
            .strip()
            for col in df.columns
        ]
        df.columns = [re.sub(r"^\_+", "", col) for col in df.columns]
        df.columns = [re.sub(r"\_+$", "", col) for col in df.columns]
        df.columns = [re.sub(r"[^\w\s]", "", col) for col in df.columns]

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
