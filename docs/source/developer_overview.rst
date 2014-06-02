==================
Developer Overview
==================

This section contains information that should come in handy if you are
developing for (or on top of) ETD Drop. You should already be familiar
with the information in :doc:`technical_overview`.

Overall, ETD Drop is an ordinary single-application Django project. The
primary difference between it and most Django apps is the total lack of
database models; All application data is represented as files on the
local filesystem, in order to make ETD Drop's scope as limited as
possible and to facilitate easy atomic integration into larger
workflows.

This project makes heavy use of Python docstrings. These are the best
places to look for details about a particular module, class, method, or
function.

.. contents::
    :local:
    :depth: 2

Project Source Code Layout
==========================

The general structure of this repository is as follows::

    etd-drop/                    # Top level git repository
        docs/                    ## Documentation (uses Sphinx Docs)
        etd_drop/                ## Django project files
            settings.py          ### Project settings
            urls.py              ### Project-level URL routing
            wsgi.py              ### Project WSGI application
        etd_drop_app             ## Main Django application code
            admin.py             ### Django Admin UI configuration
            forms.py             ### Form processing code
            static/              ### Static resources (CSS and images)
            templates/           ### HTML templates
            templatetags/        ### Custom template tag modules
                form_helpers.py  #### Template tags for forms
            tests.py             ### Unit tests
            urls.py              ### Application-level URL routing
            validators.py        ### Form validator functions
            vendor/              ### Modules included from elsewhere
                bag_describe.py  #### Description Service integration
            views.py             ### View generation code
        LICENSE                  ## Source code license
        manage.py                ## Project management script
        nginx/                   ## Sample configuration for nginx
        README.md                ## Project README
        requirements.txt         ## pip package dependencies
