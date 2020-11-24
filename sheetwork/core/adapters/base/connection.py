"""ABC to define what an concrete Connection object should look like."""
import abc


class BaseCredentials(abc.ABC):
    """Base class to define basic API contract for a Credentials class and its methods."""

    @abc.abstractmethod
    def validate_credentials(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def parse_credentials(self) -> None:
        raise NotImplementedError()


class BaseConnection(abc.ABC):  # noqa D101
    @abc.abstractmethod
    def generate_engine(self) -> None:
        raise NotImplementedError()
