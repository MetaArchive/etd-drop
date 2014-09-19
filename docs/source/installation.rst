============
Installation
============

ETD Drop is distributed as a complete Django project, making it quite 
straightforward to run. It is essentially a WSGI application, needing only 
minor database-related setup and some Python package dependencies. Popular 
ways of running Django apps include gunicorn, nginx (with uwsgi), and Apache 
(with mod_wsgi).

.. contents::
    :local:
    :depth: 2

System Requirements
===================

* Python 2.7.4 (or any higher 2.7.x release)
* virtualenv (strongly recommended)
* A writable directory large enough to accommodate your needs

Local Testing
=============

These instructions should help you to set up an instance of ETD Drop running 
locally on a personal machine or VM. This is useful for small scale testing or 
development, but not for serving the application to actual users.

Initial Setup
-------------

1. Clone this repository on your local filesystem, probably somewhere within 
   your user's home directory.
2. ``cd`` into this repository's directory.
3. Create a new virtual environment here: ``virtualenv.py venv``
4. Copy ``etd_drop/settings.py.example`` to ``etd_drop/settings.py``.
4. Edit ``etd_drop/settings.py`` in a code or plain text editor and set up your 
   any settings you need to override (see the Configuration section below).
5. Copy ``etd_drop/env_example`` to ``etd_drop/.env``.
6. Edit ``etd_drop/.env`` with a text editor and configure the settings
   to your desired setup.

Each Time You Begin a New Work Session
--------------------------------------

1. ``cd`` into this repository's directory.
2. Activate your virtual environment: ``source venv/bin/activate``
3. (Optional) Pull latest changes from git: ``git pull``
4. Install/update dependencies: ``pip install -Ur requirements.txt``
5. Ensure that the database is set up: ``DJANGO_DEBUG=1 python manage.py syncdb``

**Note:** If this is your first time running the *syncdb* command, a new 
SQLite database will be generated, and you will be prompted to create a new
administrative account. Follow the prompts and provide a username and password 
for this new account. (You can leave the "email" field blank.)

Running a Local Server
----------------------

1. ``cd`` into this repository's directory.
2. Activate your virtual environment: ``source venv/bin/activate``
3. Start the development server: ``DJANGO_DEBUG=1 python manage.py runserver``
4. When you wish to stop the server, use CTRL+C in the terminal window.

Production Server Deployment
============================

There are many approaches and choices to consider when deploying a Django 
project on a real server. The general strategy is something like the 
following:

1. Incoming requests are proxied by Nginx (which also directly serves static 
   assets belonging to the project)
2. Nginx forwards requests on to a WSGI server (like uWSGI or Gunicorn)
3. The WSGI server handles the request and displays the page

If you would prefer to use Apache, you should use mod_wsgi and refer to 
`this page <https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/>`_
for guidance in setting things up.

Otherwise, we recommend using Nginx with Gunicorn. The following steps outline 
the general process of setting up ETD Drop in this way on a Linux server.

Getting Started
---------------

This guide will assume the use of an up-to-date installation of Ubuntu Server 
12.04, though the general principles should apply to any other reasonably-
equipped Linux environment.

First, let's make sure everything we need is installed::

    sudo apt-get install -y nginx git python-virtualenv

Setting up ETD Drop in a Virtualenv
-----------------------------------

We need a place where the ETD Drop code can live. Technically the location 
doesn't matter that much, but a popular convention is ``/srv/django``. Let's 
create this location::

    sudo mkdir -p /srv/django

Now we'll fetch the ETD Drop code repository::

    cd /srv/django
    sudo git clone https://github.com/metaarchive/etd-drop

ETD Drop is now fetched at ``/srv/django/etd-drop``.
Now, let's set up a virtualenv to contain our Python packages nicely::

    sudo virtualenv /srv/venv/etd-drop

The following command "activates" the new virtualenv in your current shell so 
that we are in the correct environment for the next several steps::

    sudo -i
    source /srv/venv/etd-drop/bin/activate

Now go to the ETD Drop source code directory and fetch its dependencies::

    cd /srv/django/etd-drop
    pip install -r requirements.txt

Configure Nginx
---------------

To make things simple, we've provided a sample Nginx configuration file along 
with the ETD Drop source code. Install it as follows::

    cp /srv/django/etd-drop/nginx/etd-drop.conf /etc/nginx/sites-available
    ln -s ../sites-available/etd-drop.conf /etc/nginx/sites-enabled/
    rm /etc/nginx/sites-enabled/default # Disables the default nginx config

Configuring Settings
--------------------

Before going any further, you will need to edit 
``/srv/django/etd-drop/etd_drop/settings.py`` and configure your project's 
settings (especially the DATABASES setting if you wish to use something other 
than SQLite3 to store user accounts). Refer to :doc:`configuration` for details.

Initializing ETD Drop
---------------------

Do the following in order to initialize ETD Drop::

    source /srv/venv/etd-drop/bin/activate
    cd /srv/django/etd-drop/
    python manage.py collectstatic -c --noinput
    python manage.py syncdb
    python manage.py syncdb --noinput

At this point, you should create an initial "superuser" account (an 
administrative account which will be able to log in and manage other user 
accounts in ETD Drop). Run the following command and follow the prompts::

    python manage.py createsuperuser

Choose these credentials wisely as this account will have full administrative 
privileges inside the application.

Running the Server
------------------

Finally, the commands you will use to start up the servers::

    sudo service nginx restart
    cd /srv/django/etd-drop
    sudo DOTENV=/srv/django/etd-drop/.env /srv/venv/etd-drop/bin/gunicorn -b unix:/tmp/gunicorn.sock etd_drop.wsgi:application
