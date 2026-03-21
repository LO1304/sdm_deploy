import os
import environ
from pathlib import Path

# 1. Initialisation d'environ
env = environ.Env(
    DEBUG=(bool, False)
)

# 2. Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. Lecture du fichier .env (uniquement en local)
# Sur Render, les variables sont lues directement dans l'onglet Environment
dot_env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dot_env_path):
    environ.Env.read_env(dot_env_path)

# --- PARAMÈTRES DE SÉCURITÉ ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

# On garde les hôtes locaux et l'adresse de Render
ALLOWED_HOSTS = ['sdm-mouride-2jbn.onrender.com', 'localhost', '127.0.0.1']

# --- APPLICATIONS INSTALLÉES ---
INSTALLED_APPS = [
    'cloudinary_storage',  # TOUJOURS en premier pour les fichiers statiques
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
    'whitenoise.middleware.WhiteNoiseMiddleware', # Gestion des fichiers statiques
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

# --- BASE DE DONNÉES ---
# Note : SQLite s'efface à chaque redémarrage sur Render. 
# À l'avenir, une base PostgreSQL (ex: Neon ou Render DB) sera préférable.
import os

# Si on est sur Render, on utilise DATABASE_URL, sinon on utilise SQLite localement
if 'RENDER' in os.environ:
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
# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- CONFIGURATION CLOUDINARY ---
# --- CONFIGURATION CLOUDINARY ---
# --- CONFIGURATION CLOUDINARY ---
# On utilise .get() ou un default pour éviter le crash "KeyError" sur ton PC
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default='local'),
    'API_KEY': env('CLOUDINARY_API_KEY', default='local'),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default='local'),
    'SECURE': True,
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')

# On ne force Cloudinary que si on est sur Render
if 'RENDER' in os.environ:
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # En local, on reste simple pour ne pas dépendre d'Internet
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# Configuration moderne des stockages
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'RESOURCE_TYPE': 'auto'
}

# CETTE LIGNE DOIT ÊTRE EN DEHORS DES ACCOLADES CI-DESSUS
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- AUTRES PARAMÈTRES ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/collection/son/'
LOGOUT_REDIRECT_URL = 'login'