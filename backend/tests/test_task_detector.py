import pandas as pd
import pytest

from app.services.task_detector import detect_task


def test_detect_classification():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25, 30],
            "income": [30000, 35000, 40000, 50000],
            "approved": ["yes", "no", "yes", "yes"],
        }
    )

    result = detect_task(dataframe)

    assert result["target_column"] == "approved"
    assert result["task_type"] == "classification"


def test_detect_regression():
    dataframe = pd.DataFrame(
        {
            "area": [1000, 1500, 2000, 2500],
            "rooms": [2, 3, 3, 4],
            "price": [100000, 150000, 200000, 250000],
        }
    )

    result = detect_task(dataframe)

    assert result["target_column"] == "price"
    assert result["task_type"] == "regression"


def test_detect_explicit_target():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25, 30],
            "income": [30000, 35000, 40000, 50000],
            "approved": ["yes", "no", "yes", "yes"],
        }
    )

    result = detect_task(dataframe, target_column="age")

    assert result["target_column"] == "age"
    assert result["task_type"] == "regression"


def test_detect_invalid_target():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25],
            "approved": ["yes", "no", "yes"],
        }
    )

    with pytest.raises(ValueError, match="Target column"):
        detect_task(dataframe, target_column="does_not_exist")


def test_detect_empty_dataframe():
    dataframe = pd.DataFrame()

    result = detect_task(dataframe)

    assert result["target_column"] is None
    assert result["task_type"] is None


def test_detect_all_null_target():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25],
            "target": [None, None, None],
        }
    )

    result = detect_task(dataframe)

    assert result["target_column"] is None
    assert result["task_type"] is None


def test_detect_datetime_target():
    dataframe = pd.DataFrame(
        {
            "sales": [100, 200, 300],
            "date": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03"]
            ),
        }
    )

    result = detect_task(dataframe)

    assert result["target_column"] == "date"
    assert result["task_type"] is None