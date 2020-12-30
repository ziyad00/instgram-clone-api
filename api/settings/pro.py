from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['instgram01.herokuapp.com']

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd49g8oerua4a2b', 
        'USER': 'dyuxqpgeopzqui', 
        'PASSWORD': '599e3f6aab7ba1b75918d6f92e7528d5e377d86eb37f0fe867b7cf724dc375e1',
        'HOST': 'ec2-54-208-233-243.compute-1.amazonaws.com', 
        'PORT': '5432',
    }
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'



CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": os.environ.get('REDIS_URL'),
    }
}


REDIS_HOST = 'ec2-3-94-248-0.compute-1.amazonaws.com'
REDIS_PORT = 23739
REDIS_DB = 0
REDIS_PASSWORD = 'pe5b6ce28890a35a4136b0d640ae7323cbd66bff3a3013e957c3aa781b0a041c7'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.mailgun.org'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
#EMAIL_USE_TLS = True