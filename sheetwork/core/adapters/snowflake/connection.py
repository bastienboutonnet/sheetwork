"""Concrete Snowflake Database Connection classes."""
from typing import Dict

from pydantic import BaseModel, ValidationError, validator
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from sheetwork.core.adapters.base.connection import (
    BaseConnection,
    BaseCredentials,
    check_db_type_compatibility,
)
from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import CredentialsParsingError


class SnowflakeCredentialsModel(BaseModel):
    """Pydantic credentials validator model for Snowflake adaptor."""

    account: str
    user: str
    password: str
    role: str
    database: str
    warehouse: str
    target_schema: str

    db_type = validator("db_type", "snowflake", allow_reuse=True, check_fields=False)(
        check_db_type_compatibility
    )

    # @validator("db_type", allow_reuse=True, check_fields=False)
    # def check_db_type_compatibility(cls, value):
    #     assert value == "snowflake"
    #     return value

    class Config:
        """Handles field remapping to avoid keyword collision."""

        fields = {"target_schema": "schema"}


class SnowflakeCredentials(BaseCredentials):
    """This should be a base class down the line but for now it's kinda adhoc until all works fine."""

    def __init__(self, profile: Profile):
        """Constructs SnowflakeCredentials. All it needs is an initted Profile object.

        Args:
            profile (Profile): inited profile objects generated from parsing profiles.ymlk
        """
        self.profile = profile.profile_dict
        self.are_valid_credentials: bool = False
        self.db_type: str = str()
        self.credentials: Dict[str, str] = dict()
        self.parse_and_validate_credentials()

    def validate_credentials(self):
        # check that all necessary keys are in the profile (nullity will have been handled by
        # the yaml validator upsteam)
        db_type = self.profile.get("db_type", str())
        if db_type == "snowflake":
            must_have_keys = {
                "account",
                "user",
                "password",
                "role",
                "database",
                "warehouse",
                "target_schema",
            }
            keys_missing = must_have_keys.difference(self.profile.keys())
            if keys_missing:
                raise CredentialsParsingError(
                    f"The following keys: {keys_missing} must be in your profile."
                )
            self.are_valid_credentials = True
            self.db_type = db_type

    def parse_credentials(self):
        if self.profile.get("db_type") == "snowflake":
            must_have_keys = {
                "account",
                "user",
                "password",
                "role",
                "database",
                "warehouse",
                "target_schema",
            }
            for key in must_have_keys:
                self.credentials.update({key: self.profile.get(key, str())})

    def parse_and_validate_credentials(self) -> None:
        """Parse and validate credentials using pydandic model.

        Pydantic is called first to raise a ValidationError first and cause the app to crash.
        """
        try:
            _credentials = SnowflakeCredentialsModel(**self.profile)
        except ValidationError as e:
            raise CredentialsParsingError(f"Your profile is not valid \n {e}")

        self.credentials = _credentials.dict()
        self.are_valid_credentials = True
        self.db_type = self.profile.get("db_type", str())
        self.user = self.credentials["user"]
        self.password = self.credentials["password"]
        self.account = self.credentials["account"]
        self.role = self.credentials["role"]
        self.warehouse = self.credentials["warehouse"]
        self.database = self.credentials["database"]
        self.target_schema = self.credentials["target_schema"]


class SnowflakeConnection(BaseConnection):
    """Sets up Snowflake database connection."""

    def __init__(self, credentials: SnowflakeCredentials):
        """Constructs SnowflakeConnection by giving it an initialised SnowflakeCredentials object.

        Args:
            credentials (SnowflakeCredentials): initialised SnowflakeCredentials object obtained
                from parsing and validating profiles.yml.
        """
        self.db_type = credentials.db_type
        self.credentials = credentials
        self.generate_engine()

    def generate_engine(self):
        self.engine = create_engine(
            URL(
                account=self.credentials.account,
                user=self.credentials.user,
                password=self.credentials.password,
                role=self.credentials.role,
                warehouse=self.credentials.warehouse,
                database=self.credentials.database,
                schema=self.credentials.target_schema,
            )
        )
