from minio import Minio

client = Minio(
    "localhost:9000", access_key="minio", secret_key="minio123", secure=False
)


def test_client():
    assert client.bucket_exists("media")
