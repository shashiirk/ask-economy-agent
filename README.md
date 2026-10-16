# Ask Economy Agent

This repo keeps tutorial assets, SQL setup scripts, and application code in separate, predictable locations so things do not get dumped into one folder.

## Project layout

- [`notebooks/`](./notebooks) — tutorial and exploration notebooks
- [`sql/`](./sql) — SQL scripts
  - [`sql/setup.sql`](./sql/setup.sql) — Snowflake setup script
- [`src/`](./src) — all Python code (modules + entrypoint)

## Python code (from notebook, organized)

- Core transformation logic: [`src/dashboard.py`](./src/dashboard.py)
- Snowflake config loader: [`src/settings.py`](./src/settings.py)
- Runnable script: [`src/main.py`](./src/main.py)

Set these environment variables before running:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- Optional overrides: `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`

Run:

```bash
python src/main.py
```