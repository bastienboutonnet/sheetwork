from pathlib import Path

import pytest


FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "test_cli_args_index",
    [0, 1, 2],
)
@pytest.mark.datafiles(FIXTURE_DIR)
def test_handle(datafiles, test_cli_args_index):
    from sheetwork.core.main import handle, parser
    from sheetwork.core.sheetwork import SheetBag
    from sheetwork.core.task.init import InitTask
    from sheetwork.core.logger import GLOBAL_LOGGER as logger

    # from sheetwork.core.flags import FlagParser

    #! THE ORDER IS IMPORTANT WHEN RUNNING IN GH ACTIONS
    args_to_test = [
        ["init", "--project-name", "dummy"],
        [
            "upload",
            "--sheet-key",  # this prevents having to read config and stuff
            "test_sheet",
            "--project-dir",
            str(datafiles),
            "--profile-dir",
            str(datafiles),
            "--schema",
            "dummy",
            "--table",
            "dummy",
        ],
        [
            "upload",
            "--sheet-key",
            "test_sheet",
            "--project-dir",
            str(datafiles),
            "--profile-dir",
            str(datafiles),
            "--log-level",
            "debug",
            "--schema",
            "dummy",
            "--table",
            "dummy",
        ],
    ]

    task = handle(parser, args_to_test[test_cli_args_index], run_task=False)

    if args_to_test[0] == "upload":
        assert isinstance(task, SheetBag)
    if args_to_test[0] == "init":
        assert isinstance(task, InitTask)
    if "debug" in args_to_test:
        assert logger.level == 10  # debug is 10.


@pytest.mark.parametrize("is_version_run", [True, False])
def test_main(is_version_run):
    from sheetwork.core.main import main, parser

    if is_version_run:
        test_cli_args = ["--version"]
    else:
        test_cli_args = ["init", "--project-name", "dummy", "--force-credentials"]

    if is_version_run:
        with pytest.raises(SystemExit):
            res = main(parser, test_cli_args)
    else:
        res = main(parser, test_cli_args)
        assert res == 0
