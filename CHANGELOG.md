# 1.0.0 Kraftwerk (Unreleased)
## Overview
This is the very first version of Sheetload. It is named after the German electronic pioneers **"Kraftwerk"** as it is the pioneer (first version) of the package that will set and pave the way for future generations to come and we will all live happy forever ever after...

It loads Google Sheets into Snowflake, from the comand line and avoids the fast multiplication of `<insert_non_creative_name>_sheet_importer.py` type scripts.

## Features
- Loads google sheet into a pandas DataFrame. [#9](https://github.com/bastienboutonnet/sheetload/pull/9)
- Performs basic cleaning.[#10](https://github.com/bastienboutonnet/sheetload/pull/10)
- Pushes data to Snowflake using [data_tools.push_pandas_to_snowflake()](https://github.com/tripactions/data_tooling/blob/master/data_tools/db/pandas.py#L230). [#9](https://github.com/bastienboutonnet/sheetload/pull/9)
- `--dry_run` functionality skips pushes to database and offers preview of datatypes, and head of dataframe that would be uploaded to database. [#12](https://github.com/bastienboutonnet/sheetload/pull/12)
- `--mode dev` overrides target schema to "sand" to avoid pushing the wrong data to a production table or to allow for full flow testing while behind user permissions.[#11](https://github.com/bastienboutonnet/sheetload/pull/12)
- `--force` can be added when running in `dev` mode to force a push to otherwise overidden target schema (see bullet above). [#12](https://github.com/bastienboutonnet/sheetload/pull/12)
