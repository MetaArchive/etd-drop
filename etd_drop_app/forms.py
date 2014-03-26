import os
import zipfile

from django import forms, template
from django.conf import settings
import bagit


class NewSubmissionForm(forms.Form):
    """
    Form for submitting an ETD.
    """
    document_file = forms.FileField(
        label="Main PDF File",
        required=True,
        allow_empty_file=False,
        help_text="Upload a PDF version of your ETD. Please take care to "
        "ensure that any custom fonts are properly embedded and that your "
        "PDF displays correctly on different devices before submitting."
    )
    supplemental_file = forms.FileField(
        label="Supplemental Data",
        required=False,
        allow_empty_file=False,
        help_text="(Optional) Upload a ZIP file containing any supplemental "
        "data you wish to deposit along with your ETD."
    )
    license_file = forms.FileField(
        label="License Agreement",
        required=False,
        allow_empty_file=False,
        help_text="(Optional) Upload a signed copy of a copyright license "
        "agreement, as per the policy of your institution."
    )
    title = forms.CharField(
        label="Title",
        required=True,
        help_text="Thesis or dissertation title"
    )
    description = forms.CharField(
        label="Short Description",
        required=True,
        help_text="A one or two sentence abstract on the thesis or "
        "dissertation"
    )
    agreement = forms.BooleanField(
        label="Agreement",
        required=True,
        help_text="I accept the terms of the above agreement."
    )
    # TODO: Custom validation that PDF is really a PDF, etc...
    def save(self, author):
        """
        Saves the submission, taking care of BagIt creation and any
        other necessary ingest behavior.

        author is the User who submitted the request.
        return value is the name of the bag directory created, or None.
        """
        # Generate a name for the directory. Must be unique.
        datestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        etd_id = "%s-%s" % (datestamp, author.username)

        # Set up staging directory for this bag (e.g. "STAGING_20140326-160532_lbroglie")
        staging_name = "STAGING_%s" % etd_id
        staging_path = os.path.abspath(os.path.join(settings.ETD_STORAGE_DIRECTORY, staging_name))

        try:
            # Create the staging directory
            os.makedirs(staging_path)

            # Create a file representing information submitted in the form
            # TODO

            # Move the main document to the staging area
            document_path = os.path.join(staging_path, "document.pdf")
            with open(document_path, 'wb+') as destination:
                for chunk in self.cleaned_data['document_file']:
                    destination.write(chunk)

            # Move the license document to the staging area, if provided

            # Try to process the supplemental file as a ZipFile, if provided
            # zip = zipfile.ZipFile(self.cleaned_data['supplemental_file'], 'r')

            # Turn the staging directory into a bag
            bag_info = {
                'Internal-Sender-Identifier': self.cleaned_data['title'],
                'Internal-Sender-Description': self.cleaned_data['description']
            }
            bagit.make_bag(staging_path, bag_info)

            # Remove "STAGING_" from the name of the directory to signify completion
            final_path = os.path.abspath(os.path.join(settings.ETD_STORAGE_DIRECTORY, etd_id))
            os.rename(staging_path, final_path)

            # Return the id to signify success to the caller
            return etd_id
        except:
            # Log this event
            # TODO

            # Clean up the staging directory if it exists
            # TODO

            return None