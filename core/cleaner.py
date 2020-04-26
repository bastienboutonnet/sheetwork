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
    def columns_cleanups(
        df,
        characters_to_replace=[
            "*",
            "/",
            ".",
            "?",
            "_",
            "%",
            "s",
            "\\",
            "#",
            "&",
            "$",
            "|",
            "<",
            ">",
            "=",
            "+",
            "-",
            "'",
            '"',
        ],
        default_replacement="_",
    ):

        # clean column names by replacing characters_to_replace with default_replacement, remove trailing whitespace and consecutive default_replacement
        regex_expression = r"[" + "\\".join(characters_to_replace) + "]+"
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
