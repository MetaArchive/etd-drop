============
Installation
============

ETD Drop is distributed as a complete Django project, making it quite 
straightforward to run. It is essentially a WSGI application, needing only 
minor database-related setup and some Python package dependencies. Popular 
ways of running Django apps include gunicorn, nginx (with uwsgi), and Apache 
(with mod_wsgi).

System Requirements
===================

* Python 2.7.4 (or any higher 2.7.x release)
* virtualenv (strongly recommended)
* A writable directory large enough to accommodate your needs

Local Testing
=============

TODO (See README.md in the meantime)

Initial Setup
-------------

1. Clone this repository on your local filesystem, probably somewhere within 
   your user's home directory.
2. ``cd`` into this repository's directory.
3. Create a new virtual environment here: ``virtualenv.py venv``
4. Edit ``etd_drop/settings.py`` in a code or plain text editor and set up your 
   any settings you need to override (see the Configuration section below).

Each Time You Begin a New Work Session
--------------------------------------

1. ``cd`` into this repository's directory.
2. Activate your virtual environment: ``source venv/bin/activate``
3. (Optional) Pull latest changes from git: ``git pull``
4. Install/update dependencies: ``pip install -Ur requirements.txt``
5. Ensure that the database is set up: ``python manage.py syncdb``

**Note:** If this is your first time running the *syncdb* command, a new 
SQLite database will be generated, and you will be prompted to create a new
administrative account. Follow the prompts and provide a username and password 
for this new account. (You can leave the "email" field blank.)

Running a Local Server
----------------------

1. ``cd`` into this repository's directory.
2. Activate your virtual environment: ``source venv/bin/activate``
3. Start the development server: ``DJANGO_DEBUG=1 DJANGO_SECRET_KEY='test' python manage.py runserver``
4. When you wish to stop the server, use CTRL+C in the terminal window.

Production Server Deployment
============================

TODO
