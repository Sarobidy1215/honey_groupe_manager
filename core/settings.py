"""
Django settings for core project.
"""

from pathlib import Path
import os

# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =========================
# SECURITY
# =========================

SECRET_KEY = 'django-insecure-37oj0czhqd=mu)+kwr!&g788car%#^du&oudhb)@%kykqiw1go'

# Render / production switch
RENDER = os.getenv("RENDER", False)

DEBUG = not RENDER

ALLOWED_HOSTS = ['*']

# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cotation',
]

# =========================
# MIDDLEWARE
# =========================

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

# =========================
# URLS
# =========================

ROOT_URLCONF = 'core.urls'

# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

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

# =========================
# WSGI
# =========================

WSGI_APPLICATION = 'core.wsgi.application'

# =========================
# DATABASE
# =========================

if RENDER:
    # Démo Render (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Local MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'honey_group_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Indian/Antananarivo'

USE_I18N = True

USE_TZ = True

# =========================
# STATIC FILES
# =========================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'cotation' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise (important Render)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# LOGIN / LOGOUT
# =========================

LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/'

# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# JAZZMIN SETTINGS
# =========================

JAZZMIN_SETTINGS = {
    "site_title": "Honey Group",
    "site_header": "Honey Group Admin",
    "site_brand": "Honey Group",
    "welcome_sign": "Gestion des Cotations",
    "copyright": "Honey Group Madagascar",
    "site_logo": "img/honey.jpg",
    "login_logo": "img/honey.jpg",
    "site_icon": "img/honey.jpg",
    "theme": "flatly",
    "navigation_expanded": True,
    "show_sidebar": True,
    "changeform_format": "horizontal_tabs",

    "topmenu_links": [
        {
            "name": "Site Web",
            "url": "/",
            "new_window": True
        },
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "cotation.Circuit": "fas fa-route",
        "cotation.CircuitJour": "fas fa-calendar-day",
        "cotation.ReferenceTarifaire": "fas fa-money-bill-wave",
        "cotation.DemandeCotation": "fas fa-file-invoice-dollar",
        "cotation.ResultatCotation": "fas fa-chart-line",
        "cotation.CatalogueDestination": "fas fa-map-marked-alt",
    },
}