import logging
from django import forms
from django.conf import settings
from django.contrib import messages
import django.forms
from django.utils.safestring import mark_safe
from eulcommon.djangoextras.formfields import DynamicChoiceField
import operator

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
        options = [('info:fedora/' + c.get('pid', ''),
                    '%s %s %s' % (c.get('source_id', ''),
                                  c.get('archive_short_name', ''),
                                  c.get('title', '')))
                   for c in sorted(collections, key=lambda k: k.get('source_id', ''))]

        # always include a blank option at the beginning of the list
        # - not specified for search, force user to select on the edit form
        options.insert(0, ('', EMPTY_LABEL_TEXT))
        return options

class ItemSearch(forms.Form):
    '''Form for searching for :class:`~keep.audio.models.AudioObject`
    instances.'''

    # format_options used in search form 
    format_options = (
       ("", ""), # FIXME: use from cmodels from models?
       ('info:fedora/emory-control:Arrangement-1.0', "Born-Digital"),
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
    access_code = forms.ChoiceField(rights_access_options, label='Rights', required=False,
                    help_text='Search for items with the specified rights access status')


    # fields that can be selected to control search display output
    display_field_opts = {'pid': 'PID', 'title': 'Title', # ? ('ark_uri', 'ARK'),
                          'created': 'Date Created',
                          'last_modified': 'Last Modified',
                          'part': 'Part Note',
                          'description': 'General Note',
                          'related_files': 'Related Files',
                          'sublocation': 'Sublocation',
                          'type': 'Resource Type',
                          'access_code': 'Rights Status code',
                          'rights': 'Rights Status',
                          'digitization_purpose': 'Digitization Purpose',
                          'date_issued': 'Date Isssued',
                          'collection_label': 'Collection',
                          'duration': 'Audio file duration',
                          'ip_note': 'IP Note',
                          'copyright_date': 'Copyright Date'}

    # generate a list of tuples for ChoiceField, sorted by display label
    _display_field_choices = sorted(display_field_opts.iteritems(),
                                  key=operator.itemgetter(1))
    display_fields = forms.MultipleChoiceField(_display_field_choices, required=False,
         help_text=mark_safe('''Customize which fields should be displayed in search results.
         If none are selected, uses default search results format.'''))
    output = forms.ChoiceField([('html', 'html'), ('csv', 'csv')], initial='html', required=False,
         help_text=mark_safe('''Output format.  If csv is selected, all matching rows will be
         selected and output as a downloadable CSV file.  CSV output is only valid when display
         fields are selected.   You may want to test your search terms in html and then
         <i>revise your search</i> to switch to csv output.'''))
    display_output_fields = ['display_fields', 'output']
    'list of fields that are used to format output display'



    def search_options(self, request=None):
        '''Method to generate a dictionary of search options that can
        be passed to Solr, based on valid data in the current form.

        Takes an optional request object in order to display messages
        to users when leading wildcards are removed or ignored.
        '''

        # don't do anything if the form isn't valid
        if not self.is_valid():
            return
        
        search_opts = {
            # restrict to objects in the configured pidspace
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        }

        # translate non-blank fields from the form to search terms
        for field, val in self.cleaned_data.iteritems():
            # skip display-formatting fields
            if field in self.display_output_fields:
                continue

            # Solr does not allow wildcards at the beginning of a field search
            # TODO: could this be handled as form field validation/cleaning?
            cleaned_val = val.lstrip('*?')
            if val != cleaned_val:
                # if request was passed in, warn about leading wildcards
                if request:
                    msg = 'Text fields can\'t start with wildcards.'
                    if not cleaned_val:
                        messages.info(request, 'Ignoring search term "%s": %s' % (val, msg))
                    else:
                        messages.info(request, 'Searching for "%s" instead of "%s": %s' %
                                      (cleaned_val, val, msg))
                # update the value that will be used for searching
                self.cleaned_data[field] = val = cleaned_val

            # skip blank fields (after solr wildcard clean-up)
            if not val:
                continue


            # handle fields that need special logic
            if field == 'pid':
                # pid search field can now be object pid OR dm id
                # if the search string is purely numeric, it must be a dm1 id
                if val.isnumeric():
                    search_opts['dm1_id'] = val
                    # otherwise, search on fedora object pid
                else:
                    search_opts['pid'] = val
                    # add a wildcard if the search pid is the initial value
                    if val == self.fields['pid'].initial:
                        search_opts['pid'] += '*'

            # collection objects are indexed as collection_id in solr
            elif field in ['collection', 'simpleCollection']:
                search_opts['%s_id' % field] = val

            # all other fields: solr search field = form field
            else:
                search_opts[field] = val

        return search_opts


    def search_info(self):
        '''Generate a dictionary of search field and terms in a format
        that can be displayed to a user on the search results page.'''

        # don't do anything if the form isn't valid
        if not self.is_valid():
            return

        search_info = {}
        for field, val in self.cleaned_data.iteritems():
            if field in self.display_output_fields:
                # do not show display-formatting field values with search terms
                continue
                            
            key = self.fields[field].label  # use form display label when available
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field
            if val:     # if search value is not empty, selectively add it
                # for collections get collection object info
                if field == 'collection':
                    search_info[key] = CollectionObject.find_by_pid(val)
                elif field == 'access_code':         # for rights, numeric code + abbreviation
                    search_info[key] = '%s - %s' % (val, Rights.access_terms_dict[val].abbreviation)
                elif field == "content_model":
                    search_info[key] = dict(self.format_options)[val]
                elif field == "simpleCollection":
                    search_info[key] = SimpleCollection.find_by_pid(val)
                elif val != self.fields[field].initial:     # ignore default values
                    search_info[key] = val

        return search_info
