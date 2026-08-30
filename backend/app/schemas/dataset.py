
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    storage_uri: str
    file_type: str | None
    size_bytes: int | None
    rows: int | None
    columns: int | None
    target_column: str | None
    task_type: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

