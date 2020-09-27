import importlib
from types import ModuleType
from typing import Dict

from core.config.profile import Profile

# specify some more helpful types
Adapter = ModuleType


class AdapterContainer:
    def __init__(self):
        self.adatpters = {
            "snowflake": {
                "db_adapter": {"module": "core.adapters.impl", "class_name": "SnowflakeAdapter"},
                "connection": {
                    "module": "core.adapters.connection",
                    "class_name": "SnowflakeConnection",
                },
                "credentials": {
                    "module": "core.adapters.connection",
                    "class_name": "SnowflakeCredentials",
                },
            }
        }
        self.adapter_name: str = str()

    def register_adapter(self, profile: Profile) -> None:
        adapter_to_register = profile.profile_dict["db_type"]
        if adapter_to_register in self.adatpters.keys():
            self.adapter_name = adapter_to_register
        else:
            raise NotImplementedError(f"{adapter_to_register} is not implemented in sheetwork.")

    def load_plugins(
        self,
    ) -> Dict[str, Adapter]:
        plugins_collection = {}
        for plugin_type, module_info in self.adatpters[self.adapter_name].items():
            module = importlib.import_module(module_info["module"])
            plugins_collection[plugin_type] = getattr(module, module_info["class_name"])

        return plugins_collection
