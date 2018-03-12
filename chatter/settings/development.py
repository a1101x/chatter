import sys

from chatter.settings.base import *

DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

try:
    import rest_framework_swagger
except ImportError:
    pass
else:
    INSTALLED_APPS.append('rest_framework_swagger')
    VALIDATOR_URL = None
    del rest_framework_swagger

try:
    from elasticsearch_dsl.connections import connections
    connections.create_connection(hosts=['localhost'])
except ImportError:
    pass

try:
    import elastic_panel
except ImportError:
    elastic_panel = None
else:
    INSTALLED_APPS.append('elastic_panel')

try:
    import debug_toolbar
except ImportError:
    debug_toolbar = None
else:
    INTERNAL_IPS = ('127.0.0.1', 'localhost')
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
    ] + [
        'elastic_panel.panel.ElasticDebugPanel'
    ] if elastic_panel else []

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

DATABASES = {}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'chatter2',
            'USER': 'chatter',
            'PASSWORD': 'chatter',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': env.str('DATABASE_NAME', default='chatter'),
            'USER': env.str('DATABASE_USER', default='chatter'),
            'PASSWORD': env.str('DATABASE_PASSWORD', default='chatter'),
            'HOST': env.str('DATABASE_HOST', default='localhost'),
            'PORT': env.str('DATABASE_PORT', default='5432'),
        },
    }

SITE_URL = 'http://127.0.0.1:8000'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'APIS_SORTER': 'alpha',
    'SHOW_REQUEST_HEADERS': False,
}

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
MAILGUN_BASE_URL = env.str('MAILGUN_BASE_URL', default='')
MAILGUN_API_KEY = env.str('MAILGUN_API_KEY', default='')

EMAIL_TEMPLATE_DEFAULTS['EMAIL_TO'] = ''
EMAIL_TEMPLATE_DEFAULTS['BASE_URL'] = SITE_URL
EMAIL_TEMPLATE_DEFAULTS['FROM_EMAIL'] = EMAIL_HOST_USER
