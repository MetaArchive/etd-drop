import os
import sys
import zipfile
import json
import shutil
import logging
from datetime import datetime
from xml.dom.minidom import parseString

from django import forms, template
from django.conf import settings
from django.forms.extras import SelectDateWidget
from django.template.loader import render_to_string

import bagit
from dicttoxml import dicttoxml

from .validators import *
from vendor.bag_describe import bag_describe

logger = logging.getLogger('ETD-DROP')

CLAMD = False
if settings.ENABLE_CLAMD:
    try:
        import pyclamd
        CLAMD = True
        logger.debug("pyclamd is enabled")
    except ImportError, ie:
        logger.debug("Logging is enabled, but unable import pyclamd: %s" % ie) 
        pass

class ScanException(Exception):
    pass

class NewSubmissionForm(forms.Form):
    """
    Form for submitting an ETD.
    """
    document_file = forms.FileField(
        label="Main PDF File",
        required=True,
        allow_empty_file=False,
        validators=[MimetypeValidator(('application/pdf'))],
        help_text="Upload a PDF version of your thesis or dissertation. "
        "Please take care to ensure that any custom fonts are properly "
        "embedded and that your PDF displays correctly on different devices "
        "before submitting."
    )
    supplemental_file = forms.FileField(
        label="Supplemental Data",
        required=settings.SUBMISSION_FORM_FIELDS['supplemental_file']['required'],
        allow_empty_file=False,
        validators=[MimetypeValidator(('application/zip'))],
        help_text="Upload a ZIP file containing any supplemental "
        "files you wish to deposit along with your thesis or dissertation."
    )
    license_file = forms.FileField(
        label="License Agreement",
        required=settings.SUBMISSION_FORM_FIELDS['license_file']['required'],
        allow_empty_file=False,
        validators=[MimetypeValidator(('application/pdf'))],
        help_text="Upload a signed copy of a copyright license "
        "agreement, as per the policy of your institution."
    )
    title = forms.CharField(
        label="Title",
        required=settings.SUBMISSION_FORM_FIELDS['title']['required'],
        help_text="Title of your thesis or dissertation"
    )
    author = forms.CharField(
        label="Author",
        required=settings.SUBMISSION_FORM_FIELDS['author']['required'],
        help_text="Name of the author of this work as it appears on your title page"
    )
    subject = forms.CharField(
        label="Subject(s)",
        required=settings.SUBMISSION_FORM_FIELDS['subject']['required'],
        help_text="Any topics or subjects as they appear on your title page, separated with commas"
    )
    date = forms.DateField(
        label="Date",
        required=settings.SUBMISSION_FORM_FIELDS['date']['required'],
        widget=SelectDateWidget(years=range(2010, 2030)),
        help_text="Date of publication as it appears on your title page"
    )
    abstract = forms.CharField(
        label="Abstract",
        required=settings.SUBMISSION_FORM_FIELDS['abstract']['required'],
        widget=forms.Textarea,
        help_text="Abstract of your thesis or dissertation"
    )
    agreement = forms.BooleanField(
        label="I agree to the terms.",
        required=True
    )
    # TODO: Custom validation that PDF is really a PDF, etc...

    def is_valid(self):
        valid = super(forms.Form, self).is_valid()

        return valid

    def save(self, author):
        """
        Saves the submission, taking care of BagIt creation and any
        other necessary ingest behavior.

        author is the User who submitted the request.
        return value is the name of the bag directory created, or None.
        """
        # Generate a submission ID. Must be unique.
        datestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        etd_id = "%s-%s" % (datestamp, author.username)

        # Set up staging directory for this bag (e.g. "STAGING_20140326-160532_lbroglie")
        staging_name = "STAGING_%s" % etd_id
        staging_path = os.path.abspath(os.path.join(settings.ETD_STORAGE_DIRECTORY, staging_name))

        try:
            # Create the staging directory
            os.makedirs(staging_path)

            # Move the main document to the staging area
            document_path = os.path.join(staging_path, "etd.pdf")
            with open(document_path, 'wb+') as destination:
                for chunk in self.cleaned_data['document_file']:
                    destination.write(chunk)

            # Perform a virus scan on the staged file
            if CLAMD:
                clam_daemon = pyclamd.ClamdAgnostic()
                result = clam_daemon.scan_file(document_path)
                if result is not None:
                    logger.debug("Virus detected in file %s" % document_path)
                    raise ScanException("Error: Virus detected in uploaded ETD file")

            # Move the license document to the staging area, if provided
            if self.cleaned_data['license_file']:
                document_path = os.path.join(staging_path, "license.pdf")
                with open(document_path, 'wb+') as destination:
                    for chunk in self.cleaned_data['license_file']:
                        destination.write(chunk)

            # Try to process the supplemental file as a ZipFile, if provided
            if self.cleaned_data['supplemental_file']:
                supplemental_path = os.path.join(staging_path, "supplemental")
                supplemental_zip = zipfile.ZipFile(self.cleaned_data['supplemental_file'], 'r')
                supplemental_zip.extractall(supplemental_path)
                supplemental_zip.close()

            # Create a dict representing all the form data
            form_record = {
                'document_file': {
                    'original_filename': self.cleaned_data['document_file'].name,
                    'size': self.cleaned_data['document_file'].size,
                    'content_type': self.cleaned_data['document_file'].content_type
                },
            }
            for name in ('title', 'author', 'subject', 'date', 'abstract'):
				if self.cleaned_data[name]:
					form_record[name] = str(self.cleaned_data[name])
            if self.cleaned_data['supplemental_file']:
                form_record['supplemental_file'] = {
                    'original_filename': self.cleaned_data['supplemental_file'].name,
                    'size': self.cleaned_data['supplemental_file'].size,
                    'content_type': self.cleaned_data['supplemental_file'].content_type
                }
            if self.cleaned_data['license_file']:
                form_record['license_file'] = {
                    'original_filename': self.cleaned_data['license_file'].name,
                    'size': self.cleaned_data['license_file'].size,
                    'content_type': self.cleaned_data['license_file'].content_type 
                }
            form_record_json_path = os.path.join(staging_path, "form.json")
            with open(form_record_json_path, 'w') as form_record_file:
                json.dump(form_record, form_record_file,
                    skipkeys=True,
                    indent=2
                )
            form_record_xml_path = os.path.join(staging_path, "form.xml")
            with open(form_record_xml_path, 'w') as form_record_file:
                xml_string = parseString(dicttoxml(form_record)).toprettyxml()
                form_record_file.write(xml_string)

            # Turn the staging directory into a bag
            bag_info = {}
            if self.cleaned_data['title']:
                bag_info['Internal-Sender-Identifier'] = self.cleaned_data['title'].replace('\n', ' ').replace('\r', '')
            bagit.make_bag(staging_path, bag_info)

            # Remove "STAGING_" from the name of the directory to signify completion
            final_path = os.path.abspath(os.path.join(settings.ETD_STORAGE_DIRECTORY, etd_id))
            os.rename(staging_path, final_path)

            # Perform optional DAITSS Format Description Service metadata generation
            try:
                description_url = getattr(settings, 'DESCRIPTION_SERVICE_URL', None)
                if description_url:
					bag_describe(description_url, final_path)

            except Exception as e:
                # Log this failure of the description service
                # TODO
                if settings.DEBUG:
                    raise e
            
            # Fire any emails/notifications/webhooks the institution wants to receive
            try:
                recipients = getattr(settings, 'SUBMISSION_EMAIL_RECIPIENTS', None)
                if recipients:
                    subject = "[ETD Drop] New ETD submission"
                    body = render_to_string(
                        'etd_drop_app/email_staff_submission.txt', 
                        {
                            'submission_time': datestamp,
                            'username': author.username,
                            'identifier': etd_id,
                        }
                    )
                    sender = settings.SUBMISSION_EMAIL_FROM_ADDRESS
                    send_mail(subject, body, sender, recipients)
            except Exception as e:
                # Log this email failure
                # TODO
                if settings.DEBUG:
                    raise e

            # Return the id to signify success to the caller
            return etd_id
        except Exception as e:
            # Log this event
            # TODO

            # Clean up the staging directory if it exists
            if os.path.isdir(staging_path):
                shutil.rmtree(staging_path)

            if settings.DEBUG:
                raise e

            return None
