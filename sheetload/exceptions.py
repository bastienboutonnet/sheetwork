class SheetloadConfigMissingError(Exception):
    "When a sheet config cannot be found"


class SheetConfigParsingError(Exception):
    "For cases where sheet was found but content could not be parsed."


class ColumnNotFoundInDataFrame(Exception):
    "For cases where renamer is provided the wrong identifier name."


external_errors_to_catch = {
    "overwrite_cols_data_tools_error": "Looks like you have misspelled the name of at least one column in overwrite_defaults"
}
