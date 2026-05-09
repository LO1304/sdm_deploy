import os
import environ
from pathlib import Path

# ── Initialisation d'environ ──
env = environ.Env(DEBUG=(bool, False))

# ── Chemin de base du projet ──
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Lecture du fichier .env (local uniquement) ──
dot_env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dot_env_path):
    environ.Env.read_env(dot_env_path)

# ── SÉCURITÉ ──
SECRET_KEY = env('SECRET_KEY', default='change-me-in-production')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'sdm-mouride.onrender.com',
    'sdm-mouride-2jbn.onrender.com',
    '.onrender.com',
    '.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# ── CSRF Protection pour Render (HTTPS) ──
CSRF_TRUSTED_ORIGINS = [
    'https://sdm-mouride.onrender.com',
    'https://sdm-mouride-2jbn.onrender.com',
    'https://*.onrender.com',
]

# ── APPLICATIONS ──
INSTALLED_APPS = [
    'cloudinary_storage',   # TOUJOURS en premier
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'bibliotheque',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'sdm_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bibliotheque', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'sdm_config.wsgi.application'

# ── BASE DE DONNÉES ──
# Render avec PostgreSQL → sinon SQLite (local)
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# ── INTERNATIONALISATION ──
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── CLOUDINARY (pour les fichiers média : PDF, audio, images) ──
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default='dcajqzg2h'),
    'API_KEY':    env('CLOUDINARY_API_KEY',    default='138657288257876'),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default='8trLcatgU47lqR6ewysOQ9tAiKY'),
    'SECURE': True,
    'RESOURCE_TYPE': 'auto',
}

# ── Fichiers Statiques & Media ──
STATIC_URL  = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')

# ── Storage Configuration (Django 6.0+ compatible) ──
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.RawMediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Backward compatibility for django-cloudinary-storage 0.3.0
# (it still references the old setting names removed in Django 6.0)
STATICFILES_STORAGE = STORAGES["staticfiles"]["BACKEND"]
DEFAULT_FILE_STORAGE = STORAGES["default"]["BACKEND"]

# ── AUTRES ──
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL  = '/collection/son/'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL           = 'login'

# ── API REST & CORS ──
CORS_ALLOW_ALL_ORIGINS = True  # Pour autoriser Flutter

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}