# 1.1.0 Jean-Michel Jarre (Unreleased)
## Overview
This release focuses on making `sheetload` a lot more flexible and robust. The main addition lies with the ability to read from a config file columns which data types need to be changed in table creation when pushed to database.

## Features
- Is able to read configuratio info from a configuration file (`sheets.yml`) which contains (amongst other things) column typing often required after pulling a sheet from google as the data loaded by pandas is often interpreted as strings. [#20](https://github.com/bastienboutonnet/sheetload/pull/20)
- Allows for interactive CLI interface on whether to run default cleanups when passing `--i`. This cleanup was previously applied to all sheets by default. [#17](https://github.com/bastienboutonnet/sheetload/pull/17)
- Under the hood: validates the config file in a pretty strict way for missing tags which are required when reading from config or for unalowable tags which could potentially break things down the line. [#24](https://github.com/bastienboutonnet/sheetload/pull/24)


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
