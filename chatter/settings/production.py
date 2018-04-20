from chatter.settings.base import *

DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DATABASE_NAME', default=''),
        'USER': env.str('DATABASE_USER', default=''),
        'PASSWORD': env.str('DATABASE_PASSWORD', default=''),
        'HOST': env.str('DATABASE_HOST', default=''),
        'PORT': env.str('DATABASE_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
MAILGUN_BASE_URL = env.str('MAILGUN_BASE_URL', default='')
MAILGUN_API_KEY = env.str('MAILGUN_API_KEY', default='')

SITE_URL = ''
EMAIL_TEMPLATE_DEFAULTS['EMAIL_TO'] = ''
EMAIL_TEMPLATE_DEFAULTS['BASE_URL'] = SITE_URL
EMAIL_TEMPLATE_DEFAULTS['FROM_EMAIL'] = EMAIL_HOST_USER

REDIS_MESSAGES_TIMEOUT = 60 * 60
REDIS_CHAT_URL_HOST = env.str('REDIS_CHAT_URL_HOST', default='')
REDIS_CHAT_URL_PORT = env.int('REDIS_CHAT_URL_PORT', default=6379)
REDIS_CHAT_URL_DB = env.int('REDIS_CHAT_URL_DB', default=0)
REDIS_CHAT_CHARSET = env.str('REDIS_CHAT_URL_DB', default='utf-8')
REDIS_CHAT_DECODE_RESPONSES = env.bool('REDIS_CHAT_DECODE_RESPONSES', default=True)
ELASTICSEARCH_CHAT_HOST = env.str('ELASTICSEARCH_CHAT_HOST', default='')
