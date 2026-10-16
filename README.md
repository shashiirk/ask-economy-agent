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

## Secrets and environment setup

1. Copy [`./.env.example`](./.env.example) to `./.env` (already created locally and gitignored).
2. Fill in:
   - `SNOWFLAKE_ACCOUNT`
   - `SNOWFLAKE_USER`
   - `SNOWFLAKE_PASSWORD`
3. Optional overrides: `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`

The app loads `./.env` automatically via `python-dotenv`.
The app loads `./.env` automatically at startup.

Run:

```bash
python src/main.py
```