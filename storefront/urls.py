# Purpose: URL routes of the storefront app.
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
