sheetwork 1.0.7 Nicolas Jaar - A Coin in Nine Hands (2021-01-27)
================================================================

Features
--------

- `#337 <https://github.com/bastienboutonnet/sheetwork/issues/337>`_: "Yes" and "No" strings will now get mapped to ``True`` and ``False`` if a user asks for a column with such content to be cast to boolean.

sheetwork v1.0.6 Nicolas Jaar - Garden of Eden (2021-01-17)
===========================================================

Bug Fixes
---------

- `#323 <https://github.com/bastienboutonnet/sheetwork/issues/323>`_: Columns to be converted to booleans which contained empty strings were converted as ``np.nan`` after sheet ingestion. Because this value had not been added to the allowable values for boolean conversion, users who had null values in their sheets could have ran into the app raising an error and not wanting to convert. Given that it is perfectly fine to have ``null`` values among booleans it is now made possible.
sheetwork v1.0.5 Nicolas Jaar - Encore (2021-01-09)
===================================================

Bug Fixes
---------

- `#320 <https://github.com/bastienboutonnet/sheetwork/issues/320>`_: ``--version`` was broken because of a bad indentation choice. It is now fixed. This PR also removed some ugly left over prints. Apologies about this 🤦

sheetwork v1.0.4 Nicolas Jaar - Mi Mujer (2020-12-22)
=============================

Under The Hood/Misc
-------------------

- `#295 <https://github.com/bastienboutonnet/sheetwork/issues/295>`_: ``make_df_from_worksheet()`` now throws more errors and wraps them into the a custom exception named ``SheetLoadingError``. The previous behaviour was causing too much silentness and prevented user from seeing errors such as the ones highlighted in `#292 <https://github.com/bastienboutonnet/sheetwork/issues/292>`_


- `#304 <https://github.com/bastienboutonnet/sheetwork/issues/304>`_: Empty headers are a pain, but not uncommon. More often than not, users have their google sheet start on the second or so row. This causes all sorts of unexpected behaviour when we're trying to land the table into the database as we don't know what column names to give.

  This PR implements a check of whether the header contains empty column names and alerts raises an error asking the user to fix the GoogleSheet from the source.

  In the next feature release (v1.1.0) we will allow users to specify the index of the header so that they do not have to change it in the source in case that is not an option or so.

  **Contributed by:** `@jflairie <https://github.com/jflairie>`_



sheetwork v1.0.3 Nicolas Jaar - Space Is Only Noise If You Can See (2020-12-12)
===============================================================================

Bug Fixes
---------

- `#290 <https://github.com/bastienboutonnet/sheetwork/issues/290>`_: Boolean data-type casting was buggy somewhere between ``v1.0.0`` and ``v1.0.2`` and resulted to all non null strings to be given a ``True`` value. We now handle boolean conversion explicitly by mapping strings ``false`` and ``true`` to python ``False`` and ``True`` that pandas can actually understand and expose to the database appropriately. **NOTE**: If the user asks for a column to be cast to boolean but this column contains any other string than the aforementioned ones (and capitalised
  variants) ``sheetwork`` will throw a ``ColumnNotBooleanCompatibleError`` that will help the user locate the offending column as well as the offending value(s).



sheetwork v1.0.2 Nicolas Jaar - Killing Time (2020-12-01)
=========================================================

Features
--------

- `#282 <https://github.com/bastienboutonnet/sheetwork/issues/282>`_: Sheetwork now retries obtaining google sheets up to 3 times (max duration 10s) if it hits an ``APIError`` because the end-user or service account was rate limited or other common service availability errors encountered by end users.

  Check the PR to see the exact set of ``APIError`` that sheetwork will attempt retrying for.



sheetwork v1.0.1 Nicolas Jaar - Don't Break My Love (2020-11-25)
=============================================================================

Bug Fixes
---------

- `#252 <https://github.com/bastienboutonnet/sheetwork/issues/252>`_: The logger file handler now always prints ``DEBUG``-and-up level messages



Features
--------

- `#231 <https://github.com/bastienboutonnet/sheetwork/issues/231>`_: * Users can now use their **end user/personal** account. Previously, it was only possible to authenticate using a **service_account**. Thanks for recent changes in ``gspread`` the auth flow allows for differenciation between end user and service account that is much simpler so we ported this to here https://github.com/burnash/gspread/pull/762

  * **Internal Note/Curiosity**: To make ``oauth`` work we had to patch ``gspread``'s default credential paths (see https://github.com/burnash/gspread/issues/826). Hopefully, this is temporary.


- `#253 <https://github.com/bastienboutonnet/sheetwork/issues/253>`_: Success of failure message for database table creation now fully qualifies the table (``<database>.<schema>.<table>``). This makes the messages a lot more usable to a user who might want to copy paste and check that the table has been correctly created. (Also some ugly hardcoding in the catalog queries have been squashed).


- `#257 <https://github.com/bastienboutonnet/sheetwork/issues/257>`_: Allows more granular control over table (and schema) creation via the ``sheetwork_project.yml`` file:
  - ``always_create_table`` is now the new way to ensure that tables always get created. Whether the table is going to be replaced or trucated is governed by the ``desctructive_create_table`` flag. Closes #251

  **IMPORTANT NOTE**: ``always_create`` is now internally remapped to ``always_create_table`` and will be deprecated in a future major release.


- `#262 <https://github.com/bastienboutonnet/sheetwork/issues/262>`_: The target schema now gets created if ``always_create_schema`` is ``True``. Under the hood: SnowflakeAdaptor checks if the schema already exists on the database before creating it.


- `#265 <https://github.com/bastienboutonnet/sheetwork/issues/265>`_: In order to override (or set on demand) object creation (tables and schemas) we now provide the following CLI arguments:
  - ``create-table``
  - ``create-schema``
  - ``destructive-create-table``

  These arguments are "companions" which can override the following project configuration arguments:
  - ``always_create_table``
  - ``always_create_schema``
  - ``destructive_create_table``

  **IMPORTANT**:CLI flags will override whatever is already present in the project config


- `#282 <https://github.com/bastienboutonnet/sheetwork/issues/282>`_: Sheetwork now retries obtaining google sheets up to 3 times (max duration 10s) if it hits an ``APIError`` because the end-user or service account was rate limited or other common service availability errors encountered by end users.

  Check the PR to see the exact set of ``APIError`` that sheetwork will attempt retrying for.

Under The Hood/Misc
-------------------

- `#229 <https://github.com/bastienboutonnet/sheetwork/issues/229>`_: Uses the new ``service_account()`` wrapper from ``gspread`` to authenticate to a service account. This brings some stability with regards to the deprecation of ``oauth2`` by google as the converstion is now handled by ``gspread``.



sheetwork 1.0.0 Nicolas Jaar (2020-10-11)
=========================================

Bug Fixes
---------

- `#150 <https://github.com/bastienboutonnet/sheetwork/issues/150>`_: Columns that are now mentioned in the sheet.yml are first checked for presence in the sheet and ignored or skipped if not present with warning.


- `#155 <https://github.com/bastienboutonnet/sheetwork/issues/155>`_: Schema specification hierarchy is fixed: Flags > Config > Project.


- `#206 <https://github.com/bastienboutonnet/sheetwork/issues/206>`_: Pandas dataframe casting is disabled due to issues with mixed ints and strings (see #205, #204)


- `#221 <https://github.com/bastienboutonnet/sheetwork/issues/221>`_: Attempts to reintroduce datatype casting to solve issue with dates converion (see #216 for issue). Since the mixed str and ints issue is not solved on pandas side, int conversion doesn't actually happen (for now Snowflake deals with it ok and converts to the reguested int format).



Features
--------

- `#151 <https://github.com/bastienboutonnet/sheetwork/issues/151>`_: Raises errors when a sheet contains duplicate columns


- `#156 <https://github.com/bastienboutonnet/sheetwork/issues/156>`_: Interactive cleanup is a bit more intereactive


- `#169 <https://github.com/bastienboutonnet/sheetwork/issues/169>`_: Adds ``InitTask`` to ``sheetwork`` to ease users set their projects up.


- `#195 <https://github.com/bastienboutonnet/sheetwork/issues/195>`_: Sheetwork now checks for available updates on start (provided you have an internet connection)



Under The Hood/Misc
-------------------

- `#154 <https://github.com/bastienboutonnet/sheetwork/issues/154>`_: Logging to file always debug, logging messages in CLI look more like pretty prints.


- `#161 <https://github.com/bastienboutonnet/sheetwork/issues/161>`_: Simplify ``SheetBag`` internals: ``check_table`` is moved to the db adapter


- `#163 <https://github.com/bastienboutonnet/sheetwork/issues/163>`_: Fixes broken interactive flow of asking whether to push to db.


- `#171 <https://github.com/bastienboutonnet/sheetwork/issues/171>`_: CLI logging/progress messages are now timed


- `#173 <https://github.com/bastienboutonnet/sheetwork/issues/173>`_: Sheetwork now uses an adaptor/plugin design to allow and facilitate extensions of the tool to other databases.


- `#193 <https://github.com/bastienboutonnet/sheetwork/issues/193>`_: CLI arguments are now POSIX


- `#207 <https://github.com/bastienboutonnet/sheetwork/issues/207>`_: An proper sheetwork error is thrown when you do not provide a command to ``sheetwork`` in CLI


- `#208 <https://github.com/bastienboutonnet/sheetwork/issues/208>`_: Profile error messages are now a bit more helpful and more nicely formatted


- `#210 <https://github.com/bastienboutonnet/sheetwork/issues/210>`_: Use and try to fix most warnings from Pylance in an attempt to have more strict typing


- `#215 <https://github.com/bastienboutonnet/sheetwork/issues/215>`_: Poetry is now used a the package and dependencies manager


- `#218 <https://github.com/bastienboutonnet/sheetwork/issues/218>`_: When passing ``--log-level debug`` in CLI the format of the console output looks more like proper logs instead of the pretty prints to make following logs more easy


Previous releases
=================

There have been releases before. But at the time we were managing things differently. The old changelog can be consulted in `_old_changelog.md <_old_changelog.md>`_
