"""Entry point for building and previewing the economy dashboard dataset."""

from __future__ import annotations

from snowflake.snowpark import Session

from dashboard import build_dashboard_dataframe
from settings import snowflake_connection_params


def main() -> None:
    connection_settings = snowflake_connection_params()
    session = Session.builder.configs(connection_settings).create()
    try:
        dashboard_df = build_dashboard_dataframe(session)
        dashboard_df.show(20)
        print(f"Total rows: {dashboard_df.count()}")
        print(f"Columns: {dashboard_df.columns}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
