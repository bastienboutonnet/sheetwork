[![CodeFactor](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload/badge)](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Package Version: `v0.0.0rc3`

# sheetload 💩🤦
A handy package to load Google Sheets to Snowflake

Loads Google sheets from Data Team shared drive and uploads them to Snowflake.
Performs some cleanups on column names and string (such as removing trailing spaces etc.)

## Installation
1. Activate the virtual environment you might want to use it in (most likely it's going to be the one you set up for `data_etl`.
2. Make sure `pip` is above `v19.1` otherwise one of the required packages by `sheetload` (`data_tools`) will not be installed correctly. If you're not sure you can check by doing `pip --version`. If you're behind, you can upgrade it via `pip install -U pip`.
3. Make sure your access tokens and usernames are installed according to TripActions Data Tooling standards. Setup information can be found in [data_tools Credentials](https://github.com/tripactions/data_tooling/blob/master/README.md#credentials).
4. Install Sheetload
```bash
pip install git+ssh://git@github.com/bastienboutonnet/sheetload.git@v0.0.0rc3
```
Make sure you've setup your GitHub ssh keys, if you don't know how to do it, check [here](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/).

5. Check your installation:
```bash
sheetload --version
```
Should display something like this:
```bash
➜ sheetload --version
sheetload 0.0.0rc3
```

## Usage
Using `sheeload` is simple. You call it, and provide the following info via the command line:
- a google sheet key
- a target schema
- a target table
For example:
```bash
sheetload --sheet_key 10J52dhgTRqtI_lm4bf9B02nQu4zu5u6r0h2VIDTjRXg --schema sand --table test_table
```
This mode will load the content of the sheet into a pandas dataframe, perform default basic [cleanups](#cleanups), and push the dataframe to a Snowflake table. No data type casting is possible in this mode.

## Cleanups
### Column Names
To avoid issues with Snowflake column formatting, column names that contain spaces or `/` will be cleaned to snake case.
For example: `col a` -> `col_a`, `company/account` -> `company_account`

### String Trimming
Another common issue often found in google sheet are trailing/leading whitespace. This kind of whitespace will be removed. This can cause issues down the line if you have to match strings or perform equality tests between two strings (although it is always safer when doing so to make sure to clean your strings beforehand --but that's beyond the scope of this explanation).



