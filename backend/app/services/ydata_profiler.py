import json

import pandas as pd
from ydata_profiling import ProfileReport


def generate_profile(dataframe: pd.DataFrame) -> dict:
    """Generate a YData Profiling report."""

    report = ProfileReport(
        dataframe,
        minimal=True,
        progress_bar=False,
    )

    return json.loads(report.to_json())