from setuptools import find_packages, setup

NAME = "sheetload"
VERSION = "0.2.1a0"
DESCRIPTION = """
                sheetload is a command line tool to load sheets from google
                and upload them to snowflake
                """

REQUIRED = [line.strip() for line in open("pip-requirements.txt", "r")]

REQUIRES_PYTHON = ">=3.6.0"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author="Bastien Boutonnet",
    author_email="bastien.b1@gmail.com",
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    entry_points={"console_scripts": ["sheetload=sheetload.sheetload:run"]},
    packages=find_packages(),
)
