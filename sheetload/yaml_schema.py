validation_schema = {
    "sheets": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "sheet_name": {"required": True, "type": "string"},
                "sheet_key": {"required": True, "type": "string"},
                "worksheet": {"required": False, "type": "string"},
                "target_schema": {"required": True, "type": "string"},
                "target_table": {"required": True, "type": "string"},
                "columns": {
                    "type": "list",
                    "required": False,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"required": True, "type": "string", "maxlength": 255},
                            "datatype": {
                                "required": True,
                                "type": "string",
                                "regex": "(?i)^(int|varchar|variant|numeric|boolean|timestamp_ntz)$",
                            },
                            "identifier": {"required": False, "type": "string"},
                        },
                    },
                },
                "excluded_columns": {
                    "anyof_type": ["list", "string"],
                    "required": False,
                    "schema": {"type": "string"},
                },
            },
        },
    }
}
