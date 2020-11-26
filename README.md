![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/bastienboutonnet/sheetwork?include_prereleases) [![codecov](https://codecov.io/gh/bastienboutonnet/sheetwork/branch/dev%2Fnicolas_jaar/graph/badge.svg)](https://codecov.io/gh/bastienboutonnet/sheetwork)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/bastienboutonnet/sheetwork/dev/nicolas_jaar.svg)](https://results.pre-commit.ci/latest/github/bastienboutonnet/sheetwork/dev/nicolas_jaar)
![Sheetwork Build](https://github.com/bastienboutonnet/sheetwork/workflows/Sheetwork%20CI/badge.svg)
![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)
[![Discord](https://img.shields.io/discord/752101657218908281?label=discord)](https://discord.gg/ebSTWq)

# sheetwork 💩🤦

## What is sheetwork?

sheetwork is a handy open-source CLI-tool that allows non-coders to ingest Google Spreadsheets directly into their databases with control over data types, renaming, basic data sanitisation etc.

It offers a "close to no code" workflow that can still live alongside your codebase as all configuration lives in text files and is easily version-controllable. This makes it an ideal tool for teams.

> ⚠️ **warning** `sheetwork` is still in its early inception (don't get fooled by the 1 in the version). Please do some testing before you end up using it in production, and feel free to report bugs.

> **compatibility**:
>
> - Python: 3.6, 3.7, 3.8
>   OS: Mac OSX >10.14, Linux
> - So far all our unit tests work on Windows (tested in GitHub Actions) but no comprehensive testing has been done on this platform.
> - sheetwork currently only offers support for cloud database Snowflake. However, its design follows an adapter pattern (currently in the making) and can be extended to interact with most databases. Feel free to check how you can [contribute](CONTRIBUTING.md) to the project or reach out on [Discord](https://discord.gg/5GnNNb)..

## Why use sheetwork?

Getting google sheets into any database often requires writing custom Python code that interacts with the Google API. That's fine if you can write Python, but it may not always be an option. On top of that, if your workflow requires you to ingest a bunch of sheets you may find yourself **writing the same boiler plate code over and over**. Sheetwork offers a way to bring some DRY practices, standardisation, and simplification to basic google sheet ingestion. **It won't do a lot of transformations and doesn't have room for baking in much transformational logic because we believe this is best done by fully-fledged ETL open-source tools such as [dbt](https://www.getdbt.com/)**.

A handy package to load Google Sheets to your database right from the CLI and with easy configuration via YAML files.

🙋🏻‍♂️ **Want to use `sheetwork` on other databases? Let's talk!** ([Make an issue](https://github.com/bastienboutonnet/sheetwork/issues/new/choose), or ping me on [Discord](https://discord.gg/5GnNNb))

## Installation & Documentation

Head over to the pretty [documentation](https://bastienboutonnet.gitbook.io/sheetwork/).
