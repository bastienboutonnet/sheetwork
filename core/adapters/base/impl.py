import abc

from sqlalchemy.types import BOOLEAN, DATE, INTEGER, TIMESTAMP, VARCHAR, Numeric


class BaseAdapter(metaclass=abc.ABCMeta):
    """sets up required adapter methods
    """

    @abc.abstractmethod
    def acquire_connection(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def close_connection(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def upload(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def excecute(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def check_table(self):
        raise NotImplementedError()

    @staticmethod
    def sqlalchemy_dtypes(dtypes_dict) -> dict:
        dtypes_dict = dtypes_dict.copy()
        dtypes_map = dict(
            varchar=VARCHAR,
            int=INTEGER,
            numeric=Numeric(38, 18),
            boolean=BOOLEAN,
            timestamp_ntz=TIMESTAMP,
            date=DATE,
        )

        for col, data_type in dtypes_dict.items():
            dtypes_dict.update({col: dtypes_map[data_type]})
        return dtypes_dict
