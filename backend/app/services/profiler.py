import pandas as pd


def profile_dataframe(dataframe: pd.DataFrame) -> dict:
    columns = []

    for column in dataframe.columns:
        series = dataframe[column]

        columns.append(
            {
                "name": column,
                "dtype": str(series.dtype),
                "missing": int(series.isna().sum()),
                "unique": int(series.nunique(dropna=True)),
            }
        )

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "columns_info": columns,
    }