# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
"""
Module handling the minio connection of the application
"""

from django.conf import settings
import os
import shutil
from minio import Minio

from .models import Report
from .forms import ImageForm

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)


def handle_file_uploads(request_files, report_dict):
    """
    Handles the upload of files to minio.

    Arguments:
        request_files: Files in the form of a django request.FILES object
        report_dict: A dictionary containing information about a single report.
            The dictionary is used to find the correct report by choosing the first report
            with a matching title and matchin geocoordinates.

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

    Arguments:
        filename: The filename of the file to get.
    """
    return client.presigned_get_object(settings.BUCKET_NAME, filename)
