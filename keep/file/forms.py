import logging
import os

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from keep.collection.forms import CollectionSuggestionField


logger = logging.getLogger(__name__)

class FormListField(forms.MultipleChoiceField):
    '''Simplified version of :class:`django.forms.MultipleChoiceField`
    that returns a list of values, but does not do any checking that
    items are a member of any list.
    '''
    # NOTE: currently has no output/widget handling, since it is only
    # used to read and validate values posted via javascript

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])


class UploadForm(forms.Form):
    '''Single-file OR batch file upload form; takes a required collection and
    an optional comment and EITHER a single file via post or a list of
    filenames and uploaded files already uploaded via AJAX.'''
    collection = CollectionSuggestionField(required=True)
    file = forms.FileField(label="File", required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'long'}),
        help_text='Optional comment or log message for auditing purposes.',
        required=False)
    # list fields used only for reading/validating values added to the
    # form via javascript upload
    uploaded_files = FormListField(required=False)
    filenames = FormListField(required=False)

    def clean(self):
        cleaned_data = super(UploadForm, self).clean()
        single_file = cleaned_data.get('file')
        uploaded_files = cleaned_data.get('uploaded_files')
        filenames = cleaned_data.get('filenames')

        # one of audio file or upload files is required
        if not single_file and not uploaded_files:
            raise ValidationError('No files were uploaded.')

        # list of uploaded files and filenames needs to match
        if len(uploaded_files) != len(filenames):
            raise ValidationError('Could not match uploaded files with original filenames')

        return cleaned_data

    def files_to_ingest(self):
        '''Construct a dictionary of the files to be ingested, based
        on posted data-- either single-file upload or ajax batch
        upload.  Returns a dictionary; key is the full filepath to the
        temporary upload file, value is the original filename.
        '''
        files = {}

        single_file = self.cleaned_data.get('file')
        uploaded_files = self.cleaned_data.get('uploaded_files')
        filenames = self.cleaned_data.get('filenames')

        # check for a single audio file uploaded via form post
        if single_file:
            files[single_file.temporary_file_path()] = single_file.name

        # check for any batch-uploaded files
        if uploaded_files:
            for i in range(len(uploaded_files)):
                # calculate full path to ajax upload file and add to list
                filepath = os.path.join(settings.INGEST_STAGING_TEMP_DIR,
                                        uploaded_files[i])
                files[filepath] = filenames[i]

        return files

