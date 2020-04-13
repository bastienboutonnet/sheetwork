from setuptools import find_packages, setup

NAME = "sheetload"
VERSION = "1.0.0a1"
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
    entry_points={"console_scripts": ["sheetload=core.main:main"]},
    packages=find_packages(),
    license="MIT",
    url="https://github.com/bastienboutonnet/sheetload",
    download_url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
