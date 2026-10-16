"""Runtime configuration for Snowflake sessions."""

from __future__ import annotations

import os
from dotenv import load_dotenv


load_dotenv()


def snowflake_connection_params() -> dict[str, str]:
    """Build Snowflake connection parameters from environment variables."""
    return {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": os.environ.get("SNOWFLAKE_ROLE"),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
        "database": os.environ.get("SNOWFLAKE_DATABASE"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA"),
    }
