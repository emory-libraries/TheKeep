import re
from django import forms
from eulcommon.searchutil import search_terms


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
            return search_terms(value)
        
    def validate(self, value):
        super(forms.CharField, self).validate(' '.join(value))
        for v in value:
            if v.startswith('*') or v.startswith('?'):
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
        
