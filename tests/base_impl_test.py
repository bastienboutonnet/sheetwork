def test_sqlalchemy_dtypes():
    import sqlalchemy
    from sheetwork.core.adapters.base.impl import BaseSQLAdapter
    from sqlalchemy.sql.sqltypes import Numeric

    dtypes_dict = {
        "a": "int",
        "b": "varchar",
        "c": "numeric",
        "d": "boolean",
        "e": "timestamp_ntz",
        "f": "date",
    }
    expected_dict = {
        "a": sqlalchemy.sql.sqltypes.INTEGER,
        "b": sqlalchemy.sql.sqltypes.VARCHAR,
        "c": Numeric(precision=38, scale=18),
        "d": sqlalchemy.sql.sqltypes.BOOLEAN,
        "e": sqlalchemy.sql.sqltypes.TIMESTAMP,
        "f": sqlalchemy.sql.sqltypes.DATE,
    }
    res = BaseSQLAdapter.sqlalchemy_dtypes(dtypes_dict)

    for col, col_type in res.items():
        assert type(expected_dict[col]) == type(col_type)
