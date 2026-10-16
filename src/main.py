"""CLI entry point for multi-turn Cortex Analyst REST conversations."""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests
from snowflake.snowpark import Session

from settings import cortex_analyst_target, snowflake_connection_params

ANALYST_ENDPOINT = "/api/v2/cortex/analyst/message"
EXIT_COMMANDS = {"exit", "quit", "q"}
PROMPT_LABEL = "You> "
RESPONSE_LABEL = "Agent> "


def _post_analyst_message(
    session: Session, messages: list[dict[str, Any]], target: dict[str, str]
) -> dict[str, Any]:
    payload: dict[str, Any] = {"messages": messages}
    payload.update(target)

    response = requests.post(
        url=f"https://{session.connection.host}{ANALYST_ENDPOINT}",
        json=payload,
        headers={
            "Authorization": f'Snowflake Token="{session.connection.rest.token}"',
            "Content-Type": "application/json",
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _extract_analyst_blocks(content: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    sql_statements: list[str] = []
    text_blocks: list[str] = []

    for block in content:
        block_type = block.get("type")
        if block_type == "text":
            text = block.get("text", "")
            if text:
                text_blocks.append(text)
        elif block_type == "sql":
            statement = block.get("statement", "")
            if statement:
                sql_statements.append(statement)
    return sql_statements, text_blocks


def _clean_sql(statement: str) -> str:
    cleaned_lines = []
    for line in statement.splitlines():
        if line.strip().startswith("--"):
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines).strip()
    while cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()
    return cleaned


def _run_generated_sql(session: Session, sql_statements: list[str]) -> pd.DataFrame | None:
    for statement in sql_statements:
        cleaned_statement = _clean_sql(statement)
        if not cleaned_statement:
            continue
        return session.sql(cleaned_statement).limit(20).to_pandas()
    return None


def _format_answer(
    query_result: pd.DataFrame | None, text_blocks: list[str], sql_statements: list[str]
) -> str:
    if query_result is not None:
        if query_result.empty:
            return "No rows returned."
        if len(query_result.index) == 1:
            row = query_result.iloc[0].to_dict()
            parts = [f"{key}: {value}" for key, value in row.items()]
            return ", ".join(parts)
        return query_result.to_string(index=False)

    if text_blocks:
        return " ".join(text_blocks)

    if sql_statements:
        return "I generated SQL but could not produce a readable answer."

    return "I could not produce an answer for that question."


def main() -> None:
    try:
        connection_settings = snowflake_connection_params()
        analyst_target = cortex_analyst_target()
    except KeyError as exc:
        missing_key = exc.args[0]
        print(f"Missing required environment variable: {missing_key}")
        print(
            "Please update your .env file (see .env.example), then run again."
        )
        return

    session = Session.builder.configs(connection_settings).create()
    try:
        print("Ask Economy Agent (Snowflake Cortex Analyst)")
        print(
            "Ask questions about US macro indicators using your configured semantic view."
        )
        print("Type 'exit', 'quit', or 'q' to end the session.\n")

        conversation: list[dict[str, Any]] = []
        while True:
            try:
                question = input(PROMPT_LABEL).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not question:
                continue
            if question.lower() in EXIT_COMMANDS:
                break

            conversation.append(
                {"role": "user", "content": [
                    {"type": "text", "text": question}]}
            )

            try:
                response = _post_analyst_message(
                    session, conversation, analyst_target)
            except requests.HTTPError as exc:
                details = exc.response.text if exc.response is not None else str(
                    exc)
                print(f"{RESPONSE_LABEL} Analyst API request failed: {details}")
                conversation.pop()
                continue
            except requests.RequestException as exc:
                print(
                    f"{RESPONSE_LABEL} Network error while calling Analyst API: {exc}")
                conversation.pop()
                continue

            analyst_message = response.get("message", {})
            content = analyst_message.get("content", [])
            sql_statements, text_blocks = _extract_analyst_blocks(content)
            try:
                query_result = _run_generated_sql(session, sql_statements)
                answer = _format_answer(
                    query_result, text_blocks, sql_statements)
            except Exception as exc:
                answer = f"I generated SQL but execution failed: {exc}"

            print(f"{RESPONSE_LABEL}{answer}\n")

            conversation.append({"role": "analyst", "content": content})
    finally:
        session.close()


if __name__ == "__main__":
    main()
