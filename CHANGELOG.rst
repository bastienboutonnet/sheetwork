sheetwork 1.0.0 (2020-10-11)
============================

Bug Fixes
---------

- `#150 <https://github.com/bastienboutonnet/sheetwork/issues/150>`_: Columns that are now mentioned in the sheet.yml are first checked for presence in the sheet and ignored or skipped if not present with warning.


- `#155 <https://github.com/bastienboutonnet/sheetwork/issues/155>`_: Schema specification hierarchy is fixed: Flags > Config > Project. @jflairie


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


- `#161 <https://github.com/bastienboutonnet/sheetwork/issues/161>`_: Simplify ``SheetBag`` internals: `check_table` is moved to the db adapter


- `#163 <https://github.com/bastienboutonnet/sheetwork/issues/163>`_: Fixes broken interactive flow of asking whether to push to db.


- `#171 <https://github.com/bastienboutonnet/sheetwork/issues/171>`_: CLI logging/progress messages are now timed


- `#173 <https://github.com/bastienboutonnet/sheetwork/issues/173>`_: Sheetwork now uses an adaptor/plugin design to allow and facilitate extensions of the tool to other databases.


- `#193 <https://github.com/bastienboutonnet/sheetwork/issues/193>`_: CLI arguments are now POSIX


- `#207 <https://github.com/bastienboutonnet/sheetwork/issues/207>`_: An proper sheetwork error is thrown when you do not provide a command to ``sheetwork`` in CLI


- `#208 <https://github.com/bastienboutonnet/sheetwork/issues/208>`_: Profile error messages are now a bit more helpful and more nicely formatted


- `#210 <https://github.com/bastienboutonnet/sheetwork/issues/210>`_: Use and try to fix most warnings from Pylance in an attempt to have more strict typing


- `#215 <https://github.com/bastienboutonnet/sheetwork/issues/215>`_: Poetry is now used a the package and dependencies manager


- `#218 <https://github.com/bastienboutonnet/sheetwork/issues/218>`_: When passing ``--log-level debug`` in CLI the format of the console output looks more like proper logs instead of the pretty prints to make following logs more easy
