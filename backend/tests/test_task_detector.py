import pandas as pd

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

    result = detect_task(dataframe, target_column="does_not_exist")

    assert result["target_column"] is None
    assert result["task_type"] is None