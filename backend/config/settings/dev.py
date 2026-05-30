from .base import *  # noqa

DEBUG = True
SECRET_KEY = 'django-insecure-dev-only-wms-2026-key-change-in-production'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F821
    }
}

CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
CELERY_TASK_ALWAYS_EAGER = True
