from typing import Any

import pandas as pd


def detect_task(
    dataframe: pd.DataFrame,
    target_column: str | None = None,
) -> dict[str, Any]:
    """
    Detect the target column and ML task type from a dataframe.

    Rules:
    - If target_column is provided, use it.
    - Otherwise, use the last column as the target candidate.
    - Categorical/string target -> classification.
    - Numeric target -> regression.
    """

    if dataframe.empty or len(dataframe.columns) == 0:
        return {
            "target_column": None,
            "task_type": None,
        }

    if target_column is not None:
        if target_column not in dataframe.columns:
            return {
                "target_column": None,
                "task_type": None,
            }

        target = dataframe[target_column]
    else:
        target_column = dataframe.columns[-1]
        target = dataframe[target_column]

    if target.isna().all():
        return {
            "target_column": None,
            "task_type": None,
        }

    if pd.api.types.is_numeric_dtype(target):
        task_type = "regression"
    else:
        task_type = "classification"

    return {
        "target_column": target_column,
        "task_type": task_type,
    }