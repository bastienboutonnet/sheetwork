from typing import TYPE_CHECKING
from pathlib import Path

from core.logger import GLOBAL_LOGGER as logger
from core.exceptions import ProjectIsAlreadyCreated
from core.clients.system import open_dir_cmd, make_dir, make_file
from core.ui.printer import green
import time

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
- Inside that project, we dropped an empty "sheets.yml" to get you started.
- And we created a "sheetwork_project.yml" containing the bare essentials to get you started.
- An empty google credentials file was dropped in {google_path} and we called it {project_name}.json
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
name: '{project_name}'

# change the following to your default destination schema
target_schema: 'sandbox'

# we set sheetwork to always create tables, feel free to set that to false if you don't like it.
always_create: true
"""


class InitTask:
    def __init__(self, flags: "FlagParser"):
        self.flags = flags
        self.project_name: str = flags.project_name
        self.profiles_path: Path = PROFILES_PATH
        self.project_path: Path = PROJECT_PATH
        self.google_path: Path = Path()
        self.assert_project_name()

    def assert_project_name(self):
        if not self.flags.project_name:
            logger.error(f"Please provide a project name to init your project with.")

    def override_paths(self):
        if self.flags.profile_dir:
            self.profiles_path = Path(self.flags.profile_dir)

        if self.flags.project_dir:
            self.project_path = Path(self.flags.project_dir)

    def create_profiles_dir(self):
        if not self.profiles_path.exists():
            make_dir(self.profiles_path)
        else:
            logger.debug(f"{self.profiles_path} already exists.")

    def create_profiles_file(self):
        profile_file = Path(self.profiles_path, "profiles").with_suffix(".yml")
        if not profile_file.exists():
            make_file(profile_file)
        else:
            logger.debug(f"{profile_file} already exists.")

    def create_google_dir_and_file(self):
        self.google_path = self.profiles_path / "google"
        google_file = self.google_path / f"{self.project_name}.json"

        if not self.google_path.exists():
            make_dir(self.google_path)
        else:
            logger.debug(f"{self.google_path} already exists.")

        if not google_file.exists():
            make_file(google_file)
        else:
            logger.debug(f"{google_file} already exists.")

    def create_project_dir(self):
        project_dir = self.project_path / f"{self.project_name}"
        if not project_dir.exists():
            make_dir(project_dir)
        else:
            raise ProjectIsAlreadyCreated(
                f"""\n
                {self.project_name} already exists, so we'll stop.
                If you created it by mistake, delete it and run this again.
                """
            )

    def create_project_file(self):
        full_path = Path(self.project_path, self.project_name, "sheetwork_project").with_suffix(
            ".yml"
        )
        if not full_path.exists():
            project_file_content = PROJECT_FILE.format(project_name=self.project_name)
            make_file(full_path, project_file_content)

    def show_complete(self):
        done_message = INIT_DONE.format(
            project_name=self.project_name,
            project_path=self.project_path,
            profiles_path=self.profiles_path,
            google_path=self.google_path,
            profiles_doc_url=PROFILE_DOC_URL,
            google_creds_doc_url=GOOGLE_CREDS_DOC_URL,
            project_doc_url=PROJECT_DOC_URL,
            sheets_config_doc_url=SHEETS_CONFIG_DOC_URL,
            open_cmd=open_dir_cmd(),
        )
        logger.info(green(done_message))

    def run(self):
        logger.info("❤️ Taking peantut butter and jelly out of the cupboard...🍇")
        time.sleep(3)
        self.override_paths()
        self.create_project_dir()
        self.create_project_file()
        self.create_profiles_dir()
        self.create_profiles_file()
        self.create_google_dir_and_file()
        self.show_complete()
