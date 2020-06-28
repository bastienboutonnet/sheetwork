import abc


class BaseCredentials(metaclass=abc.ABCMeta):
    # TODO: Need to firgure out how to impose properties to be set
    # and provided by the init

    @abc.abstractmethod
    def validate_credentials(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def parse_credentials(self):
        raise NotImplementedError()


class BaseConnection(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_engine(self):
        raise NotImplementedError()
