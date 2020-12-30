"""Concrete Postgres Database Connector classes."""

from typing import Dict

from pydantic import BaseModel, ValidationError, validator
from sqlalchemy.engine import create_engine

from sheetwork.core.adapters.base.connection import BaseConnection
from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import CredentialsParsingError


class PostgresCredentialsModel(BaseModel):
    """Pydantic credentials validator model for postgres adaptor."""

    db_type: str
    user: str
    password: str
    database: str
    host: str = "localhost"
    port: str = "5432"
    target_schema: str

    @validator("db_type")
    def check_db_type_compatibility(cls, value):
        assert value == "postgres"
        return value


class PostgresCredentials:
    """Parses and sets up Postgres credentials object."""

    def __init__(self, profile: Profile) -> None:
        """Constructor for postgress credentials."""
        self._profile = profile.profile_dict
        self.are_valid_credentials: bool = False
        self._db_type: str = str()
        self.credentials: Dict[str, str] = dict()
        self.user: str = str()
        self.password: str = str()
        self.host: str = str()
        self.port: str = str()
        self.database: str = str()
        self.target_schema: str = str()

    def parse_and_validate_credentials(self) -> None:
        """Parse and validate credentials using pydandic model.

        Pydantic is called first to raise a ValidationError first and cause the app to crash.
        """
        try:
            _credentials = PostgresCredentialsModel(**self._profile)
        except ValidationError as e:
            raise CredentialsParsingError(f"Your profile is not valid \n {e}")

        self.credentials = _credentials.dict()
        self._db_type = self._profile.get("db_type", str())
        self.are_valid_credentials = True
        self.user = self.credentials["user"]
        self.password = self.credentials["password"]
        self.host = self.credentials["host"]
        self.port = self.credentials["port"]
        self.database = self.credentials["database"]
        self.target_schema = self.credentials["target_schema"]


class PostgresConnection(BaseConnection):
    """Sets up Postgres connector engine."""

    def __init__(self, credentials: PostgresCredentials) -> None:
        """Constructs Postgress connector object."""
        self._credentials = credentials
        self.generate_engine()

    def generate_engine(self) -> None:
        """Creates a Postgress connection engine."""
        engine_str = (
            "postgresql+psycopg2://"
            f"{self._credentials.user}"
            f":{self._credentials.password}"
            f"@{self._credentials.host}"
            f"{':'+self._credentials.port if self._credentials.port else str()}"
            f"{'/'+self._credentials.database if self._credentials.database else str()}"
        )
        self._engine_str = engine_str
        self.engine = create_engine(engine_str)
