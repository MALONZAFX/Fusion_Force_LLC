import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ================= DEPLOYMENT ENVIRONMENT =================
# Detect deployment environment
IS_RAILWAY = os.getenv('RAILWAY', 'False').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fusion-force-llc-secret-key-2025-dev-only')

# ================= DEBUG MODE =================
# Smart debug mode detection - FIXED
if IS_RAILWAY:
    # On Railway, always use production settings (DEBUG=False)
    DEBUG = False
else:
    # Local development
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ================= DOMAIN CONFIGURATION =================
# ALLOWED_HOSTS - ALWAYS include Railway domains
ALLOWED_HOSTS = [
    'fusionforcellc-production.up.railway.app',  # Your specific Railway domain
    '.railway.app',                             # All Railway subdomains
    '.up.railway.app',                          # All Railway app domains
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
]

# Add any custom hosts from environment variable
env_hosts = os.getenv('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in env_hosts.split(',') if host.strip()])

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# CSRF TRUSTED ORIGINS
CSRF_TRUSTED_ORIGINS = [
    'https://fusionforcellc-production.up.railway.app',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Add any custom origins from environment
env_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if env_origins:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in env_origins.split(',') if origin.strip()])

# Remove duplicates
CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'whitenoise.runserver_nostatic',
    
    # Your apps
    'main.apps.MainConfig',
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
# Check for DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,  # Always use SSL on Railway
        )
    }
else:
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
if not DEBUG:
    # Production security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ================= STATIC FILES CONFIGURATION =================
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise configuration - Fixed to use simple storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Using CompressedStaticFilesStorage (no manifest issues)
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Additional WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False  # Don't raise errors for missing files
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh only in debug mode
WHITENOISE_MAX_AGE = 31536000  # 1 year cache for static files
WHITENOISE_INDEX_FILE = True  # Serve index.html for directories

# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================= EMAIL CONFIGURATION =================
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Fusion Force <info@fusionforce.com>')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'admin@fusionforce.com')

# ================= CUSTOM SETTINGS =================
# Admin URL
ADMIN_URL = os.getenv('ADMIN_URL', 'fusionforce-admin/')

# Session settings
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

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
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
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
PORT = int(os.environ.get('PORT', 8000))

# For Railway deployment
if not DEBUG:
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Custom settings for your project
# Add any additional custom settings below this line