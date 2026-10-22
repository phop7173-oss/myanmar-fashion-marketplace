# Purpose: storefront views. Views only present; business rules live in a service layer.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Show the placeholder home page. Anyone may view it; it reads no data."""
    return render(request, "storefront/home.html")
