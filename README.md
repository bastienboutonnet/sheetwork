[![CodeFactor](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload/badge)](https://www.codefactor.io/repository/github/bastienboutonnet/sheetload)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Package Version: `v0.1.0b0`

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
pip install git+ssh://git@github.com/bastienboutonnet/sheetload.git@v0.1.0b0
```
Make sure you've setup your GitHub ssh keys, if you don't know how to do it, check [here](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/).

5. Check your installation:
```bash
sheetload --version
```
Should display something like this:
```bash
➜ sheetload --version
sheetload 0.1.0b0
```

## Usage
Using `sheeload` is simple. You call it, and provide the following info via the command line:
- a google sheet key
- a target schema
- a target table
For example:
```bash
sheetload --sheet_key adkajhsdkajhkajh8768271872613akjsdhaksjd --schema sand --table test_table
```
This mode will load the content of the sheet into a pandas dataframe, perform default basic [cleanups](#cleanups), and push the dataframe to a Snowflake table. No data type casting is possible in this mode.

## Cleanups
### Column Names
To avoid issues with Snowflake column formatting, column names that:
- contain spaces
- `/`
- camelCasing
- `.`
will be cleaned to snake case.
For example: `col a` -> `col_a`, `company/account` -> `company_account`

### String Trimming
Another common issue often found in google sheet are trailing/leading whitespace. This kind of whitespace will be removed. This can cause issues down the line if you have to match strings or perform equality tests between two strings (although it is always safer when doing so to make sure to clean your strings beforehand --but that's beyond the scope of this explanation).



## Usage
There are two ways of using `sheeload`:

### CLI Only
This is the simplest and quickes useage mode. All you need is to call `sheetload` with:
- a googlesheet key
- a target schema
- a target table
```bash
sheetload --sheet_key adkajhsdkajhkajh8768271872613akjsdhaksjd --schema sand --table test_table
```
This mode will load the content of the sheet into a pandas dataframe, perform default basic cleanups (INSERT DOC LINK LATER), and push the dataframe to a Snowflake table. No data type casting is possible in this mode.

### CLI + Config
This is a more involved mode, but great to put in place when you've tested things or if you know you will have to cast datatypes.
- Create a `sheets.yml` file in the path of your choosing. This config file should look like so:
```yaml
sheets:
  - sheet_name: test_sheet
    sheet_key: 10J52dhgTRqtI_lm4bf9B02nQu4zu5u6r0h2VIDTjRXg
    target_schema: sand
    target_table: bb_test_sheetload
    # the following is optional, but if columns are provided both a name and a datatype
    # must be provided.
    columns:
      - name: col_a
        datatype: int
      - name: col_b
        datatype: varchar
```

Sheets are referred to by a human readable name (`sheet_name`). This is the name you will need to use later when calling `sheetload`.
The rest of the information is pretty straighforward. Column datatype casting is achived by adding a `columns` entry listing all the columns for which a specific datatype must be cast see [Important notes section below](#Important-notes-on-`Sheets.yml`-formatting) for info on column name formatting.
- Navigate to the folder containing your `sheets.yml` file:
```bash
cd /path/to/your/yml/folder
```
- Call `sheetload`🧼 providing only a sheet name `--sheet_name` in this example it would be `test_sheet`. So it all should look like this
```bash
sheetload --sheet_name test_sheet
```

#### Important Notes on `Sheets.yml` formatting
- **Do you need to list ALL the columns in your sheet?**
No! You don't have to. You can leave the columns part empty and **you only need to add a column if you want to override its format when it's saved to Snowflake**
- **Do the column names need to be in the format of the original sheet?**
No. **Actually they shouldn't!** As mentioned [earlier in the documentation](#column-names) Sheetload needs to convert the name of the columns in a format that works with Snowflake and as such you should write the columns in the `sheets.yml` file as they would end up in Snowflake.
- **Not sure exactly how the columns will be reformated?**
Yeah that's kinda expected. Besides checking [the cleanup steps documentation above](#column-names) you should add the `--dry_run` flag to see what would happen to your sheet. This mode will not write to Snowflake, and will display handy information about the look of your data frame:

It first gives you a list of all the columns in the table **formatted for Snowflake** as well as the data type of each of the columns so that you can spot whether you might have to override any of them when writing to Snowflake. **IMPORTANT**: These are *Pandas datatypes*. It will look like this:
```
2019-11-16 12:59:15 - data_tools.logging - [INFO] - POST-CLEANING PREVIEW: This is what you would push to the database:

DataFrame DataTypes:

col_a    object
col_b    object
dtype: object
```

Then it will also show you a preview of the dataframe (first few rows). **NOTE: For dataframes with many columns the preview will likely be trucated** (this issue will be addressed in an upcoming release [see issue #39](https://github.com/bastienboutonnet/sheetload/issues/39)). The preview will look like this:
```
DataFrame Preview:

  col_a col_b
0     1  as .
1     2     b
2     3     c
```

### Useful flags
These flags are valid for both of the execution modes [outlined above](#usage).

**Dry Run**: Dry runs (skipping pushing to the database) can be achieved by adding the `--dry_run` flag.

**Interactive Cleanup**: You may want to see what the file looks like and decide whether you need to apply cleanups at all. You can do this by using the `--i` flag.
Down the line we expect this mode to have more functionality

**Create Table**: The target table may not be present on the database. You can create it by adding the `--create_table` flag.

### Other Flags 🤯
There are a few more flags linked to modes, log level and forcing intented protection measures down. Here is the full list of flags with their use, defaults etc. (You can get that by doing `sheetload -h`)
```
usage: sheetload [-h] [--version] [--mode MODE] [--log_level LOG_LEVEL]
                 [--sheet_name SHEET_NAME] [--sheet_key SHEET_KEY]
                 [--schema SCHEMA] [--table TABLE] [--create_table] [--force]
                 [--dry_run] [--i]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --mode MODE           Chooses between prod or dev run
  --log_level LOG_LEVEL
                        sets the log level
  --sheet_name SHEET_NAME
                        Name of your sheet from config
  --sheet_key SHEET_KEY
                        Google sheet Key
  --schema SCHEMA       Target Schema Name
  --table TABLE         Target Table Name
  --create_table        Creates target table before pushing.
  --force               Forces target schema to be followed. Even when in DEV
                        mode.
  --dry_run             Skips pushing to database
  --i                   Turns on interactive mode, which allows previews and
                        cleanup choices
```



