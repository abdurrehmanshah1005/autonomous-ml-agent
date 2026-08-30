
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dataset import Dataset
from app.models.project import Project
from app.schemas.dataset import DatasetResponse
from app.services.dataset import create_dataset


router = APIRouter(
    prefix="/projects/{project_id}/datasets",
    tags=["datasets"],
)


@router.post(
    "",
    response_model=DatasetResponse,
    status_code=201,
)
async def upload_dataset(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    project = db.execute(
        select(Project).where(Project.id == project_id)
    ).scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported currently",
        )

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    dataset = create_dataset(
        project_id=project_id,
        filename=file.filename,
        data=data,
        content_type=file.content_type or "text/csv",
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset

