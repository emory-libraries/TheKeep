import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from eulcommon.searchutil import search_terms, parse_search_terms


class SolrSearchField(forms.CharField):
    '''Extension of :class:`django.forms.CharField` with validation
    and conversion for use with Solr searching via :mod:`sunburnt`.

    Returns a list of keyword terms tokenized into words and phrases
    by :meth:`eulcommon.searchutil.search_terms`.  Validates that none
    of the tokenized search terms starts with a wildcard * or ?, since
    Solr does not handle wildcards at the beginning of search terms.
    '''

    invalid = 'Search terms may not begin with wildcards * or ?'
    
    def to_python(self, value):
        if not value:
            return []
        else:
            try:
                return parse_search_terms(value)
            except Exception:
                 raise forms.ValidationError('There was an error parsing your search: %s' \
                                             % value)
        
    def validate(self, value):
        strval = ' '.join([v[1] if v is None else '%s:%s' % v for v in value])
        super(forms.CharField, self).validate(strval)
        for v in value:
            if v[1]: # could be None if we get field: with no value
                if  v[1].startswith('*') or v[1].startswith('?'):
                    raise forms.ValidationError(self.invalid)

class KeywordSearch(forms.Form):
    '''Simple search form with a single unrequired
    :class:`SolrSearchField`.'''
    # usage information with search details
    help_info = '''<ul>
    <li>Search across text and id fields and user names in all content.</li>
    <li>Search matches keywords by default; use quotes <b>" "</b> for
        exact phrases.</li>
    <li>Wildcards <b>*</b> and <b>?</b> may be used anywhere except the
        beginning of a word.</li>
    <li>Use item type (<b>collection</b>, <b>audio</b>, <b>born-digital</b>)
        to narrow your search.</li>
    <li>Search with no terms to find all content, sorted by most
        recently uploaded.</li>
    <li>Search by <b>user:name</b> or <b>added_by:name</b> to find
        items created or modified by a specific person. Type <b>user:</b> and
        wait to see suggestions.</li>
    <li><b>Tip:</b> Use the down arrow in an empty search box to see a
        list of supported fields.</li>
    </ul>        
    '''
    keyword = SolrSearchField(required=False,
                              help_text=help_info)

    # fields that can be used in keyword search
    allowed_fields = {
        'user': 'users',
        'added_by': 'added_by',
    }
    '''Dictionary of fields that can be used via the keyword search box.
    Key is the field name users should use in the search box; corresponding
    value is the Solr field that should be searched.
    '''
    field_descriptions = {
        'user:': 'items by user (edit/create)',
        'added_by:': 'items by user (create/upload only)'
    }
    '''Description of search fields for display to user, as they
    should be used in the keyword search.'''

    facet_fields = dict([(k, '%s_facet' % v) for k,v in allowed_fields.iteritems()])
    '''Dictionary of fields that can be faceted, e.g. for
    autocomplete in keyword search.  Key is the search box field; value is
    the Solr facet field.
    '''
