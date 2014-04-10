from __future__ import unicode_literals
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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

########################
## CORE CONFIGURATION ##
########################
# For official Django production deployment information, see:
# https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# You must set this setting in production!
# https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database connection information
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/1.6/ref/settings/#debug
DEBUG = bool(int(get_env_setting('DJANGO_DEBUG', default=False)))

# Email server settings (for sending notification emails to staff)
# https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend
# https://docs.djangoproject.com/en/1.6/topics/email/#smtp-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# Set this to where you want large files to be temporarily kept during upload
# (Defaults to /tmp on Unix-like systems)
# FILE_UPLOAD_TEMP_DIR = "/data/tmp"

# Files smaller than this size (in bytes) will be uploaded to memory instead 
# of the FILE_UPLOAD_TEMP_DIR location. (Defaults to 2621440, which is 2.5 MB)
# FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/1.6/ref/settings/#secret-key
SECRET_KEY = get_env_setting('DJANGO_SECRET_KEY', default=None)

# https://docs.djangoproject.com/en/1.6/topics/i18n/
TIME_ZONE = 'UTC'

############################
## END CORE CONFIGURATION ##
############################

############################
## ETD DROP CONFIGURATION ##
############################
# Set this to where you want the submission packages to go
# e.g. ETD_STORAGE_DIRECTORY = "/data/submissions"
ETD_STORAGE_DIRECTORY = get_env_setting('ETD_STORAGE_DIRECTORY', default=mkdtemp(prefix="etd-drop"))

# Contact info shown on homepage
CONTACT_PHONE = "(000) 000-0000"
CONTACT_EMAIL = "example@domain.edu"

# Uncomment if you want to get DAITSS Format Description Service output for 
# submissions (see https://github.com/MetaArchive/bag-describe)
#DESCRIPTION_SERVICE_URL = "http://localhost:3000"

# List of email addresses to receive emails when submissions are received
SUBMISSION_EMAIL_RECIPIENTS = [
    # "example1@domain.edu",
    # "example2@domain.edu",
]

# "From" address used for submission notification emails sent to staff
SUBMISSION_EMAIL_FROM_ADDRESS = "noreply@domain.edu"

# Homepage heading
HOMEPAGE_HEADING = "Submit Your Thesis"

# Homepage text
HOMEPAGE_TEXT = """
ETD Drop allows our graduate students to easily submit a copy of their thesis or dissertation electronically.

After logging in you will be asked to upload your document as a PDF. If you have any supplemental files you will also have the option to submit this content as a ZIP file.

If required, please make sure you have a signed and scanned Copyright License in PDF form available to include with your submission.

Lastly, the submission form will ask for your document's title and abstract. You can copy and paste these from your document into the corresponding form inputs.

It's that easy.
"""

# Footer text
FOOTER_TEXT = """
Footer text
"""

# Add a URL to a logo image you wish to be displayed in the footer
LOGO_IMAGE_URL = ""

# This is the agreement that will be displayed on the submission form
SUBMISSION_AGREEMENT = """
By clicking the box below I agree that this submission is complete. Any errors in this submission will require a complete re-submission. Please be sure.
"""

# Determines which fields are visible/mandatory in the submission form
SUBMISSION_FORM_FIELDS = {
    'supplemental_file': {
        'visible': True,
        'required': False,
    },
    'license_file': {
        'visible': True,
        'required': False,
    },
    'title': {
        'visible': True,
        'required': True,
    },
    'author': {
        'visible': True,
        'required': True,
    },
    'subject': {
        'visible': True,
        'required': False,
    },
    'date': {
        'visible': True,
        'required': False,
    },
    'abstract': {
        'visible': True,
        'required': True,
    },
}

################################
## END ETD DROP CONFIGURATION ##
################################

TEMPLATE_DEBUG = bool(int(get_env_setting('DJANGO_DEBUG', default=False)))

# Tolerate lack of SECRET_KEY when using DEBUG mode
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "This key is for debug mode, only!"

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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/www/etd-drop/static/'

# Post-login redirect behavior
LOGIN_REDIRECT_URL = '/submit'

# Messages overrides (for Bootstrap CSS)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Override the default absolute URLs for Users
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "",
}
