from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm

# Create your views here.
from .models import Category, Report


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
        reportForm = ReportForm(request.POST)
        # TOOD Inputvalidations
        reportForm.save()
        return redirect("index")
    else:
        reportForm = ReportForm()

    return render(request, "georeport/create.html", context={"reportForm": reportForm})
