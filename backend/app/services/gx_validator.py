from typing import Any

import great_expectations as gx
import pandas as pd


def validate_dataframe(dataframe: pd.DataFrame) -> dict[str, Any]:
    """Run basic data-quality validation using Great Expectations."""

    context = gx.get_context()

    data_source = context.data_sources.add_pandas(
        name="dataset_intelligence",
    )

    data_asset = data_source.add_dataframe_asset(
        name="dataset",
    )

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "batch",
    )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": dataframe}
    )

    expectations = []

    for column in dataframe.columns:
        expectations.append(
            gx.expectations.ExpectColumnValuesToNotBeNull(
                column=column,
            )
        )

    results = []

    for expectation in expectations:
        result = batch.validate(expectation)

        results.append(
            {
                "expectation": result.expectation_config.to_json_dict(),
                "success": result.success,
                "result": result.result,
            }
        )

    return {
        "success": all(result["success"] for result in results),
        "expectations": results,
    }