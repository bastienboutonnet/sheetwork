class SheetloadConfigMissingError(Exception):
    "When a sheet config cannot be found"


class GoogleCredentialsFileMissingError(Exception):
    "When the google credentials file could not be located."


class GoogleSpreadSheetNotFound(Exception):
    "When a referred spreadsheet cannot be found"


class NoWorkbookLoadedError(Exception):
    "When the workbook object is None"


class WorksheetNotFoundError(Exception):
    "when a referred worksheet cannot be found in the workbook"


class YAMLFileEmptyError(Exception):
    "When a yaml that exists returns nothing"


class SheetConfigParsingError(Exception):
    "For cases where sheet was found but content could not be parsed."


class ProfileParserError(Exception):
    "When no dict or an invalid dict came out of the profile reader"


class ColumnNotFoundInDataFrame(Exception):
    "For cases where renamer is provided the wrong identifier name."


class InvalidProfileError(Exception):
    "For when some values in a profile that should not be none are."


external_errors_to_catch = {
    "overwrite_cols_data_tools_error": (
        "Looks like you have misspelled the name of at least one column in overwrite_defaults"
    )
}
