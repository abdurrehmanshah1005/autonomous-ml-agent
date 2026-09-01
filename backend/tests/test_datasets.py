
import io
import uuid

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.dataset import Dataset
from app.models.project import Project


client = TestClient(app)


def create_test_project() -> uuid.UUID:
    db = SessionLocal()

    try:
        project = Project(
            name="Dataset Test Project",
            description="Project created for dataset endpoint testing",
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project.id
    finally:
        db.close()


def test_upload_dataset():
    project_id = create_test_project()

    csv_content = """sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
6.2,3.4,5.4,2.3,virginica
6.0,3.0,4.8,1.8,virginica
"""

    response = client.post(
        f"/projects/{project_id}/datasets",
        files={
            "file": (
                "test_iris.csv",
                io.BytesIO(csv_content.encode()),
                "text/csv",
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["project_id"] == str(project_id)
    assert data["name"] == "test_iris.csv"
    assert data["file_type"] == "csv"
    assert data["rows"] == 4
    assert data["columns"] == 5
    assert data["size_bytes"] > 0
    assert data["storage_uri"].startswith("s3://datasets/")

    dataset_id = uuid.UUID(data["id"])

    db = SessionLocal()

    try:
        dataset = db.get(Dataset, dataset_id)

        assert dataset is not None
        assert dataset.project_id == project_id
        assert dataset.name == "test_iris.csv"
    finally:
        db.close()


def test_upload_dataset_project_not_found():
    project_id = uuid.uuid4()

    response = client.post(
        f"/projects/{project_id}/datasets",
        files={
            "file": (
                "test.csv",
                io.BytesIO(b"name,value\nA,1\nB,2\n"),
                "text/csv",
            )
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_upload_non_csv_dataset():
    project_id = create_test_project()

    response = client.post(
        f"/projects/{project_id}/datasets",
        files={
            "file": (
                "test.txt",
                io.BytesIO(b"hello world"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are supported currently"


def test_upload_empty_dataset():
    project_id = create_test_project()

    response = client.post(
        f"/projects/{project_id}/datasets",
        files={
            "file": (
                "empty.csv",
                io.BytesIO(b""),
                "text/csv",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"

def test_get_dataset_profile():
    project_id = create_test_project()

    csv_content = """sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
6.2,3.4,5.4,2.3,virginica
6.0,3.0,4.8,1.8,virginica
"""

    upload_response = client.post(
        f"/projects/{project_id}/datasets",
        files={
            "file": (
                "profile_test.csv",
                io.BytesIO(csv_content.encode()),
                "text/csv",
            )
        },
    )

    assert upload_response.status_code == 201

    dataset_id = upload_response.json()["id"]

    profile_response = client.get(
        f"/projects/{project_id}/datasets/{dataset_id}/profile"
    )

    assert profile_response.status_code == 200

    data = profile_response.json()

    assert data["dataset_id"] == dataset_id
    assert len(data["columns_info"]) == 5

    assert data["columns_info"][0]["name"] == "sepal_length"
    assert data["columns_info"][0]["dtype"] == "float64"
    assert data["columns_info"][0]["missing"] == 0

    assert data["columns_info"][4]["name"] == "species"
    assert data["columns_info"][4]["dtype"] == "str"


def test_get_dataset_profile_not_found():
    project_id = uuid.uuid4()
    dataset_id = uuid.uuid4()

    response = client.get(
        f"/projects/{project_id}/datasets/{dataset_id}/profile"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"

