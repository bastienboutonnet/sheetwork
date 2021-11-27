"""ABC to define what an concrete Connection object should look like."""
import abc


class BaseCredentials(abc.ABC):
    """Base class to define basic API contract for a Credentials class and its methods."""

    @abc.abstractmethod
    def parse_and_validate_credentials(self):
        ...


class BaseConnection(abc.ABC):  # noqa D101
    @abc.abstractmethod
    def generate_engine(self) -> None:
        raise NotImplementedError()


def check_db_type_compatibility(field: str, expected_db: str) -> str:
    """Pydantic validation decocator that checks that the a field has an expected value.

    Args:
        field (str): Value to check.
        expected_db (str): Name of the expected database.

    Returns:
        str: the value of the field to check if validation is passed.
    """
    assert field == expected_db
    return field
