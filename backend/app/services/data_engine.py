from io import BytesIO

import duckdb
import pandas as pd
import polars as pl


def read_csv(data: bytes) -> pl.DataFrame:
    """Read CSV bytes into a Polars DataFrame."""
    return pl.read_csv(BytesIO(data))


def to_pandas(dataframe: pl.DataFrame) -> pd.DataFrame:
    """Convert a Polars DataFrame to Pandas when required."""
    return dataframe.to_pandas()


def query(
    dataframe: pl.DataFrame,
    sql: str,
) -> pl.DataFrame:
    """Run DuckDB SQL against a Polars DataFrame."""

    connection = duckdb.connect()

    try:
        connection.register("dataset", dataframe)

        result = connection.sql(sql)

        return pl.from_arrow(result.arrow())

    finally:
        connection.close()