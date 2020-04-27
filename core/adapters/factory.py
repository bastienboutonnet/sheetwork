from typing import Dict, Type
from core.adapters.base.impl import BaseAdapter

Adapter = BaseAdapter


class AdapterContainer:
    def __init__(self):
        self.adatpters = None
        self.adapter_types: Dict[str, Type[Adapter]] = dict()
