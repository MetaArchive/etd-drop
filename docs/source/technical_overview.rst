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

.. contents::
    :local:
    :depth: 2

Data Storage Format
===================

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
    * form.xml (XML-encoded representation of what was submitted via the form)
    * supplemental/ (contents of the supplemental data ZIP file, if provided)

  * bagit.txt
  * bag-info.txt
  * manifest-md5.txt

You might recognize this structure as a BagIt bag. The submission package is 
stored in this format to allow for easier management and the ability to verify 
file checksums at a later point in time.

Form Data Representation
------------------------

Along with the uploaded files, ETD Drop includes JSON and XML documents 
containing the values given by the user via the submission form (along with 
some basic metadata relating to the files that were uploaded). The documents 
are stored as ``form.json`` and ``form.xml``, and are found within the 
``data`` directory of a submission package. This document is small and should 
be easy to parse (even for a human). The presence of individual keys will 
depend on which form fields were enabled in ``settings.py`` and what was 
actually provided by the user. Here is a sample of the contents of a typical 
``form.json``::

    {
      "document_file": {
        "content_type": "application/pdf", 
        "original_filename": "thesis.pdf", 
        "size": 2149036
      }, 
      "license_file": {
        "content_type": "application/pdf", 
        "original_filename": "license.pdf", 
        "size": 81439
      }, 
      "abstract": "Sample abstract.", 
      "supplemental_file": {
        "content_type": "application/zip", 
        "original_filename": "supplemental_data.zip", 
        "size": 5181242
      }, 
      "title": "Sample Title",
      "author": "Sample Author"
    }

And here is an equivalent example of a ``form.xml`` file::

    <?xml version="1.0" ?>
    <root>
      <author type="str">Sample Author</author>
      <abstract type="str">Sample abstract.</abstract>
      <title type="str">Sample Title</title>
      <document_file type="dict">
        <content_type type="str">application/pdf</content_type>
        <original_filename type="str">thesis.pdf</original_filename>
        <size type="int">2149036</size>
      </document_file>
      <license_file type="dict">
        <content_type type="str">application/pdf</content_type>
        <original_filename type="str">license.pdf</original_filename>
        <size type="int">81439</size>
      </license_file>
      <supplemental_file type="dict">
        <content_type type="str">application/zip</content_type>
        <original_filename type="str">supplemental_data.zip</original_filename>
        <size type="int">5181242</size>
      </supplemental_file>
    </root>

Understanding the Project Code
==============================

For more in-depth information suited for developers, continue to the
:doc:`developer_overview`.
