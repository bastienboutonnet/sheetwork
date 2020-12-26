"""Concrete Database Connection classes. This may be broken into db specific modules down the road."""
from typing import Dict

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from sheetwork.core.adapters.base.connection import BaseConnection, BaseCredentials
from sheetwork.core.config.profile import Profile
from sheetwork.core.exceptions import CredentialsParsingError


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
        self.validate_credentials()
        self.parse_credentials()

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
                "schema",
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
                "schema",
            }
            for key in must_have_keys:
                self.credentials.update({key: self.profile.get(key, str())})


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
                account=self.credentials.credentials.get("account"),
                user=self.credentials.credentials.get("user"),
                password=self.credentials.credentials.get("password"),
                role=self.credentials.credentials.get("role"),
                warehouse=self.credentials.credentials.get("warehouse"),
                database=self.credentials.credentials.get("database"),
                schema=self.credentials.credentials.get("schema"),
            )
        )
