import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fusion-force-llc-secret-key-2025-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Changed default to False for production

# ================= DOMAIN CONFIGURATION =================
# Parse ALLOWED_HOSTS from environment variable
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ALWAYS add Railway domains
ALLOWED_HOSTS.extend([
    'fusionforcellc-production.up.railway.app',
    '.railway.app',  # Allows all Railway subdomains
    '.up.railway.app',  # More specific Railway domain pattern
    '*',  # For Railway internal routing
    '0.0.0.0',
    '192.168.1.*',
])

# Parse CSRF_TRUSTED_ORIGINS from environment variable
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = [origin for origin in CSRF_TRUSTED_ORIGINS if origin]  # Remove empty strings

# ALWAYS add Railway domains to CSRF trusted origins
CSRF_TRUSTED_ORIGINS.extend([
    'https://fusionforcellc-production.up.railway.app',
    'https://*.railway.app',
    'https://*.up.railway.app',
])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'whitenoise.runserver_nostatic',  # For static files
    
    # Your apps
    'main.apps.MainConfig',  # Your main app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fusion_force.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'main/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'fusion_force.wsgi.application'

# ================= DATABASE CONFIGURATION =================
# Check for DATABASE_URL environment variable (Railway provides this)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Use dj-database-url to parse the DATABASE_URL (Railway PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Default to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ================= SECURITY SETTINGS =================
# Security settings for production
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Additional security
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_PROXY_SSL_HEADER = None

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For production collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configure Whitenoise compression and caching
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh in development

# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================= EMAIL CONFIGURATION =================
# Use console backend for development, SMTP for production
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# Only configure SMTP if not using console backend
if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Fusion Force <info@fusionforce.com>')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'admin@fusionforce.com')

# ================= CUSTOM SETTINGS =================
# Admin URL - Customize for security
ADMIN_URL = os.getenv('ADMIN_URL', 'fusionforce-admin/')

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fusion-force-cache',
    }
}

# Django admin customization
ADMIN_SITE_HEADER = 'FUSION-FORCE ADMIN'
ADMIN_SITE_TITLE = 'Fusion Force Administration'
ADMIN_INDEX_TITLE = 'Dashboard'

# Railway-specific settings
PORT = int(os.environ.get('PORT', 8000))  # Railway provides PORT environment variable

# For Railway deployment
if not DEBUG:
    # Ensure static files work on Railway
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    
    # Railway uses PORT environment variable
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    
    # For Railway's proxy
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')