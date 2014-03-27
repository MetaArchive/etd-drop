# ETD Drop (Django)

## Overview

ETD Drop is a Django project+app providing a simple web application for
submitting Electronic Theses and Dissertations (ETDs).

### Storage and Database Requirements

ETD Drop does not use any database operations for storing its data. ETD 
submissions are immediately processed into BagIt bags stored on disk, and
lookups take place simply by scanning the directory where they are stored.
The storage location is defined in `etd_drop/settings.py` (see Configuration
below).

A database is needed by the default Django authentication system, though you 
could substitute your own authentication system in its place and potentially
avoid needing any kind of database at all.

Database connection options are handled in `etd_drop/settings.py`. By default,
a SQLite database will be created and used.


## Project Directory Structure

    etd-drop-django/
    ├── etd_drop/         # Django project files
    │   ├── settings.py   ## Project settings
    ├── etd_drop_app      # Main Django application code
    │   ├── forms.py      ## Form processing code
    │   ├── static/       ## Static resources (CSS and images)
    │   ├── templates/    ## HTML templates
    │   ├── urls.py       ## URL routing patterns
    │   ├── views.py      ## View generation code
    ├── LICENSE           # Source code license
    ├── manage.py         # Project management script
    ├── README.md         # Project README
    └── requirements.txt  # pip package dependencies


## Installation and Local Testing

Note: You will want to have Python 2.7.4 and virtualenv installed before
continuing.

### Initial Setup

1. Clone this repository on your local filesystem, probably somewhere within 
   your user's home directory.
2. `cd` into this repository's directory.
3. Create a new virtual environment here: `virtualenv.py venv`
4. Edit `etd_drop/settings.py` in a code or plain text editor and set up your 
   any settings you need to override (see the Configuration section below).

### Each Time You Begin a New Work Session

1. `cd` into this repository's directory.
2. Activate your virtual environment: `source venv/bin/activate`
3. (Optional) Pull latest changes from git: `git pull`
4. Install/update dependencies: `pip install -Ur requirements.txt`
5. Ensure that the database is set up: `python manage.py syncdb`

**Note:** If this is your first time running the *syncdb* command, a new 
SQLite database will be generated, and you will be prompted to create a new
administrative account. Follow the prompts and provide a username and password 
for this new account. (You can leave the "email" field blank.)

### Running a Local Server

1. `cd` into this repository's directory.
2. Activate your virtual environment: `source venv/bin/activate`
3. Start the development server: `python manage.py runserver`
4. When you wish to stop the server, use CTRL+C in the terminal window.


## Developers

Here are some notes in case you're doing some development work on this project.

### Adding or Changing Module Dependencies

If you install any new Python modules using `pip install` or if you choose to
bump any of the versions of currently used modules, you will want to update the
requirements.txt file accordingly.  This is easily done with the following
command:

    $ pip freeze > requirements.txt

This will overwrite the current requirements.txt with a new one based on the
modules and versions currently installed in the virtualenv.
