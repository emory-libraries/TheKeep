from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from eulcommon.searchutil import search_terms, pages_to_show, parse_search_terms

from keep.audio.models import AudioObject
from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject # ? simplecollection ? 
from keep.common.utils import solr_interface
from keep.search.forms import KeywordSearch

json_serializer = DjangoJSONEncoder(ensure_ascii=False, indent=2)

@staff_member_required  # FIXME: not redirecting to correct login page
def keyword_search(request):
    '''Combined keyword search across all :mod:`keep` repository
    items.
    '''
    searchform = KeywordSearch(request.GET)
    solr = solr_interface()

    ctx = {'form': searchform}
    if searchform.is_valid():
        search_terms = searchform.cleaned_data['keyword']
        terms = [t[1] for t in search_terms if t[0] is None]
        solrquery = solr.query(*terms) \
                    	.facet_by(['collection_label', 'archive_short_name',
                                   'content_model', 'object_type',
                                   'ingest_user', 'audit_trail_users'])
        for t in search_terms:
            if t[0] is not None:
                if t[0] == 'user':
                    field = 'users'
                solrquery = solrquery.query(**{field:t[1]})

        # if there are any search terms, sort by relevance and display score
        if terms:
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
                    'search_terms': terms})

            
    return render(request, 'search/results.html', ctx)


def keyword_search_suggest(request):
    term = request.GET.get('term', '')
    # if term ends with : it can't be parsed (invalid)
    term_prefix, sep, term_suffix = term.rpartition(' ')
    if term_suffix.endswith(':'):
        field = term_suffix.rstrip(':')
        prefix = ''
    else:
        # parse
        parsed_terms = parse_search_terms(term_suffix)
        field, prefix = parsed_terms[-1]

    print 'field = ', field
    if field == 'user':


        solr = solr_interface()
        facetq = solr.query().paginate(rows=0)
        # return the 15 most common terms in the requested facet field
        # with a specified prefix
        facet_field = 'users_facet'
        facetq = facetq.facet_by(facet_field, prefix=prefix,
                                           sort='count',
                                           limit=15)
        facets = facetq.execute().facet_counts.facet_fields
    
        # generate a dictionary to return via json with label (facet value
        # + count), and actual value to use
        suggestions = [{'label': '%s (%d)' % (facet, count),
                        'value': '%s %s:"%s" ' % (term_prefix, field, facet)}
                       for facet, count in facets[facet_field]
                       ]
    else:
        suggestions = []
    
    return  HttpResponse(json_serializer.encode(suggestions),
                         mimetype='application/json')
            

