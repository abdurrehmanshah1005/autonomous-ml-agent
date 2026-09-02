import json
import uuid
from uuid import UUID

from app.models.dataset import Dataset
from app.models.dataset_profile import DatasetProfile
from app.services.data_engine import read_csv, to_pandas
from app.services.profiler import profile_dataframe
from app.services.storage import storage
from app.services.task_detector import detect_task
from app.services.quality import analyze_quality
from app.services.ydata_profiler import generate_profile


DATASET_BUCKET = "datasets"


def create_dataset(
    project_id: UUID,
    filename: str,
    data: bytes,
    content_type: str,
) -> tuple[Dataset, DatasetProfile]:

    dataset_id = uuid.uuid4()

    dataframe = read_csv(data)
    pandas_dataframe = to_pandas(dataframe)

    profile = profile_dataframe(pandas_dataframe)
    task_info = detect_task(pandas_dataframe)
    quality_info = analyze_quality(pandas_dataframe)

    # Generate detailed YData profiling report
    ydata_profile = generate_profile(pandas_dataframe)

    # Store original dataset in MinIO
    storage_uri = storage.upload_file(
        bucket_name=DATASET_BUCKET,
        object_name=f"{project_id}/{dataset_id}/{filename}",
        data=data,
        content_type=content_type,
    )

    # Store YData profiling report in MinIO
    ydata_profile_uri = storage.upload_file(
        bucket_name=DATASET_BUCKET,
        object_name=(
            f"{project_id}/{dataset_id}/"
            "profiling/ydata_profile.json"
        ),
        data=json.dumps(ydata_profile).encode("utf-8"),
        content_type="application/json",
    )

    dataset = Dataset(
        id=dataset_id,
        project_id=project_id,
        name=filename,
        storage_uri=storage_uri,
        file_type="csv",
        size_bytes=len(data),
        rows=profile["rows"],
        columns=profile["columns"],
        target_column=task_info["target_column"],
        task_type=task_info["task_type"],
    )

    dataset_profile = DatasetProfile(
        dataset_id=dataset_id,
        columns_info=profile["columns_info"],
        quality_info=quality_info,
        ydata_profile_uri=ydata_profile_uri,
    )

    return dataset, dataset_profile