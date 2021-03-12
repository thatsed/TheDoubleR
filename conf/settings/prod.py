"""
Production Django settings for TheDoubleR project.
"""
import os

from .base import *

DATA_DIR = Path('/data')

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

if 'POSTGRES_HOST' in os.environ.keys():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ['POSTGRES_HOST'],
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATA_DIR / 'db.sqlite3',
        }
    }

STATIC_ROOT = DATA_DIR / 'static'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': DATA_DIR / 'cache/django',
    }
}
