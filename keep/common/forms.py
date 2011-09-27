import logging
from django import forms
from django.conf import settings
import django.forms
from django.utils.safestring import mark_safe
from eulcommon.djangoextras.formfields import DynamicChoiceField
from keep.collection.forms import archive_choices
from keep.collection.models import CollectionObject, SimpleCollection
from keep.common.models import Rights

class ReadonlyTextInput(forms.TextInput):
    'Read-only variation on :class:`django.forms.TextInput`'
    readonly_attrs = {
        'readonly': 'readonly',
        'class': 'readonly long',
        'tabindex': '-1',
    }
    def __init__(self, attrs=None):
        if attrs is not None:
            self.readonly_attrs.update(attrs)
        super(ReadonlyTextInput, self).__init__(attrs=self.readonly_attrs)


# rights access status code options - used in edit & search forms
# use code for value, display code + abbreviation so code can be used for short-cut selection
rights_access_options = [ (item[0], '%s : %s' % (item[0], item[1])) for item in Rights.access_terms ]
rights_access_options.insert(0, ('', ''))

EMPTY_LABEL_TEXT = ''

def _simple_collection_options():
    sc_opts = SimpleCollection.simple_collections()

    options = [('info:fedora/' + sc.get('pid', ''), '%s ' % ( sc.get('label', '')))
    for sc in sorted(sc_opts, key=lambda k: k['label'])]

    options.insert(0, ("", ""))

    return options

def _collection_options():
        collections = [c for c in CollectionObject.item_collections()
                        if settings.FEDORA_PIDSPACE in c['pid'] ]
        logging.debug('Calculated collections: ' + ' '.join(c['pid'] for c in collections))
        # generate option list with URI as value and source id - title display
        # sort on source id
        options = [('info:fedora/' + c.get('pid', ''), '%s - %s' % (c.get('source_id', ''), c.get('title', '')))
                for c in sorted(collections, key=lambda k: k['source_id'])]

        # always include a blank option at the beginning of the list
        # - not specified for search, force user to select on the edit form
        options.insert(0, ('', EMPTY_LABEL_TEXT))
        return options

class ItemSearch(forms.Form):
    '''Form for searching for :class:`~keep.audio.models.AudioObject`
    instances.'''

    #format_options used in search form 
    format_options = (
       ("", ""),
       ('info:fedora/emory-control:Arrangement-1.0', "Arrangement"),
       ('info:fedora/emory-control:EuterpeAudio-1.0', "Audio"),
    )



    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')
    notes = forms.CharField(required=False,
            help_text='Search for word or phrase in general note, digitization purpose, or related files.  May contain wildcards * or ?.')
    collection = DynamicChoiceField(label="Collection",  choices=_collection_options,
                    help_text='''Limit to items in the specified collection.
                    Start typing collection number to let your browser search within the list.''',
                    required=False)
    simpleCollection = DynamicChoiceField(choices=_simple_collection_options, label='Simple Collection', required=False,
                    help_text='Search for items with the specified SimpleCollection')
    content_model = forms.ChoiceField(label="Format",  choices=format_options,
                    help_text="Limit to items with given format.", required=False)
    pid = forms.CharField(required=False, help_text='Search by fedora pid, DM id or DM other id.',
            initial='%s:' % settings.FEDORA_PIDSPACE, label="Pid/DM ID/Other ID")
    date = forms.CharField(required=False,
            help_text=mark_safe('''Search date created, issued, or uploaded.  Most dates
            are in <b>YYYY</b>, <b>YYYY-MM</b> or <b>YYYY-MM-DD</b> format.<br/>
            Date uploaded is in <b>YYYY-MM-DDTHH:MM:SS.mmmmmmmZ</b> format.
            May contain wildcards * or ?.<br/>
            <i>Example:</i> search <b>2011-02*</b> for all items uploaded in February 2011.'''))
    #Add "No Verdict option to search only by copying original list of options and adding to it
    rights_access_options_search = rights_access_options[:]
    rights_access_options_search.insert(1, ('0', 'No Verdict'))
    access_code = forms.ChoiceField(rights_access_options_search, label='Rights', required=False,
                    help_text='Search for items with the specified rights access status')
    archive = DynamicChoiceField(label="Archive", required=False,
                    choices=archive_choices, initial='',
                    help_text='Search for items that are owned by the specified Archive')