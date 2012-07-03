import logging
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict, SortedDict
from eulcommon.searchutil import pages_to_show, parse_search_terms
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.collection.models import SimpleCollection
from keep.common.models import Rights
from keep.common.utils import solr_interface
from keep.search.forms import KeywordSearch

logger = logging.getLogger(__name__)

json_serializer = DjangoJSONEncoder(ensure_ascii=False, indent=2)

# FIXME: should this be @permission_required("common.marbl_allowed") ?
# sets ?next=/audio/ but does not return back here

@login_required
def site_index(request):
    '''Simple site index page, with links to main functionality and
    date/month facets linking to searches for recently added items.
    '''
    today = date.today()
    month_ago = today - timedelta(days=30)
    three_months = today - timedelta(days=31 * 3)

    solr = solr_interface()

    # search for all content added in the last month
    # and return just the facets for date created
    facetq = solr.query().filter(created_date__range=(month_ago, today))  \
                .facet_by('created_date', sort='index',
                          limit=10, mincount=1) \
                .paginate(rows=0)
    facets = facetq.execute().facet_counts.facet_fields

    # reverse order and convert to datetime.date for use with naturalday
    recent_items = []
    recent_dates = facets['created_date']
    recent_dates.reverse()
    for day, count in recent_dates:
        y,m,d = day.split('-')
        recent_items.append((date(int(y),int(m),int(d)), count))

    # search for content added in the last few months
    # and return just the facets for year-month
    facetq = solr.query().filter(created_date__range=(three_months, today))  \
                .facet_by('created_month', sort='index',
                          mincount=1) \
                .paginate(rows=0)
    recent_months = facetq.execute().facet_counts.facet_fields['created_month']
    recent_months.reverse()

    return render(request, 'search/site_index.html',
                  {'recent_items': recent_items, 'recent_months': recent_months})


@login_required
def keyword_search(request):
    '''Combined keyword search across all :mod:`keep` repository
    items.
    '''
    searchform = KeywordSearch(request.GET)

    ctx = {'form': searchform}
    if searchform.is_valid():
        search_terms = searchform.cleaned_data['keyword']

        solr = solr_interface()
        # start with a default query to add filters & search terms
        q = solr.query()
        
        # separate out normal and fielded search terms in keyword search string
        # TODO: should this logic be shifted to form validation/cleaning?
        search_info = MultiValueDict()
        terms = []
        # add field-based search terms to query and search info for display
        for t in search_terms:
            field, val = t
            # add non-field terms to list of terms
            # - no field name
            if field is None:  
                terms.append(val)
            # - unrecognized field name or incomplete term
            elif val is None or field not in searchform.allowed_fields:
                # just search on the text we were given
                if val is None:
                    term = '%s:' % field
                else:
                    if ' ' in val: # assume exact phrase if quoted
                        val = "%s" % val
                    term = '%s:%s' % (field, val)
                terms.append(term)

            # field/value pair
            else:
                solr_field = searchform.allowed_fields[field]
                search_val = val
                # add wildcard to end of search dates
                # (indexed by YYYY-MM-DD; allow match on YYYY or YYYY-MM)
                if field == 'created':
                    search_val += '*'
                # add field/value search to the solr query
                q = q.query(**{solr_field: search_val})
                # add to search info for display to user
                search_info.update({field: val})

        # search on all collected search terms
        q = q.query(*terms)         

        # get a copy of current url options for pagination
        # and to generate links to remove active filters
        urlopts = request.GET.copy()

        # handle facets
        display_filters = []
        # - list of tuples: display name, link to remove the filter
        active_filters = dict((field, []) for field in
                              searchform.facet_field_names.iterkeys())
        # - dictionary of filters in use, for exclusion from displayed
        # facets
        
        # filter the solr search based on any facets in the request
        for filter, facet_field in searchform.facet_field_names.iteritems():
            # For multi-valued fields (author, subject), we could have multiple
            # filters on the same field; treat all facet fields as lists.
            for val in request.GET.getlist(filter):

                # ignore any facet if the value is not set
                if not val:
                    continue
                
                # filter the current solr query
                q = q.filter(**{facet_field: val})

                # add to list of active filters
                active_filters[filter].append(val)

                # add to list for user display & removal
                # - copy the urlopts and remove only the current value 
                unfacet_urlopts = urlopts.copy()
                val_list = unfacet_urlopts.getlist(filter)
                val_list.remove(val)
                unfacet_urlopts.setlist(filter, val_list)
                # tuple of filter display value, url to remove it
                # - add details to label when the value doesn't make it obvious
                if filter in ['added by', 'modified by']:
                    label = '%s %s' % (filter, val)
                elif filter == 'access status':
                    # use access status abbreviation instead of numeric code
                    label = Rights.access_terms_dict[val].abbreviation
                else:
                    label = val
                    
                display_filters.append((label,
                                        unfacet_urlopts.urlencode()))
        #Exclude results if user does not have correct perm
        if not request.user.has_perm('common.marbl_allowed'):
            q = q.exclude(content_model=AudioObject.AUDIO_CONTENT_MODEL)
        if not request.user.has_perm('common.arrangement_allowed'):
            q = q.exclude(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
            q = q.exclude(content_model=SimpleCollection.COLLECTION_CONTENT_MODEL)


        # Update solr query to return values & counts for the
        # configured facet fields
        q = q.facet_by(searchform.facet_field_names.values(),
                       mincount=1, limit=15, sort='count')
        # TODO: add support for missing=True for access_code

        # if there are any search terms, sort by relevance and display score
        if search_terms:
            q = q.sort_by('-score').field_limit(score=True)
            ctx['show_relevance'] = True
        # then sort by most recently created
        # (primary sort when no search terms, secondary otherwise)
        q = q.sort_by('-created')

        # list of currently known types for display in results
        known_object_types = ['audio', 'collection', 'born-digital']

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
        # calculate page links to show
        show_pages = pages_to_show(paginator, page)

        # convert the facets from the solr result for display to user
        facets = SortedDict()
        facet_fields = results.object_list.facet_counts.facet_fields
        for display_name, field in searchform.facet_field_names.iteritems():
            if field in facet_fields and facet_fields[field]:
                show_facets = []
                # skip any display facet values that are already in effect
                for val in facet_fields[field]:
                    if val[0] not in active_filters[display_name]:
                        show_facets.append(val)
                if show_facets:
                    facets[display_name] = show_facets

        ctx.update({
            'page': results,
            'show_pages': show_pages,
            'known_types': known_object_types,
            'search_opts': request.GET.urlencode(),
            'search_terms': terms,
            'search_info': search_info,
            'url_params': urlopts.urlencode(),
            'facets': facets,
            'active_filters': display_filters,
        })
            
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

    # if term is empty or ends in a space, suggest available search fields
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
            # date created is a special caes
            if field == 'created':
                sort = 'index'
                category = 'Date Added'
                # if less than 4 characters, suggest year
                if len(prefix) < 4:
                    facet_field = 'created_year'
                    result_fmt = '%s'
                # between 4 and 7, suggest year-month
                elif len(prefix) < 7:
                    facet_field = 'created_month'
                    result_fmt = '%s'
                # suggest full dates
                else:
                    result_fmt = '%s '
            else:
                sort = 'count'
                category = 'Users'
                result_fmt = '"%s" '

            solr = solr_interface()
            facetq = solr.query().paginate(rows=0)
            # return the 15 most common terms in the requested facet field
            # with a specified prefix
            facetq = facetq.facet_by(facet_field, prefix=prefix,
                                     sort=sort, limit=15)
            facets = facetq.execute().facet_counts.facet_fields

            # generate a dictionary to return via json with label (facet value
            # + count), and actual value to use
            suggestions = [{'label': '%s (%d)' % (facet, count),
                            'value': '%s%s:' % (value_prefix, field) + \
	                                        result_fmt % facet,
                            'category': category}
                           for facet, count in facets[facet_field]
                           ]
    
    return  HttpResponse(json_serializer.encode(suggestions),
                         mimetype='application/json')
            

