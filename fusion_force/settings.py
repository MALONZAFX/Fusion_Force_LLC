"""
Django settings for fusion_force project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SIMPLE CONFIG
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123456')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # READ FROM ENV
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# APPS - REMOVE UNNECESSARY FOR NOW
INSTALLED_APPS = [
    'django.contrib.staticfiles',  # KEEP FOR STATIC FILES
    'main',  # YOUR APP
    # REMOVED: admin, auth, contenttypes, sessions, messages
]

# MIDDLEWARE - SIMPLIFIED
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # FOR STATIC FILES
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # REMOVED: SessionMiddleware, AuthMiddleware, MessageMiddleware
]

ROOT_URLCONF = 'fusion_force.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # REMOVED: auth, messages context processors
            ],
        },
    },
]

WSGI_APPLICATION = 'fusion_force.wsgi.application'

# DATABASE - DISABLED COMPLETELY
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',  # DUMMY DATABASE
    }
}

print("=== DATABASE DEBUG ===")
print("🚫 DATABASE DISABLED - Using dummy backend")
print("=====================")

# NO PASSWORD VALIDATORS (NO DATABASE)
AUTH_PASSWORD_VALIDATORS = []

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA FILES (DISABLED FOR NOW)
# MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECURITY SETTINGS FOR PRODUCTION
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

print("✅ Django settings loaded - NO DATABASE MODE")