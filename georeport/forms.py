# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from django.forms import ModelForm

from .models import Report


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "description", "latitude", "longitude", "email", "category"]
