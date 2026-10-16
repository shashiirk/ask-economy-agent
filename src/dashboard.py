"""Builds the economic metrics dashboard dataset from Snowflake public data."""

from __future__ import annotations

from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark.types import DoubleType


def build_dashboard_dataframe(session: Session) -> DataFrame:
    """Return one row per date with CPI, unemployment, and mortgage metrics."""
    econ = session.table(
        "SNOWFLAKE_PUBLIC_DATA_FREE.PUBLIC_DATA_FREE.FINANCIAL_ECONOMIC_INDICATORS_TIMESERIES"
    )
    housing = session.table(
        "SNOWFLAKE_PUBLIC_DATA_FREE.PUBLIC_DATA_FREE.FREDDIE_MAC_HOUSING_TIMESERIES"
    )

    cpi = (
        econ.filter(F.col("GEO_ID") == "country/USA")
        .filter(
            F.col("VARIABLE_NAME")
            == "CPI: All items, Monthly, 1982-84 Index Date (Seasonally adjusted)"
        )
        .select(
            F.col("DATE"),
            F.col("VALUE").cast(DoubleType()).alias("VALUE"),
            F.lit("CPI").alias("METRIC"),
        )
    )

    unemployment = (
        econ.filter(F.col("GEO_ID") == "country/USA")
        .filter(
            F.col("VARIABLE_NAME")
            == "Current Labor Force: Unemployment Rate - 20 yrs. & over, Monthly (Seasonally adjusted)"
        )
        .select(
            F.col("DATE"),
            F.col("VALUE").cast(DoubleType()).alias("VALUE"),
            F.lit("UNEMPLOYMENT_RATE").alias("METRIC"),
        )
    )

    mortgage = (
        housing.filter(
            F.col("VARIABLE_NAME")
            == "30-Year Fixed Rate Mortgage Rate, National Average"
        )
        .select(
            F.col("DATE"),
            F.col("VALUE").cast(DoubleType()).alias("VALUE"),
            F.lit("MORTGAGE_RATE_30Y").alias("METRIC"),
        )
    )

    combined = cpi.union_all(unemployment).union_all(mortgage)

    return (
        combined.pivot("METRIC", ["CPI", "UNEMPLOYMENT_RATE", "MORTGAGE_RATE_30Y"])
        .agg(F.max("VALUE"))
        .sort(F.col("DATE").desc())
    )

