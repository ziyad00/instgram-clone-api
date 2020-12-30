"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from copy import deepcopy
import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',


    # third party
    'rest_framework',
    'rest_framework.authtoken',  
    'djoser',
    'rest_framework_simplejwt',
    'drf_yasg',


    # local
    'account',
    'images.apps.ImagesConfig',
    'actions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

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


#AUTH_USER_MODEL = 'account.User'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DATA_DIR = f"{BASE_DIR}/data"

AVATAR_URI_PREFIX = "/public/avatar"
AVATAR_UPLOAD_DIR = f"{DATA_DIR}{AVATAR_URI_PREFIX}"


STATICFILES_DIRS = [os.path.join(DATA_DIR, "static")]
SITE_ID = 1

LOGGING_HANDLERS = ['console']
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'standard': {
           'format': '[%(asctime)s] - [%(levelname)s] - [%(name)s:%(lineno)d]  - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S'
       }
   },
   'handlers': {
       'console': {
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
           'formatter': 'standard'
       },
   #    'sentry': {
    #       'level': 'ERROR',
     #      'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
      #     'formatter': 'standard'
       #}
   },
   'loggers': {
       'django.request': {
           'handlers': LOGGING_HANDLERS,
           'level': 'ERROR',
           'propagate': True,
       },
       'django.db.backends': {
           'handlers': LOGGING_HANDLERS,
           'level': 'ERROR',
           'propagate': True,
       },
        'dramatiq': {
            'handlers': LOGGING_HANDLERS,
            'level': 'DEBUG',
            'propagate': False,
        },
       '': {
           'handlers': LOGGING_HANDLERS,
           'level': 'WARNING',
           'propagate': True,
       }
   },
}






REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', 
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
    
}

DJOSER = {
    #'LOGIN_FIELD': 'email',
 #   'SERIALIZERS': {
  #  'user_create': 'api.serializers.UserSerializer',
   # 'user': 'api.serializers.UserSerializer'

    #}
}


SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}


# Activate Django-Heroku.
django_heroku.settings(locals())

PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT  =   os.path.join(PROJECT_ROOT, 'staticfiles')