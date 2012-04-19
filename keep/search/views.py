from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from eulcommon.searchutil import search_terms, pages_to_show

from keep.common.utils import solr_interface
from keep.search.forms import KeywordSearch

@staff_member_required
def keyword_search(request):
    searchform = KeywordSearch(request.GET)
    solr = solr_interface()

    ctx = {'form': searchform}
    if searchform.is_valid():
        keyword = searchform.cleaned_data['keyword']
        terms = search_terms(keyword)

        # search on the keyword terms and sort by recently created
        solrquery = solr.query(*terms).sort_by('-created') \
                    	.facet_by(['collection_label', 'archive_short_name',
                                   'content_model'])
        # TODO: rights access status facet (string field)
        # TODO: item type (collection, audio)
        

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
                        'search_opts': request.GET.urlencode()})
            
    return render(request, 'search/results.html', ctx)

