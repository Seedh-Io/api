"""
Django settings for backend_api project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Rest Framework
    'rest_framework',
    'knox',

    # Custom Apps
    'users',
    'business',
    'metadata',
    'packages',
    'orders',
    'payments'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middlewares from Libraries
    'log_request_id.middleware.RequestIDMiddleware',
]

ROOT_URLCONF = 'backend_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2'
        ,
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'backend_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Todo add this to config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "seedh",
        'USER': "",
        'PASSWORD': "",
        'HOST': "localhost",
        'PORT': "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# todo Add this to config
log_location = "./Logs"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'backend_api.formatter.CustomJSONLoggerFormatter.CustomJSONLoggerFormatter',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'fileInfo': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': log_location + "/info.log",
            'when': 'D',
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
        'fileWarning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'filename': log_location + "/warning.log",
            'formatter': 'verbose'
        },
        'jsonFile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'filename': log_location + "/info_json.log",
            'formatter': 'json',
            'filters': ['request_id']
        }

    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console', 'fileInfo', 'fileWarning'],
        #     'level': "DEBUG",
        #     'propagate': True,
        # },
        '': {
            'handlers': ['console', 'jsonFile'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['jsonFile'],
            'level': 'DEBUG',
        }
    }
}

# Custom Authentication
AUTH_USER_MODEL = 'users.UserModel'

REST_KNOX = {
    'TOKEN_TTL': timedelta(hours=10),
    'AUTO_REFRESH': True,
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'backend_api.helpers.custom_exception_helper.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'backend_api.formatter.JSONResponseFormatter.JSONResponseFormatter',
    )
}

WEBSITE_HOST = "localhost:8000"
ENV = "development"
