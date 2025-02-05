# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

"""
Module containing the django-views.
Each view is associated with a url in urls.py.
A view takes a request and creates a respond for the request.
"""

from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def index(request):
    """
    Function which handles request going to "/georeport".
    """
    return render(request, "georeport/index.html")


# TODO: Category-List
# TODO: Category-Detail
# TODO: Subcategories

# TODO: Report-List
# TODO: Create-Report

# TODO: Detailview Report

# TODO: Finish Link
