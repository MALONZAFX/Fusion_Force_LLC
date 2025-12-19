# fusion_force/wsgi.py - SIMPLIFIED VERSION
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion_force.settings')

# NO WHITENOISE INITIALIZATION HERE - handle it in settings.py instead
application = get_wsgi_application()