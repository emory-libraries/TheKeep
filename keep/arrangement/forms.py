from django import forms

from eulxml.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField


from keep.common.models import FileMasterTech, Rights
from keep.common.forms import ReadonlyTextInput

from keep.arrangement.models import ArrangementMods

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

    class Meta:
        model = FileMasterTech
        fields = [ 'local_id', 'md5', 'computer', 'path',
                   'rawpath', 'attributes', 'created',
                   'modified', 'type', 'creator' ]
        widgets = {
            'local_id': ReadonlyTextInput,
            'md5': ReadonlyTextInput,
            'computer': forms.TextInput(attrs={'class': 'long'}),
            'path': forms.TextInput(attrs={'class': 'long'}),
            'rawpath': forms.TextInput(attrs={'class': 'long'}),
            'attributes': forms.TextInput(attrs={'class': 'long'}),
            'type': forms.TextInput(attrs={'class': 'long'}),
            'creator': forms.TextInput(attrs={'class': 'long'}),
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

class ArrangementModsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.Rights` metadata.
    """

    #type = forms.ChoiceField(SourceTech.speed_options, label='Recording Speed',
                    #required=True, help_text='Speed at which the sound was recorded')
    title = forms.CharField(label="Series", required=False, widget=forms.TextInput(attrs={'class': 'long'}))
    #identifier = forms.CharField(label="Identifier", required=False, widget=forms.TextInput(attrs={'class': 'long'}))




    class Meta:
        model = ArrangementMods
        fields = [ 'title' ]
        #fields = [ 'subseries' ]


    def __init__(self, **kwargs):
        super(ArrangementModsForm, self).__init__(**kwargs)


class ArrangementObjectEditForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       

        if instance is None:
            filetech_instance = None
            rights_instance = None
            mods_instance = None
        else:
            filetech_instance = instance.filetech.content
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
