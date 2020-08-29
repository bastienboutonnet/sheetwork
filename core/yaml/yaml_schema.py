config_schema = {
    "sheets": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "sheet_name": {"required": True, "type": "string"},
                "sheet_key": {"required": True, "type": "string"},
                "worksheet": {"required": False, "type": "string"},
                "target_schema": {"required": False, "type": "string"},
                "target_table": {"required": True, "type": "string"},
                "snake_case_camel": {"required": False, "type": "boolean"},
                "columns": {
                    "type": "list",
                    "required": False,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {
                                "required": True,
                                "type": "string",
                                "maxlength": 255,
                            },
                            "datatype": {
                                "required": True,
                                "type": "string",
                                "regex": "(?i)^(int|varchar|numeric|boolean|date|timestamp_ntz)$",
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

profiles_schema = {
    "profiles": {
        "required": True,
        "type": "dict",
        "valuesrules": {
            "type": "dict",
            "schema": {
                "target": {"required": True, "type": "string"},
                "outputs": {
                    "required": True,
                    "type": "dict",
                    "valuesrules": {
                        "type": "dict",
                        "schema": {
                            "db_type": {"required": True, "type": "string"},
                            "account": {"required": False, "type": "string"},
                            "user": {"required": True, "type": "string"},
                            "password": {"required": True, "type": "string"},
                            "role": {"required": False, "type": "string"},
                            "database": {"required": False, "type": "string"},
                            "warehouse": {"required": False, "type": "string"},
                            "schema": {"required": False, "type": "string"},
                            "guser": {"required": True, "type": "string"},
                        },
                    },
                },
            },
        },
    }
}

project_schema = {
    "name": {"required": True, "type": "string"},
    "target_schema": {"required": False, "type": "string"},
    "always_create": {"required": False, "type": "boolean"},
    "paths": {
        "type": "dict",
        "required": False,
        "schema": {
            "profile_dir": {"required": False, "type": "string"},
            "sheet_config_dir": {"required": False, "type": "string"},
        },
    },
}
