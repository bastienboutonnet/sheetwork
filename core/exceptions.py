from colorama import Fore


class SheetLoadError(Exception):
    def __init__(self, message):
        super().__init__(Fore.RED + message)


class SheetloadConfigMissingError(SheetLoadError):
    "When a sheet config cannot be found"


class GoogleCredentialsFileMissingError(SheetLoadError):
    "When the google credentials file could not be located."


class GoogleSpreadSheetNotFound(SheetLoadError):
    "When a referred spreadsheet cannot be found"


class NoWorkbookLoadedError(SheetLoadError):
    "When the workbook object is None"


class WorksheetNotFoundError(SheetLoadError):
    "when a referred worksheet cannot be found in the workbook"


class YAMLFileEmptyError(SheetLoadError):
    "When a yaml that exists returns nothing"


class SheetConfigParsingError(SheetLoadError):
    "For cases where sheet was found but content could not be parsed."


class ProfileParserError(SheetLoadError):
    "When no dict or an invalid dict came out of the profile reader"


class ProjectFileParserError(SheetLoadError):
    "When no dict comes out of loading project or other less specific project parsing related stuff"


class ColumnNotFoundInDataFrame(SheetLoadError):
    "For cases where renamer is provided the wrong identifier name."


class InvalidProfileError(SheetLoadError):
    "For when some values in a profile that should not be none are."


class NearestFileNotFound(SheetLoadError):
    "When the path finder has reached its max iterations without finding the expected file."


class CredentialsParsingError(SheetLoadError):
    "When the credentials parser cannot find the right keys and other nasties."


class UnsupportedDataTypeError(SheetLoadError):
    "When a requested cast isn't supported by the database or mapping enforced by sheetload."


class DatabaseError(SheetLoadError):
    "To catch db interaction errors"


class TableDoesNotExist(SheetLoadError):
    "When query for rows and cols came back empty or none"


class DuplicatedColumnsInSheet(SheetLoadError):
    "when a google sheet contains the same column name twice"


class TargetSchemaMissing(SheetLoadError):
    "when no target schema whatsoever can be found"
