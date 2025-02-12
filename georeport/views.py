# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

"""
Module containing the django-views.
Each view is associated with a url in urls.py.
A view takes a request and creates a respond for the request.
"""

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_GET, require_safe, require_http_methods

from pinpoint_report.settings import DEFAULT_FROM_EMAIL
from .models import Category, Report

from .forms import ReportForm
from django.conf import settings
from django.core.mail import send_mail

from Crypto.Cipher import ChaCha20
from base64 import urlsafe_b64decode

from .admin import send_update


# TODO: test
@require_safe
def index(request) -> HttpResponse:
    """
    Function which handles request going to "/georeport".

    Returns:
        HttpResponse
    """
    reports = Report.objects.all()  # type: ignore Attribute object unknown
    categories = Category.objects.all()  # type: ignore Attribute object unknown

    return render(
        request,
        "georeport/index.html",
        context={"report_list": reports, "category_list": categories},
    )


# Test available
@require_GET
def get_categories(request, id=None) -> JsonResponse:
    """
    Creates a jsonResponse containing the available categories.
    If an id was given, only direct subcategories of the category with the given id are returned.

    Arguments:
        request: HttpRequest

        id: int
            Integer-identifier of the category, from which the subcategories shall be send.
            If it is not provided, all categories are included in the response

    Returns:
        JsonResponse: Contains categories as data
    """
    if id is None:
        cats = Category.objects.all()  # type:ignore Object attribute unknown
    else:
        cats = Category.objects.filter(parent__id=id)  # type: ignore Attribute object us unknown
    data = [{"id": cat.id, "name": cat.name} for cat in cats]
    data = {"categories": data}
    return JsonResponse(data)


# Test available
@require_safe
def category_detail_view(request, id) -> HttpResponse:
    """
    Function to handle requests to see information about a single category identified by id

    Arguments:
        request: HttpRequest
        id: int
            Integer-identifier of the category to be seen.
    """
    cat = get_object_or_404(Category, pk=id)

    # Check if the user is allowed to view the category
    user = request.user
    allowed_user = cat.users.all()
    allowed_groups = cat.groups.all()
    allowed = False
    if user.is_superuser:
        allowed = True
    if user in allowed_user:
        allowed = True

    for group in allowed_groups:
        if user in group.user_set.all():
            allowed = True

    # If User is allowd to view the category provice it, otherwise rise 403- PermissionDenied
    if allowed:
        return render(request, "georeport/category.html", context={"categroy": cat})

    else:
        raise PermissionDenied


# TODO: Report-List


# Test available
@require_http_methods(["GET", "POST"])
def create_report_view(request):
    if request.method == "POST":
        post = request.POST

        # create custom dictionary for Report-Form
        report = {}
        report["title"] = post["title"]
        report["description"] = post["description"]
        report["category"] = post["category"]
        report["email"] = post["email"]
        report["longitude"] = post["longitude"]
        report["latitude"] = post["latitude"]
        reportForm = ReportForm(report)
        # TODO: Check if category is a leaf
        # NOTE: Currently not implemented, since it is assumed, that
        # reports are created with the website, and there every category-selection is required
        if reportForm.is_valid():
            reportForm.save()
            send_creation_confirmation(report)
            send_creation_mail(report)

        return redirect("georeport:index")

    return render(
        request,
        "georeport/create.html",
        context={"categories": Category.objects.all()},  # type: ignore Attribute objects unknown
    )


# Test available
@require_safe
def report_detail_view(request, id):
    """
    Returns the detail-view page of a single report
    """
    report = get_object_or_404(Report, pk=id)

    if report.published:
        return render(request, "georeport/detail.html", context={"report": report})

    raise PermissionDenied


# TODO: Finish Link
# TODO: Tests
@require_GET
def close_with_link_view(request, b64nonce, b64ct):
    nonce = urlsafe_b64decode(b64nonce)
    ct = urlsafe_b64decode(b64ct)
    cipher = ChaCha20.new(key=settings.KEY, nonce=nonce)
    pk = cipher.decrypt(ct)
    id = int(pk)
    report = get_object_or_404(Report, pk=id)

    if report.state == 1:
        report.state = 2
        report.save()
        send_update(report)
    return redirect("georeport:report", id)


# TODO:Tests
def send_creation_confirmation(report_dict):
    if not settings.SEND_MAIL:
        return
    report = (
        Report.objects.filter(title=report_dict["title"])  # type:ignore
        .filter(latitude=report_dict["latitude"])
        .filter(longitude=report_dict["longitude"])
        .first()
    )
    recipient_list = [report.email]
    subject = "Report created"
    message = f'The report with title "{report.title}" was created with id {report.id}'
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=DEFAULT_FROM_EMAIL,
        fail_silently=True,
    )


# TODO: Tests
# TODO: Recruse groupmembers mail addresses
def send_creation_mail(report_dict):
    if not settings.SEND_MAIL:
        return
    report = (
        Report.objects.filter(title=report_dict["title"])  # type:ignore
        .filter(latitude=report_dict["latitude"])
        .filter(longitude=report_dict["longitude"])
        .first()
    )
    recipient_list = []
    subject = f"Report {report.id} was created."
    message = (
        f'A new report with id: {report.id} and title "{report.title}" was created.'
    )

    for user in report.category.users.all():
        recipient_list.append(user.email)
    for group in report.category.groups.all():
        for user in group.user_set.all():
            recipient_list.append(user.email)

    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=DEFAULT_FROM_EMAIL,
        fail_silently=True,
    )
