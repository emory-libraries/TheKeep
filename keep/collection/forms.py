import logging

from django import forms
import django.forms
from django.forms import BaseForm
from django.utils.safestring import mark_safe

from eulfedora.rdfns import relsext as relsextns

from eulxml.forms import XmlObjectForm, SubformField
from eulcommon.djangoextras.formfields import DynamicChoiceField

from keep import mods
from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionMods, CollectionObject, SimpleCollection
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

def archive_choices():
    choices = [('info:fedora/%s' % a['pid'],
                a['title']) for a in CollectionObject.archives(format=dict)]
    choices.insert(0, ('', ''))   # blank option at the beginning (default)
    return choices



class CollectionSearch(forms.Form):
    '''Form for searching for :class:`~keep.collection.models.CollectionObject`
    instances.'''
    search_tips = mark_safe('''<ul>
    <li>Search is NOT case sensitive.</li>
    <li>Search matches whole words only, including  punctuation.
      You should use wildcards <b>*</b> and <b>?</b> to get around
      this limitation.  For example, if a name is entered as
      <b>Rushdie, Salman</b>, you may want to search for <b>rushdie*</b>.</li>
    <li>If search terms are entered in multiple inputs, only records matching
      values in <b>all</b> search fields are returned.</li>
    </ul>''')
    wildcard_tip = '''May contain wildcards <b>*</b> or <b>?</b>.'''
    source_id = forms.IntegerField(required=False, label='Collection Number',
            help_text=mark_safe('''Search by manuscript or series number (e.g.,
                enter <b>100</b> for <b>MSS100</b> or <b>Series 100</b>).'''))
    title = forms.CharField(required=False,
            help_text=mark_safe('Search by collection title word or phrase. ' + wildcard_tip))
    creator = forms.CharField(required=False,
            help_text=mark_safe('Search by collection creator. '  + wildcard_tip))
    archive_id = DynamicChoiceField(label="Archive",  choices=archive_choices,
                                    initial='', required=False)

                                

class AccessConditionForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.AccessCondition` :

        * suppress default label of 'text'
        * use :class:`~django.forms.Textarea` widget
        * make not required
    '''
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = mods.AccessCondition
        exclude = ['type']

class NamePartForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.NamePart`

        * suppress default label 'text'
        * use :class:`~django.forms.TextInput` with class *long*
    '''
    text = forms.CharField(label='Name Part',
                            widget=forms.TextInput(attrs={'class': 'long'}))
    class Meta:
        model = mods.NamePart

class RoleForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS name
    :class:`~keep.mods.Role` information

        * suppress default label 'text'
        * configure type with initial value 'text' and make read-only
    '''
    text = forms.CharField(label='Role',
                            widget=forms.TextInput(attrs={'class': 'long'}))
    # for our purposes, all roles will be type='text': set as initial value & make read only
    type = forms.CharField(label='Type', initial='text', widget=forms.HiddenInput)
    class Meta:
        model = mods.Role

class NameForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~keep.mods.Name` information.

        * use custom :class:`~keep.mods.NamePart` and
          :class:`~keep.mods.Role` forms (:class:`NamePartForm`, :class:`RoleForm`)
        * customize id field label & help text
        * suppress displayForm and affiliation fields
    '''
    id = forms.CharField(required=False, label='Identifier',
                        widget=forms.TextInput(attrs={'class': 'long'}),
                        help_text="Optional; supply for NAF names.")
    name_parts = SubformField(formclass=NamePartForm)
    roles = SubformField(formclass=RoleForm)
    class Meta:
        model = mods.Name
        exclude = ['display_form', 'affiliation']


class CollectionForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit descriptive
    metadata on a :class:`~keep.collection.models.CollectionObject`.

    Takes a :class:`~keep.collection.models.CollectionObject` as form instance.
    This stands in contrast to a regular :class:`~eulxml.forms.XmlObjectForm`,
    which would take an :class:`~euxml.xmlmap.XmlObject`. This form edits a whole
    :class:`~keep.collection.models.CollectionObject`, although most of the editing
    is on the MODS datastream (which is an :class:`~eulxml.xmlmap.XmlObject`).
    The most expedient way to make a :class:`~keep.collection.models.CollectionObject`
    editable was to make a customized :class:`~eulxml.forms.XmlObjectForm`
    that mostly deals with the  MODS datastream.
    '''

    # TODO: would be nice to have an ObjectChoiceField analogous to django's ModelChoiceField
    collection = DynamicChoiceField(label="Archive",  choices=archive_choices,
                    required=False,
                    help_text="Owning repository for this collection of materials.")
                    # using URI because it will be used to set a relation in RELS-EXT
    source_id = forms.IntegerField(label="Source Identifier",
                    help_text="Source archival collection number (enter 100 for MSS100 or Series 100)")
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
            if mods_instance.origin_info and \
               mods_instance.origin_info.created:
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
            self.instance.create_origin_info()
            for i in range(len(self.instance.origin_info.created)):
                self.instance.origin_info.created.pop()
            self.instance.origin_info.created.append(mods.DateCreated(
                    date=self.cleaned_data['date_created'],
                    key_date=True,
                    ))
            # if there is a date end, store it and set end & start attributes
            if 'date_end' in self.cleaned_data and self.cleaned_data['date_end']:
                self.instance.create_origin_info()
                self.instance.origin_info.created.append(mods.DateCreated(
                    date=self.cleaned_data['date_end'],
                    point='end',
                    ))
                self.instance.origin_info.created[0].point = 'start'

            # set relation to archive object when an instance was passed in
            if hasattr(self, 'object_instance'):
                self.object_instance.set_collection(self.cleaned_data['collection'])

        # must return mods portion because XmlObjectForm depends on it for validation
        return self.instance

#Simple Collection

# Simple Collection status options - used in edit screen
simple_collection_options = (
                  ('Processed', 'Processed'),
                  ('Accessioned', 'Accessioned')
    )

class SimpleCollectionModsForm(XmlObjectForm):
    """:class:`~eulxml.forms.XmlObjectForm` to edit
    :class:`~keep.common.models.SimpleCollection` metadata.
    """
    restrictions_on_access = forms.ChoiceField(simple_collection_options, label='Status',
           help_text='Indicates if collection members are visible')

    class Meta:
        model = CollectionMods
        fields = [ 'restrictions_on_access' ]


class SimpleCollectionEditForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, data=None, instance=None, initial={}, **kwargs):

        if instance is None:
            mods_instance = None
        else:
            mods_instance = instance.mods.content
            self.object_instance = instance
            orig_initial = initial

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
        self.mods = SimpleCollectionModsForm(instance=mods_instance, prefix='mods', **common_opts)


        self.mods.error_css_class = self.error_css_class
        self.mods.required_css_class = self.error_css_class

        super(SimpleCollectionEditForm, self).__init__(data=data, initial=initial)

    #Update member ArrangementObjects to specified status
    def update_objects(self, status):
        success_count= 0
        fail_count = 0

        #translate form status codes to fedora state code
        codes = {'Processed': 'A', 'Accessioned' : 'I'}

        #target state for every object in the collection
        if status not in codes:
            return (0 ,0) # could not complete task due to bad status
        else:
            state =  codes[status]

        repo = Repository()
        pids = list(self.object_instance.rels_ext.content.objects(self.object_instance.uriref, relsextns.hasMember))

        for pid in pids:
            try:
                obj = repo.get_object(pid=pid, type=ArrangementObject)
                obj.state=state
                saved = obj.save()
                if saved:
                    success_count = success_count + 1  #add to success count if something goes right
                else:
                    fail_count = fail_count + 1  #add to fail count if something goes wrong
                    logger.error("Failed to update ArrangementObject %s:%s" % (obj.pid, obj.label))
            except:
                fail_count = fail_count + 1  #add to fail count if something goes wrong
                logger.error("Failed to update ArrangementObject %s:%s" % (obj.pid, obj.label))

        return (success_count, fail_count) 
