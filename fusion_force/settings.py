"""
Django settings for fusion_force project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SIMPLE CONFIG
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123456')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# APPS - KEEP BASIC DJANGO APPS
INSTALLED_APPS = [
    'django.contrib.admin',  # KEEP
    'django.contrib.auth',  # KEEP
    'django.contrib.contenttypes',  # KEEP
    'django.contrib.sessions',  # KEEP
    'django.contrib.messages',  # KEEP
    'django.contrib.staticfiles',
    'main',  # YOUR APP
]

# MIDDLEWARE - FULL SET
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fusion_force.urls'

# In settings.py, update TEMPLATES:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Project-level templates
            BASE_DIR / 'main' / 'templates',  # App templates
        ],
        'APP_DIRS': True,  # This looks in app/templates/ directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fusion_force.wsgi.application'

# DATABASE - DUMMY (NO DATABASE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

print("=== DATABASE DEBUG ===")
print("🚫 DATABASE DISABLED - Using dummy backend")
print("=====================")

# PASSWORD VALIDATORS (WON'T BE USED)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

print("✅ Django settings loaded - NO DATABASE MODE")