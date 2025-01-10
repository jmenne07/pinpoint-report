# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm
import json

# Create your views here.
from .models import Category, Report
import pdb


def index(request):
    reports = Report.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "georeport/index.html",
        context={"report_list": reports, "category_list": categories},
    )


def details(request, id):
    report = get_object_or_404(Report, pk=id)
    if report.published:
        return render(request, "georeport/detail.html", context={"report": report})
    else:
        return HttpResponseForbidden("The report is not published")


def category_details(request, id):
    category = get_object_or_404(Category, pk=id)
    return render(request, "georeport/category.html", context={"category": category})


def create(request):
    if request.method == "POST":
        post = request.POST
        report = {}
        report["title"] = post["title"]
        report["longitude"] = post["longitude"]
        report["latitude"] = post["latitude"]
        report["category"] = post["category"]
        report["email"] = post["email"]

        reportForm = ReportForm(report)
        # reportForm = ReportForm(request.POST)

        # TODO Inputvalidation
        reportForm.save()
        return redirect("index")
    else:
        reportForm = ReportForm()

    return render(
        request,
        "georeport/create.html",
        context={"reportForm": reportForm, "categories": Category.objects.all()},
    )


def get_subcategories(request, id):
    subcats = Category.objects.filter(parent__id=id)
    data = [{"id": cat.id, "name": cat.name} for cat in subcats]
    data = {"subcategories": data}
    return JsonResponse(data)
