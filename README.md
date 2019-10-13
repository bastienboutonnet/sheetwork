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



## Usage
There are two ways of using `sheeload`:

### CLI Only
This is the simplest and quickes useage mode. All you need is to call `sheetload` with:
- a googlesheet key
- a target schema
- a target table
```bash
sheetload --sheet_key 10J52dhgTRqtI_lm4bf9B02nQu4zu5u6r0h2VIDTjRXg --schema sand --table test_table
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
The rest of the information is pretty straighforward. Column datatype casting is achived by adding a `columns` entry listing all the columns for which a specific datatype must be cast.
- Navigate to the folder containing your `sheet.yml` file:
```bash
cd /path/to/your/yml/folder
```
- Call `sheetload`🧼 providing only a sheet name `--sheet_name` in this example it would be `test_sheet`. So it all should look like this
```bash
sheetload --sheet_name test_sheet
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



