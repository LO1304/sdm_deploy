import os
import environ
from pathlib import Path

# ── Initialisation d'environ ──
env = environ.Env(DEBUG=(bool, False))

# ── Chemin de base du projet ──
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Lecture du fichier .env (local et PythonAnywhere) ──
dot_env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dot_env_path):
    environ.Env.read_env(dot_env_path)

# ── SÉCURITÉ ──
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'sdm-mouride.onrender.com',
    'sdm-mouride-2jbn.onrender.com',
    '.onrender.com',
    '.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
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
# Render avec PostgreSQL → sinon SQLite (local et PythonAnywhere)
if 'RENDER' in os.environ and 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
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

# ── CLOUDINARY (une seule définition propre) ──
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default='local'),
    'API_KEY':    env('CLOUDINARY_API_KEY',    default='local'),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default='local'),
    'SECURE': True,
    'RESOURCE_TYPE': 'auto',
}

# ── FICHIERS STATIQUES & MEDIA ──
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')
MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')

# Stockage : Cloudinary uniquement sur Render, local sinon
if 'RENDER' in os.environ:
    STATICFILES_STORAGE  = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
else:
    STATICFILES_STORAGE  = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ── AUTRES ──
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL  = '/collection/son/'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL           = 'login'