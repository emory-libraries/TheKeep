import logging

from django import forms
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from eulxml.xmlmap import mods
from eulxml.forms import XmlObjectForm, SubformField
from eulcm.xmlmap.mods import MODS
from eulcommon.djangoextras.formfields import DynamicChoiceField
from eultheme.forms import TelephoneInput

from keep.collection.models import CollectionObject
from keep.common.utils import solr_interface

logger = logging.getLogger(__name__)

def archive_choices():
    choices = [(a['pid'],
                a['title']) for a in CollectionObject.archives(format=dict)]
    choices.insert(0, ('', ''))   # blank option at the beginning (default)
    return choices

def archive_alias_choices():
    choices = []
    # we need pid aliases keyed on pid for lookup
    pid_aliases_by_pid = dict([(v, k) for k, v in settings.PID_ALIASES.iteritems()])
    for a in CollectionObject.archives(format=dict):
        if a['pid'] in pid_aliases_by_pid:
            alias = pid_aliases_by_pid[a['pid']]
            # use the alias for *both* display and submit value
            choices.append((alias, alias.upper()))
    choices.insert(0, ('', '---'))   # blank option at the beginning (default)
    return choices


class CollectionSearch(forms.Form):
    '''Form for searching for :class:`~keep.collection.models.CollectionObject`
    instances.'''
    search_tips = mark_safe('''<ul>
    <li>Search is NOT case sensitive.</li>
    <li>Search matches phrases. Wildcards
    <li>Search matches whole words anywhere in the field. Punctuation is
      ignored. Use wildcards <b>*</b> and <b>?</b> for broader matching. Note
      that these wildcards cannot be used at the beginning of a field.</li>
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


class FindCollection(forms.Form):
    '''Shortcut to find a collection quickly by number and owning archive.

    .. Note::

       In order to display the appropriate list of libraries/archives based on
       the current user permissions, you must pass the user at initialization
       time, i.e.::

            form = FindCollection(request.GET, user=request.user)

    '''
    collection = forms.IntegerField(required=True,
        help_text='Search by collection number',
        widget=TelephoneInput(attrs={'placeholder':'Collection number',
                                     'class': 'form-control'}))

    archive = DynamicChoiceField(label="Archive", choices=archive_alias_choices,
         initial='', required=True, help_text='Filter by owning archive')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        if 'user' in kwargs:
            del kwargs['user']
        super(FindCollection, self).__init__(*args, **kwargs)

        # if user is defined, use class method to find libraries with content
        # the user has permission to view
        if self.user is not None:
            self.fields['archive'].choices = self.archive_choices_by_user


    def archive_choices_by_user(self):
        # this method shouldn't be set if user isn't defined, but just in case
        if not self.user:
            return archive_alias_choices()

        # NOTE: should be possible to query for archives directly,
        # but filtering on audio items requires two levels of joins,
        # and it's unclear how that actually works

        # use collection facet query to get list of archives
        q = CollectionObject.item_collection_query()
        q = q.facet_by('archive_id', sort='count', mincount=1) \
              .paginate(rows=0)

        # - depending on permissions, restrict to collections with researcher audio
        if not self.user.has_perm('collection.view_collection') and \
               self.user.has_perm('collection.view_researcher_collection'):
            q = q.join('collection_id', 'pid', researcher_access=True)
            q = q.join('collection_id', 'pid', has_access_copy=True)

        # make a list of user-viewable archive pids
        archives = [pid for pid, count in q.execute().facet_counts.facet_fields['archive_id']]

        choices = []
        # we need pid aliases keyed on pid for lookup
        pid_aliases_by_pid = dict([(v, k) for k, v in settings.PID_ALIASES.iteritems()])
        for a in archives:
            if a in pid_aliases_by_pid:
                alias = pid_aliases_by_pid[a]
                # use the alias for *both* display and submit value
                choices.append((alias, alias.upper()))
        choices.insert(0, ('', '---'))   # blank option at the beginning (default)

        return choices


class AccessConditionForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~eulcm.xmlmap.mods.AccessCondition` :

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
    :class:`~eulcm.xmlmap.mods.NamePart`

        * suppress default label 'text'
        * use :class:`~django.forms.TextInput` with class *form-control*
    '''
    text = forms.CharField(label='Name Part',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = mods.NamePart

class RoleForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS name
    :class:`~eulxml.xmlmap.mods.Role` information

        * suppress default label 'text'
        * configure type with initial value 'text' and make read-only
    '''
    text = forms.CharField(label='Role',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    # for our purposes, all roles will be type='text': set as initial value & make read only
    type = forms.CharField(label='Type', initial='text', widget=forms.HiddenInput)
    class Meta:
        model = mods.Role

class NameForm(XmlObjectForm):
    '''Custom :class:`~eulxml.forms.XmlObjectForm` to edit MODS
    :class:`~eulxml.xmlmap.mods.Name` information.

        * use custom :class:`~eulxml.xmlmap.mods.NamePart` and
          :class:`~eulxml.xmlmap.mods.Role` forms (:class:`NamePartForm`, :class:`RoleForm`)
        * customize id field label & help text
        * suppress displayForm and affiliation fields
    '''
    id = forms.CharField(required=False, label='Identifier',
                        widget=forms.TextInput(attrs={'class': 'form-control'}),
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

    error_css_class = 'has-error'

    # TODO: would be nice to have an ObjectChoiceField analogous to django's ModelChoiceField
    collection = DynamicChoiceField(label="Archive",  choices=archive_choices,
                    required=True,
                    help_text="Owning repository for this collection of materials.")
                    # using URI because it will be used to set a relation in RELS-EXT
    source_id = forms.IntegerField(label="Source Identifier",
                    help_text="Source archival collection number (enter 100 for MSS100 or Series 100)",
                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(help_text="Title of the archival collection",
                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    # NOTE: handling date range with custom input forms and logic on update_instance
    # this could possibly be handled by a custom XmlObjectForm for originInfo
    date_created = forms.CharField(help_text="Date created, or start date for a date range.", required=False)
    date_end = forms.CharField(help_text="End date for a date range. Leave blank if not a range.",
                                required=False)
    name = SubformField(formclass=NameForm)
    restrictions_on_access = SubformField(formclass=AccessConditionForm)
    use_and_reproduction = SubformField(formclass=AccessConditionForm)
    comment = forms.CharField(label="Comment",  required=False,
                    help_text="Optional description of changes made.",
                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MODS
        fields = (
            'collection', 'source_id', 'title', 'resource_type', 'name',
            'restrictions_on_access', 'use_and_reproduction',
            )
        widgets = {
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
        }

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

            if self.object_instance.collection:
                initial['collection'] = self.object_instance.collection.pid

            if 'initial' not in kwargs:
                kwargs['initial'] = {}
            kwargs['initial'].update(initial)
        else:
            mods_instance = None

        super(CollectionForm, self).__init__(data=data, instance=mods_instance,
                                             **kwargs)

    def clean(self):
        """Perform cross-field validation/cleaning on the form. Currently,
        verify that collection and source_id are unique together.
        """
        cleaned_data = super(CollectionForm, self).clean()
        if cleaned_data.get('collection', '') and \
                (cleaned_data.get('source_id', '') or cleaned_data.get('source_id', '') == 0) and \
           self._duplicate_exists(cleaned_data):
            msg = "A collection already exists with this Archive and Source Id."
            self._errors['collection'] = self.error_class([msg])
            self._errors['source_id'] = self.error_class([msg])
            del cleaned_data['collection']
            del cleaned_data['source_id']

        return cleaned_data

    def _duplicate_exists(self, cleaned_data):
        """Determine if saving this form would create a duplicate
        collection. Specifically, verify that there is no other collection
        with the same collection (archive) and source_id present in solr.
        """
        collection = cleaned_data.get('collection')
        source_id = cleaned_data.get('source_id')

        solr = solr_interface()
        query = solr.query(
                content_model=CollectionObject.COLLECTION_CONTENT_MODEL,
                source_id=source_id, archive_id=collection)
        response = query.execute()

        # if there are no matches then this is definitely not a
        if response.result.numFound == 0:
            return False

        if response.result.numFound > 1:
            # if there's already more than one match then this is definitely
            # a duplicate
            return True

        # otherwise there's exactly one. if it's this object then this *is*
        # the collection with that archive/id.
        return (response[0]['pid'] != self.object_instance.pid)


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
                self.object_instance.collection = self.object_instance.get_object(self.cleaned_data['collection'])

        # must return mods portion because XmlObjectForm depends on it for validation
        return self.instance

#Simple Collection
class SimpleCollectionEditForm(forms.Form):
    status = forms.ChoiceField(
        label='Status',
        choices=[('Accessioned', 'Accessioned'),
                 ('Processed', 'Processed')],
        help_text='Indicates if collection members are visible'
    )


class CollectionSuggestionWidget(forms.MultiWidget):
    '''Custom :class:`django.forms.MultiWidget` for use with
    :class:`CollectionSuggestionField`.
    '''
    def __init__(self, attrs=None):
        hidden_attrs = {'class': 'collection-suggest-id' }
        text_attrs = {'class': 'collection-suggest form-control' }
        if attrs:
            text_attrs.update(attrs)
            hidden_attrs.update(attrs)
        widgets = (forms.HiddenInput(attrs=hidden_attrs),
                   forms.TextInput(attrs=text_attrs))
        super(CollectionSuggestionWidget, self).__init__(widgets, attrs)

    def decompress(self, pid):
        # break single field value (pid) into multi-value needed for
        # multi-value field

        if pid:
            # main (hidden) value is collection id; if set, get collection
            # information to display as pre-set value in the visible field
            coll = CollectionObject.find_by_pid(pid)
            if coll:
                # if source id is available, include in label
                if 'source_id' in coll:
                    label = '%(source_id)s %(title)s' % coll
                else:
                    label = coll['title']
            else:
                # fallback - should only happen if collection is not
                # indexed or pid is invalid
                logger.error('No collection information found for %s' % pid)
                label = '%s (title not found)' % pid

            return [pid, label]

        return [None, None]

class CollectionSuggestionField(forms.MultiValueField):
    '''Custom :class:`django.forms.MultiValueField` to support
    auto-complete input for selecting collections.  This field is made
    up of two fields: the primary field, a hidden field that stores
    the pid for the selected
    :class:`~keep.collection.models.CollectionObject`; and a text
    field used for display, which is expected to be used as an
    auto-complete input and set the hidden id.
    '''

    widget = CollectionSuggestionWidget

    default_error_messages = {
        'required': 'This field is required. You must choose a collection ' +
        'from the suggested values.'
    }

    default_help_text = 'Collection this item belongs to. ' + \
       'Begin typing collection number and/or title words and choose from the suggestions.'


    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        if 'help_text' not in kwargs:
            kwargs['help_text'] = self.default_help_text
        fields = (
            forms.CharField(error_messages=errors, localize=localize),
            forms.CharField(error_messages=errors, localize=localize)
        )
        super(CollectionSuggestionField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if id is empty
            # (label is for display purposes only, so doesn't really matter)
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['required'])
            return data_list[0]
        return None

