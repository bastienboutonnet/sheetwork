# FIXME: There might be a better way to do that.
# Ideally this class has a basic message which can be overridden.


class SheetloadConfigMissingError(Exception):
    "When a sheet config cannot be found"


class SheetConfigParsingError(Exception):
    "For cases where sheet was found but content could not be parsed."


# FIXME: There might also be a better way to do this. Check with Youri.
external_errors_to_catch = {
    "overwrite_cols_data_tools_error": "Looks like you have misspelled the name of at least one column in overwrite_defaults"
}