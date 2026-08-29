
from app.services.storage import storage


def test_upload_file():
    bucket = "datasets"
    object_name = "test/test.txt"
    content = b"Hello from Autonomous ML Agent!"

    uri = storage.upload_file(
        bucket_name=bucket,
        object_name=object_name,
        data=content,
        content_type="text/plain",
    )

    assert uri == f"s3://{bucket}/{object_name}"

    response = storage.client.get_object(
        bucket_name=bucket,
        object_name=object_name,
    )

    try:
        downloaded = response.read()
        assert downloaded == content
    finally:
        response.close()
        response.release_conn()

    storage.client.remove_object(
        bucket_name=bucket,
        object_name=object_name,
    )

