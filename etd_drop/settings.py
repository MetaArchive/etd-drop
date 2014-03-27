"""
Django settings for etd_drop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
from os import environ
from tempfile import mkdtemp

from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting, default=None, required=False):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        if required and default==None:
            error_msg = "Set the %s env variable" % setting
            raise ImproperlyConfigured(error_msg)
        return default

############################
## ETD DROP CONFIGURATION ##
############################

# Set this to where you want the submission packages to go
ETD_STORAGE_DIRECTORY = get_env_setting('ETD_STORAGE_DIRECTORY', default=mkdtemp(prefix="etd-drop"))
#ETD_STORAGE_DIRECTORY = "/data/submissions"

# Set this to where you want large files to be temporarily kept during upload
# (Defaults to /tmp on Unix-like systems)
#FILE_UPLOAD_TEMP_DIR = "/data/tmp"

# Files smaller than this size (in bytes) will be uploaded to memory instead 
# of the FILE_UPLOAD_TEMP_DIR location. (Defaults to 2621440, which is 2.5 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

# Uncomment if you want to get DAITSS Format Description Service output for 
# submissions
#DESCRIPTION_SERVICE_URL = "http://localhost:3000"

# This is the agreement that will be displayed on the submission page.
SUBMISSION_AGREEMENT = """
I agree to submit this thing to this web site, and to not get upset about it later on.

This is a second paragraph of the agreement.
"""

################################
## END ETD DROP CONFIGURATION ##
################################


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8j0yk=h17!#5)io)-23g(_)9rw!h3@lrf-aht%tvx4g*t*@7yq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(get_env_setting('DJANGO_DEBUG', default=False))
TEMPLATE_DEBUG = bool(get_env_setting('DJANGO_DEBUG', default=False))

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'etd_drop_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'etd_drop.urls'
WSGI_APPLICATION = 'etd_drop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

# Post-login redirect behavior
LOGIN_REDIRECT_URL = '/submit'

# Messages overrides (for Bootstrap CSS)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
