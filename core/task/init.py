from typing import TYPE_CHECKING
from pathlib import Path

from core.logger import GLOBAL_LOGGER as logger

if TYPE_CHECKING:
    from core.flags import FlagParser

PROJECT_DOC_URL = "https://bastienboutonnet.gitbook.io/sheetwork/installation-and-configuration/untitled/set-up-your-sheetwork-project"
PROFILE_DOC_URL = "https://bastienboutonnet.gitbook.io/sheetwork/installation-and-configuration/untitled/set-up-your-sheetwork-profile"
GOOGLE_CREDS_DOC_URL = "https://bastienboutonnet.gitbook.io/sheetwork/installation-and-configuration/untitled/connecting-to-google-sheets"
SHEETS_CONFIG_DOC_URL = "https://bastienboutonnet.gitbook.io/sheetwork/usage/sheet-configuration"

INIT_DONE = """
Your new sheetwork project "{project_name}" has been created <3.

Here is what happened behind the scenes:
- {project_path} was created.
- A sheetwork_project.yml was created containing bare essentials
- Inside that project, we dropped an empty "sheets.yml" to get you started.
- An empty google credentials file was dropped in ~/.sheetwork/google and we called it {project_name}.json
- If it was your first time setting up sheetwork on your machine we also created a profiles.yml file

What you need to do now:
- Fill up your profiles.yml file. You can access it by running the following command:

    {open_cmd} {profiles_path}

- For help on how to fill your profiles.yml file head over to:
    {profiles_doc_url}

- You will need to fill up the {project_name}.json file with your google credentials key. For help see:
    {google_creds_doc_url}

Optionally:
- You might want to change some defaults in your {project_path}/{project_name}.yml file. For help:
    {project_doc_url}

- You might want to configure a sheet to import in your sheets.yml file. For help:
    {sheets_config_doc_url}
"""

PROFILES_PATH = Path("~/.sheetwork/").expanduser()
PROJECT_PATH = Path.cwd()

PROJECT_FILE = """
test
"""


class InitTask:
    def __init__(self, flags: "FlagParser"):
        self.flags = flags
        self.project_name = flags.project_name
        self.profiles_path = PROFILES_PATH
        self.project_path = PROJECT_PATH
        self.google_path = str()
        self.assert_project_name()

    @staticmethod
    def make_dir(path: Path):
        path.mkdir()

    @staticmethod
    def make_file(path: Path, filename: str = str(), contents=None):
        if filename:
            fullpath = path / filename
        else:
            fullpath = path
        if contents:
            with fullpath.open("w", encoding="utf-8") as f:
                f.write(contents)
        else:
            fullpath.touch()

    def assert_project_name(self):
        if not self.flags.project_name:
            logger.error(f"Please provide a project name to init your project with.")

    def override_paths(self):
        if self.flags.profiles_path:
            self.profiles_path = Path(self.flags.profiles_path)

        if self.flags.project_path:
            self.project_path = Path(self.flags.project_path)

    def create_profiles_dir(self):
        if not self.profiles_path.exists():
            self.make_dir(self.profiles_path)

    def create_google_dir_and_file(self):
        google_path = self.project_path / "google"
        google_file = google_path / f"{self.project_name}.json"

        if not google_path.exists():
            self.make_dir(google_path)

        if not google_file.exists():
            self.make_file(google_file)

    # check if a profile exists in defult or provided profile dir
    # if it doesn't exist make it
    # check if a /google/ folder exists
    # if not make it
    # check if a "project_name".json file exists
    # if not, make it
    # create project folder
    # create project file
    # populate the project file with default and project_name
    # create sheets.yml
