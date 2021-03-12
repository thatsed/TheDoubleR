"""
Development Django settings for TheDoubleR project.
"""
from .base import *


SECRET_KEY = ')0txxob)v34=8_mybd=t=t2nx-wc6q@zu_fzy+ic0b4bhbn3l1'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
    }
}
