from urllib import urlencode

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from keep.audio.models import AudioObject
from keep.search.forms import SearchForm
from keep.common.utils import solr_interface

# placeholder for new public-facing site index page
def site_index(request):
    form = SearchForm()
    return render(request, 'search/site_index.html',
        {'form': form})

def search(request):
    form = SearchForm(request.GET)
    ctx = {'form': form}
    if form.is_valid():
        search_terms = form.cleaned_data['keyword']
        search_opts = form.cleaned_data
        # solr search field parses into list of tuples of field, search terms
        # this search doesn't support any field: searching yet, so just assume all are keywords
        search_terms = [v for k, v in search_terms]

        solr = solr_interface()
        base_search_opts = {
            # restrict to audio items by content model
            'content_model': AudioObject.AUDIO_CONTENT_MODEL,
            # restrict to items that have an access copy available
            'has_access_copy': True,
            # restrict to items that are allowed to be accessed
            'researcher_access': True,
        }
        # TODO: adjust researcher access filter for logged in staff
        # with additional permissions

        # start with a default query to add filters & search terms
        q = solr.query().filter(**base_search_opts)
        if search_terms:
            q = q.query(*search_terms)
            q = q.sort_by('-score').field_limit(score=True)
            # NOTE: do we want a secondary sort after score?
        else:
            q = q.sort_by('title_exact')

        # if a collection search term is specified
        if 'collection' in search_opts and search_opts['collection']:
            collection = search_opts['collection']
            # search on *either* collection name or collection number
            q = q.query(solr.Q(collection_label=collection) | solr.Q(collection_source_id=collection))

        # date search
        if search_opts.get('start_date', None) or search_opts.get('end_date', None):
            sdate = search_opts.get('start_date', None)
            edate = search_opts.get('end_date', None)
            # NOTE: needs to handle date format variation (YYYY, YYYY-MM, etc)

            if sdate is not None:
                # ensure we search on 4-digit year
                sdate = '%04d' % int(sdate)

            # convert end date to end of year in order to catch any date variants
            # within that year; e.g. 2001-12-31 will always come after 2001-04, etc
            if edate is not None:
                edate = "%04d-12-31" % int(edate)

            # single date search: start and end date should be the same;
            # using same logic as range to match any dates within that year
            # if only one of start or end is specified, results in an open range
            # i.e. anything after start date or anything before end date

            # if both values are set, use sunburnt range query
            if sdate is not None and edate is not None:
                created_q = solr.Q(date_created__range=(sdate, edate))
                issued_q = solr.Q(date_issued__range=(sdate, edate))
                # q = q.query(date__range=(sdate, edate))
            elif sdate is not None:
                # restrict by start date
                # YYYY will be before any date in that year, e.g. "2001" >= "2001-11"
                # q = q.query(date__gte='%04d' % sdate)
                created_q = solr.Q(date_created__gte=sdate)
                issued_q = solr.Q(date_issued__gte=sdate)
            elif edate is not None:
                # restrict by end date
                # q = q.query(date__lte=str(edate))
                created_q = solr.Q(date_created__lte=sdate)
                issued_q = solr.Q(date_issued__lte=sdate)

            # NOTE: explicitly search on date created or date issued,
            # to avoid complications with other values in the generic date field
            q = q.query(created_q | issued_q)

        # paginate the solr result set
        paginator = Paginator(q, 30)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        # url parameters for pagination links
        url_params = request.GET.copy()
        if 'page' in url_params:
            del url_params['page']

        ctx.update({
            'results': results,
            'search_opts': request.GET.urlencode(),
            'search_terms': search_terms,
            'url_params': urlencode(url_params)
        })

    return render(request, 'search/results.html', ctx)


