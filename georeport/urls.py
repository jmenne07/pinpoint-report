# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.details, name="detail"),
    path("create", views.create, name="create"),
    path("category/<int:id>", views.category_details, name="category"),
]
