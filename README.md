[![CodeFactor](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload/badge)](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Package Version: `v1.0.0rc1`

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
pip install git@github.com:bastienboutonnet/sheetload.git@v1.0.0rc1
```
Make sure you've setup your GitHub ssh keys, if you don't know how to do it, check [here](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/).

5. Check your installation:
```bash
sheetload --version
```
Should display something like this:
```bash
➜ sheetload --version
sheetload 1.0.0rc1
```

