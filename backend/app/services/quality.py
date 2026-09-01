import pandas as pd


def analyze_quality(dataframe: pd.DataFrame) -> dict:
    constant_columns = []
    high_cardinality_columns = []
    likely_id_columns = []
    missing_columns = []

    for column in dataframe.columns:
        series = dataframe[column]

        unique = series.nunique(dropna=True)
        missing = int(series.isna().sum())

        if unique <= 1:
            constant_columns.append(column)

        column_name = column.lower()

        

        looks_like_id_name = (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.endswith("uuid")
            or column_name.endswith("identifier")
        )

        if (
            len(series) > 0
            and unique == len(series)
            and looks_like_id_name
        ):
            likely_id_columns.append(column)

        if (
            len(series) > 0
            and unique / len(series) >= 0.9
            and not pd.api.types.is_numeric_dtype(series)
        ):
            high_cardinality_columns.append(column)

        if missing > 0:
            missing_columns.append(
                {
                    "name": column,
                    "count": missing,
                    "percentage": round(
                        (missing / len(series)) * 100, 2
                    ),
                }
            )

    warnings = []

    if constant_columns:
        warnings.append(
            f"Constant columns detected: {', '.join(constant_columns)}"
        )

    if likely_id_columns:
        warnings.append(
            f"Possible identifier columns: {', '.join(likely_id_columns)}"
        )

    if high_cardinality_columns:
        warnings.append(
            f"High-cardinality categorical columns: "
            f"{', '.join(high_cardinality_columns)}"
        )

    if missing_columns:
        warnings.append("Dataset contains missing values")

    duplicate_rows = int(dataframe.duplicated().sum())

    if duplicate_rows > 0:
        warnings.append(
            f"Dataset contains {duplicate_rows} duplicate rows"
        )

    return {
        "duplicate_rows": duplicate_rows,
        "missing_columns": missing_columns,
        "constant_columns": constant_columns,
        "high_cardinality_columns": high_cardinality_columns,
        "likely_id_columns": likely_id_columns,
        "warnings": warnings,
    }