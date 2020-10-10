import importlib
from typing import Type

from sheetwork.core.adapters.base.connection import BaseConnection, BaseCredentials
from sheetwork.core.adapters.base.impl import BaseSQLAdapter
from sheetwork.core.config.profile import Profile


class AdapterContainer:
    def __init__(self):
        self.adatpters = {
            "snowflake": {
                "sql_adapter": {
                    "module": "sheetwork.core.adapters.impl",
                    "class_name": "SnowflakeAdapter",
                },
                "connection_adapter": {
                    "module": "sheetwork.core.adapters.connection",
                    "class_name": "SnowflakeConnection",
                },
                "credentials_adapter": {
                    "module": "sheetwork.core.adapters.connection",
                    "class_name": "SnowflakeCredentials",
                },
            }
        }
        self.adapter_name: str = str()
        self.credentials_adapter: Type[BaseCredentials] = BaseCredentials
        self.connection_adapter: Type[BaseConnection] = BaseConnection
        self.sql_adapter: Type[BaseSQLAdapter] = BaseSQLAdapter

    def register_adapter(self, profile: Profile) -> None:
        adapter_to_register = profile.profile_dict["db_type"]
        if adapter_to_register in self.adatpters.keys():
            self.adapter_name = adapter_to_register
        else:
            raise NotImplementedError(f"{adapter_to_register} is not implemented in sheetwork.")

    def load_plugins(self) -> None:
        for adap, module_info in self.adatpters[self.adapter_name].items():
            module = importlib.import_module(module_info["module"])
            setattr(self, adap, getattr(module, module_info["class_name"]))
