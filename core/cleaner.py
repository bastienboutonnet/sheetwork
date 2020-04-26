import re

import inflection
import pandas


class SheetCleaner:
    def __init__(self, df: pandas.DataFrame, casing: bool = False):
        self.df = df
        self.casing = casing
        assert isinstance(
            self.df, pandas.DataFrame
        ), f"SheetCleaner can only process a pandas.DataFrame. You are feeding a {type(self.df)}."

    def cleanup(self):
        clean_df = self.df.copy(deep=True)

        if self.casing:
            clean_df = self.camel_to_snake(clean_df)
        clean_df = self.columns_cleanups(clean_df)
        clean_df = self.fields_cleanups(clean_df)

        return clean_df

    @staticmethod
    def columns_cleanups(df, default_replacement="_", characters_to_replace=None):

        # only keep letters (default) or replace a given list of characters
        if not characters_to_replace:
            regex_expression = "[^a-zA-Z]+"
        else:
            regex_expression = r"[" + "\\".join(characters_to_replace) + "]+"

        # replace specified characters with the default_replacement and remove consecutive and trailing whitespace and default_replacement
        df.columns = [
            re.sub(regex_expression, default_replacement, col).strip().strip(default_replacement)
            for col in df.columns
        ]

        # remove empty cols
        if "" in df.columns:
            df = df.drop([""], axis=1)

        # make all columns lowercase
        df.columns = map(str.lower, df.columns)
        return df

    @staticmethod
    def fields_cleanups(df):

        # clean trailing spaces in fields
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].str.strip()

        return df

    @staticmethod
    def camel_to_snake(df: pandas.DataFrame) -> pandas.DataFrame:
        df.columns = [inflection.underscore(col) for col in df.columns]
        return df
