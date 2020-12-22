import pytest
from pathlib import PosixPath, Path


def test_assert_project_name():
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.task.init import InitTask
    from sheetwork.core.exceptions import MissnigInitProjectName
    from sheetwork.core.main import parser

    with pytest.raises(MissnigInitProjectName):
        InitTask(FlagParser(parser)).assert_project_name()


def test_override_paths():
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.task.init import InitTask
    from sheetwork.core.main import parser

    flag_parser = FlagParser(parser)
    flag_parser.consume_cli_arguments(
        ["init", "--project-name", "dummy", "--project-dir", "dummy", "--profile-dir", "dummy"]
    )
    init_task = InitTask(flag_parser)
    init_task.override_paths()

    assert init_task.profiles_path == Path("dummy")
    assert init_task.project_path == Path("dummy")
