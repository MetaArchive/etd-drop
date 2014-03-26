from django import forms, template

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
    def save(self, author):
        """
        Saves the submission, taking care of BagIt creation and any
        other necessary ingest behavior.
        author is the User who submitted the request.
        return value is the name of the bag directory created, or None.
        """
        return "worked"
        return None