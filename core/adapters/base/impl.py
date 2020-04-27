import abc


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
