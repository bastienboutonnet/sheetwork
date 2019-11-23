import re

import pandas


class SheetCleaner:
    def __init__(self, df):
        self.df = df
        assert isinstance(
            self.df, pandas.DataFrame
        ), f"SheetCleaner can only process a pandas.DataFrame. You are feeding a {type(self.df)}."

    def cleanup(self):
        clean_df = self.df.copy(deep=True)

        clean_df = self.columns_cleanups(clean_df)
        clean_df = self.fields_cleanups(clean_df)

        return clean_df

    @staticmethod
    def columns_cleanups(df):

        # clean column names (slashes and spaces to understore), remove trailing whitespace
        df.columns = [re.sub(r"^\d+", "", col) for col in df.columns]
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
        return df

    @staticmethod
    def fields_cleanups(df):

        # clean trailing spaces in fields
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].str.strip()

        return df
