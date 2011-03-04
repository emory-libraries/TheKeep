import logging

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from eulcore.django.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcore.django.forms.fields import W3CDateField, DynamicChoiceField

from keep import mods
from keep.audio.models import AudioMods, SourceTech, DigitalTech, Rights, CodecCreator
from keep.collection.models import CollectionObject

logger = logging.getLogger(__name__)

class UploadForm(forms.Form):
    'Single-file upload form; takes a label and a file'
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object. 255 characters max. (optional)',
                required=False)
    audio = forms.FileField(label="File")


def _cmp_collections(a, b):
    # compare pidspaces alphabetically, then compare pid length numerically
    # (so that short pids sort before long ones), then compare pids
    # alphabetically)
    return cmp((a.pidspace, len(a.pid), a.pid),
               (b.pidspace, len(b.pid), b.pid))

EMPTY_LABEL_TEXT = ''

# rights access status code options - used in edit & search forms
# use code for value, display code + abbreviation so code can be used for short-cut selection
rights_access_options = [ (item[0], '%s : %s' % (item[0], item[1])) for item in Rights.access_terms ]
rights_access_options.insert(0, ('', ''))

def _collection_options():
        collections = [c for c in CollectionObject.item_collections()
                        if settings.FEDORA_PIDSPACE in c['pid'] ]
        logging.debug('Calculated collections: ' + ' '.join(c['pid'] for c in collections))
        # generate option list with URI as value and source id - title display
        # sort on source id
        options = [('info:fedora/' + c['pid'], '%s - %s' % (c['source_id'], c['title']))
                for c in sorted(collections, key=lambda k: k['source_id'])]

        # always include a blank option at the beginning of the list
        # - not specified for search, force user to select on the edit form
        options.insert(0, ('', EMPTY_LABEL_TEXT))
        return options

class ItemSearch(forms.Form):
    '''Form for searching for :class:`~keep.audio.models.AudioObject`
    instances.'''
    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')
    description = forms.CharField(required=False,
            help_text='Search for word or phrase in general note or digitization purpose.  May contain wildcards * or ?.')
    collection = DynamicChoiceField(label="Collection",  choices=_collection_options,
                    help_text='''Limit to items in the specified collection.
                    Start typing collection number to let your browser search within the list.''',
                    required=False)
    pid = forms.CharField(required=False, help_text='Search by fedora pid.',
            initial='%s:' % settings.FEDORA_PIDSPACE)
    date = forms.CharField(required=False,
            help_text='Search date created or issued.  May contain wildcards * or ?.')
    rights = forms.ChoiceField(rights_access_options, required=False,
                    help_text='Search for items with the specified Rights access condition')

    
class SimpleNoteForm(XmlObjectForm):
    """Custom :class:`~eulcore.django.forms.XmlObjectForm` to simplify editing
    a MODS :class:`~keep.mods.Note`.  Displays text content input only,
    as a :class:`~django.forms.Textarea` with no label; no other note attributes
    are displayed.
    """
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = mods.Note
        fields = ['text']


class SimpleDateForm(XmlObjectForm):
    """Custom :class:`~eulcore.django.forms.XmlObjectForm` to edit a MODS
    :class:`~keep.mods.Date`.  Currently only allows editing the date
    value itself, using a :class:`~eulcore.django.forms.fields.W3CDateField`.
    """
    date = W3CDateField(label='', required=False)
    class Meta:
        model = mods.Date
        fields = ['date']


class OriginInfoForm(XmlObjectForm):
    """Custom :class:`~eulcore.django.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.OriginInfo`.  Currently only consists
    of simple date entry for date created and issued using :class:`SimpleDateForm`.
    """
    #Create the subform fields from fields (xmlmap) in eulcore.
    created = SubformField(formclass=xmlobjectform_factory(mods.DateCreated,
                            form=SimpleDateForm, max_num=1))
    issued = SubformField(formclass=xmlobjectform_factory(mods.DateIssued,
                            form=SimpleDateForm, max_num=1))
    class Meta:
        model = mods.OriginInfo


class ModsEditForm(XmlObjectForm):
    """:class:`~eulcore.django.forms.XmlObjectForm` for editing
    :class:`~keep.audio.models.AudioMods`.
    """
    # TODO: ARK will need to be set on form init from instance
    # read-only text input to display ARK (not editable)
    identifier = forms.CharField(label="Identifier", required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'readonly', 'tabindex': '-1'}))
    origin_info = SubformField(formclass=OriginInfoForm, label='Origin Info')
    general_note = SubformField(formclass=SimpleNoteForm, label='General Note')
    # FIXME: label as part number note? add directions/examples?
    part_note = SubformField(formclass=SimpleNoteForm, label='Part Note')
    
    class Meta:
        model = AudioMods
        fields = (
            'identifier', 'title', 'origin_info',
            'general_note', 'part_note',
            )
        widgets = {
            'title': forms.Textarea,
            }


class SourceTechForm(XmlObjectForm):
    """Custom :class:`~eulcore.django.forms.XmlObjectForm` to edit
    :class:`~keep.audio.models.SourceTech` metadata.
    """
    # note: speed and reel_size conflict with autogenerated subforms;
    # these fields needed to be named something different for them to work
    _speed = forms.ChoiceField(SourceTech.speed_options, label='Recording Speed',
                    required=True, help_text='Speed at which the sound was recorded')
    reel = forms.ChoiceField(SourceTech.reel_size_options, label='Reel Size',
                    help_text='Size of tape reel', required=False)

    class Meta:
        model = SourceTech
        # temporarily making repeating fields into single fields
        # (stringlistfields not yet supported by xmlobjectform)
        fields = ['note', 'related_files', 'conservation_history',
            '_speed', 'sublocation', 'form', 'sound_characteristics', 'stock',
            'housing', 'reel']
        widgets = {
            'note': forms.Textarea,
            'related_files': forms.TextInput(attrs={'class': 'long'}),
            'conservation_history': forms.TextInput(attrs={'class': 'long'}),
        }

    def __init__(self, **kwargs):       
        super(SourceTechForm, self).__init__(**kwargs)
        # populate initial data for fields not auto-generated & handled by XmlObjectForm
        # speed in xml maps to a single custom field

        speed = '_speed'
        speed_value = 'speed-value'
        speed_aspect = 'speed-aspect'
        speed_unit = 'speed-unit'
        if speed not in self.initial and speed_value in self.initial \
            and speed_unit in self.initial and speed_aspect in self.initial \
            and self.initial[speed_aspect] and self.initial[speed_value] \
            and self.initial[speed_unit]:
            self.initial[speed] = '|'.join([self.initial[speed_aspect],
                                               self.initial[speed_value],
                                               self.initial[speed_unit]])
        reel = 'reel'
        reel_value = 'reel_size-value'
        if reel not in self.initial and reel_value in self.initial:
            self.initial[reel] = self.initial[reel_value]

    def update_instance(self):
        # override default update to handle extra fields
        super(SourceTechForm, self).update_instance()
        
        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            if self.cleaned_data.get('_speed', ''):
                # format of option list is 'value unit' (e.g., 16 rpm or 15 inches/sec
                # - split and save in appropriate fields
                aspect, value, unit = self.cleaned_data['_speed'].split('|')
                self.instance.create_speed()
                self.instance.speed.aspect = aspect
                self.instance.speed.value = value
                self.instance.speed.unit = unit

            if 'reel' in self.cleaned_data:
                self.instance.create_reel_size()
                self.instance.reel_size.value = self.cleaned_data['reel']
                # for now, all values are inches - may need to refine later
                self.instance.reel_size.unit = 'inches'

        # return object instance
        return self.instance

class UserChoiceField(forms.ModelChoiceField):
    '''Extend Django's :class:`~django.forms.ModelChoiceField` to set a custom
    label for displaying user objects'''
    def label_from_instance(self, obj):
        return '%s (%s)' % (', '.join([obj.last_name, obj.first_name]),
                            obj.username)

class DigitalTechForm(XmlObjectForm):
    """Custom :class:`~eulcore.django.forms.XmlObjectForm` to edit
    :class:`~keep.audio.models.DigitalTech` metadata.
    """
    engineer = UserChoiceField(label='Transfer Engineer',
        queryset=User.objects.filter(password='!').order_by('last_name'),
        empty_label=EMPTY_LABEL_TEXT,
        # limit to LDAP users (no password in django db) and sort by last name
        help_text=mark_safe('''The person who performed the digitization or
        conversion that produced the file.<br/>
        Search by typing first letters of the last name.
        (Users must log in to this site once to be listed.)'''))
    hardware = forms.ChoiceField(sorted(CodecCreator.options), label='Codec Creator',
                    help_text='Hardware, software, and software version used to create the digital file',
                    required=True)
    date_captured = W3CDateField(help_text='Date digital capture was made', required=True)
    class Meta:
        model = DigitalTech
        fields = ['date_captured', 'note', 'digitization_purpose', 'engineer', 'hardware']
        widgets = {
            'note': forms.Textarea,
            'digitization_purpose': forms.TextInput(attrs={'class': 'long'}),
        }

    def __init__(self, **kwargs):
        super(DigitalTechForm, self).__init__(**kwargs)
        # populate initial data for fields not auto-generated & handled by XmlObjectForm
        engineer = 'engineer'
        engineer_id = 'transfer_engineer-id'
        if engineer_id in self.initial and self.initial[engineer_id]:
            # find corresponding User object based on transfer engineer id (ldap only for now)
            self.initial[engineer] = User.objects.get(username=self.initial[engineer_id]).id

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
            user = self.cleaned_data['engineer']
            self.instance.create_transfer_engineer()
            self.instance.transfer_engineer.id = user.username
            self.instance.transfer_engineer.id_type = 'ldap'    # ldap only for now
            self.instance.transfer_engineer.name = user.get_full_name()

            # set codec creator
            cc_id = self.cleaned_data['hardware']
            # required, so should always be present and overwrite any previous data
            if cc_id:
                hardware, software, version = CodecCreator.configurations[cc_id]
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
    """:class:`~eulcore.django.forms.XmlObjectForm` to edit
    :class:`~keep.audio.models.Rights` metadata.
    """

    access = forms.ChoiceField(rights_access_options, label='Access Status',
                    help_text='File access conditions, as determined by analysis of copyright, donor agreements, permissions, etc.')
    copyright_date = W3CDateField(required=False)

    class Meta:
        model = Rights
        fields = [ 'access', 'copyright_holder_name', 'copyright_date' ]
        widgets = {
            'copyright_holder_name': forms.TextInput(attrs={'class': 'long'}),
        }

    def __init__(self, **kwargs):
        super(RightsForm, self).__init__(**kwargs)

        # XmlObjectForm magically populates fields based directly on
        # XmlObject field names, but we have a couple form fields that
        # aren't.
        access = 'access'
        access_condition_code = 'access_condition-code'
        if access_condition_code in self.initial:
            self.initial[access] = self.initial[access_condition_code]

    def update_instance(self):
        super(RightsForm, self).update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            access_code = self.cleaned_data['access']
            access_text = Rights.access_terms_dict[access_code].text
            self.instance.create_access_condition()
            self.instance.access_condition.code = access_code
            self.instance.access_condition.text = access_text

        return self.instance


class AudioObjectEditForm(forms.Form):
    """:class:`~django.forms.Form` for metadata on an
    :class:`~keep.audio.models.AudioObject`.

    Takes an :class:`~keep.audio.models.AudioObject`. This stands in contrast
    to a regular :class:`~eulcore.django.forms.XmlObjectForm`, which would
    take an :class:`~eulcore.xmlmap.XmlObject`. This form edits a whole
    :class:`~keep.audio.models.AudioObject` by editing multiple XML
    datastreams (whose content are instances of :class:`~eulcore.xmlmap.XmlObject`),
    with individual :class:`~eulcore.django.forms.XmlObjectForm` form instances
    for each XML datastream.
    """
    collection = DynamicChoiceField(label="Collection",
        choices=_collection_options, required=True,
        help_text="Collection this item belongs to. " +
        "Start typing collection number to let your browser search within the list.")

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       
        if instance is None:
            mods_instance = None
            st_instance = None
            dt_instance = None
            rights_instance = None
        else:
            mods_instance = instance.mods.content
            st_instance = instance.sourcetech.content
            dt_instance = instance.digitaltech.content
            rights_instance = instance.rights.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            # populate fields not auto-generated & handled by XmlObjectForm
            if self.object_instance.collection_uri:
                initial['collection'] = str(self.object_instance.collection_uri)

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

        for form in ( self.mods, self.sourcetech, self.digitaltech,
                      self.rights ):
            form.error_css_class = self.error_css_class
            form.required_css_class = self.error_css_class

        super(AudioObjectEditForm, self).__init__(data=data, initial=initial)

    def is_valid(self):
        return all(form.is_valid() for form in \
                    [ super(AudioObjectEditForm, self),
                      self.mods,
                      self.sourcetech,
                      self.digitaltech,
                      self.rights,
                    ])

    def update_instance(self):
        # override default update to handle extra fields
        #super(AudioObjectEditForm, self).update_instance()
        self.object_instance.mods.content = self.mods.update_instance()
        self.object_instance.sourcetech.content = self.sourcetech.update_instance()
        self.object_instance.digitaltech.content = self.digitaltech.update_instance()
        self.object_instance.rights.content = self.rights.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection_uri = self.cleaned_data['collection']

        # must return mods because XmlObjectForm depends on it for # validation
        return self.object_instance
