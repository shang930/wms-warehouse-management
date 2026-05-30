"""Django base settings for WMS."""

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / 'apps'

DJANGO_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework','rest_framework_simplejwt','corsheaders',
    'django_filters','drf_spectacular','django_extensions','channels',
]
LOCAL_APPS = [
    'apps.users','apps.goods','apps.warehouse','apps.supplier','apps.customer',
    'apps.stock','apps.asn','apps.dn','apps.cyclecount','apps.capital','apps.report',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('DB_NAME','wms'),'USER':os.getenv('DB_USER','wms_user'),'PASSWORD':os.getenv('DB_PASSWORD','wms_password'),'HOST':os.getenv('DB_HOST','127.0.0.1'),'PORT':os.getenv('DB_PORT','5432')}}
CACHES = {'default':{'BACKEND':'django.core.cache.backends.redis.RedisCache','LOCATION':os.getenv('REDIS_URL','redis://127.0.0.1:6379/0')}}
CELERY_BROKER_URL = os.getenv('CELERY_BROKER','redis://127.0.0.1:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_BACKEND','redis://127.0.0.1:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CHANNEL_LAYERS = {'default':{'BACKEND':'channels_redis.core.RedisChannelLayer','CONFIG':{'hosts':[os.getenv('REDIS_URL','redis://127.0.0.1:6379/3')]}}}

AUTH_USER_MODEL = 'users.User'
SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME':timedelta(hours=8),'REFRESH_TOKEN_LIFETIME':timedelta(days=7),'ROTATE_REFRESH_TOKENS':True,'AUTH_HEADER_TYPES':('Bearer',)}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_FILTER_BACKENDS':('django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter'),
    'DEFAULT_PAGINATION_CLASS':'utils.pagination.StandardPagination',
    'PAGE_SIZE':20,
    'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER':'utils.exceptions.custom_exception_handler',
}
SPECTACULAR_SETTINGS = {'TITLE':'WMS API','DESCRIPTION':'仓库管理系统 RESTful API','VERSION':'1.0.0','SERVE_INCLUDE_SCHEMA':False}

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
LOGGING = {'version':1,'disable_existing_loggers':False,'formatters':{'verbose':{'format':'[{levelname}] {asctime} {module} {message}','style':'{'}},'handlers':{'console':{'class':'logging.StreamHandler','formatter':'verbose'}},'root':{'handlers':['console'],'level':'INFO'}}
