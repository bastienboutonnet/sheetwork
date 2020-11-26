# Contributing

Thanks for looking into making `sheetwork` better! We have some loosely defined rules, preferences etc. to make the process a bit smoother but above all, don't let that deter you from contributing.

> ⚠️ **Wanna use `sheetwork` with another database than Snowflake?** ✨ Let's talk!! 🎉 I'm really eager to grow the database adapters for `sheetwork`. Create an issue on GitHub or DM me on [Discord](https://discord.gg/5GnNNb)

## How can you contribute?

- It **usually starts with creating an issue** (reporting a bug, or discussing a feature). In fact, even if you don't know how to code it or don't have the time, you're already helping out by pointing out potential issues or functionality that you would like to see implemented.
- **Creating an issue is not necessary!**
  - See an already published issue that you think you can tackle? Drop a line on it and get cracking or ask questions on how you can help.
  - Feel really confident about the implementation of something and don't mind just putting a PR against the repo? Why the hell not.

## Advised Process/Conventions

### Git stuff

It's apprecited if you could follow a few of the guidelines around branch and PR naming, but don't let that deter you from contributing.

#### Branches

Below is the preferred format:

```bash
feat/my_awesome_feature
fix/describe_what_you_fix
refactor/describe_what_you_refactor
docs/what_is_changing_what_you_are_explaining
```

#### Pull Requests

We follow [conventional-commits](https://www.conventionalcommits.org/en/v1.0.0/) to standardise commits, and help with CHANGELOG.md generation.
If you feel like you don't want to bother with it it's ok but we will rename your PR at merge time or during the review to make sure the git history is kept consistent.

**PR linting will fail if the PR isn't name with one of prefixes below**. Don't worry though, we'll get that sorted before merging 🎉

Here is what your PR names should ideally look like:

```txt
feat: my awesome feature
fix: relax version requiremtents on pandas
docs: document new feature
refactor: move cleanups into its own class
```

Use the template provided for you as a guide to cover most aspects of your PR. Feel free to delete stuff you think isn't relevant. The template is **just** a guide.

#### Commits and Conventions

Please follow generally accepted git best practices by using **descriptive commit messages**, **imperative mood** ("Fix typo" instead of "Fixing typo" for example), and feel free to clean up your branch by squashing any commits you deem will not need to be there.

We'll squash your PR at merge time.

#### Fork it, let's go! 🥁

Fork the repo and get going. If you're not too experienced with forks, feel free to shoot me a DM on [Discord](https://discord.gg/5GnNNb)

**Shit how do we do this fork thing?**
In most cases it's pretty easy

1. Create a fork from this GitHub account into yours
2. Clone your fork via ssh or http depending on how you like to authenticate and all that. For example:

   ```bash
   git clone git@github.com:<your_username>/sheetwork.git
   ```

3. Modify your code locally
   As you would for a regular cloned repo, `git branch`, `git add`, `git commit`, `git push`.
   The push will go to your fork remote which is totally fine.

4. Create a Pull Request
   When the time comes to merge your code back on the original repo (here). Go to your fork's GitHub page, click the "Pull Request" button and choose to merge into the original repo.

5. If you need to ingest changes from the fork. Say, you want to update or pull the origial repo you can add the original repo as another remote called `upstream` (actually you can name if whatever you want but usually that's how people name this) to your config like so:

   ```bash
   git remote add upstream https://github.com/bastienboutonnet/sheetwork.git
   ```

### Python Stuff

#### Formatting

- Please use `black` to format your python code. CI checks on the PR will fail if files don't comply with it. **We can of course fix this later on in the review process**. Black comes as an extention in most IDEs, formats things for you and is just a breeze. If you don't know what black is, here's [Black's GitHub](https://github.com/psf/black).
- If you could make sure you don't leave trailing whitespace around that would be great (Most IDEs will have an option for that)
- Finally, make sure you introduce an empty line at the end of your files (Also very easy to set this up in your IDE).

#### Linting/Type Hinting

- It is recommended to use Type Hinting and have [`mypy`](http://mypy-lang.org/) enabled as your linter. Most IDE's have an extension or a way to help with this. Typing isn't necessary but **really, really** preferred.
- [`flake8`](https://flake8.pycqa.org/en/latest/) is also a great linter to run, it'll help you catch a few potential bugs early on and push you to enforce common [PEP8](https://www.python.org/dev/peps/pep-0008/) rules

### Development

The whole package is managed using [Poetry](https://python-poetry.org/). It's really really good and ensures reproducibility. **If this is holding you up from contributing feel free to shoot me a DM on [Discord](https://discord.gg/5GnNNb) and I can deploy good old `setup.py` files for you to use `pip install -e .` in your venv management tool of choice, although I think `pip` install edidable from current folder should work --but not sure.**

1. [Install Poetry on your system](https://python-poetry.org/docs/#installation) --I personally recommend installing it via [`pipx`](https://github.com/pipxproject/pipx) but that's entirely up to you.
2. `cd` to your fork and run `poetry install` in the root folder of the repo. Poetry will create a virtual environment for python, install dependencies and install `sheetwork` in **editable** mode so that you can directly run and test `sheetwork` as you develop without having to install over and over.
3. The easiest way to activate the poetry virtual env is to call `poetry shell` it'll wrap around your shell and and activate the sheetwork venv, to deactivate or get out of the shell simply type `exit`. More info on [the Poetry documentation website](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment)

### Testing

If you're comfortable writing tests for your features, I use the [`pytest`](https://docs.pytest.org/en/stable/) framework. It'll be installed automatically when you set up your poetry environment. If you don't know how to write tests that's fine, we'll work it out with you during the review process 💪🏻

Have a look into the `tests/` folder for how the tests are written and if you want to trigger tests locally you can do so from the root of the repo with

```bash
pytests tests/
```

## Wow you're still reading!? Thanks a lot for taking the time to make sheetwork better! ✨

Thanks for your interest in contributing. I really appreciate it and I hope those guidelines don't sound too much. If you have any questions feel free to DM me or reach out the community on [Discord](https://discord.gg/5GnNNb).
