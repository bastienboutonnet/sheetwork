from .mockers import TO_CAST_DF, CAST_DF, generate_test_df


CASTING_DICT = {
    "col_int": "int",
    "col_varchar": "varchar",
    "created_date": "date",
}


def test_cast_pandas_dtypes():
    from core.utils import cast_pandas_dtypes

    to_cast = generate_test_df(TO_CAST_DF)
    cast_df = cast_pandas_dtypes(to_cast, CASTING_DICT)
    expected_cast = generate_test_df(CAST_DF)

    assert cast_df.to_dict() == expected_cast.to_dict()

