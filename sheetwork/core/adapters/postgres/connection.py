"""Concrete Postgres Database Connector classes."""

from sheetwork.core.adapters.base.connection import BaseConnection, BaseCredentials


class PostgresCredentials(BaseCredentials):
    """Parses and sets up Postgres credentials object."""

    def __init__(self) -> None:
        """Constructor for postgress credentials."""
        ...

    def validate_credentials(self) -> None:
        """Crendentials structure validator."""
        ...

    def parse_credentials(self) -> None:
        """Credentials parser."""
        ...


class PostgresConnection(BaseConnection):
    """Sets up Postgres connector engine."""

    def __init__(self) -> None:
        """Constructs Postgress connector object."""
        ...

    def generate_engine(self) -> None:
        """Creates a Postgress connection engine."""
        ...
