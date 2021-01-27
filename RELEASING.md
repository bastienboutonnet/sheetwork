# Releasing & Packaging

I'm writing this down here because I always forget...

## Preparing the release

- Make sure all code is merged
- On the repo root call `towncrier` to generate the changelog. I usually like to do a `--draft` to make sure things are peachy first.

  ```bash
  towncrier --version <insert_version> --draft
  ```

- When the draft looks good I just run it again without draft.
- `cd changelog/`, news fragments should be deteted if I have chosen correctly in the interaction flow. If not delete them.
- `cmd + c, cmd + p` changelog into the main repo [`CHANGELOG.rst`](CHANGELOG.rst)
- Reformat it a bit (add the release pretty name). Make sure to add `@username` to credit contributors other than myself.
- Bump the version with `bumpversion`, I'll generally do a `--dry-run` first to make sure all is fine and dandy.

  ```bash
  bumpversion --tag release --new-version 1.0.3 --verbose --allow-dirty --dry-run
  ```

- `git push --follow-tags` this will take care of pushing the bump commit and changes.

## Releasing the package with Poetry

- `poetry build` this will make source and wheel dist files.
- Send to test PyPI. If it isn't configured already do the following:

  ```bash
  poetry config repositories.testpypi https://test.pypi.org/legacy/
  ```

- `poetry publish -r testpypi` this will send it over to the test repo
- build a new temporary `venv` and try to install it from PyPI test:

  ```bash
  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sheetwork
  ```

- if it installs and runs on a test sheet and all that fun stuff then publish it to **the real PyPI** :sparkles:
- `poetry publish`
