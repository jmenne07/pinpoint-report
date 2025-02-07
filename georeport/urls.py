from . import views
from django.urls import path
# TODO: Adjust to open311
#  /services: -> List with Categories  <- GET ✅
#  /sercvice/{id} -> single Category <- GET ✅
#  /requests -> Create a new Request <- POST
#  /requests -> Get all Requests <- GET
#  /requests/{id} -> Get a specific Request <- GET

app_name = "georeport"

urlpatterns = [
    path("", views.index, name="index"),
    #  path("<int:id>", views.details, name="detail"),
    #  path("create", views.create, name="create"),
    path("category/<int:id>", views.category_detail_view, name="category"),
    path("services/<int:id>", views.category_detail_view, name="servcice"),
    path("category/<int:id>/children", views.get_categories, name="subcategories"),
    path("services/", views.get_categories),
    #  path("<str:b64nonce>/<str:b64ct>", views.finish_link, name="finish"),
]
