"""
WSGI config for etd_drop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etd_drop.settings")


#Attempt to set environment variables from DOTENV, if we've been provided
#a path
DOTENV_path = os.environ.get('DOTENV', None)
if DOTENV_path is not None:
    import dotenv
    dotenv.read_dotenv(DOTENV_path) 

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
