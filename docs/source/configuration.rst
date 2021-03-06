=============
Configuration
=============

ETD Drop is configured using values defined in the ``settings.py`` file in the 
``etd_drop`` directory of the project.

.. contents::
    :local:
    :depth: 2

Environment Variables
=====================

For ease of deployment or local testing, some configuration values can be set 
using environment variables. Environment variables can be set up in web server 
configurations (like Apache and Nginx), set in your personal .bashrc 
or .profile files for easy personal use, or stated at the beginning of a 
terminal command (for example: ``DJANGO_DEBUG=1 python manage.py runserver``).

ETD-Drop supports the 'dotenv' configuration convention, and will look for a
.env file in the top level directory with values for runtime-configurable
settings.

DJANGO_DEBUG
------------

Accepted values: 1 (meaning debug mode is on) or 0 (meaning debug mode is off)

Overrides the default DEBUG setting.

DJANGO_SECRET_KEY
-----------------

Accepted values: Any string

Overrides the SECRET_KEY setting, which should be set to a long, randomized 
string of characters used for security purposes (see the SECRET_KEY section 
later in this page).

ETD_STORAGE_DIRECTORY
---------------------

Accepted values: Any valid pathname

Overrides the ETD_STORAGE_DIRECTORY setting, which is where the stored
ETDs that are uploaded will be kept. Make sure that this directory exists
and is writable by the ETD-Drop process.

ENABLE_CLAMD
------------

Accepted values: 1 (on) or 0 (off) (default)

Set to 1 if you want ETD-Drop to use Clam Antivirus to scan uploaded ETDs.
This requires that the Clam-AV Daemon be installed and running.

DJANGO_LOGGING_LEVEL
--------------------

Accepted values: 'DEBUG', 'INFO', 'WARNING', 'ERROR' or 'CRITICAL'

Overrides the LOGGING_LEVEL setting, which controls the severity of events
that will be reported by the logger.

DJANGO_LOGGING_PATH
-------------------

Accepted values: Any valid pathname

Overrides the LOGGING_PATH setting, which controls where ETD-Drop will
keep its logs. Make sure that the file is writable by the ETD-Drop
process.

Core settings
=============

These are standard Django settings you will want to pay special attention to:

ALLOWED_HOSTS
-------------

See: https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts

DATABASES
---------

Specifies the connection information Django should use for all of its 
database operations (in the case of ETD Drop, this is for users/sessions).

By default, this is configured to use a SQLite3 file located in the project 
directory (which will be created automatically if it doesn't exist). 
SQLite3 should be sufficient for the needs of this application, but you may 
still prefer to change these settings to use an external database (e.g. MySQL) 
instead.

See: https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DEBUG
-----

Default: bool(int(get_env_setting('DJANGO_DEBUG', default=False)))

A boolean (True or False) value that decides if Django should run in "debug" 
mode. In debug mode, Django runs with fewer security restrictions and allows 
detailed error messages to be displayed in the browser. **It is very 
important not to use debug mode in production environments.**

The default value of DEBUG attempts to load the setting from an environment 
variable named DJANGO_DEBUG (which should be set to 1 if True or 0 if False). 
If this environment variable is not set, False will be used by default.

EMAIL_BACKEND
-------------

Default: 'django.core.mail.backends.smtp.EmailBackend'

The Django email backend to use for sending email. SMTP is the default, which 
is the most commonly-used server type for sending email.

For a full list of possible backends, see: 
https://docs.djangoproject.com/en/1.6/topics/email/#smtp-backend

See general information about this setting, see:
https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend

EMAIL_HOST
----------

Default: 'localhost'

Hostname of SMTP server (or other selected backend type).

EMAIL_HOST_PASSWORD
-------------------

Default: ''

Password for authenticating with SMTP server (or other selected backend type).

EMAIL_HOST_USER
---------------

Default: ''

Username for authenticating with SMTP server (or other selected backend type).

EMAIL_PORT
----------

Default: 25

EMAIL_USE_TLS
-------------

Default: ``False``

See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-use-tls

FILE_UPLOAD_TEMP_DIR
--------------------

Default: ``None``

The location where user-submitted files are temporarily kept before the 
submission package is built. If not defined (or set to ``None``), the system's 
default temporary directory (e.g. ``/tmp``) will be used.

To account for large uploads, you may wish to change this setting to a path 
on a volume where storage is plentiful.

FILE_UPLOAD_MAX_MEMORY_SIZE
---------------------------

Default: 2621440

Uploaded files smaller than this size (in bytes) will be temporarily stored 
in memory (RAM) instead of being stored as a file in ``FILE_UPLOAD_TEMP_DIR``. 
This results in faster uploads, but will consume more system memory during 
uploads depending on how high this limit is set.

Note: 2621440 bytes = 2.5 MB

SECRET_KEY
----------

Default: ``SECRET_KEY = get_env_setting('DJANGO_SECRET_KEY', default=None)``

A string containing a unique, unpredictable set of characters known only to 
the server.

The default value attempts to do two things:

1. If an environment variable called DJANGO_SECRET_KEY is set, it will use 
   that value for this setting.
2. Otherwise, the setting will be set to ``None`` and the application will 
   not be able to start.

One way of generating a good random key is using the following command::

    python -c 'import random; import string; print "".join([random.SystemRandom().choice(string.digits + string.letters + string.punctuation) for i in range(100)])'

See: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-SECRET_KEY

TIME_ZONE
---------

Default: 'UTC'

See: https://docs.djangoproject.com/en/1.6/topics/i18n/

ETD Drop settings
=================

These settings apply specifically to the functionality of ETD Drop, and will 
allow you to customize some of the functionality and presentation of the ETD 
Drop web application itself:

ETD_STORAGE_DIRECTORY
---------------------

Default: ``get_env_setting('ETD_STORAGE_DIRECTORY', default=mkdtemp(prefix="etd-drop"))``

A string representing the absolute path of the directory where ETD submissions 
should be stored. In practice, you will want to use a directory on a volume 
that is

* large enough to accommodate the submissions you anticipate receiving
* able to be accessed by the people in your organization whose staff will be 
  responsible for receiving and processing the submission packages (via SFTP, 
  SCP, Windows shared directory (SMB), etc.).

The default value attempts to do two things:

1. If an environment variable called ETD_STORAGE_DIRECTORY is set, it will use 
   that value for this setting.
2. Otherwise, it will try to create a directory in your system's temporary 
   directory (e.g. ``/tmp``) prefixed with the name "etd-drop" and use that 
   location instead. (This is useful for local testing, but obviously should 
   not be used in production since anything stored there will not be 
   permanently saved!)

If you would rather not use an environment variable to specify the directory, 
you can replace this line with something as simple as:

    ETD_STORAGE_DIRECTORY = "/mnt/data"

(replacing `/mnt/data` with the actual path you wish to use).

CONTACT_PHONE
-------------

A string containing a phone number that will be displayed on the homepage for 
users to call if they need help. If this setting is blank or undefined, the 
phone number will be hidden.

CONTACT_EMAIL
-------------

A string containing an email address that will be displayed on the homepage 
for users to email if they need help. If this setting is blank or undefined, 
the email address will be hidden.

DESCRIPTION_SERVICE_URL
-----------------------

Default: Not set

A string containing a URL to a running instance of the DAITSS Format 
Description service (https://github.com/daitss/describe).

If set, the description service will be used to generate PREMIS-formatted 
identification/validation/characterization data (powered by DROID, JHOVE) for 
each of the files in the submission package when submissions are created.

For more information about this process and how to run your own instance of 
the Format Description Service in your environment, see: 
https://github.com/MetaArchive/bag-describe

Example: ``DESCRIPTION_SERVICE_URL = "http://localhost:3000"``

SUBMISSION_EMAIL_RECIPIENTS
---------------------------

Default: ``[]``

A list of strings representing email addresses to notify when a new submission 
is received. If this list is empty, no email will be sent.

SUBMISSION_EMAIL_FROM_ADDRESS
----------------------------- 

Default: "noreply@domain.edu"

A string containing the email address that will appear in the "From" header 
for notification emails sent by ETD Drop.

HOMEPAGE_HEADING
----------------

A string containing the title you wish to be shown on the homepage.
By default, this is set to ``"Submit Your Thesis"``.

HOMEPAGE_TEXT
-------------

A string containing the text you wish to appear on the homepage underneath the 
page title.
Any line breaks you use in this string will be converted to line breaks in the 
HTML, and a blank line between two lines of text will convert to a paragraph 
break.

By default, this is set to::

    """
    ETD Drop allows our graduate students to easily submit a copy of their thesis or dissertation electronically.

    After logging in you will be asked to upload your document as a PDF. If you have any supplemental files you will also have the option to submit this content as a ZIP file.

    If required, please make sure you have a signed and scanned Copyright License in PDF form available to include with your submission.

    Lastly, the submission form will ask for your document's title and abstract. You can copy and paste these from your document into the corresponding form inputs.

    It's that easy.
    """

FOOTER_TEXT
-----------

A string containing the text you wish to appear in the footer.
Any line breaks you use in this string will be converted to line breaks in the 
HTML, and a blank line between two lines of text will convert to a paragraph 
break.

By default, this is set to::

    """
    Footer text
    """

LOGO_IMAGE_URL
--------------

A string containing a URL to a logo image you wish to appear in the footer.

SUBMISSION_AGREEMENT
--------------------

A string containing the text you wish to appear above the "agreement" checkbox 
at the bottom of the submission form. Typically this represents the terms that 
the user will be agreeing to when submitting their ETD.
Any line breaks you use in this string will be converted to line breaks in the 
HTML, and a blank line between two lines of text will convert to a paragraph 
break.

By default, this is set to::

    """
    By clicking the box below I agree that this submission is complete. Any errors in this submission will require a complete re-submission. Please be sure.
    """

SUBMISSION_FORM_FIELDS
----------------------

This setting allows you to hide or make mandatory the various submission form 
fields that make up a submission. For instance, if you want to completely hide 
the "Subject" field from the form, you would change the following lines::

    'subject': {
        'visible': True,
        'required': False,
    },

to this::

    'subject': {
        'visible': False,
        'required': False,
    },
