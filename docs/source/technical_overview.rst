==================
Technical Overview
==================

ETD Drop is a simple web application for accepting online submissions of
electronic theses and dissertations (ETDs), written in Django.
Submissions are saved to a configurable location on disk in an easy to 
navigate structure, making them easy for your staff (or custom software) to 
review and move into the next stage of your ETD workflow.

A database is only required in order to facilitate user authentication, 
though with a bit of Django expertise it is possible to replace the default 
authentication system with a different one (e.g. using LDAP) potentially
eliminating the need for a database altogether.

Data Storage Format
-------------------

When an ETD submission is received from a user, the following steps 
take place:

1. The form data is validated according to which fields are marked with
   ``'required': True`` in your settings.py file.
2. A submission identifier is generated according to the following naming 
   scheme: YYYYMMDD-HHMMSS-username (e.g. `20140401-182104-stephen` would be a 
   submission made on April 1, 2014, at 18:21:04, by a user logged in as 
   "stephen")
3. A directory in the ETD_STORAGE_DIRECTORY location is created with the 
   following structure:

* (identifier)/

  * data/

    * etd.pdf (the main thesis/dissertation PDF file)
    * license.pdf (the license agreement PDF file, if provided)
    * form.json (JSON-encoded representation of what was submitted via the form)
    * supplemental/ (contents of the supplemental data ZIP file, if provided)

  * bagit.txt
  * bag-info.txt
  * manifest-md5.txt

You might recognize this structure as a BagIt bag. The submission package is 
stored in this format to allow for easier management and the ability to verify 
file checksums at a later point in time.
