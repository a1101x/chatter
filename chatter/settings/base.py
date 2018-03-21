import os
import datetime

from envparse import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',

    # third party apps
    'channels',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_jwt',
    'rest_auth',
    'allauth',
    'allauth.account',
    'corsheaders',
    'mapwidgets',

    # our apps
    'apps.user',
    'apps.phone',
    'apps.location',
    'apps.mailer'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')],
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

WSGI_APPLICATION = 'chatter.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = False

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='amqp://localhost')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERY_SEND_EVENTS = False
CELERY_RESULT_BACKEND = None

AUTH_USER_MODEL = 'user.User'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'apps.utils.renderer.ChatterRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'apps.utils.exception_handler.chatter_exception_handler',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365)
}

REST_USE_JWT = True
REST_SESSION_LOGIN = False
OLD_PASSWORD_FIELD_ENABLED = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with'
)

MAP_WIDGETS = {
    'GooglePointFieldWidget': (
        ('zoom', 10),
        ('mapCenterLocation', [47.8388, 35.139567]),
    ),
    'LANGUAGE': 'en',
    'GOOGLE_MAP_API_KEY': env.str('GOOGLE_MAP_API_KEY', default=''),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.utils.backend.EmailOrUsernameModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

EMAIL_TEMPLATE_DEFAULTS = {
    'CONTEXT': {
        'header_image': '/static/images/logo.png',
        'footer_links': [],
        'footer_content': 'Footer content from settings.',
        'footer_copyright': '',
        'colors': {
            'background': "#EEEEEE",
            'container_border': "#DDDDDD",
            'container_background': "#FFFFFF",
            'container': "#505050",
            'title': "#444444",
            'footer': "#888888",
            'footer_link': "#2C9AB7",
            'button': "#2C9AB7",
        }
    },
    'TEMPLATE_NAME': 'mail/default.html'
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'apps.user.serializers.JWTUserSerializer',
    'LOGIN_SERIALIZER': 'apps.user.serializers.LoginSerializer'
}

CHANNEL_REDIS_HOST = env.str('CHANNEL_REDIS_HOST', default='localhost')
CHANNEL_REDIS_PORT = env.int('CHANNEL_REDIS_PORT', default=6379)
ASGI_APPLICATION = 'chatter.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(CHANNEL_REDIS_HOST, CHANNEL_REDIS_PORT)],
        },
    },
}

ACTIVATION_CODE_LIFETIME = env.int('ACTIVATION_CODE_LIFETIME', default=30)
