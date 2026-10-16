# Ask Economy Agent

A CLI-based Snowflake Cortex Analyst client for asking natural-language questions about US economy metrics.

The app:
- Sends your question to the Cortex Analyst REST API
- Uses your configured semantic view
- Executes generated SQL in Snowflake
- Prints the result in a looped CLI session until you exit

## Project layout

- [`src/main.py`](./src/main.py) — interactive CLI agent loop
- [`src/settings.py`](./src/settings.py) — `.env` loading + Snowflake/Cortex config
- [`sql/setup.sql`](./sql/setup.sql) — Snowflake database/schema/warehouse setup
- [`sql/economic_dashboard_metrics_dynamic_table.sql`](./sql/economic_dashboard_metrics_dynamic_table.sql) — dynamic table definition used by your semantic layer

## Prerequisites

Before running the app, make sure these exist in Snowflake:
- Database/schema/warehouse from [`sql/setup.sql`](./sql/setup.sql)
- Dynamic table from [`sql/economic_dashboard_metrics_dynamic_table.sql`](./sql/economic_dashboard_metrics_dynamic_table.sql)
- Semantic view referenced by `SNOWFLAKE_SEMANTIC_VIEW`
- The semantic view points to data that is queryable by your user/role
- Your configured role has privileges to:
  - use the configured warehouse/database/schema
  - read objects used by the semantic view (including the dynamic table)
  - call Cortex Analyst REST API for that semantic object
- Network/auth setup allows Snowflake token-based REST calls from this Python client

## Environment setup

1. Copy [`.env.example`](./.env.example) to `.env`.
2. Fill all required values:
   - `SNOWFLAKE_ACCOUNT`
   - `SNOWFLAKE_USER`
   - `SNOWFLAKE_PASSWORD`
   - `SNOWFLAKE_SEMANTIC_VIEW`
   - `SNOWFLAKE_ROLE`
   - `SNOWFLAKE_WAREHOUSE`
   - `SNOWFLAKE_DATABASE`
   - `SNOWFLAKE_SCHEMA`

## Run

```bash
python src/main.py
```

## CLI usage

- Prompt format: `You> ...`
- Response format: `Agent> ...`
- Exit commands: `exit`, `quit`, `q` (or Ctrl+C / Ctrl+D)