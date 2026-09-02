from app.services.data_engine import (
    query,
    read_csv,
    to_pandas,
)


CSV_DATA = b"""name,age,city
Ali,20,Lahore
Ahmed,22,Islamabad
Sara,21,Lahore
"""


def test_read_csv():
    dataframe = read_csv(CSV_DATA)

    assert dataframe.height == 3
    assert dataframe.width == 3
    assert dataframe.columns == [
        "name",
        "age",
        "city",
    ]


def test_duckdb_query():
    dataframe = read_csv(CSV_DATA)

    result = query(
        dataframe,
        """
        SELECT city, COUNT(*) AS count
        FROM dataset
        GROUP BY city
        ORDER BY city
        """,
    )

    assert result.height == 2
    assert result.columns == [
        "city",
        "count",
    ]


def test_to_pandas():
    dataframe = read_csv(CSV_DATA)

    pandas_dataframe = to_pandas(dataframe)

    assert pandas_dataframe.shape == (3, 3)
    assert list(pandas_dataframe.columns) == [
        "name",
        "age",
        "city",
    ]