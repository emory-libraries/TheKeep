import logging

import mods
from django import forms
from django.conf import settings
from django.core.cache import cache

from eulcore.django.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcore.django.forms.fields import W3CDateField, DynamicChoiceField

from digitalmasters import mods
from digitalmasters.audio.models import AudioMods
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
            options.insert(0, ('', '--'))
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


class EditForm(XmlObjectForm):
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
    # FIXME: this needs to save to RELS-EXT
    collection = DynamicChoiceField(label="Collection",
                    choices=_collection_options,
                    help_text="Collection this item belongs to.", required=False)
                    # using URI because it will be used to set a relation in RELS-EXT
                    
    # TODO: ARK will need to be set on form init from instance
    # read-only text input to display ARK (not editable)
    identifier = forms.CharField(label="Identifier", required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'long'}))
    origin_info = SubformField(formclass=OriginInfoForm)
    general_note = SubformField(formclass=SimpleNoteForm)
    # FIXME: label as part number note? add directions/examples?
    part_note = SubformField(formclass=SimpleNoteForm)
    
    class Meta:
        model = AudioMods
        fields = (
            'collection', 'identifier', 'title', 
            'origin_info', 'general_note', 'part_note',
            )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'long'}),
            }

    def __init__(self, data=None, instance=None, initial={}, **kwargs):
        # overriding to accept an AudioObject instead of AudioMods
        if instance is None:
            mods_instance = None
        else:
            mods_instance = instance.mods.content
            self.object_instance = instance
            orig_initial = initial
            initial = {}

            # populate fields not auto-generated & handled by XmlObjectForm
            if self.object_instance.collection_uri:
                initial['collection'] = str(self.object_instance.collection_uri)

            # passed-in initial values override ones calculated here
            initial.update(orig_initial)

        super_init = super(EditForm, self).__init__
        super_init(data=data, instance=mods_instance, initial=initial, **kwargs)

    def update_instance(self):
        # override default update to handle extra fields
        super(EditForm, self).update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set collection if we have all the attributes we need
            if hasattr(self, 'object_instance'):
                self.object_instance.collection_uri = self.cleaned_data['collection']

        # must return mods because XmlObjectForm depends on it for # validation
        return self.instance
