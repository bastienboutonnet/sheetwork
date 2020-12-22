import pytest
from mock import patch, PropertyMock
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize("platform", ["win32", "darwin", "other"])
def test_open_dir_cmd(platform):
    from sheetwork.core.clients.system import open_dir_cmd

    expected_open_cmd_str = {"win32": "start", "darwin": "open", "other": "xdg-open"}

    def mock_sys_platform(self):
        return platform

    with patch("sheetwork.core.clients.system.sys") as mocked_sys:
        type(mocked_sys).platform = PropertyMock(return_value=platform)
        open_cmd_str = open_dir_cmd()

        assert open_cmd_str == expected_open_cmd_str[platform]


@pytest.mark.datafiles(FIXTURE_DIR)
def test_make_file(datafiles):
    from sheetwork.core.clients.system import make_file

    contents_to_write = "dummy_content"
    filename = Path(datafiles).joinpath("dummy_file").with_suffix(".txt")
    make_file(path=filename, contents=contents_to_write)

    assert filename.is_file()


@pytest.mark.datafiles(FIXTURE_DIR)
def test_make_dir(datafiles):
    from sheetwork.core.clients.system import make_dir

    dir_path = Path(datafiles).joinpath("dummy_subdir")
    make_dir(path=dir_path)

    assert dir_path.exists()
