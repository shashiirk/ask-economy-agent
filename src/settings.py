"""Runtime configuration for Snowflake sessions."""

from __future__ import annotations

import os


def snowflake_connection_params() -> dict[str, str]:
    """Build Snowflake connection parameters from environment variables."""
    return {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.environ.get("SNOWFLAKE_DATABASE", "ECON_AGENT_DB"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA", "ANALYTICS"),
    }

