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


class ProjectFileParserError(Exception):
    "When no dict comes out of loading project or other less specific project parsing related stuff"


class ColumnNotFoundInDataFrame(Exception):
    "For cases where renamer is provided the wrong identifier name."


class InvalidProfileError(Exception):
    "For when some values in a profile that should not be none are."


class NearestFileNotFound(Exception):
    "When the path finder has reached its max iterations without finding the expected file."


class CredentialsParsingError(Exception):
    "When the credentials parser cannot find the right keys and other nasties."


class UnsupportedDataTypeError(Exception):
    "When a requested cast isn't supported by the database or mapping enforced by sheetload."


class DatabaseError(Exception):
    "To catch db interaction errors"


class TableDoesNotExist(Exception):
    "When query for rows and cols came back empty or none"
