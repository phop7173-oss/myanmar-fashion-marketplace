# Purpose: proves the placeholder home page works (the T-010 trivial test).
from django.test import Client


def test_home_page_returns_ok_and_shows_the_site_name() -> None:
    response = Client().get("/")

    assert response.status_code == 200
    assert "Myanmar Fashion Marketplace" in response.content.decode()
