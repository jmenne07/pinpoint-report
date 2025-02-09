from . import views
from django.urls import path
# TODO: Adjust to open311
#  /services: -> List with Categories  <- GET ✅
#  /sercvice/{id} -> single Category <- GET ✅
#  /requests -> Create a new Request <- POST
#  /requests -> Get all Requests <- GET
#  /requests/{id} -> Get a specific Request <- GET ✅

app_name = "georeport"

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<int:id>", views.category_detail_view, name="category"),
    path("category/<int:id>/children", views.get_categories, name="subcategories"),
    path("services/<int:id>", views.category_detail_view, name="servcice"),
    path("services/", views.get_categories, name="category-list"),
    path("<int:id>", views.report_detail_view, name="report"),
    path("requests/<int:id>", views.report_detail_view, name="request-id"),
    path("create", views.create_report_view, name="create"),
    #  path("<str:b64nonce>/<str:b64ct>", views.finish_link, name="finish"),
]
