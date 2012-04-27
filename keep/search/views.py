from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from eulcommon.searchutil import search_terms, pages_to_show, parse_search_terms

from keep.audio.models import AudioObject
from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject # ? simplecollection ? 
from keep.common.utils import solr_interface
from keep.search.forms import KeywordSearch

json_serializer = DjangoJSONEncoder(ensure_ascii=False, indent=2)

@login_required
def keyword_search(request):
    '''Combined keyword search across all :mod:`keep` repository
    items.
    '''
    searchform = KeywordSearch(request.GET)
    solr = solr_interface()

    ctx = {'form': searchform}
    if searchform.is_valid():
        search_terms = searchform.cleaned_data['keyword']
        # collect non-field search terms
        terms = [t[1] for t in search_terms if t[0] is None]
        solrquery = solr.query(*terms) \
                    	.facet_by(['collection_label', 'archive_short_name',
                                   'content_model', 'object_type',
                                   'ingest_user', 'audit_trail_users'])

        search_info = MultiValueDict()
        # add field-based search terms to query and search info for display
        for t in search_terms:
            field, val = t
            if field is None:  # skip non-field  terms (already handled)
                continue

            # handle unrecognized field name or incomplete term
            if val is None or field not in searchform.allowed_fields:
                # just search on the text we were given
                if val is None:
                    term = '%s:' % field
                else:
                    if ' ' in val:
                        val = "%s" % val
                    term = '%s:%s' % (field, val)
                solrquery = solrquery.query(term)
                terms.append(term)

            else:
                searchfield = searchform.allowed_fields[field]
                solrquery = solrquery.query(**{searchfield: val})
                search_info.update({field: val})

        # if there are any search terms, sort by relevance and display score
        if search_terms:
            solrquery = solrquery.sort_by('-score').field_limit(score=True)
            ctx['show_relevance'] = True
        # if no terms, sort by most recently created
        # (secondary sort when using relevance)
        solrquery = solrquery.sort_by('-created')
        
        # TODO: rights access status facet (string field)
        known_object_types = ['audio', 'collection', 'born-digital']

        paginator = Paginator(solrquery, 30)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        # calculate page links to show
        show_pages = pages_to_show(paginator, page)
        ctx.update({'page': results, 'show_pages': show_pages,
                    'known_types': known_object_types,
                    'search_opts': request.GET.urlencode(),
                    'search_terms': terms,
                    'search_info': search_info})

            
    return render(request, 'search/results.html', ctx)

@login_required
def keyword_search_suggest(request):
    '''Suggest helper for keyword search.  If the search string ends
    with a recognized field name with an optional value,
    e.g. ``user:`` or ``user:A``, looks up existing values using Solr
    facets.  Returns a JSON response with the 15 most common matching
    terms in the requested field with the search term prefix, if any.
    If the search string is empty or ends with a space, suggests
    available search fields with an explanation.

    .. Note::

        Due to the current implementation and the limitations of facet
        querying in Solr, the search term is case-sensitive and only
        matches at the beginning of the string.
    
    Return format is suitable for use with `JQuery UI Autocomplete`_
    widget.

    .. _JQuery UI Autocomplete: http://jqueryui.com/demos/autocomplete/

    :param request: the http request passed to the original view
        method (used to retrieve the search term)
    '''
    term = request.GET.get('term', '')
    
    suggestions = []

    # if term empty or ends in a space, suggest available search fields
    if term == '' or term[-1] == ' ':
        suggestions = [
            {'label': field,
             'value': '%s%s' % (term, field),
             'category': 'Search Fields',
             'desc': desc}
            for field, desc in KeywordSearch.field_descriptions.iteritems()
        ]

    # otherwise, check if there is a field to look up values for
    else:

        term_prefix, sep, term_suffix = term.rpartition(' ')
        value_prefix = term_prefix + sep
        # parse the last search term 
        try:
            # parse could error in some cases
            parsed_terms = parse_search_terms(term_suffix)
        except Exception:
            field, prefix = None, ''

        field, prefix = parsed_terms[-1]
        if prefix is None:
            prefix = ''

        # if field can be faceted, suggest terms
        if field in KeywordSearch.facet_fields.keys():
            facet_field = KeywordSearch.facet_fields[field]

            solr = solr_interface()
            facetq = solr.query().paginate(rows=0)
            # return the 15 most common terms in the requested facet field
            # with a specified prefix
            facetq = facetq.facet_by(facet_field, prefix=prefix,
                                               sort='count',
                                               limit=15)
            facets = facetq.execute().facet_counts.facet_fields

            # generate a dictionary to return via json with label (facet value
            # + count), and actual value to use
            suggestions = [{'label': '%s (%d)' % (facet, count),
                            'value': '%s%s:"%s" ' % (value_prefix, field, facet),
                            'category': 'Users'}
                           for facet, count in facets[facet_field]
                           ]
    
    return  HttpResponse(json_serializer.encode(suggestions),
                         mimetype='application/json')
            

