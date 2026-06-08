from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(_file_).resolve().parent.parent

SECRET_KEY = 'django-insecure-cambia-esto-en-produccion'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'corsheaders',

    # Nuestras apps
    'usuarios',
    'validacion',
    'votacion',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # debe ir primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'votacion_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'votacion_backend.wsgi.application'

# =========================
# BASE DE DATOS MYSQL
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        # Variables para GitHub Actions y producción
        'NAME': os.getenv('DB_NAME', 'votacion_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# =========================
# JWT
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# =========================
# CORS
# =========================
CORS_ALLOW_ALL_ORIGINS = True

# =========================
# MEDIA FILES
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================
# INTERNACIONALIZACIÓN
# =========================
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'

USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# MODELO DE USUARIO
# =========================
AUTH_USER_MODEL = 'usuarios.Votante'

# =========================
# WEBHOOKS N8N
# =========================
N8N_WEBHOOK_VOTO = 'https://jhoanaronith.app.n8n.cloud/webhook/36edb614-1e26-485d-a734-59b522befd56'

N8N_WEBHOOK_ALERTA = 'https://jhoanaronith.app.n8n.cloud/webhook-test/3c72772a-3180-4e7e-9a0d-860aa98da8ec'

CORREO_ADMIN = "jhoaro2503@gmail.com"