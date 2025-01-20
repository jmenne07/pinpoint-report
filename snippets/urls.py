from functools import partial
from django.urls import path, include
from rest_framework import renderers
from rest_framework.decorators import renderer_classes
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SnippetViewSet, UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"", SnippetViewSet, basename="snippet")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [path("", include(router.urls))]
