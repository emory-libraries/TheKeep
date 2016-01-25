import logging
from keep.common.models import PremisSoftwareEnvironment, PremisHardwareEnvironment, PremisEnvironment, PremisObject
import os

from eulxml.forms import XmlObjectForm, SubformField
from eulxml.xmlmap import mods
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from keep.common.forms import ReadonlyTextInput, comment_field, EMPTY_LABEL_TEXT
from keep.collection.forms import CollectionSuggestionField
from keep.audio.forms import RightsForm
from keep.file.models import DiskImageMods, DiskImagePremis, Application, large_file_uploads


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
    comment = comment_field()

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


def largefile_staging_bags():
    # form option list of available bagit files uploaded to large-file staging area
    options = [('', EMPTY_LABEL_TEXT)]
    options.extend([(lf, os.path.basename(lf)) for lf in large_file_uploads()])
    return options

class LargeFileIngestForm(forms.Form):
    '''Ingest content from a BagIt uploaded to a large-file staging space.
    Takes a required collection, an optional comment and, and a selection
    from the list of available bags.'''
    collection = CollectionSuggestionField(required=True)
    bag = DynamicChoiceField(label='File to ingest', choices=largefile_staging_bags)
    # TODO: possibly support multiple bags?
    comment = comment_field()


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
    abstract = SubformField(formclass=AbstractForm)
    coveringdate_start = W3CDateField(
        label='Covering Dates',
        help_text='start and end dates for disk content in YYYY, YYYY-MM, or YYYY-MM-DD',
        required=False)
    coveringdate_end = W3CDateField(label='', required=False)

    class Meta:
        model = DiskImageMods
        fields = (
            'title', 'identifier', 'resource_type', 'genre',
            'coveringdate_start', 'coveringdate_end', 'abstract'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'long'}),
            'identifier': ReadonlyTextInput,
            'resource_type': ReadonlyTextInput,
            'genre': ReadonlyTextInput,
        }

## technical metadata (premis)

class SoftwareEnvironmentForm(XmlObjectForm):
    class Meta:
        model = PremisSoftwareEnvironment
        fields = ('name', 'version', 'type')

class HardwareEnvironmentForm(XmlObjectForm):
    other_information = forms.CharField(required=False,
        widget=forms.Textarea)

    class Meta:
        model = PremisHardwareEnvironment
        fields = ('name', 'type', 'other_information')

class EnvironmentForm(XmlObjectForm):
    software = SubformField(formclass=SoftwareEnvironmentForm)
    hardware = SubformField(formclass=HardwareEnvironmentForm)

    class Meta:
        model = PremisEnvironment
        fields = ('software', 'hardware')

class PremisObject(XmlObjectForm):
    original_environment = SubformField(formclass=EnvironmentForm)
    class Meta:
        model = PremisObject
        fields = ('original_environment', )


def creating_applications():
    options = [(app.id, unicode(app)) for app in Application.objects.all()]
    options.insert(0, ('', EMPTY_LABEL_TEXT))
    return options


class PremisEditForm(XmlObjectForm):
    # NOTE: extending xmlobjet form to make use of existing schema validation
    # logic & integration to form validation.
    # However, this form does not use any xmlobject form fields.

    application = DynamicChoiceField(
        label='Creating Application', choices=creating_applications)
    date = forms.DateField(label='Imaging Date', input_formats=['%Y-%m-%d', '%Y/%m/%d'],
                           help_text='Date created in YYYY-MM-DD or YYYY/MM/DD format')
    object = SubformField(PremisObject)

    class Meta:
        model = DiskImagePremis
        fields = ('object', )

    def __init__(self, data=None, instance=None, prefix=None, initial={}, **kwargs):
        if instance is not None:
            # set initial form data based on the xml
            # NOTE: migrated objects have two sets of characteristics,
            # and the creating application to be displayed is the second one.
            # Always display and update the last of any creating applications
            if instance.object and instance.object.characteristics and \
              instance.object.characteristics[-1].creating_application:
                creating_app = instance.object.characteristics[-1].creating_application
                initial['date'] = creating_app.date
                try:
                    app = Application.objects.get(name=creating_app.name,
                      version=creating_app.version)
                    initial['application'] = app.id
                except ObjectDoesNotExist:
                    pass

        super(PremisEditForm, self).__init__(data=data, instance=instance,
                                             prefix=prefix, initial=initial,
                                             **kwargs)

    def update_instance(self):
        super(PremisEditForm, self).update_instance()

        data = self.cleaned_data
        # update premis fields based on form data
        self.instance.object.create_creating_application()
        app = Application.objects.get(id=data['application'])
        # Update the last of any creating applications in the metadata
        self.instance.object.characteristics[-1].creating_application.name = app.name
        self.instance.object.characteristics[-1].creating_application.version = app.version
        self.instance.object.characteristics[-1].creating_application.date = data['date']
        return self.instance


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
    comment = comment_field()

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):
        if instance is None:
            mods_instance = None
            # rights_instance = None
        else:
            mods_instance = instance.mods.content
            rights_instance = instance.rights.content
            premis_instance = instance.provenance.content
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
        self.premis = PremisEditForm(instance=premis_instance, prefix='premis', **common_opts)

        for form in (self.mods, self.rights, self.premis):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(DiskImageEditForm, self).__init__(data=data, initial=initial)

    def is_valid(self):
        return all(form.is_valid() for form in \
                    [ super(DiskImageEditForm, self),
                      self.mods,
                      self.rights,
                      self.premis,
                    ])

    def update_instance(self):
        # override default update to handle extra fields
        self.object_instance.mods.content = self.mods.update_instance()
        self.object_instance.rights.content = self.rights.update_instance()
        self.object_instance.provenance.content = self.premis.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection = self.object_instance.get_object(self.cleaned_data['collection'])

        return self.object_instance


class SupplementalFileForm(forms.Form):
    dsid = forms.CharField(required=False,
        widget=forms.HiddenInput)
    label = forms.CharField(required=False,
        help_text='filename for display; will be set from uploaded file if not specified',
        widget=forms.TextInput(attrs={'class': 'long'}),)
    file = forms.FileField(label="File", required=True,
        help_text='Supplemental files to be kept with this object',
        widget=forms.widgets.ClearableFileInput)
    # file (either existing datastream or new upload) should always be present

    def clean(self):
        cleaned_data = super(SupplementalFileForm, self).clean()
        label = cleaned_data.get('label', '')
        file = cleaned_data.get('file')

        # if file is present and label is not, fill in label from file title
        if file and not label:
            cleaned_data['label'] = file.name

        # Always return the full collection of cleaned data.
        return cleaned_data

SupplementalFileFormSet = formset_factory(SupplementalFileForm, extra=3)
