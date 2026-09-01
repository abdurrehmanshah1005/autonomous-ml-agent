import pandas as pd

from app.services.quality import analyze_quality


def test_quality_analysis():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "name": ["Ali", "Ahmed", "Bilal", "Sara"],
            "age": [20, None, 25, 30],
            "constant": ["yes", "yes", "yes", "yes"],
        }
    )

    result = analyze_quality(dataframe)

    assert result["duplicate_rows"] == 0
    assert result["constant_columns"] == ["constant"]
    assert result["likely_id_columns"] == ["id"]

    assert result["missing_columns"] == [
        {
            "name": "age",
            "count": 1,
            "percentage": 25.0,
        }
    ]

    assert len(result["warnings"]) > 0


def test_quality_duplicate_rows():
    dataframe = pd.DataFrame(
        {
            "name": ["Ali", "Ahmed", "Ali"],
            "age": [20, 22, 20],
        }
    )

    result = analyze_quality(dataframe)

    assert result["duplicate_rows"] == 1
    assert "Dataset contains 1 duplicate rows" in result["warnings"]


def test_quality_clean_dataset():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25, 30],
            "income": [30000, 35000, 40000, 50000],
        }
    )

    result = analyze_quality(dataframe)

    assert result["duplicate_rows"] == 0
    assert result["missing_columns"] == []
    assert result["constant_columns"] == []
    assert result["likely_id_columns"] == []
    assert result["high_cardinality_columns"] == []
    assert result["warnings"] == []