from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.

from .models import Report, ReportForm


def index(request):
    reports = Report.objects.all()
    return render(request, "georeport/index.html", context={"report_list": reports})


def details(request, id):
    report = get_object_or_404(Report, pk=id)
    return render(request, "georeport/detail.html", context={"report": report})


def create(request):
    if request.method == "POST":
        reportForm = ReportForm(request.POST)
        # TOOD Inputvalidations
        reportForm.save()
        return redirect("index")
    else:
        reportForm = ReportForm()

    return render(request, "georeport/create.html", context={"reportForm": reportForm})
