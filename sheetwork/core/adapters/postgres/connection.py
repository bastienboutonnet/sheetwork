"""Concrete Postgres Database Connector classes."""

from typing import Dict

from pydantic import BaseModel, ValidationError, validator
from sqlalchemy.engine import create_engine, url

from sheetwork.core.adapters.base.connection import BaseConnection, check_db_type_compatibility
from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import CredentialsParsingError


class PostgresCredentialsModel(BaseModel):
    """Pydantic credentials validator model for postgres adaptor."""

    user: str
    password: str
    database: str
    host: str = "localhost"
    port: str = "5432"
    target_schema: str

    db_type = validator("db_type", "postgres", allow_reuse=True, check_fields=False)(
        check_db_type_compatibility
    )

    # @validator("db_type", allow_reuse=True)
    # def check_db_type_compatibility(cls, value):
    #     assert value == "postgres"
    #     return value

    class Config:
        """Handles field renamings."""

        fields = {"target_schema": "schema"}  # "schema" is a reserved keyword by pydantic.


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
        self.user = self.credentials.get("user", str())
        self.password = self.credentials.get("password", str())
        self.host = self.credentials.get("host", str())
        self.port = self.credentials.get("port", str())
        self.database = self.credentials.get("database", str())
        self.target_schema = self.credentials.get("target_schema", str())


class PostgresConnection(BaseConnection):
    """Sets up Postgres connector engine."""

    def __init__(self, credentials: PostgresCredentials) -> None:
        """Constructs Postgress connector object."""
        self._credentials = credentials
        self.generate_engine()

    def generate_engine(self) -> None:
        """Creates a Postgress connection engine."""
        # engine_str = (
        #     "postgresql+psycopg2://"
        #     f"{self._credentials.user}"
        #     f":{self._credentials.password}"
        #     f"@{self._credentials.host}"
        #     f"{':'+self._credentials.port if self._credentials.port else str()}"
        #     f"{'/'+self._credentials.database if self._credentials.database else str()}"
        # )
        # self._engine_str = engine_str
        # self.engine = create_engine(engine_str)
        self._engine_url = url.URL(
            drivername="postgresql+psycopg2",
            host=self._credentials.host,
            username=self._credentials.user,
            password=self._credentials.password,
            database=self._credentials.database,
            port=self._credentials.port,
        )
        self.engine = create_engine(self._engine_url)
