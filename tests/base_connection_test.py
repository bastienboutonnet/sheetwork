def test_check_db_type_compatibility():
    from sheetwork.core.adapters.base.connection import check_db_type_compatibility

    field_value = check_db_type_compatibility("a", "a")
    assert field_value == "a"
