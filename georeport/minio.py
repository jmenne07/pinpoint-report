# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

from django.conf import settings
import os
import shutil
from minio import Minio
from .models import Report
from .forms import ImageForm

client = Minio(
    "localhost:9000", access_key="minio", secret_key="minio123", secure=False
)


def handle_file_uploads(request_files, report_dict):
    """
    Handles the upload of files to
    minio
    """
    report = (
        Report.objects.filter(title=report_dict["title"])  # type:ignore
        .filter(latitude=report_dict["latitude"])
        .filter(longitude=report_dict["longitude"])
        .first()
    )
    # client = Minio(
    #    f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
    #    access_key=settings.MINIO_ACCESS_KEY,
    #    secret_key=settings.SECRET_KEY,
    #    secure=False,
    # )

    files = request_files.getlist("image")
    bucketname = settings.BUCKET_NAME
    if not client.bucket_exists(bucketname):
        client.make_bucket(bucketname)

    pathprefix = "./georeport/static/georeport/images"
    for f in files:
        if not os.path.exists(pathprefix):
            os.makedirs(pathprefix)

        image = {}
        image["file"] = f.name
        path = os.path.join(pathprefix, f.name)
        with open(path, "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        client.fput_object(bucketname, image["file"], path)

        image["report"] = report
        imgForm = ImageForm(image)
        imgForm.save()
    shutil.rmtree(pathprefix)


def get_url(filename):
    """
    Wrapper for presigned_get_object
    """
    return client.presigned_get_object(settings.BUCKET_NAME, filename)
