import pandas as pd

from app.services.ydata_profiler import generate_profile


def test_generate_profile():
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22, 23],
            "city": ["Lahore", "Lahore", "Islamabad", "Lahore"],
        }
    )

    profile = generate_profile(dataframe)

    assert isinstance(profile, dict)
    assert "variables" in profile
    assert "table" in profile
    assert "age" in profile["variables"]
    assert "city" in profile["variables"]