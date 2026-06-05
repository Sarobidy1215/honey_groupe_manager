"""
Django settings for core project.
"""

import os  # Ajouté pour lire l'environnement ou les chemins de fichiers
from pathlib import Path

# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# ENVIRONMENT DETECTION
# =========================
# Si la variable d'environnement INFOMANIAK_ENV existe, on est sur le serveur.
# Sinon, on considère qu'on est en local.
IS_PRODUCTION = os.environ.get('INFOMANIAK_ENV') == 'True'

# =========================
# SECURITY
# =========================

SECRET_KEY = 'django-insecure-37oj0czhqd=mu)+kwr!&g788car%#^du&oudhb)@%kykqiw1go'

# Le mode DEBUG doit être False en production pour la sécurité
DEBUG = not IS_PRODUCTION


if IS_PRODUCTION:
    # Configuration pour le serveur INFOMANIAK
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ao7dvw_cotation_db',           # Le nom exact créé à l'étape 1
            'USER': 'ao7dvw_sarobidy',              # L'utilisateur créé à l'étape 2
            'PASSWORD': 'rUfqCkMT282L@R', # Ton mot de passe de l'étape 2
            'HOST': 'ao7dvw.myd.infomaniak.com',     # Le serveur hôte fourni par Infomaniak
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }

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
    # WhiteNoise permet à Django de servir les fichiers statiques de Jazzmin efficacement en production
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
# DATABASE CONFIGURATION
# =========================

if IS_PRODUCTION:
    # Configuration pour le serveur INFOMANIAK
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ao7dvw_cotation_db',           # Ta nouvelle base propre sur Infomaniak
            'USER': 'ao7dvw_sarobidy',              # L'utilisateur associé créé sur Infomaniak
            'PASSWORD': 'TON_MOT_DE_PASSE_SECURISE', # Le mot de passe défini sur l'interface
            'HOST': 'ao7dvw.myd.infomaniak.com',     # Le serveur hôte que tu as trouvé
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }
else:
    # Configuration de ton environnement LOCAL
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
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
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

# Optimisation WhiteNoise pour la production (compression des fichiers CSS/JS)
if IS_PRODUCTION:
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
            "new_window": True,
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