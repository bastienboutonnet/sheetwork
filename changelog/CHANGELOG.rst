This is an automatically generated changelog. Please consult the reformatted one which resides in the repository's root as ``CHANGELOG.rst``.

.. towncrier release notes start

sheetwork v1.0.1 Nicolas Jaar - Don't Break My Love (2020-11-25)
=============================

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



Under The Hood/Misc
-------------------

- `#229 <https://github.com/bastienboutonnet/sheetwork/issues/229>`_: Uses the new `service_account()` wrapper from `gspread` to authenticate to a service account. This brings some stability with regards to the deprecation of `oauth2` by google as the converstion is now handled by `gspread`.
