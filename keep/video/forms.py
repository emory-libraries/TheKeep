import logging

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from datetime import datetime

from eulxml.xmlmap import mods
from eulxml.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcm.xmlmap.boda import Rights
from eulcommon.djangoextras.formfields import W3CDateField, DynamicChoiceField

from keep.video.models import VideoMods, VideoSourceTech, VideoDigitalTech, VideoCodecCreator
from keep.collection.forms import NameForm, CollectionSuggestionField
from keep.common.models import rights_access_terms_dict, TransferEngineer
from keep.common.forms import ReadonlyTextInput, rights_access_options, \
     EMPTY_LABEL_TEXT, CommentForm

logger = logging.getLogger(__name__)


class SimpleNoteForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to simplify editing
    a MODS :class:`~eulxml.xmlmap.mods.Note`.  Displays text content input only,
    as a :class:`~django.forms.Textarea` with no label; no other note attributes
    are displayed.
    """
    text = forms.CharField(label='',
        widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = mods.Note
        fields = ['text']


class SimpleShortNoteForm(SimpleNoteForm):
    'Same as :class:`SimpleNoteForm` but with a text input instead of a textarea.'
    text = forms.CharField(label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


class SimpleDateForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to edit a MODS
    :class:`~eulxml.xmlmap.mods.Date`.  Currently only allows editing the date
    value itself, using a :class:`~eulcommon.djangoextras.formfields.W3CDateField`.
    """
    date = W3CDateField(label='', required=False)
    class Meta:
        model = mods.Date
        fields = ['date']


class OriginInfoForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~eulxml.xmlmap.mods.OriginInfo`.  Currently only consists
    of simple date entry for date created and issued using :class:`SimpleDateForm`.
    """
    form_label = 'Origin Info'
    #Create the subform fields from fields (xmlmap) in eulxml.
    created = SubformField(formclass=xmlobjectform_factory(mods.DateCreated,
                            form=SimpleDateForm, max_num=1))
    issued = SubformField(formclass=xmlobjectform_factory(mods.DateIssued,
                            form=SimpleDateForm, max_num=1),
                          label='Date Issued')
    class Meta:
        model = mods.OriginInfo
        fields = ['created', 'issued']



class ModsEditForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` for editing
    :class:`~keep.video.models.VideoMods`.
    """
    # ARK value is set in form instance data by VideoEditForm init
    # read-only text input to display ARK (not editable)
    identifier = forms.CharField(label="Identifier", required=False,
        widget=ReadonlyTextInput)
    resource_type = forms.CharField(required=False, widget=ReadonlyTextInput)
    origin_info = SubformField(formclass=OriginInfoForm)
    general_note = SubformField(formclass=SimpleNoteForm)

    names = SubformField(formclass=NameForm)

    class Meta:
        model = VideoMods
        fields = (
            'identifier', 'dm1_id', 'dm1_other_id', 'title', 'origin_info',
            'general_note', 'resource_type',
        )
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control'}),
            'identifier': ReadonlyTextInput,
            'dm1_id': ReadonlyTextInput,
            'dm1_other_id': ReadonlyTextInput,
        }


class SourceTechForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.video.models.VideoSourceTech` metadata.
    """

    signal_format = forms.ChoiceField(VideoSourceTech.signal_format_options, label='Signal Format/region',
                     required=False)

    class Meta:
        model = VideoSourceTech
        # temporarily making repeating fields into single fields
        # (stringlistfields not yet supported by xmlobjectform)
        fields = ['note', 'conservation_history',
            'speed', 'sublocation', 'form', 'signal_format', 'sound_characteristics', 'chroma', 'gauge', 'stock']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'conservation_history': forms.TextInput(attrs={'class': 'form-control'}),
            'sublocation': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
        }


def _transfer_engineer_id(**kwargs):
    '''Generate a transfer engineer id for use on the form. Keyword
    arguments are expected to include type and id.'''
    # this method is an attempt to ensure consistency in field order
    # TODO: could this method be part of the TransferEngineer object?
    return'%(type)s|%(id)s' % kwargs


class DigitalTechForm(XmlObjectForm):
    """Custom :class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.video.models.VideoDigitalTech` metadata.
    """
    engineer = DynamicChoiceField(label='Transfer Engineer',
        # choices method will be set at form instance initialization
        required=VideoDigitalTech._fields['transfer_engineer'].required,
        # use required setting from xmlobject field (TODO: need a better way to access this...)
        help_text=mark_safe('''The person who performed the digitization or
        conversion that produced the file.<br/>
        Search by typing first letters of the last name.
        (Users must log in to this site once to be listed.)'''))

    def _transfer_engineer_options(self):
        '''Method to use to dynamically populate the engineer
        DymanicChoiceField.  Generates a list of all LDAP users in the
        django DB with a select value that includes the id and idtype
        to be set in the DigitalTech.transfer_engineer field.  If the
        current data instance includes a non-LDAP user (i.e., user
        information migrated from the legacy system), add that user
        and id to the list so it will display and update correctly
        when the form is saved.

        This method must be assigned to engineer field choices at
        object init so we have access to the current object instance.
        '''
        # get a list of  LDAP users; limiting by presence of ldap profile, sorting by last name
        options = [(_transfer_engineer_id(type=TransferEngineer.LDAP_ID_TYPE,
                                          id=user.username),
                    '%s (%s)' % (user.get_full_name(), user.username))
                   for user in get_user_model().objects.filter(groups__name='Video Curator').order_by('last_name')]
        options.insert(0, ('', EMPTY_LABEL_TEXT))

        # add local transfer engineer options to the list
        for id, label in TransferEngineer.local_engineers.iteritems():
            options.append((_transfer_engineer_id(type=TransferEngineer.LOCAL_ID_TYPE,
                                                  id=id), label))

        # if there is an instance with a non-ldap id, add that to the options
        if self.instance:
            if self.instance.transfer_engineer and \
                   self.instance.transfer_engineer.id_type == TransferEngineer.DM_ID_TYPE:
                current_id =  _transfer_engineer_id(type=self.instance.transfer_engineer.id_type,
                                                    id=self.instance.transfer_engineer.id)
                display_label = "%s (DM %s)" % (self.instance.transfer_engineer.name,
                                                self.instance.transfer_engineer.id)
                options.append((current_id, display_label))
        return options


    hardware = forms.ChoiceField(sorted(VideoCodecCreator.options), label='Codec Creator',
                    help_text='Hardware, software, and software version used to create the digital file',
                    required=False)
    class Meta:
        model = VideoDigitalTech
        fields = ['note', 'digitization_purpose', 'engineer', 'hardware', 'codec_quality']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'digitization_purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, **kwargs):
        super(DigitalTechForm, self).__init__(**kwargs)
        # bind the dynamic field choices for transfer engineer
        self.fields['engineer'].choices = self._transfer_engineer_options

        # populate initial data for fields not auto-generated & handled by XmlObjectForm

        # set engineer value based on id and id type
        engineer = 'engineer'			# aliases for data keys in initial data
        engineer_id = 'transfer_engineer-id'
        engineer_type = 'transfer_engineer-id_type'
        if engineer_id in self.initial and engineer_type in self.initial:
            self.initial[engineer] = _transfer_engineer_id(id=self.initial[engineer_id],
                                                       type=self.initial[engineer_type])

        hardware = 'hardware'
        codec_creator_id = 'codec_creator-id'
        if codec_creator_id in self.initial:
            self.initial[hardware] = self.initial[codec_creator_id]

    def update_instance(self):
        # override default update to handle extra fields
        super(DigitalTechForm, self).update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set transfer engineer id and name based on User object
            if self.cleaned_data['engineer']:
                usertype, sep, userid  = self.cleaned_data['engineer'].partition('|')
            else:
                usertype, userid = None, None
            # transfer engineer is optional - set in xml if present, otherwise remove
            if usertype and userid:
                self.instance.create_transfer_engineer()
                self.instance.transfer_engineer.id = userid
                self.instance.transfer_engineer.id_type = usertype

                # if this an ldap user, look up by username to get full name
                if usertype == TransferEngineer.LDAP_ID_TYPE:
                    user = get_user_model().objects.filter(username=userid).get()
                    self.instance.transfer_engineer.name = user.get_full_name()

                elif usertype == TransferEngineer.DM_ID_TYPE:
                    # The only way an old-DM id can be set is if that is what was
                    # present in the record before editing.
                    # In that case, use the display name from the initial data.
                    self.instance.transfer_engineer.name = self.initial['transfer_engineer-name']

                elif usertype == TransferEngineer.LOCAL_ID_TYPE:
                    self.instance.transfer_engineer.name = TransferEngineer.local_engineers[userid]
            else:
                del(self.instance.transfer_engineer)

            # set codec creator
            cc_id = self.cleaned_data['hardware']
            # required, so should always be present and overwrite any previous data
            if cc_id:
                hardware, software, version = VideoCodecCreator.configurations[cc_id]
                self.instance.create_codec_creator()
                self.instance.codec_creator.id = cc_id
                # hardware may be multiple, so treat as a list
                for old_hw in self.instance.codec_creator.hardware_list:
                    self.instance.codec_creator.hardware_list.remove(old_hw)
                self.instance.codec_creator.hardware_list.extend(hardware)
                self.instance.codec_creator.software = software
                self.instance.codec_creator.software_version = version


        # return object instance
        return self.instance


class RightsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.video.models.Rights` metadata.
    """

    access = forms.ChoiceField(rights_access_options, label='Access Status',
           help_text='File access status, as determined by analysis of copyright, donor agreements, permissions, etc.')
    copyright_date = W3CDateField(required=False)

    class Meta:
        model = Rights
        fields = [ 'access', 'copyright_holder_name', 'copyright_date',
                   'block_external_access', 'ip_note' ]
        widgets = {
            'copyright_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_note': forms.Textarea(attrs={'class': 'form-control'}),
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


class VideoEditForm(forms.Form):
    """:class:`~django.forms.Form` for metadata on an
    :class:`~keep.video.models.Video`.

    Takes an :class:`~keep.video.models.Video`. This stands in contrast
    to a regular :class:`~eulxml.forms.XmlObjectForm`, which would
    take an :class:`~eulxml.xmlmap.XmlObject`. This form edits a whole
    :class:`~keep.video.models.Video` by editing multiple XML
    datastreams (whose content are instances of :class:`~eulxml.xmlmap.XmlObject`),
    with individual :class:`~eulxml.forms.XmlObjectForm` form instances
    for each XML datastream.
    """

    collection = CollectionSuggestionField(required=True)

    error_css_class = 'has-error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):
        if instance is None:
            mods_instance = None
            st_instance = None
            dt_instance = None
            rights_instance = None
            comment_instance = None
        else:
            mods_instance = instance.mods.content
            st_instance = instance.sourcetech.content
            dt_instance = instance.digitaltech.content
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
        self.sourcetech = SourceTechForm(instance=st_instance, prefix='st', **common_opts)
        self.digitaltech = DigitalTechForm(instance=dt_instance, prefix='dt', **common_opts)
        self.rights = RightsForm(instance=rights_instance, prefix='rights', **common_opts)
        self.comments = CommentForm( prefix='comments',**common_opts)

        for form in ( self.mods, self.sourcetech, self.digitaltech,
                      self.rights, self.comments ):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(VideoEditForm, self).__init__(data=data, initial=initial)

    def is_valid(self):
        return all(form.is_valid() for form in \
                    [ super(VideoEditForm, self),
                      self.mods,
                      self.sourcetech,
                      self.digitaltech,
                      self.rights,
                      self.comments,
                    ])

    def update_instance(self):
        # override default update to handle extra fields
        #super(VideoEditForm, self).update_instance()
        
        self.object_instance.mods.content = self.mods.update_instance()
        if self.object_instance.mods.content.record_info:
            self.object_instance.mods.content.record_info.change_date = str(datetime.now().isoformat())
        self.object_instance.sourcetech.content = self.sourcetech.update_instance()
        self.object_instance.digitaltech.content = self.digitaltech.update_instance()
        self.object_instance.rights.content = self.rights.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection = self.object_instance.get_object(self.cleaned_data['collection'])

        # must return mods because XmlObjectForm depends on it for # validation
        return self.object_instance
