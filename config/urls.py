# Purpose: top-level URL routing; delegates to each app's own URLs.
from django.urls import include, path

urlpatterns = [
    path("", include("storefront.urls")),
]
