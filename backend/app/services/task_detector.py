from typing import Any

import pandas as pd


def detect_task(
    dataframe: pd.DataFrame,
    target_column: str | None = None,
) -> dict[str, Any]:
    """
    Detect the target column and ML task type from a dataframe.

    Rules:
    - An explicitly provided target column must exist.
    - Otherwise, the last column is used as a target candidate.
    - Categorical/string targets -> classification.
    - Numeric targets -> regression.
    - Datetime targets -> unknown.
    """

    if dataframe.empty or len(dataframe.columns) == 0:
        return {
            "target_column": None,
            "task_type": None,
        }

    if target_column is not None:
        if target_column not in dataframe.columns:
            raise ValueError(
                f"Target column '{target_column}' not found in dataset"
            )
    else:
        target_column = dataframe.columns[-1]

    target = dataframe[target_column]

    if target.isna().all():
        return {
            "target_column": None,
            "task_type": None,
        }

    if pd.api.types.is_datetime64_any_dtype(target):
        return {
            "target_column": target_column,
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