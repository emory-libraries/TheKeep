from django import forms
from eultheme.forms import TelephoneInput
from eulcommon.djangoextras.formfields import DynamicChoiceField

from keep.repoadmin.forms import SolrSearchField
from keep.collection.models import CollectionObject
from keep.collection.forms import archive_choices
from keep.common.utils import solr_interface




class SearchForm(forms.Form):
    '''Public-facing search form, with keyword search.

    .. Note::

       In order to display the appropriate list of libraries based on
       the current user permissions, you must pass the user at initialization
       time, i.e.::

            form = SearchForm(request.GET, user=request.user)

    '''

    keyword = SolrSearchField(required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='One or more keywords; can include (but not start with) wildcards * and ?, and exact phrases in quotes.')
    collection = forms.CharField(required=False,
        help_text='Search by collection number or words in collection name',
        widget=forms.TextInput(attrs={'placeholder':'Search by collection name or number'}))
    library = DynamicChoiceField(label="Library",  choices=archive_choices,
        initial='', required=False,
        help_text='Restrict search to materials owned by the specified library.')

    start_date = forms.IntegerField(required=False,
        help_text=''''Search by start year;  use with end date to specify a range or single year''',
        widget=TelephoneInput(attrs={'class': 'form-control', 'placeholder': 'Start year'}))
    end_date = forms.IntegerField(required=False,
        help_text='Search by end date; use with start date to specify a range or single year',
        widget=TelephoneInput(attrs={'class': 'form-control', 'placeholder': 'End year'}))

    _adv_fields = ['collection', 'library']

    @property
    def advanced_fields(self):
        'list fields that are considered part of the "advanced" search'
        return [self[f] for f in self._adv_fields]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        if 'user' in kwargs:
            del kwargs['user']
        super(SearchForm, self).__init__(*args, **kwargs)

        # if user is defined, use class method to find libraries with content
        # the user has permission to view
        if self.user is not None:
            self.fields['library'].choices = self.library_choices_by_user

    def library_choices_by_user(self):
        # this method shouldn't be set if user isn't defined, but just in case
        if not self.user:
            return archive_choices()

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

        facets = q.execute().facet_counts.facet_fields

        solr = solr_interface()
        archive_info = dict([(pid.replace('info:fedora/', ''), {'count': count})
                        for pid, count in facets['archive_id']])

        # construct a boolean pid query to match any archive pids
        # in order to lookup titles and match them to pids
        pid_q = solr.Q()
        for pid in archive_info.keys():
            pid_q |= solr.Q(pid=pid)
        query = solr.query(pid_q) \
                    .field_limit(['pid', 'title']) \
                    .sort_by('title')

        choices = [('info:fedora/%s' % a['pid'], a['title']) for a in query]
        choices.insert(0, ('', ''))   # blank option at the beginning (default)
        return choices


