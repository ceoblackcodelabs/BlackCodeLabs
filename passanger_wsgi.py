"""
Entry point for Phusion Passenger (cPanel "Setup Python App").

Passenger looks for a module-level `application` callable in this exact
file, at the application's root directory. It does NOT run manage.py --
it imports this file directly, so it needs to be able to find the project
(BlackCodeLabs/) and the virtualenv Passenger creates for the app.
"""
import os
import sys

# The directory this file lives in -- the project root (contains manage.py).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlackCodeLabs.settings')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
