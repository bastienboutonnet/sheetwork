# Sheetwork Changelog

## 1.0.0 Nicolas Jaar (Unreleased)

### Overview

This release is the first release that is usable as a fully open source package. That being said **it is still a beta!**
To celebrate its independence, we have named it after extremely independent artist **"Nicolas Jaar**.

**IMPORTANT!**

- This release got a huge version bump and breaks **all** functionality of previously installed `sheetwork`
- Check documentation for [**Installation**](https://bastienboutonnet.gitbook.io/sheetwork/installation-and-configuration/installation) and [**Configuration**](https://bastienboutonnet.gitbook.io/sheetwork/installation-and-configuration/untitled)
- Refactor your jobs according to **Usage** (see [documentation](https://bastienboutonnet.gitbook.io/sheetwork/))

### Features

- Solid management of credentials, target schemas, database interaction with `Project`, `Config`, and `Profile` concepts. INSERT LINK TO DOC. (#81, #76, #91, #80, #73)
- Allows ability to convert `CamelCased` columns in the original sheet to `snake_case (#112)
- Ability to call sheetwork from anywhere on disc provided paths to config, profiles, and projects files are provided at runtime (#82)
- Adds support for short flag names for commonly used arguments (#70)
- Adds `sheetwork init` task to automatically set up a new sheetwork project and folders for you INSERT LINKS TO DOC

### Under The Hood

- Checks for duplicate columns in sheet (#145, #151)
- Checks that column up for exclusion are in df otherwise throws errors (#145)
- Improve interactive clean up (#156)
- Fixes a bug with default target schemas (#155)
- Fixes `--help` formatting (#147)
- Connects to Snowflake via SQLAlchemy (#102)
- Implements its own logger and logs to file (#98, #121)
- Is case insensitive, except when referring to columns in sheet via `identifier:` for renames (#63)
- Implements an Adaptor/Plugin design to allow for adapting to other databases (#173)

## 0.2.1 Daft Punk (2019/12/10)

Documentation Missed and was not usable.

## 0.0.0 Kraftwerk (2019/11/06)

### Overview

This is the very first version of sheetwork. It is named after the German electronic pioneers **"Kraftwerk"** as it is the pioneer (first version) of the package that will set and pave the way for future generations to come and we will all live happy forever ever after...

It loads Google Sheets into Snowflake, from the comand line and avoids the fast multiplication of `<insert_non_creative_name>_sheet_importer.py` type scripts.

### Features

- Loads google sheet into a pandas DataFrame. [#9](https://github.com/bastienboutonnet/sheetwork/pull/9)
- Performs basic cleaning.[#10](https://github.com/bastienboutonnet/sheetwork/pull/10)
- Pushes data to Snowflake using [data_tools.push_pandas_to_snowflake()](https://github.com/tripactions/data_tooling/blob/master/data_tools/db/pandas.py#L230). [#9](https://github.com/bastienboutonnet/sheetwork/pull/9)
- `--dry_run` functionality skips pushes to database and offers preview of datatypes, and head of dataframe that would be uploaded to database. [#12](https://github.com/bastienboutonnet/sheetwork/pull/12)
- `--mode dev` overrides target schema to "sand" to avoid pushing the wrong data to a production table or to allow for full flow testing while behind user permissions.[#11](https://github.com/bastienboutonnet/sheetwork/pull/12)
- `--force` can be added when running in `dev` mode to force a push to otherwise overidden target schema (see bullet above). [#12](https://github.com/bastienboutonnet/sheetwork/pull/12)

## 0.1.0 Jean-Michel Jarre (2019/11/04)

### Overview

This release focuses on making `sheetwork` a lot more flexible and robust. The main addition lies with the ability to read from a config file columns which data types need to be changed in table creation when pushed to database.

### Features

- Is able to read configuratio info from a configuration file (`sheets.yml`) which contains (amongst other things) column typing often required after pulling a sheet from google as the data loaded by pandas is often interpreted as strings. [#20](https://github.com/bastienboutonnet/sheetwork/pull/20)
- Allows for interactive CLI interface on whether to run default cleanups when passing `--i`. This cleanup was previously applied to all sheets by default. [#17](https://github.com/bastienboutonnet/sheetwork/pull/17)
- Under the hood: validates the config file in a pretty strict way for missing tags which are required when reading from config or for unalowable tags which could potentially break things down the line. [#24](https://github.com/bastienboutonnet/sheetwork/pull/24)
