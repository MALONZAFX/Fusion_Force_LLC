"""
Django settings for fusion_force project.
"""
import os
from pathlib import Path
import dj_database_url  

BASE_DIR = Path(__file__).resolve().parent.parent

# SIMPLE CONFIG
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123456')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # READ FROM ENV
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # YOUR APP
]

# MIDDLEWARE - ADD WHITENOISE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ADD THIS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fusion_force.wsgi.application'

# DATABASE - POSTGRESQL READY
db_url = os.getenv('DATABASE_URL', '')
if db_url and 'postgresql://' in db_url:
    print("🚨 FORCING POSTGRESQL CONNECTION")
    DATABASES = {
        'default': dj_database_url.parse(db_url, conn_max_age=600)
    }
else:
    print("⚠️ Using SQLite (local development)")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


print("=== DATABASE DEBUG ===")
print(f"DATABASE_URL exists: {'DATABASE_URL' in os.environ}")
print(f"DATABASE_URL value: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")
print(f"Database engine: {DATABASES['default']['ENGINE']}")
print("=====================")

# PASSWORDS
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

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # ADD THIS

# MEDIA FILES
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECURITY SETTINGS FOR PRODUCTION
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

print("✅ Django settings loaded")