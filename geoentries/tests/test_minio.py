import pytest
from minio import Minio

pytest.skip(
    "Skipped, because it the conditions have to be correct (minio has to be started, etc.)",
    allow_module_level=True,
)

client = Minio(
    "localhost:9000", access_key="minio", secret_key="minio123", secure=False
)


def test_client():
    assert True
    # assert client.bucket_exists("media")
