from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY","changeme")
DEBUG = os.getenv("DJANGO_DEBUG","0") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","").split(",") if os.getenv("ALLOWED_HOSTS") else ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",

    # Apps de terceros
    "corsheaders",
    "rest_framework",
    "drf_spectacular",

    # Tus apps
    "customers",
    "products",
    "sales",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND":"django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors":[
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE":"django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB","ventas"),
        "USER": os.getenv("POSTGRES_USER","ventas"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD","ventas"),
        "HOST": os.getenv("POSTGRES_HOST","localhost"),
        "PORT": os.getenv("POSTGRES_PORT","5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-co"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Sistema de Ventas - API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),   # Access token válido 30 min
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),      # Refresh token válido 5 días
    "ROTATE_REFRESH_TOKENS": False,                   # No rota el refresh al usarlo
    "BLACKLIST_AFTER_ROTATION": True,                 # Si rotas, el anterior queda inválido
    "AUTH_HEADER_TYPES": ("Bearer",),                 # Autenticación con "Authorization: Bearer <token>"
}

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS","").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else []
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True