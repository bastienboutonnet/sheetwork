This is an automatically generated changelog. Please consult the reformatted one which resides in the repository's root as ``CHANGELOG.rst``.

.. towncrier release notes start

sheetwork v1.0.5 (2021-01-09)
=============================

Bug Fixes
---------

- `#320 <https://github.com/bastienboutonnet/sheetwork/issues/320>`_: ``--version`` was broken because of a bad indentation choice. It is now fixed. This PR also removed some ugly left over prints. Apologies about this...


sheetwork v1.0.4 (2020-12-22)
=============================

Under The Hood/Misc
-------------------

- `#295 <https://github.com/bastienboutonnet/sheetwork/issues/295>`_: ``make_df_from_worksheet()`` now throws more errors and wraps them into the a custom exception named ``SheetLoadingError``. The previous behaviour was causing too much silentness and prevented user from seeing errors such as the ones highlighted in #292


- `#304 <https://github.com/bastienboutonnet/sheetwork/issues/304>`_: Empty headers are a pain, but not uncommon. More often than not, users have their google sheet start on the second or so row. This causes all sorts of unexpected behaviour when we're trying to land the table into the database as we don't know what column names to give.

  This PR implements a check of whether the header contains empty column names and alerts raises an error asking the user to fix the GoogleSheet from the source.

  In the next feature release (v1.1.0) we will allow users to specify the index of the header so that they do not have to change it in the source in case that is not an option or so.

  **Contributed by: @jflairie**


- `#306 <https://github.com/bastienboutonnet/sheetwork/issues/306>`_: Adds test coverage to many more parts of the code bringing it from 67% to 80+


sheetwork v1.0.3 (2020-12-12)
=============================

Bug Fixes
---------

- `#290 <https://github.com/bastienboutonnet/sheetwork/issues/290>`_: Boolean data-type casting was buggy somewhere between ``v1.0.0`` and ``v1.0.2`` and resulted to all non null strings to be given a ``True`` value. We now handle boolean conversion explicitly by mapping strings ``false`` and ``true`` to python ``False`` and ``True`` that pandas can actually understand and expose to the database appropriately. **NOTE**: If the user asks for a column to be cast to boolean but this column contains any other string than the aforementioned ones (and capitalised
  variants) ``sheetwork`` will throw a ``ColumnNotBooleanCompatibleError`` that will help the user locate the offending column as well as the offending value(s).


sheetwork v1.0.1 Nicolas Jaar - Don't Break My Love (2020-11-25)
================================================================

Bug Fixes
---------

- `#252 <https://github.com/bastienboutonnet/sheetwork/issues/252>`_: The logger file handler now always prints `DEBUG`-and-up level messages



Features
--------

- `#231 <https://github.com/bastienboutonnet/sheetwork/issues/231>`_: * Users can now use their **end user/personal** account. Previously, it was only possible to authenticate using a **service_account**. Thanks for recent changes in `gspread` the auth flow allows for differenciation between end user and service account that is much simpler so we ported this to here https://github.com/burnash/gspread/pull/762
  * **Internal Note/Curiosity**: To make `oauth` work we had to patch `gspread`'s default credential paths (see https://github.com/burnash/gspread/issues/826). Hopefully, this is temporary.


- `#253 <https://github.com/bastienboutonnet/sheetwork/issues/253>`_: Success of failure message for database table creation now fully qualifies the table (`<database>.<schema>.<table>`). This makes the messages a lot more usable to a user who might want to copy paste and check that the table has been correctly created. (Also some ugly hardcoding in the catalog queries have been squashed).


- `#257 <https://github.com/bastienboutonnet/sheetwork/issues/257>`_: Allows more granular control over table (and schema) creation via the `sheetwork_project.yml` file:
  - `always_create_table` is now the new way to ensure that tables always get created. Whether the table is going to be replaced or trucated is governed by the `desctructive_create_table` flag. Closes #251

  **IMPORTANT NOTE**: `always_create` is now internally remapped to `always_create_table` and will be deprecated in a future major release.


- `#262 <https://github.com/bastienboutonnet/sheetwork/issues/262>`_: The target schema now gets created if `always_create_schema` is `True`. Under the hood: SnowflakeAdaptor checks if the schema already exists on the database before creating it.


- `#265 <https://github.com/bastienboutonnet/sheetwork/issues/265>`_: In order to override (or set on demand) object creation (tables and schemas) we now provide the following CLI arguments:
  - `create-table`
  - `create-schema`
  - `destructive-create-table`

  These arguments are "companions" which can override the following project configuration arguments:
  - `always_create_table`
  - `always_create_schema`
  - `destructive_create_table`

  **IMPORTANT**:CLI flags will override whatever is already present in the project config

- `#282 <https://github.com/bastienboutonnet/sheetwork/issues/282>`_: Sheetwork now retries obtaining google sheets up to 3 times (max duration 10s) if it hits an ``APIError`` because the end-user or service account was rate limited or other common service availability errors encountered by end users.

  Check the PR to see the exact set of ``APIError`` that sheetwork will attempt retrying for.


Under The Hood/Misc
-------------------

- `#229 <https://github.com/bastienboutonnet/sheetwork/issues/229>`_: Uses the new `service_account()` wrapper from `gspread` to authenticate to a service account. This brings some stability with regards to the deprecation of `oauth2` by google as the converstion is now handled by `gspread`.
