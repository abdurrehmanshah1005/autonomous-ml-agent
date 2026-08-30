
import uuid
from io import BytesIO
from uuid import UUID

import pandas as pd

from app.models.dataset import Dataset
from app.services.storage import storage


DATASET_BUCKET = "datasets"


def create_dataset(
    project_id: UUID,
    filename: str,
    data: bytes,
    content_type: str,
) -> Dataset:
    dataset_id = uuid.uuid4()

    dataframe = pd.read_csv(BytesIO(data))

    storage_uri = storage.upload_file(
        bucket_name=DATASET_BUCKET,
        object_name=f"{project_id}/{dataset_id}/{filename}",
        data=data,
        content_type=content_type,
    )

    return Dataset(
        id=dataset_id,
        project_id=project_id,
        name=filename,
        storage_uri=storage_uri,
        file_type="csv",
        size_bytes=len(data),
        rows=len(dataframe),
        columns=len(dataframe.columns),
    )

