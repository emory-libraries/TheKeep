from django import forms

from eulxml.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField

from keep.arrangement.models import ProcessingBatchMods
from keep.common.models import FileMasterTech, Rights

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

    class Meta:
        model = FileMasterTech
        fields = [ 'md5', 'computer', 'path',
                   'rawpath', 'attributes', 'created',
                   'modified', 'type', 'creator' ]
        widgets = {
            'md5': forms.TextInput(attrs={'class': 'long'}),
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

    class Meta:
        model = Rights
        fields = [ 'access', 'copyright_holder_name', 'copyright_date',
                   'block_external_access', 'ip_note' ]
        widgets = {
            'copyright_holder_name': forms.TextInput(attrs={'class': 'long'}),
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


class ArrangementObjectEditForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       

        mods_instance = None
        st_instance = None
        filetech_instance = None
        rights_instance = None

        common_opts = {'data': data, 'initial': initial}
        self.filetech = FileTechEditForm(instance=filetech_instance, prefix='filetech', **common_opts)
        self.rights = RightsForm(instance=rights_instance, prefix='rights', **common_opts)

        for form in ( self.filetech,
                      self.rights ):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(ArrangementObjectEditForm, self).__init__(data=data, initial=initial)

##
# ProcessingBatch
##

class ProcessingBatchModsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.ProcessingBatch` metadata.
    """

    class Meta:
        model = ProcessingBatchMods
        fields = [ 'restrictions_on_access' ]
        widgets = {
            'restrictions_on_access': forms.CheckboxInput(attrs={'class': 'checkbox-warning'}),
        }

    def __init__(self, **kwargs):
        super(ProcessingBatchModsForm, self).__init__(**kwargs)



class ProcessingBatchEditForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):

        mods_instance = None


        common_opts = {'data': data, 'initial': initial}
        self.mods = ProcessingBatchModsForm(instance=mods_instance, prefix='mods', **common_opts)


        self.mods.error_css_class = self.error_css_class
        self.mods.required_css_class = self.error_css_class

        super(ProcessingBatchEditForm, self).__init__(data=data, initial=initial)