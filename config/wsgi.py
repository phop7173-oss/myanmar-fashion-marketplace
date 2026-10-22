# Purpose: WSGI entry point used by a production web server (hosting is decided in D-02).
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
