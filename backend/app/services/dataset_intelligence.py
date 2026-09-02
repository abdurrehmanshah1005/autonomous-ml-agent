from typing import Any

from app.services.data_engine import read_csv, to_pandas
from app.services.profiler import profile_dataframe
from app.services.quality import analyze_quality
from app.services.task_detector import detect_task
from app.services.ydata_profiler import generate_profile


def analyze_dataset(
    data: bytes,
    target_column: str | None = None,
) -> dict[str, Any]:
    """Build a unified intelligence report for a dataset."""

    # Read using Polars as our primary data engine.
    dataframe = read_csv(data)

    # Convert to Pandas only at the compatibility boundary.
    pandas_dataframe = to_pandas(dataframe)

    # Run our existing deterministic analysis.
    profile = profile_dataframe(pandas_dataframe)
    quality = analyze_quality(pandas_dataframe)
    task = detect_task(
        pandas_dataframe,
        target_column=target_column,
    )

    # Generate the richer YData Profiling report.
    ydata_profile = generate_profile(pandas_dataframe)

    return {
        "dataset": {
            "rows": profile["rows"],
            "columns": profile["columns"],
            "duplicate_rows": profile["duplicate_rows"],
        },
        "columns": {
            "info": profile["columns_info"],
            "types": profile["column_types"],
        },
        "quality": quality,
        "task": task,
        "ydata_profile": ydata_profile,
    }