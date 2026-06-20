"""
Django settings for visitor_management project.
"""

import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# In production (Render), this is set as an environment variable.
# Locally, it falls back to a dev-only default.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure--f$*s*mxh6-w+@y_g37_)cib6aj72*3jz0y0ubn#sb_@%&8jxd'
)

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG=False as an environment variable on Render.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
extra_hosts = os.environ.get('ALLOWED_HOSTS', '')
if extra_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in extra_hosts.split(',') if h.strip()])
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

CSRF_TRUSTED_ORIGINS = []
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f'https://{render_hostname}')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'visitors',
]

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

ROOT_URLCONF = 'visitor_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'visitor_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# Uses DATABASE_URL env var (Postgres) if present, otherwise local sqlite3.

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files (visitor photo uploads)
# NOTE: Render's free tier has an ephemeral filesystem - uploaded photos
# will be wiped on every redeploy/restart. Fine for testing; for real
# persistent photo storage, use a service like Cloudinary (see README).
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security hardening (only matters when DEBUG=False, i.e. in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
