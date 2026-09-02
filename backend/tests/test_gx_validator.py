import pandas as pd

from app.services.gx_validator import validate_dataframe


def test_validate_dataframe():
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22, 23],
            "city": ["Lahore", "Lahore", "Islamabad", "Lahore"],
        }
    )

    result = validate_dataframe(dataframe)

    assert result["success"] is True
    assert len(result["expectations"]) == 2

    for expectation in result["expectations"]:
        assert expectation["success"] is True