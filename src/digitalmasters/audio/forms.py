import logging

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.safestring import mark_safe

from eulcore.django.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcore.django.forms.fields import W3CDateField, DynamicChoiceField

from digitalmasters import mods
from digitalmasters.audio.models import AudioMods, SourceTech, DigitalTech, CodecCreator
from digitalmasters.collection.models import CollectionObject

logger = logging.getLogger(__name__)

class UploadForm(forms.Form):
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object in Fedora. 255 characters max.')
    audio = forms.FileField(label="Audio file")


def _cmp_collections(a, b):
    # compare pidspaces alphabetically, then compare pid length numerically
    # (so that short pids sort before long ones), then compare pids
    # alphabetically)
    return cmp((a.pidspace, len(a.pid), a.pid),
               (b.pidspace, len(b.pid), b.pid))

EMPTY_LABEL_TEXT = ''

_COLLECTION_OPTIONS_CACHE_KEY = 'collection-options'
def _collection_options(include_blank=False):
        # by default only cache for a minute at a time so users can see changes quickly
        cache_duration = 60
        # when running in development environment, cache for longer
        if settings.DEV_ENV:
            cache_duration = 60*30
        options = cache.get(_COLLECTION_OPTIONS_CACHE_KEY, None)
        if options is None:
            collections = [ c for c in CollectionObject.item_collections()
                            if c.pidspace == settings.FEDORA_PIDSPACE ]
            collections.sort(cmp=_cmp_collections)
            logging.debug('Calculated collections: ' + repr(collections))
            options = [(c.uri, '%s - %s' % (c.mods.content.source_id, c.label)) for c in collections]
            cache.set(_COLLECTION_OPTIONS_CACHE_KEY, options, cache_duration)

        # if include_blank is requested, insert an empty option at the beginning of the list
        if include_blank:
            options.insert(0, ('', EMPTY_LABEL_TEXT))
        return options

def _collection_options_with_blank():
    # collection is optional for search but not for edit form
    return _collection_options(include_blank=True)

class ItemSearch(forms.Form):
    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')
    description = forms.CharField(required=False,
            help_text='Search for word or phrase in general note or digitization purpose.  May contain wildcards * or ?.')
    # FIXME: should we cache these choices ? 
    collection = DynamicChoiceField(label="Collection",  choices=_collection_options_with_blank,
                    help_text='''Limit to items in the specified collection.
                    Start typing collection number to let your browser search within the list.''',
                    required=False)
    pid = forms.CharField(required=False, help_text='Search by fedora pid.',
            initial='%s:' % settings.FEDORA_PIDSPACE)
    date = forms.CharField(required=False,
            help_text='Search date created or issued.  May contain wildcards * or ?.')
    rights = forms.CharField(required=False,
            help_text='Search for word or phrase within access conditions.  May contain wildcards * or ?.')

    
class SimpleNoteForm(XmlObjectForm):
    """Custom XmlObjectForm to simplify editing a MODS note.  Displays text content
    input only, as a textarea with no label; no other note attributes are displayed.
    """
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = mods.Note
        fields = ['text']


class SimpleDateForm(XmlObjectForm):
    """Custom XmlObjectForm to edit a MODS date.  Currently only allows
    editing the date value itself, using a W3CDateField.
    """
    date = W3CDateField(label='', required=False)
    class Meta:
        model = mods.Date
        fields = ['date']


class OriginInfoForm(XmlObjectForm):
    """Custom XmlObjectForm to edit MODS originInfo.  Currently only consists
    of bare-minimum date entry for date created and issued.
    """
    #Create the subform fields from fields (xmlmap) in eulcore.
    created = SubformField(formclass=xmlobjectform_factory(mods.DateCreated,
                            form=SimpleDateForm, max_num=1))
    issued = SubformField(formclass=xmlobjectform_factory(mods.DateIssued,
                            form=SimpleDateForm, max_num=1))
    class Meta:
        model = mods.OriginInfo


class ModsEditForm(XmlObjectForm):
    """XmlObjectForm for metadata on a :class:`AudioObject`.

    Takes an :class:`AudioObject` as form instance. This stands in contrast
    to a regular :class:`eulcore.django.forms.XmlObjectForm`, which would
    take an :class:`eulcore.xmlmap.XmlObject`. This form edits a whole
    :class:`AudioObject`, although currently most of the editing is on the
    MODS datastream (which is an :class:`eulcore.xmlmap.XmlObject`). The
    most expedient way to make an :class:`AudioObject` editable was to make
    a customized :class:`eulcore.django.forms.XmlObjectForm` that mostly
    deals with the MODS datastream.
    """
    #collection = DynamicChoiceField(label="Collection",
    #                choices=_collection_options,
    #                help_text="Collection this item belongs to.", required=False)
                    # using URI because it will be used to set a relation in RELS-EXT
                    
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
            'collection', 'identifier', 'title', 
            'origin_info', 'general_note', 'part_note',
            )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'long'}),
            }


class SourceTechForm(XmlObjectForm):
    """Custom XmlObjectForm to edit SourceTech metadata.
    """
    # note: speed and reel_size conflict with autogenerated subforms;
    # these fields needed to be named something different for them to work
    _speed = forms.ChoiceField(SourceTech.speed_options, label='Recording Speed',
                    help_text='Speed at which the sound was recorded')
    reel = forms.ChoiceField(SourceTech.reel_size_options, label='Reel Size',
                    help_text='Size of tape reel', required=False)

    class Meta:
        model = SourceTech
        # temporarily making repeating fields into single fields
        # (stringlistfields not yet supported by xmlobjectform)
        fields = ['note', 'related_files', 'conservation_history', 'manufacturer',
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

        speed = self.add_prefix('_speed')
        speed_value = self.add_prefix('speed-value')
        speed_aspect = self.add_prefix('speed-aspect')
        speed_unit = self.add_prefix('speed-unit')
        if speed not in self.initial and speed_value in self.initial \
            and speed_unit in self.initial and speed_aspect in self.initial \
            and self.initial[speed_aspect] and self.initial[speed_value] \
            and self.initial[speed_unit]:
            self.initial[speed] = '|'.join([self.initial[speed_aspect],
                                               self.initial[speed_value],
                                               self.initial[speed_unit]])
        reel = self.add_prefix('reel')
        reel_value = self.add_prefix('reel_size-value')
        if reel not in self.initial and reel_value in self.initial:
            self.initial[reel] = self.initial[reel_value]

    def update_instance(self):
        # override default update to handle extra fields
        super(SourceTechForm, self).update_instance()
        
        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            if '_speed' in self.cleaned_data:
                # format of option list is 'value unit' (e.g., 16 rpm or 15 inches/sec
                # - split and save in appropriate fields
                aspect, value, unit = self.cleaned_data['_speed'].split('|')
                self.instance.speed.aspect = aspect
                self.instance.speed.value = value
                self.instance.speed.unit = unit

            if 'reel' in self.cleaned_data:
                self.instance.reel_size.value = self.cleaned_data['reel']
                # for now, all values are inches - may need to refine later
                self.instance.reel_size.unit = 'inches'

        # return object instance
        return self.instance

class UserChoiceField(forms.ModelChoiceField):
    'Extend django choice field to set a custom label for displaying user objects'
    def label_from_instance(self, obj):
        return '%s (%s)' % (', '.join([obj.last_name, obj.first_name]),
                            obj.username)

class DigitalTechForm(XmlObjectForm):
    """Custom XmlObjectForm to edit DigitalTech metadata.
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
        engineer = self.add_prefix('engineer')
        engineer_id = self.add_prefix('transfer_engineer-id')
        if engineer_id in self.initial and self.initial[engineer_id]:
            # find corresponding User object based on transfer engineer id (ldap only for now)
            self.initial[engineer] = User.objects.get(username=self.initial[engineer_id]).id

        hardware = self.add_prefix('hardware')
        codec_creator_id = self.add_prefix('codec_creator-id')
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
            self.instance.transfer_engineer.id = user.username
            self.instance.transfer_engineer.id_type = 'ldap'    # ldap only for now
            self.instance.transfer_engineer.name = user.get_full_name()

            # set codec creator
            cc_id = self.cleaned_data['hardware']
            # required, so should always be present and overwrite any previous data
            if cc_id:
                hardware, software, version = CodecCreator.configurations[cc_id]
                self.instance.codec_creator.id = cc_id
                # hardware may be multiple, so treat as a list
                for old_hw in self.instance.codec_creator.hardware_list:
                    self.instance.codec_creator.hardware_list.remove(old_hw)
                self.instance.codec_creator.hardware_list.extend(hardware)
                self.instance.codec_creator.software = software
                self.instance.codec_creator.software_version = version

            
        # return object instance
        return self.instance

class AudioObjectEditForm(forms.Form):
    """XmlObjectForm for metadata on a :class:`AudioObject`.

    Takes an :class:`AudioObject` as form instance. This stands in contrast
    to a regular :class:`eulcore.django.forms.XmlObjectForm`, which would
    take an :class:`eulcore.xmlmap.XmlObject`. This form edits a whole
    :class:`AudioObject`, although currently most of the editing is on the
    MODS datastream (which is an :class:`eulcore.xmlmap.XmlObject`). The
    most expedient way to make an :class:`AudioObject` editable was to make
    a customized :class:`eulcore.django.forms.XmlObjectForm` that mostly
    deals with the MODS datastream.
    """
    collection = DynamicChoiceField(label="Collection",
        choices=_collection_options, required=False,
        help_text="Collection this item belongs to. " +
        "Start typing collection number to let your browser search within the list.")

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):       
        if instance is None:
            mods_instance = None
            st_instance = None
            dt_instance = None
        else:
            mods_instance = instance.mods.content
            st_instance = instance.sourcetech.content
            dt_instance = instance.digitaltech.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            # populate fields not auto-generated & handled by XmlObjectForm
            if self.object_instance.collection_uri:
                initial['collection'] = str(self.object_instance.collection_uri)

            # passed-in initial values override ones calculated here
            initial.update(orig_initial)

        common_opts = {'data': data, 'initial': initial}
        # FIXME: use prefixes to ensure uniqueness? (not yet fully supported by XmlObjectForm)
        self.mods = ModsEditForm(instance=mods_instance, prefix='mods', **common_opts)
        self.sourcetech = SourceTechForm(instance=st_instance, prefix='st', **common_opts)
        self.digitaltech = DigitalTechForm(instance=dt_instance, prefix='dt', **common_opts)
        self.mods.error_css_class = self.error_css_class
        self.sourcetech.error_css_class = self.error_css_class
        self.mods.required_css_class = self.required_css_class
        self.sourcetech.required_css_class = self.required_css_class
        super(AudioObjectEditForm, self).__init__(data=data, initial=initial)

    def is_valid(self):
        return super(AudioObjectEditForm, self).is_valid() and \
                self.mods.is_valid() and self.sourcetech.is_valid() and \
                self.digitaltech.is_valid()

    def update_instance(self):
        # override default update to handle extra fields
        #super(AudioObjectEditForm, self).update_instance()
        self.object_instance.mods.content = self.mods.update_instance()
        self.object_instance.sourcetech.content = self.sourcetech.update_instance()
        self.object_instance.digitaltech.content = self.digitaltech.update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection_uri = self.cleaned_data['collection']

        # must return mods because XmlObjectForm depends on it for # validation
        return self.object_instance
