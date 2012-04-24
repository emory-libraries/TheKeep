from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from eulcommon.searchutil import search_terms, pages_to_show

from keep.audio.models import AudioObject
from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject # ? simplecollection ? 
from keep.common.utils import solr_interface
from keep.search.forms import KeywordSearch

@staff_member_required  # FIXME: not redirecting to correct login page
def keyword_search(request):
    '''Combined keyword search across all :mod:`keep` repository
    items.
    '''
    searchform = KeywordSearch(request.GET)
    solr = solr_interface()

    ctx = {'form': searchform}
    if searchform.is_valid():
        terms = searchform.cleaned_data['keyword']

        # search on the keyword terms and sort by relevance
        solrquery = solr.query(*terms).sort_by('-score').sort_by('-created') \
                    	.field_limit(score=True) \
                    	.facet_by(['collection_label', 'archive_short_name',
                                   'content_model', 'object_type'])

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
                    'search_opts': request.GET.urlencode()})

            
    return render(request, 'search/results.html', ctx)

