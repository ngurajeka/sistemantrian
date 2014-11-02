"""
Django settings for sistemantriankpp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8(h_0p!u+%wa4(gy$e7^9v++xt731-lg_iyskv%la_wbtu_=)g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'queue',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sistemantriankpp.urls'

WSGI_APPLICATION = 'sistemantriankpp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistemantriankpp',
        'USER': 'root',
        'PASSWORD': 'sqlserverslackmachine',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Makassar'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATICFILES_FINDERS = (
 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 'django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.DefaultStorageFinder',
 )

SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'
 
# FILE_UPLOAD_TEMP_DIR = os.path.join(PROJECT_DIR, "media/temp")
# FILE_UPLOAD_PERMISSIONS = 0600

DJANGORESIZED_DEFAULT_SIZE = [140, 140]
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
TEMPLATE_CONTEXT_PROCESSORS = (
 'django.contrib.auth.context_processors.auth',
 'django.core.context_processors.request',
 'django.contrib.messages.context_processors.messages',
 )
LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'
GRAPPELLI_ADMIN_TITLE = "KPP Pratama Bulukumba"
GRAPPELLI_CLEAN_INPUT_TYPES = True
