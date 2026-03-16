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
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL')
    )
}
# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- CONFIGURATION CLOUDINARY ---
# --- CONFIGURATION CLOUDINARY ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'RESOURCE_TYPE': 'auto' 
}
# Remplace tes lignes actuelles par celles-ci :
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build') # On change le nom ici

# Indispensable pour la compatibilité Cloudinary + Django 6 sur Render
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

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