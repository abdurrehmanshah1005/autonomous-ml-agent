import uuid
from uuid import UUID

from app.models.dataset import Dataset
from app.models.dataset_profile import DatasetProfile
from app.services.profiler import profile_csv
from app.services.storage import storage


DATASET_BUCKET = "datasets"


def create_dataset(
    project_id: UUID,
    filename: str,
    data: bytes,
    content_type: str,
) -> tuple[Dataset, DatasetProfile]:

    dataset_id = uuid.uuid4()

    profile = profile_csv(data)

    storage_uri = storage.upload_file(
        bucket_name=DATASET_BUCKET,
        object_name=f"{project_id}/{dataset_id}/{filename}",
        data=data,
        content_type=content_type,
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
    )

    dataset_profile = DatasetProfile(
        dataset_id=dataset_id,
        columns_info=profile["columns_info"],
    )

    return dataset, dataset_profile