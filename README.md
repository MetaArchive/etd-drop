# ETD Drop

**This software is still being developed and is not ready for production use.**

## Overview

ETD Drop is a Django project+app providing a simple web application for
submitting Electronic Theses and Dissertations (ETDs).

## Documentation

You can find the ETD Drop documentation online on Read The Docs:

http://premis-event-service.readthedocs.org/en/latest/installation.html

The documentation is also browsable locally, within the `docs/source` 
directory of this repository. To build a local HTML version viewable offline, 
`cd` to the `docs` directory and run `make html`, and then open 
`docs/build/html/index.html`. (Be sure to have the dependencies listed in 
`requirements.txt` available before running `make html`.)

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
