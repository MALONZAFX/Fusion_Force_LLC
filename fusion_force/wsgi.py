# fusion_force/wsgi.py - CORRECTED VERSION
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion_force.settings')

application = get_wsgi_application()

# Only initialize WhiteNoise in production (when staticfiles directory exists)
# This prevents the startup error you've been seeing
if os.path.isdir('staticfiles'):
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root='staticfiles')