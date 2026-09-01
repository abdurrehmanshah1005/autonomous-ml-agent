import pandas as pd

from app.services.profiler import profile_dataframe


def test_profile_dataframe():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Ali", "Ahmed", "Bilal"],
            "age": [20, 22, 25],
        }
    )

    result = profile_dataframe(dataframe)

    assert result["rows"] == 3
    assert result["columns"] == 3
    assert result["duplicate_rows"] == 0

    assert result["column_types"]["numeric"] == ["id", "age"]
    assert result["column_types"]["categorical"] == ["name"]
    assert result["column_types"]["datetime"] == []


def test_profile_missing_values():
    dataframe = pd.DataFrame(
        {
            "name": ["Ali", None, "Bilal", None],
            "age": [20, 22, None, 25],
        }
    )

    result = profile_dataframe(dataframe)

    name_info = result["columns_info"][0]
    age_info = result["columns_info"][1]

    assert name_info["missing"] == 2
    assert name_info["missing_percentage"] == 50.0

    assert age_info["missing"] == 1
    assert age_info["missing_percentage"] == 25.0


def test_profile_duplicate_rows():
    dataframe = pd.DataFrame(
        {
            "name": ["Ali", "Ahmed", "Ali"],
            "age": [20, 22, 20],
        }
    )

    result = profile_dataframe(dataframe)

    assert result["duplicate_rows"] == 1


def test_profile_likely_id():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Ali", "Ahmed", "Bilal"],
        }
    )

    result = profile_dataframe(dataframe)

    assert result["columns_info"][0]["likely_id"] is True
    assert result["columns_info"][1]["likely_id"] is False