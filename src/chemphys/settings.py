import os
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'w7r3-u^_v1e447kb%(k65^=c7$gp+)-d+*lqw1wa_ma^8ye#&c'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Nik', 'nik@init-ltd.ru'),)
MANAGERS = ADMINS

ALLOWED_HOSTS = (
    '127.0.0.1',
    'localhost',
    'chemphys.init-ltd.ru',
    'chemphys.edu.ru',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'journal',
    'pages',
    'mailauth',
    'ctxhelp',
    'udc',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'chemphys.middleware.LocaleMiddlewareEx',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'chemphys.urls'

WSGI_APPLICATION = 'chemphys.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'chemphys', 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages"
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'chemphys', 'templates'), )

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'mailauth.backend.MailAuthBackend',
)
AUTH_USER_MODEL = 'journal.JournalUser'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'chemphys', 'locale'), )
LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

USE_I18N = True
USE_L10N = True

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'chemphys', 'static'), )
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FROM_EMAIL = 'no-reply@chemphys.edu.ru'


from settings_local import *
