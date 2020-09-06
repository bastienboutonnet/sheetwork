import os
from setuptools import find_packages, setup

NAME = "sheetwork"
VERSION = "1.0.0b3"
DESCRIPTION = """
    sheetwork is a command line tool to load sheets from google
    and upload them to snowflake
    """

REQUIRES_PYTHON = ">=3.6.0"

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bastien Boutonnet",
    author_email="bastien.b1@gmail.com",
    install_requires=[
        "requests<2.23.0",
        "gspread==3.3.0",
        "sqlalchemy==1.3.16",
        "cerberus==1.3.2",
        "pandas==1.1.1",
        "pyyaml==5.3.1",
        "snowflake-sqlalchemy==1.2.3",
        "oauth2client==4.1.3",
        "inflection==0.5.1",
        "colorama==0.4.3",
        "luddite==1.0.1",
        "packaging==20.4",
    ],
    python_requires=REQUIRES_PYTHON,
    entry_points={"console_scripts": ["sheetwork = core.main:main"]},
    packages=find_packages(),
    license="MIT",
    url="https://github.com/bastienboutonnet/sheetwork",
    download_url="https://github.com/bastienboutonnet/sheetwork/archive/v1.0.0b3.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
