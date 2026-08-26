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
    environ.Env.read_env(dot_env_path, overwrite=True)

# ── SÉCURITÉ ──
SECRET_KEY = env('SECRET_KEY', default='change-me-in-production')
# SECURITÉ : Ne pas laisser en True en production !
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = ['sdm-mouride.com', 'www.sdm-mouride.com', 'sdm-mouride.onrender.com', 'sdm-mourit.onrender.com', 'sdm-mouride-2jbn.onrender.com', 'localhost', '127.0.0.1']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── SÉCURITÉ RENFORCÉE DES SESSIONS ──
SESSION_COOKIE_AGE = 1209600  # 2 semaines
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True        # Empêche l'accès JS au cookie de session
SESSION_COOKIE_SAMESITE = 'Lax'      # Protection CSRF via cookies
SECURE_BROWSER_XSS_FILTER = True     # Protection XSS navigateur
SECURE_CONTENT_TYPE_NOSNIFF = True   # Empêche MIME type sniffing

# En production HTTPS uniquement :
if not DEBUG:
    SESSION_COOKIE_SECURE = True     # Cookie uniquement via HTTPS
    CSRF_COOKIE_SECURE = True        # CSRF uniquement via HTTPS
    SECURE_SSL_REDIRECT = False      # Render gère HTTPS en amont

CSRF_TRUSTED_ORIGINS = [
    'https://sdm-mouride.onrender.com',
    'https://sdm-mouride-2jbn.onrender.com',
    'https://*.onrender.com',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# ── VALIDATION DES MOTS DE PASSE RENFORCÉE ──
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'bibliotheque.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# ── APPLICATIONS ──
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'bibliotheque',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'bibliotheque.debug_middleware.GlobalDebugMiddleware',
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
                'bibliotheque.context_processors.notifications_processor',
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
            conn_max_age=0,  # 0 pour fermer la connexion après chaque requête (évite les connexions mortes)
            conn_health_checks=True, # Vérifie que la DB est en vie avant de faire la requête
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
TIME_ZONE = 'Africa/Dakar'  # Fuseau horaire du Sénégal
USE_I18N = True
USE_TZ = True

# ── CLOUDINARY (pour les fichiers média : PDF, audio, images) ──
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':    env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
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

# ── Storage Configuration ──
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.RawMediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# On garde Cloudinary sous la main pour les images si besoin
CLOUDINARY_STORAGE_CONFIG = CLOUDINARY_STORAGE

# WhiteNoise configuration
WHITENOISE_MANIFEST_STRICT = False

# Backward compatibility for django-cloudinary-storage 0.3.0
# (it still references the old setting names removed in Django 6.0)
STATICFILES_STORAGE = STORAGES["staticfiles"]["BACKEND"]
DEFAULT_FILE_STORAGE = STORAGES["default"]["BACKEND"]

# ── AUTRES ──
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
# ── AUTHENTIFICATION — Toujours rediriger vers l'accueil ──
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# ── API REST & CORS ──
CORS_ALLOWED_ORIGINS = [
    'https://sdm-mouride.com',
    'https://www.sdm-mouride.com',
    'https://sdm-mouride.onrender.com',
    'https://sdm-mourit.onrender.com',
    'https://sdm-mouride-2jbn.onrender.com',
    'http://localhost:8088',
    'http://127.0.0.1:8088',
]
# CORS_ALLOW_ALL_ORIGINS = True  # Désactivé pour la production

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