import pandas as pd


def profile_dataframe(dataframe: pd.DataFrame) -> dict:
    columns_info = []

    numeric_columns = []
    categorical_columns = []
    datetime_columns = []

    for column in dataframe.columns:
        series = dataframe[column]

        dtype = str(series.dtype)
        missing = int(series.isna().sum())
        unique = int(series.nunique(dropna=True))

        if pd.api.types.is_numeric_dtype(series):
            numeric_columns.append(column)
        elif pd.api.types.is_datetime64_any_dtype(series):
            datetime_columns.append(column)
        else:
            categorical_columns.append(column)

        likely_id = (
            len(series) > 0
            and unique == len(series)
            and (
                column.lower() == "id"
                or column.lower().endswith("_id")
            )
        )

        columns_info.append(
            {
                "name": column,
                "dtype": dtype,
                "missing": missing,
                "missing_percentage": round(
                    (missing / len(series)) * 100, 2
                ) if len(series) > 0 else 0.0,
                "unique": unique,
                "likely_id": likely_id,
            }
        )

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "duplicate_rows": int(dataframe.duplicated().sum()),
        "columns_info": columns_info,
        "column_types": {
            "numeric": numeric_columns,
            "categorical": categorical_columns,
            "datetime": datetime_columns,
        },
    }