from django import forms
from django.conf import settings

from eulcore.django.forms import XmlObjectForm, SubformField

from digitalmasters.audio.models import Mods, CollectionMods, ModsDate, CollectionObject, \
    ModsAccessCondition, ModsName, ModsNamePart, ModsRole, ModsOriginInfo

class UploadForm(forms.Form):
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object in Fedora. 255 characters max.')
    audio = forms.FileField(label="Audio file")

class SearchForm(forms.Form):
    pid = forms.CharField(required=False, help_text='Search by fedora pid.',
            initial='%s:' % settings.FEDORA_PIDSPACE)
    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')

class CollectionSearch(forms.Form):
    mss = forms.CharField(required=False, label='Manuscript Number', initial='MSS',
            help_text='Search by collection manuscript number (e.g, MSS123)')
    title = forms.CharField(required=False,
            help_text='Search by collection title word or phrase.  May contain wildcards * or ?.')
    creator = forms.CharField(required=False,
            help_text='Search by collection creator')
    # NOTE: this only sets choices on load time (should be OK for search)
    collection_list = [(o.uri, o.label) for o in CollectionObject.top_level()]
    collection_list.insert(0, ('', '--'))   # add a blank option first
    collection = forms.ChoiceField(label="Collection", required=False,
                    choices=collection_list, initial='')

class EditForm(XmlObjectForm):
    class Meta:
        model = Mods
        fields = [
            'title', 'resource_type', 'note',
            'origin_info.created.date', 'origin_info.created.key_date',
            ]

        widgets = {
            'note' : {'text': forms.Textarea },
            'origin_info' : { 'created' : { 'date': forms.DateInput }}
            }

class AccessConditionForm(XmlObjectForm):
    """Custom XmlObjectForm to edit MODS accessCondition fields:
     * suppress default label 'text'
     * use Textarea
     * make not required
    """
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = ModsAccessCondition
        exclude = ['type']

class NamePartForm(XmlObjectForm):
    """Custom XmlObjectForm to edit MODS name namePart
     * suppress default label 'text'
    """
    text = forms.CharField(label='Name Part', 
                            widget=forms.TextInput(attrs={'class': 'long'}))
    class Meta:
        model = ModsNamePart

class RoleForm(XmlObjectForm):
    """Custom XmlObjectForm to edit MODS name role information
     * suppress default label 'text'
     * configure type with initial value 'text' and make read-only
    """
    text = forms.CharField(label='Role',
                            widget=forms.TextInput(attrs={'class': 'long'}))
    # for our purposes, all roles will be type='text': set as initial value & make read only
    type = forms.CharField(label='Type', initial='text',
                    widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = ModsRole

class NameForm(XmlObjectForm):    
    """Custom XmlObjectForm to edit MODS name information
     * use custom namePart and role forms
     * customize id field label & help text
     * suppress displayForm and affiliation
    """
    id = forms.CharField(required=False, label='Identifier',
                        help_text="Optional; supply for NAF names.")
    name_parts = SubformField(formclass=NamePartForm)
    roles = SubformField(formclass=RoleForm)
    class Meta:
        model = ModsName
        exclude = ['display_form', 'affiliation']

class CollectionForm(XmlObjectForm):
    """Custom XmlObjectForm to edit descriptive metadata on a :class:`CollectionObject`.

    Takes a :class:`CollectionObject` as form instance.  This stands in contrast
    to a regular :class:`eulcore.django.forms.XmlObjectForm`, which would take
    an :class:`eulcore.xmlmap.XmlObject`. This form edits a whole
    :class:`CollectionObject`, although most of the editing is on the MODS
    datastream (which is an :class:`eulcore.xmlmap.XmlObject`). The most expedient
    way to make a :class:`CollectionObject` editable was to make a customized
    :class:`eulcore.django.forms.XmlObjectForm` that mostly deals with the
    MODS datastream.
    """
    
    # NOTE: this only sets choices on load time
    # TODO: would be nice to have an ObjectChoiceField analogous to django's ModelChoiceField
    collection = forms.ChoiceField(label="Collection",
                    choices=[(o.uri, o.label) for o in CollectionObject.top_level()],
                    help_text="Top-level collection this collection falls under.")
                    # using URI because it will be used to set a relation in RELS-EXT
    source_id = forms.CharField(label="Source Identifier",
                    help_text="Source archival collection number, e.g. MSS123")
    title = forms.CharField(help_text="Title of the archival collection",
                    widget=forms.TextInput(attrs={'class': 'long'}))
    # NOTE: handling date range with custom input forms and logic on update_instance
    # this could possibly be handled by a custom XmlObjectForm for originInfo
    date_created = forms.CharField(help_text="Date created, or start date for a date range.")
    date_end = forms.CharField(help_text="End date for a date range. Leave blank if not a range.",
                                required=False)
    name = SubformField(formclass=NameForm)
    restrictions_on_access = SubformField(formclass=AccessConditionForm)
    use_and_reproduction = SubformField(formclass=AccessConditionForm)
    class Meta:
        model = CollectionMods
        fields = (
            'collection', 'source_id', 'title', 'resource_type', 'name',
            'restrictions_on_access', 'use_and_reproduction',
            )

    def __init__(self, data=None, instance=None, **kwargs):
        # overriding init to accept a CollectionObject instead of CollectionMods
        # - set initial data for extra fields (collection & dates) from instance
        # - pass mods xmlobject to parent XmlObjectForm
        if instance is not None:
            # store the digital object, store mods to pass on to parent init
            self.object_instance = instance
            mods_instance = instance.mods.content
            
            # populate fields not auto-generated & handled by XmlObjectForm
            initial = {}
            if mods_instance.origin_info.created:
                initial['date_created'] = mods_instance.origin_info.created[0].date
                if len(mods_instance.origin_info.created) > 1:
                    initial['date_end'] = mods_instance.origin_info.created[1].date

            if self.object_instance.collection_id is not None:
                initial['collection'] = self.object_instance.collection_id

            if 'initial' not in kwargs:
                kwargs['initial'] = {}
            kwargs['initial'].update(initial)
        else:
            mods_instance = None
            
        super(CollectionForm, self).__init__(data=data, instance=mods_instance,
                                             **kwargs)
        
    def update_instance(self):
        # override default update to handle extra fields (collection & dates)
        # NOTE: collection membership can only be set when a CollectionObject
        #       was passed in as form instance
        super(CollectionForm, self).update_instance()

        # cleaned data only available when the form is valid,
        # but xmlobjectform is_valid calls update_instance
        if hasattr(self, 'cleaned_data'):
            # set date created - could be a single date or a date range
            # remove existing dates and re-add
            for i in range(len(self.instance.origin_info.created)):
                self.instance.origin_info.created.pop()
            self.instance.origin_info.created.append(ModsDate(
                    date=self.cleaned_data['date_created'],
                    key_date=True,
                    ))
            # if there is a date end, store it and set end & start attributes
            if 'date_end' in self.cleaned_data and self.cleaned_data['date_end']:
                self.instance.origin_info.created.append(ModsDate(
                    date=self.cleaned_data['date_end'],
                    point='end',
                    ))
                self.instance.origin_info.created[0].point = 'start'

            # set relation to top-level collection when an instance was passed in
            if hasattr(self, 'object_instance'):
                self.object_instance.set_collection(self.cleaned_data['collection'])

        # must return mods portion because XmlObjectForm depends on it for validation
        return self.instance
