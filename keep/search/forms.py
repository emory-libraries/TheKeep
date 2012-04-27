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
            return parse_search_terms(value)
        
    def validate(self, value):
        strval = ' '.join([v[1] if v is None else '%s:%s' % v for v in value])
        super(forms.CharField, self).validate(strval)
        for v in value:
            if v[1].startswith('*') or v[1].startswith('?'):
                raise forms.ValidationError(self.invalid)

class KeywordSearch(forms.Form):
    '''Simple search form with a single unrequired
    :class:`SolrSearchField`.'''
    # usage information with search details
    help_info = '''<p>Search across text and id fields in all content.</p>
<p>Search matches keywords by default; use quotes <b>" "</b> for exact phrases.</p>
<p>Wildcards <b>*</b> and <b>?</b> may be used anywhere except the beginning of a word.</p>
<p>Use item type (<b>collection</b>, <b>audio</b>, <b>born-digital</b>) to narrow your search.</p>
<p>Search with no terms to find all content, sorted by most recently uploaded.</p>
    '''
    keyword = SolrSearchField(required=False,
                              help_text=help_info)

