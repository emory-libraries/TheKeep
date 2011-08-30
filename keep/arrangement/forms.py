from django import forms

import mods

from eulxml.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField


from keep.common.models import FileMasterTech, Rights
from keep.common.forms import ReadonlyTextInput

from keep.arrangement.models import ArrangementMods, Series1, Series2

##
# Arrangement
##
# rights access status code options - used in edit & search forms
# use code for value, display code + abbreviation so code can be used for short-cut selection
rights_access_options = [ (item[0], '%s : %s' % (item[0], item[1])) for item in Rights.access_terms ]
rights_access_options.insert(0, ('', ''))


class FileTechEditForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """

    created = W3CDateField(required=False)
    modified = W3CDateField(required=False)

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
        model = FileMasterTech
        fields = [ 'local_id', 'md5', 'computer', 'path',
                   'rawpath', 'attributes', 'created',
                   'modified', 'type', 'creator' ]
        widgets = {
            'local_id': ReadonlyTextInput,
            'md5': ReadonlyTextInput,
            'computer': ReadonlyTextInput,
            'path': ReadonlyTextInput,
            'rawpath': ReadonlyTextInput,
            'attributes': ReadonlyTextInput,
            'type': ReadonlyTextInput,
            'creator': ReadonlyTextInput,
        }

    def __init__(self, **kwargs):
        super(FileTechEditForm, self).__init__(**kwargs)

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
            access_text = Rights.access_terms_dict[access_code].text
            self.instance.create_access_status()
            self.instance.access_status.code = access_code
            self.instance.access_status.text = access_text

        return self.instance


class Series2PartForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.NamePart`

        * suppress default label 'text'
        * use :class:`~django.forms.TextInput` with class *long*
    '''
    title = forms.CharField(label='Series Title', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series2_storedtitle'}))

    uri = forms.CharField(label='URI', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series2_storeduri'}))

    base_ark = forms.CharField(label='Base Ark', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series2_storedark'}))

    full_id = forms.CharField(label='Full ID', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series2_storedfullid'}))

    short_id = forms.CharField(label='Short ID', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series2_storedshortid'}))

    class Meta:
        fields = ['title', 'uri', 'base_ark', 'full_id', 'short_id']
        model = Series2

class SeriesPartForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.NamePart`

        * suppress default label 'text'
        * use :class:`~django.forms.TextInput` with class *long*
    '''
    title = forms.CharField(label='Series Title', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series1_storedtitle'}))


    uri = forms.CharField(label='URI', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series1_storeduri'}))

    base_ark = forms.CharField(label='Base Ark', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series1_storedark'}))

    full_id = forms.CharField(label='Full ID', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series1_storedfullid'}))

    short_id = forms.CharField(label='Short ID', required=False,
                            widget=ReadonlyTextInput(attrs={'class': 'long series1_storedshortid'}))

    series = SubformField(formclass=Series2PartForm)

    class Meta:
        fields = ['series', 'title', 'uri', 'base_ark', 'full_id', 'short_id']
        model = Series1

class ArrangementModsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """
    series = SubformField(formclass=SeriesPartForm)

    class Meta:
        model = ArrangementMods
        fields = [ 'series']

    #def __init__(self, **kwargs):
        #super(ArrangementModsForm, self).__init__(**kwargs)


class ArrangementObjectEditForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       

        if instance is None:
            filetech_instance = None
            rights_instance = None
            mods_instance = None
        else:
            filetech_instance = instance.filetech.content.file[0] # <-this is not right
            rights_instance = instance.rights.content
            mods_instance = instance.mods.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            # populate fields not auto-generated & handled by XmlObjectForm
            #if self.object_instance.collection_uri:
                #initial['collection'] = str(self.object_instance.collection_uri)

            if self.object_instance.ark:
                initial['identifier'] = self.object_instance.ark
            else:
                initial['identifier'] = self.object_instance.pid + ' (PID)'

            # passed-in initial values override ones calculated here
            initial.update(orig_initial)

        common_opts = {'data': data, 'initial': initial}
        self.filetech = FileTechEditForm(instance=filetech_instance, prefix='filetech', **common_opts)
        self.rights = RightsForm(instance=rights_instance, prefix='rights', **common_opts)
        self.mods = ArrangementModsForm(instance=mods_instance, prefix='mods', **common_opts)


        for form in ( self.filetech,
                      self.rights,
                      self.mods ):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(ArrangementObjectEditForm, self).__init__(data=data, initial=initial)

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
        self.object_instance.rights.content = self.rights.update_instance()
        self.object_instance.filetech.content = self.filetech.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        #if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            #if hasattr(self, 'object_instance'):
                #self.object_instance.collection_uri = self.cleaned_data['collection']

        # must return mods because XmlObjectForm depends on it for # validation
        return self.object_instance
