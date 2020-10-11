# Updating Changelog

This directory contains `newsfragments` which are used by `towncrier` to help automatically generate the `CHANGELOG.md`. These files are **ReST**-formatted.

## How to update the changelog

The `CHANGELOG` is read by users to know what new features are coming up, what bugs are fixed or potentially breaking changes. The description should be written with **users in mind**.

### Create a newsfragment file

Each file should be named like `<ISSUE/PR_NUMBER>.<TYPE>.rst`. `<ISSSUE/PR_NUMBER>` should be the GitHub `#NUMBER` of the issue or PR you worked on.
`<TYPE>` can be any of the following (if you feel your work does not fall under any of these get in touch and we can add more/consider --either make an issue or make it known during the review process):

- `feature`: new user facing features
- `fix`: anything that fixes a bug.
- `misc`: anything that is more "Under the hood". This section could be written with developers in mind, but should still be informative to general users.

For example:
If you worked on a PR introducing a new feature in PR 123, the filename should be `123.feature.rst`

### Writing the content of the newsfragment

As we said earlier, the changelog is mainly for users so we want to make sure we write something users can understand. You should try to be concise but don't compromise on clarity. `towncrier` preserves the paragraphs and formatting introduced in the file (code blocks, lists and so on), but for entries other than `features` it is usually better to stick to a single concise paragraph.
