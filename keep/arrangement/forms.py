from django import forms
from django.utils.safestring import mark_safe

from eulxml.xmlmap import mods
from datetime import datetime

from eulxml.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField
from eulcommon.djangoextras.validators import FileTypeValidator

from eulcm.xmlmap.boda import Rights, ArrangementMods, \
     Series1, Series2, FileMasterTech, FileMasterTech_Base

from keep.common.models import rights_access_terms_dict
from keep.common.forms import ReadonlyTextInput, CommentForm, rights_access_options


##
# Arrangement
##


class FileTechPartForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """

    # TODO: none of these fields are actually editable.  
    # If that continues to be the case, we should remove
    # this form and simply display the file-tech metadata
    # on the appropriate page.

    #created = W3CDateField(required=False)
    #modified = W3CDateField(required=False)

    created = forms.CharField(label="Created", required=False,
        widget=ReadonlyTextInput)

    modified = forms.CharField(label="Modified", required=False,
        widget=ReadonlyTextInput)


    md5 = forms.CharField(label="MD5 Sum", required=False,
        widget=ReadonlyTextInput)

    local_id = forms.CharField(label="Generated Local ID", required=False,
        widget=ReadonlyTextInput)

    computer = forms.CharField(label="Computer", required=False,
        widget=ReadonlyTextInput)

    path = forms.CharField(label="Original Path", required=False,
        widget=ReadonlyTextInput)

    rawpath = forms.CharField(label="Raw Path (Base64)", required=False,
        widget=ReadonlyTextInput)

    attributes = forms.CharField(label="Attributes", required=False,
        widget=ReadonlyTextInput)

    type = forms.CharField(label="Type", required=False,
        widget=ReadonlyTextInput)

    creator = forms.CharField(label="Creator", required=False,
        widget=ReadonlyTextInput)

    class Meta:
        model = FileMasterTech_Base
        fields = [ 'local_id', 'md5', 'computer', 'path',
                   'rawpath', 'attributes', 'created',
                   'modified', 'type', 'creator' ]
        #widgets = {
            #'local_id': ReadonlyTextInput,
            #'md5': ReadonlyTextInput,
            #'computer': ReadonlyTextInput,
            #'path': ReadonlyTextInput,
            #'rawpath': ReadonlyTextInput,
            #'attributes': ReadonlyTextInput,
            #'type': ReadonlyTextInput,
            #'creator': ReadonlyTextInput,
        #}

    def __init__(self, **kwargs):
        super(FileTechPartForm, self).__init__(**kwargs)

class FileTechEditForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """
    file = SubformField(formclass=FileTechPartForm, can_delete=False)

    class Meta:
        model = FileMasterTech
        fields = [ 'file']

class RightsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """

    access = forms.ChoiceField(rights_access_options, label='Access Status',
           help_text='File access status, as determined by analysis of copyright, donor agreements, permissions, etc.')
    copyright_date = W3CDateField(required=False)
    access_restriction_expiration = W3CDateField(required=False)

    class Meta:
        model = Rights
        fields = [ 'access', 'copyright_date', 'access_restriction_expiration',
                   'block_external_access', 'ip_note' ]
        widgets = {
            'ip_note': forms.Textarea,
            'block_external_access': forms.CheckboxInput(attrs={'class': 'checkbox-warning'}),
        }

    def __init__(self, **kwargs):
        super(RightsForm, self).__init__(**kwargs)

        # XmlObjectForm magically populates fields based directly on
        # XmlObject field names, but we have a couple form fields that
        # aren't.
        access = 'access'
        access_status_code = 'access_status-code'
        if access_status_code in self.initial:
            self.initial[access] = self.initial[access_status_code]

    def update_instance(self):
        super(RightsForm, self).update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            access_code = self.cleaned_data['access']
            access_text = rights_access_terms_dict[access_code].text
            self.instance.create_access_status()
            self.instance.access_status.code = access_code
            self.instance.access_status.text = access_text

        return self.instance


class Series2PartForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit series
    information in MODS
    '''
    title = forms.CharField(label='Series Title', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series2_storedtitle'}))

    uri = forms.CharField(label='URI', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series2_storeduri'}))
    md5 = forms.CharField(label="MD5 Sum", required=False,
        widget=ReadonlyTextInput)

    base_ark = forms.CharField(label='Base Ark', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series2_storedark'}))

    full_id = forms.CharField(label='Full ID', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series2_storedfullid'}))

    short_id = forms.CharField(label='Short ID', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series2_storedshortid'}))

    class Meta:
        fields = ['title', 'uri', 'base_ark', 'full_id', 'short_id']
        model = Series2

class SeriesPartForm(XmlObjectForm):
    '''
    Custom :class:`~eulxml.forms.XmlObjectForm` to edit Series
    information.
    '''
    title = forms.CharField(label='Series Title', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series1_storedtitle'}))


    uri = forms.CharField(label='URI', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series1_storeduri'}))

    base_ark = forms.CharField(label='Base Ark', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series1_storedark'}))

    full_id = forms.CharField(label='Full ID', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series1_storedfullid'}))

    short_id = forms.CharField(label='Short ID', required=False,
                            widget=forms.TextInput(attrs={'class': 'long series1_storedshortid'}))

    series = SubformField(formclass=Series2PartForm)

    class Meta:
        fields = ['series', 'title', 'uri', 'base_ark', 'full_id', 'short_id']
        model = Series1

class ArrangementModsForm(XmlObjectForm):
    """
    :class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.arrangment.models.ArrangementMods` metadata.
    """
    series = SubformField(formclass=SeriesPartForm)

    class Meta:
        model = ArrangementMods
        fields = [ 'series']

    #def __init__(self, **kwargs):
        #super(ArrangementModsForm, self).__init__(**kwargs)


class ArrangementObjectEditForm(forms.Form):
    '''
    Form to edit multiple datastreams on an
    :class:`~keep.arangement.models.ArrangementObject`.  Wrapper for
    editing :attr:`~keep.arangement.models.ArrangementObject.filetech`,
    :attr:`~keep.arangement.models.ArrangementObject.mods`, and
    :attr:`~keep.arangement.models.ArrangementObject.rights`.
    
    '''
    error_css_class = 'error'
    required_css_class = 'required'

    pdf = forms.FileField(label='PDF', required=False,
        help_text=mark_safe('''Upload a PDF version of this document for researcher access. <br/>
        After selecting your PDF, click "Save" below to submit the form and upload the file.'''),
        validators=[FileTypeValidator(types=['application/pdf'],
            message='Please upload a valid PDF')])

    comment = forms.CharField(max_length=255, label="Comment",  required=False,
        help_text="Brief description of changes to be stored in item history (optional)",
        widget=forms.TextInput(attrs={'class': 'long'}))

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       

        if instance is None:
            filetech_instance = None
            rights_instance = None
            mods_instance = None
        else:
            if hasattr(instance, 'filetech') and instance.filetech.exists:
                filetech_instance = instance.filetech.content
            else:
                filetech_instance = None
            rights_instance = instance.rights.content
            mods_instance = instance.mods.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            if self.object_instance.ark:
                initial['identifier'] = self.object_instance.ark
            else:
                initial['identifier'] = self.object_instance.pid + ' (PID)'

            # passed-in initial values override ones calculated here
            initial.update(orig_initial)

        common_opts = {'data': data, 'initial': initial}
        self.filetech = FileTechEditForm(instance=filetech_instance, prefix='fs', **common_opts)
        self.rights = RightsForm(instance=rights_instance, prefix='rights', **common_opts)
        self.mods = ArrangementModsForm(instance=mods_instance, prefix='mods', **common_opts)

        for form in (self.filetech, self.rights, self.mods):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(ArrangementObjectEditForm, self).__init__(data=data, initial=initial, **kwargs)

    def is_valid(self):
        return all(form.is_valid() for form in \
                    [ super(ArrangementObjectEditForm, self),
                      self.mods,
                      self.rights,
                      self.filetech,
                    ])

    def update_instance(self):
        # override default update to handle extra fields
        self.object_instance.mods.content = self.mods.update_instance()
        if self.object_instance.mods.content.record_info.change_date:
            self.object_instance.mods.content.record_info.change_date = str(datetime.now().isoformat())
        self.object_instance.rights.content = self.rights.update_instance()
        # NOTE: filetech form is currently used entirely for display,
        # all fields are read-only. Do NOT update object file-tech metadata.

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # if a pdf was uploaded and this object has a pdf datastream, add/update content
            if self.cleaned_data.get('pdf', None) and hasattr(self.object_instance, 'pdf'):
                uploaded_file = self.cleaned_data['pdf']
                self.object_instance.pdf.content = uploaded_file
                self.object_instance.pdf.mimetype = uploaded_file.content_type
                self.object_instance.pdf.label = uploaded_file.name

        # must return mods because XmlObjectForm depends on it for # validation
        return self.object_instance
