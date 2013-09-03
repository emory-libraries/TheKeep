import logging
import os

from eulxml.forms import XmlObjectForm, SubformField
from eulxml.xmlmap import mods

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from keep.common.fedora import LocalMODS
from keep.common.forms import ReadonlyTextInput
from keep.collection.forms import CollectionSuggestionField
from keep.audio.forms import RightsForm


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

class AbstractForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to simplify editing
    a MODS :class:`~eulxml.xmlmap.mods.Abstract`.  Displays text content input only,
    as a :class:`~django.forms.Textarea` with no label; no other note attributes
    are displayed.
    """
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = mods.Abstract
        fields = ['text']


class ModsEditForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` for editing
    :class:`~keep.common.fedora.LocalMODS`.
    """
    # ARK value is set in form instance data by AudioObjectEditForm init
    # read-only text input to display ARK (not editable)
    identifier = forms.CharField(label="Identifier", required=False,
        widget=ReadonlyTextInput)
    resource_type = forms.CharField(required=False, widget=ReadonlyTextInput)
    abstract = SubformField(formclass=AbstractForm)
    # general_note = SubformField(formclass=SimpleNoteForm)
    # part_note = SubformField(formclass=SimpleNoteForm)

    # names = SubformField(formclass=NameForm)

    class Meta:
        model = LocalMODS
        fields = (
            'title', 'identifier', 'resource_type', 'abstract',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'long'}),
            'identifier': ReadonlyTextInput,
        }


class DiskImageEditForm(forms.Form):
    """:class:`~django.forms.Form` for metadata on an
    :class:`~keep.file.models.DiskImage`.

    Takes an :class:`~keep.file.models.DiskImage` as form instance,
    in contrast to a regular :class:`~eulxml.forms.XmlObjectForm`, which would
    take an :class:`~eulxml.xmlmap.XmlObject`. This form edits a whole
    :class:`~keep.file.models.DiskImage` by editing multiple XML
    datastreams (whose contents are instances of :class:`~eulxml.xmlmap.XmlObject`),
    with individual :class:`~eulxml.forms.XmlObjectForm` form instances
    for each XML datastream.
    """

    collection = CollectionSuggestionField(required=True)

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):
        if instance is None:
            mods_instance = None
            # rights_instance = None
        else:
            mods_instance = instance.mods.content
            rights_instance = instance.rights.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            # populate fields not auto-generated & handled by XmlObjectForm
            if self.object_instance.collection:
                initial['collection'] = str(self.object_instance.collection.uri)

            if self.object_instance.ark:
                initial['identifier'] = self.object_instance.ark
            else:
                initial['identifier'] = self.object_instance.pid + ' (PID)'

            # passed-in initial values override ones calculated here
            initial.update(orig_initial)

        common_opts = {'data': data, 'initial': initial}
        self.mods = ModsEditForm(instance=mods_instance, prefix='mods', **common_opts)
        self.rights = RightsForm(instance=rights_instance, prefix='rights', **common_opts)
 #       self.comments = CommentForm( prefix='comments',**common_opts)

        for form in ( self.mods, ):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(DiskImageEditForm, self).__init__(data=data, initial=initial)

    def is_valid(self):
        return all(form.is_valid() for form in \
                    [ super(DiskImageEditForm, self),
                      self.mods,
                      self.rights,
                    ])

    def update_instance(self):
        # override default update to handle extra fields
        #super(AudioObjectEditForm, self).update_instance()
        self.object_instance.mods.content = self.mods.update_instance()
        self.object_instance.rights.content = self.rights.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection = self.object_instance.get_object(self.cleaned_data['collection'])

        return self.object_instance


