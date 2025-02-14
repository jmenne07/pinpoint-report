# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

from django.forms import ModelForm
from .models import Image, Report


class ReportForm(ModelForm):
    """
    Small class to map a dictionary to the report model.
    Thic class extends the django-ModelForm
    """

    class Meta:
        """
        Metaclass describing the Report Form
        """

        model = Report
        fields = ["title", "description", "email", "category", "latitude", "longitude"]


class ImageForm(ModelForm):
    """
    Small class to map a dictionary to the Image model.
    Thic class extends the django-ModelForm
    """

    class Meta:
        """
        Metaclass describing the Image Form
        """

        model = Image
        fields = ["file", "report"]
        """
        Fields for this form:

            File: Name of the file
            Report: the report to which the image is ascociated.
        """
