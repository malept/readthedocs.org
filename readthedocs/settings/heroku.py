from .base import *  # noqa
import json
import os
import dj_database_url
from urlparse import urlparse

DATABASES = {
    'default': dj_database_url.config(),
}

DEBUG = os.environ.get('HEROKU_DEBUG') == '1'
TEMPLATE_DEBUG = DEBUG
CELERY_ALWAYS_EAGER = False

SECRET_KEY = os.environ['SECRET_KEY']
PRODUCTION_DOMAIN = os.environ['APP_DOMAIN_NAME']
SESSION_COOKIE_DOMAIN = PRODUCTION_DOMAIN

SLUMBER_API_HOST = 'https://{}'.format(PRODUCTION_DOMAIN)
SLUMBER_USERNAME = os.environ['SLUMBER_USERNAME']
SLUMBER_PASSWORD = os.environ['SLUMBER_PASSWORD']

DEFAULT_PRIVACY_LEVEL = 'private'

GLOBAL_ANALYTICS_CODE = os.environ.get('GOOGLE_ANALYTICS_CODE', '')

ADMINS = MANAGERS = json.loads(os.environ['ADMIN_INFO'])

del LOGGING

MEDIA_ROOT = 'media'
ADMIN_MEDIA_PREFIX = '{}admin/'.format(MEDIA_URL)
STATIC_ROOT = 'staticfiles'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(SITE_ROOT, 'whoosh_index'),
    },
}

unparsed_redis_url = os.environ['REDISTOGO_URL']
redis_url = urlparse(unparsed_redis_url)
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
        'PREFIX': 'docs',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PASSWORD': redis_url.password,
        },
    },
}

REDIS = {
    'host': redis_url.hostname,
    'port': redis_url.port,
    'password': redis_url.password,
    'db': 0,
}

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'

INSTALLED_APPS.append('kombu.transport.django')

es_url_unparsed = os.environ.get('BONSAI_URL')
if es_url_unparsed:
    es_url = urlparse(es_url_parsed)
    ES_HOSTS = [{
        'host': es_url.hostname,
        'port': es_url.port,
        'use_ssl': es_url.scheme == 'https',
        'http_auth': (es_url.username, es_url.password),
    }]
ES_DEFAULT_NUM_SHARDS = 1

BUGSNAG = {
    'project_root': os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                  '../..')),
    'use_ssl': True,
}

MIDDLEWARE_CLASSES += (
    'bugsnag.django.middleware.BugsnagMiddleware',
)

USE_SUBDOMAIN = False
NGINX_X_ACCEL_REDIRECT = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Lock builds for 10 minutes
REPO_LOCK_SECONDS = 300

# Don't re-confirm existing accounts
ACCOUNT_EMAIL_VERIFICATION = 'none'

# set GitHub scope
SOCIALACCOUNT_PROVIDERS = {
    'github': { 'SCOPE': ['user:email', 'public_repo', 'read:org', 'admin:repo_hook', 'repo:status']}
}

TIME_ZONE = os.environ.get('RTFD_TIME_ZONE', TIME_ZONE)

try:
    from local_settings import *  # noqa
except ImportError:
    pass
