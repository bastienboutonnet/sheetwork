import abc
from typing import Any, Dict, Optional

import pandas
from sqlalchemy.types import BOOLEAN, DATE, INTEGER, TIMESTAMP, VARCHAR, Numeric


class BaseSQLAdapter(abc.ABC):
    """sets up required adapter methods"""

    @abc.abstractmethod
    def acquire_connection(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def close_connection(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def upload(self, df: pandas.DataFrame, override_schema: str = str()) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def excecute_query(self, query: str, return_results: bool = False) -> Optional[Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def check_table(self, target_schema: str, target_table: str) -> None:
        raise NotImplementedError()

    @staticmethod
    def sqlalchemy_dtypes(dtypes_dict: Dict[str, Any]) -> Dict[str, Any]:
        dtypes_dict = dtypes_dict.copy()
        dtypes_map: Dict[str, Any] = dict(
            int=INTEGER,
            varchar=VARCHAR,
            numeric=Numeric(38, 18),
            boolean=BOOLEAN,
            timestamp_ntz=TIMESTAMP,
            date=DATE,
        )

        for col, data_type in dtypes_dict.items():
            dtypes_dict.update({col: dtypes_map[data_type]})
        return dtypes_dict
