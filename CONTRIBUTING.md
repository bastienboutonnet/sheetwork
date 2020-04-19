# Contributing

Thanks for looking into making `sheetwork` better! We have some loosely defined rules, preferences etc. to make the process a bit smoother but above all, don't let that deter you from contributing.

## How can you contribute?

- It **usually starts with creating an issue** (reporting a bug, or discussing a feature). In fact, even if you don't know how to code it or don't have the time, you're already helping out by pointing out potential issues or functionality that you would like to see implemented.
- **Creating an issue is not necessary!**
  - See an already published issue that you think you can tackle? Drop a line on it and get cracking or ask questions on how you can help.
  - Feel really confident about the implementation of something and don't mind just putting a PR against the repo? Why the hell not.

## Advised Process/Conventions

### Git stuff

Please name your branch with a prefix denoting the type of change you're makeing. Generally contributions fall within the following categories but if you don't find yours feel free to get creative:

#### Branches

```bash
feature/my_awesome_feature
fix/describe_what_you_fix
refactor/describe_what_you_refactor
docs/what_is_changing_what_you_are_explaining
```

#### Pull Requests

Please prefix your PRs with the same prefix you gave your branch, feel free to use a different title message. **PR linting will fail if the PR isn't name with one of the following prefixes**. For example:

```txt
Feature: My awesome feature
Fix: Relax version requiremtents on pandas
Docs: Document new feature
```

Use the template provided for you as a guide to cover most aspects of your PR. Feel free to delete stuff you think isn't relevant. The template is **just** a guide.

#### Commits and Conventions

Please follow generally accepted git best practices by using **descriptive commit messages**, **imperative mood** ("Fix typo" instead of "Fixing typo" for example), and feel free to clean up your branch by squashing any commits you deem will not need to be there. Also totally OK to squash the entire branch into one commit. Note, most likely, I will squash and merge your branch at the point of integration anyway.

#### Fork it!

Easiest is probably to fork the repo, do your work and push back to the repo. I can give a few contributor seats but it may run out or I may have to kick people out which isn't really fun.

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

- Please use `black` to format your python code. No one likes to spend hours discussing code style and PRs failing to comply to black will fail CI checks anyway. Black comes as an extention in most IDEs, formats things for you and is just a breeze. If you don't know what black is, here's [Black's GitHub](https://github.com/psf/black).
- Don't leave trailing whitespace lying around (also easy to knock off or hightlight automatically in your IDE).
- Don't forget an empty line at the end of all files (yes, your IDE or an extention can do it for you!).

#### Linting

- It is recommended to use Type Hinting and have [`mypy`](http://mypy-lang.org/) enabled as your linter. Most IDE's have an extension or a way to help with this. Typing isn't necessary but **really, really** preferred.

### Development

1. It is highly recommended to make a virtual environment **just** for developing the app so you have a clean slate and don't end up messing your previously working version of it.
2. Activate your venv
3. Clone your fork wherever you like to keep your repos
4. Navigate to the repo's folder's root in your terminal
5. Install the app from this local source in `--editable` mode so that any changes you make will directly be reflected. You won't need to install it over and over again to test it!

    ```bash
    pip install -e .
    ```

6. Make sure you also install the development pip requirements which include testing libraries etc. (Note. The app's basic requirement will be installed in the previous step, so no need to care for this one.)

    ```bash
    pip install -r dev-pip-requirements.txt
    ```

### Testing

Would be really nice if you could write tests for your functionality but this is not necessary or always possible. If the code owner is adament you should write a test they will guide you in the PR process. If you feel like writing tests as part of your PR (Thanks in advance). We're currently using the `pytest` framework.

Have a look into the `tests/` folder for how the tests are written and if you want to trigger tests locally you can do so from the root of the repo with

```bash
pytests tests/
```

## Wow you're still reading!? Thanks a lot for taking the time to make sheetwork better!

Thanks for your interest in contributing. I really appreciate it and I hope those guidelines don't sound too much.
