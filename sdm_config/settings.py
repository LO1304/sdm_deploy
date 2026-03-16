import os
import environ
from pathlib import Path

# Initialisation d'environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier .env
# Assure-toi que ton fichier .env est bien à la racine (au même niveau que manage.py)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- PARAMÈTRES DE SÉCURITÉ (Extraits du .env) ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

# En production, on ajoute l'adresse de Render iciLLOWED_HOSTS = ['sdm-project.onrender.com', '127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['sdm-mouride-2jbn.onrender.com', 'localhost', '127.0.0.1']
# --- APPLICATIONS INSTALLÉES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Doit être AVANT staticfiles
    'django.contrib.staticfiles',
    'cloudinary',
    'bibliotheque', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Ajouté pour les fichiers statiques en production
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES ET MÉDIA ---
STATIC_URL = 'static/'
# Configuration du stockage pour Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "cloudinary_storage.storage.StaticHashedCloudinaryStorage",
    },
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Obligatoire pour la production

# Configuration Cloudinary via le fichier .env
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'
# MEDIA_ROOT n'est plus nécessaire avec Cloudinary mais on le laisse par sécurité
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/collection/son/'
LOGOUT_REDIRECT_URL = 'login'


