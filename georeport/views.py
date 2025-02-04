# Create your views here.

# TODO: Index-Views
# TODO: Category-List
# TODO: Report-List
# TODO: Create-Report
# TODO: DetailView
# TODO: Category-Detail
# TODO: Supcategories


from django.http import HttpResponse


def index(request):
    return HttpResponse(b"Pinpoint-Report")
