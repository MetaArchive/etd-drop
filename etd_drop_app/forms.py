import os
import sys
import zipfile
import json
import shutil
from datetime import datetime

from django import forms, template
from django.conf import settings
from django.forms.extras import SelectDateWidget

import bagit

from .validators import *


class NewSubmissionForm(forms.Form):
    """
    Form for submitting an ETD.
    """
    document_file = forms.FileField(
        label="Main PDF File",
        required=True,
        allow_empty_file=False,
        validators=[MimetypeValidator('application/pdf')],
        help_text="Upload a PDF version of your thesis or dissertation. "
        "Please take care to ensure that any custom fonts are properly "
        "embedded and that your PDF displays correctly on different devices "
        "before submitting."
    )
    supplemental_file = forms.FileField(
        label="Supplemental Data",
        required=settings.SUBMISSION_FORM_FIELDS['supplemental_file']['required'],
        allow_empty_file=False,
        validators=[MimetypeValidator('application/zip')],
        help_text="Upload a ZIP file containing any supplemental "
        "files you wish to deposit along with your thesis or dissertation."
    )
    license_file = forms.FileField(
        label="License Agreement",
        required=settings.SUBMISSION_FORM_FIELDS['license_file']['required'],
        allow_empty_file=False,
        validators=[MimetypeValidator('application/pdf')],
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
        widget=SelectDateWidget,
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
            form_record_path = os.path.join(staging_path, "form.json")
            form_record_file = open(form_record_path, 'w')
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
            json.dump(form_record, form_record_file,
                skipkeys=True,
                indent=2
            )
            form_record_file.close()
            # TODO: Maybe write an XML version also

            # Turn the staging directory into a bag
            bag_info = {}
            if self.cleaned_data['title']:
                bag_info['Internal-Sender-Identifier'] = self.cleaned_data['title'].replace('\n', ' ').replace('\r', '')
            bagit.make_bag(staging_path, bag_info)

            # Remove "STAGING_" from the name of the directory to signify completion
            final_path = os.path.abspath(os.path.join(settings.ETD_STORAGE_DIRECTORY, etd_id))
            os.rename(staging_path, final_path)
            
            # Fire any emails/notifications/webhooks the institution wants to receive
            # TODO

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
