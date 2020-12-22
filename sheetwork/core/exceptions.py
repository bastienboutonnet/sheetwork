"""Contains all Sheetwork exceptions. Truely exceptional!"""
from colorama import Fore


class SheetWorkError(Exception):
    """Custom Exeption type mainly there to print things in Red."""

    def __init__(self, message: str):  # noqa D107
        super().__init__(f"{Fore.RED}{message}")


class SheetWorkConfigMissingError(SheetWorkError):
    """When a sheet config cannot be found."""


class GoogleCredentialsFileMissingError(SheetWorkError):
    """When the google credentials file could not be located."""


class GoogleSpreadSheetNotFound(SheetWorkError):
    """When a referred spreadsheet cannot be found."""


class NoWorkbookLoadedError(SheetWorkError):
    """When the workbook object is None."""


class SheetLoadingError(SheetWorkError):
    """When a referred an error happens during sheet loading."""


class YAMLFileEmptyError(SheetWorkError):
    """When a yaml that exists returns nothing."""


class SheetConfigParsingError(SheetWorkError):
    """For cases where sheet was found but content could not be parsed."""


class ProfileParserError(SheetWorkError):
    """When no dict or an invalid dict came out of the profile reader."""


class ProjectFileParserError(SheetWorkError):
    """When no dict comes out of loading project or other less specific project parsing related stuff."""


class ColumnNotFoundInDataFrame(SheetWorkError):
    """For cases where renamer is provided the wrong identifier name."""


class InvalidProfileError(SheetWorkError):
    """For when some values in a profile that should not be none are."""


class NearestFileNotFound(SheetWorkError):
    """When the path finder has reached its max iterations without finding the expected file."""


class CredentialsParsingError(SheetWorkError):
    """When the credentials parser cannot find the right keys and other nasties."""


class UnsupportedDataTypeError(SheetWorkError):
    """When a requested cast isn't supported by the database or mapping enforced by SheetWork."""


class DatabaseError(SheetWorkError):
    """To catch db interaction errors."""


class NoAcquiredConnectionError(SheetWorkError):
    """For when no connection has been acquied."""


class TableDoesNotExist(SheetWorkError):
    """When query for rows and cols came back empty or none."""


class DuplicatedColumnsInSheet(SheetWorkError):
    """when a google sheet contains the same column name twice."""


class TargetSchemaMissing(SheetWorkError):
    """when no target schema whatsoever can be found."""


class TargetObjectNotProvided(SheetWorkError):
    """When no target object could be fround because it was not CLI or config provided."""


class ProjectIsAlreadyCreated(SheetWorkError):
    """when using sheetwork init and a project is found."""


class MissnigInitProjectName(SheetWorkError):
    """when no project name is requested."""


class InvalidOrMissingCommandError(SheetWorkError):
    """when no  command or invalid command is requested."""


class GoogleClientNotAuthenticatedError(SheetWorkError):
    """when you forgot to run authenticate or it failed."""


class ColumnNotBooleanCompatibleError(SheetWorkError):
    """when a column that is asked for being concerted to bool does not have compatible values."""


class EmptyHeaderError(SheetWorkError):
    """when at least 1 column header is made of whitespaces only."""
