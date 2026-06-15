"""
Django settings for backend project.
"""

from pathlib import Path

import environ

from .env_adapter import get_environment_config

# ---------------------------------------------------------------------------
# Platform — all the detection logic resides in env_adapter.py
# ---------------------------------------------------------------------------

platform = get_environment_config()
IS_PROD = platform.is_production

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

if not IS_PROD:
    env_file = ".env.local" if Path(".env.local").is_file() else ".env"
    environ.Env.read_env(env_file)

DEBUG = env.bool("DEBUG", default=False)

if IS_PROD:
    SECRET_KEY = env("SECRET_KEY")
else:
    SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-in-production")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
ALLOWED_HOSTS.extend(platform.extra_allowed_hosts)  # hostname inyectado por la plataforma

# ---------------------------------------------------------------------------
# Apps & Middleware
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "graphene_django",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="dummy"),
        "HOST": env("DB_HOST", default="dummy"),
        "USER": env("DB_USER", default="dummy"),
        "PASSWORD": env("DB_PASSWORD", default="dummy"),
        "PORT": env("DB_PORT", default="5432"),
        "OPTIONS": {
            "sslmode": "require" if IS_PROD else "disable",
        },
    }
}

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------

STATIC_URL = "static/"

if IS_PROD:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------

GRAPHENE = {"SCHEMA": "core.schema.schema"}

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

if IS_PROD:
    CORS_ALLOWED_ORIGINS = [
        env("CORS_ORIGIN_MAIN", default="https://crashcourse.jcvegab.dev"),
    ]
    CORS_ALLOWED_ORIGIN_REGEXES = [
        env("CORS_ORIGIN_REGEX", default=r"^https://.*-jcvegab\.vercel\.app$"),
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

CSRF_COOKIE_SECURE = IS_PROD
SESSION_COOKIE_SECURE = IS_PROD
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")