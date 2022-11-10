from django.conf import settings
import logging
from datetime import date, timedelta
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDict
from collections import OrderedDict as SortedDict
from eulcommon.djangoextras.auth import user_passes_test_with_403, \
    user_passes_test_with_ajax
from eulcommon.searchutil import pages_to_show, parse_search_terms

from keep.accounts.utils import filter_by_perms
from keep.collection.forms import FindCollection
from keep.common.models import rights_access_terms_dict
from keep.common.utils import solr_interface
from keep.repoadmin.forms import KeywordSearch

logger = logging.getLogger(__name__)

json_serializer = DjangoJSONEncoder(ensure_ascii=False, indent=2)


def is_staff(user):
    return user.is_staff


@user_passes_test_with_403(is_staff)
def dashboard(request):
    '''Admin dashboard page for staff users, with links to main
    functionality and date/month facets linking to searches for
    recently added or checksummed items.
    '''
    today = date.today()
    month_ago = today - timedelta(days=30)
    three_months = today - timedelta(days=31 * 3)

    solr = solr_interface()

    # search for all content added in the last month
    # and return just the facets for date created and collection name
    # - limit of 31 to ensure we get all dates in range
    facetq = solr.query().filter(created_date__range=(month_ago, today))  \
                .facet_by('created_date', sort='index',
                          limit=31, mincount=1) \
                .facet_by('collection_label_facet', sort='count',
                          limit=10, mincount=1) \
                .paginate(rows=0)
    # filter the facet query by user permissions
    # facetq = filter_by_perms(facetq, request.user)
    facets = facetq.execute().facet_counts.facet_fields

    # reverse order and convert to datetime.date for use with naturalday
    recent_items = []
    recent_dates = facets['created_date']
    recent_dates.reverse()
    # limit to just the 10 most recent dates
    for day, count in recent_dates[:10]:
        y, m, d = day.split('-')
        recent_items.append((date(int(y), int(m), int(d)), count))

    recent_collections = facets['collection_label_facet']

    # search for content added in the last few months
    # and return just the facets for year-month
    facetq = solr.query().filter(created_date__range=(three_months, today))  \
                .facet_by('created_month', sort='index',
                          mincount=1) \
                .paginate(rows=0)
    # also filter this query by user perms
    # facetq = filter_by_perms(facetq, request.user)
    recent_month_facet = facetq.execute().facet_counts.facet_fields['created_month']
    recent_month_facet.reverse()
    recent_months = []
    for month, count in recent_month_facet:
        y, m = month.split('-')
        recent_months.append((date(int(y), int(m), 1), count))

    # search for fixity checks in the last 30 days
    facetq = solr.query().filter(last_fixity_check__range=(month_ago, today))  \
                .facet_by('last_fixity_result', mincount=1) \
                .paginate(rows=0)
    # facetq = filter_by_perms(facetq, request.user)
    facets = facetq.execute().facet_counts.facet_fields
    recent_fixity_checks = facets['last_fixity_result']

    return TemplateResponse(request, 'repoadmin/site_dashboard.html',
        {'recent_items': recent_items, 'recent_months': recent_months,
        'recent_collections': recent_collections,
        'recent_fixity_checks': recent_fixity_checks,
        'month_ago': month_ago, 'manual_url': settings.KEEP_MANUAL_URL,
        'find_collection': FindCollection()})


@user_passes_test_with_403(is_staff)
def keyword_search(request):
    '''Combined keyword search across all :mod:`keep` repository
    items.
    '''
    searchform = KeywordSearch(request.GET)
    missing_label = '[null]'

    ctx = {'form': searchform}
    if searchform.is_valid():
        search_terms = searchform.cleaned_data['keyword']

        solr = solr_interface()
        # start with a default query to add filters & search terms
        # *first* filter to restrict to content models user has permission to view
        # q = filter_by_perms(solr.query(), request.user)
        q = solr.query()

        # optional date filter for fixity check
        fixity_check_mindate = searchform.cleaned_data.get('fixity_check_mindate', None)
        if fixity_check_mindate:
            today = date.today()
            q = q.query(last_fixity_check__range=(fixity_check_mindate, today))

        # use solr grouping queries to cluster original and migrated objects
        # if they appear in the same search result set
        q = q.group_by('original_pid', limit=5, sort='created desc', format='simple')

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
                    if ' ' in val:  # assume exact phrase if quoted
                        val = "%s" % val
                    term = '%s:%s' % (field, val)
                terms.append(term)

            # field/value pair
            else:
                solr_field = searchform.allowed_fields[field]
                search_val = val
                # special case for searching for collection source id
                if field == 'coll' and search_val and search_val.isdigit():
                    solr_field = 'collection_source_id'
                # add wildcard to end of search dates
                # (indexed by YYYY-MM-DD; allow match on YYYY or YYYY-MM)
                if field == 'created':
                    search_val += '*'
                # add field/value search to the solr query
                q = q.query(**{solr_field: search_val})
                # add to search info for display to user
                field = 'collection' if field == 'coll' else field
                search_info.update({field: val})

        # search on all collected search terms
        q = q.query(*terms)
        # FIXME: there should be a way to exclude these by type
        # Exclude archival collection (Top-level library)
        for p in settings.PID_ALIASES.values():
            q = q.exclude(pid=p)

        # get a copy of current url options for pagination
        # and to generate links to remove active filters
        urlopts = request.GET.copy()

        # handle facets
        display_filters = []
        # - list of tuples: display name, link to remove the filter
        active_filters = dict((field, []) for field in
                              searchform.facet_field_names.keys())
        # - dictionary of filters in use, for exclusion from displayed
        # facets

        # filter the solr search based on any facets in the request
        for filter_val, facet_field in searchform.facet_field_names.items():
            # For multi-valued fields (author, subject), we could have multiple
            # filters on the same field; treat all facet fields as lists.
            for val in request.GET.getlist(filter_val):

                # ignore any facet if the value is not set
                if not val:
                    continue

                # special case: search for items without a field
                if val == missing_label:
                    q = q.exclude(**{'%s__any' % facet_field: True})

                else:
                    # filter the current solr query
                    q = q.filter(**{facet_field: val})

                # add to list of active filters
                active_filters[filter_val].append(val)

                # add to list for user display & removal
                # - copy the urlopts and remove only the current value
                unfacet_urlopts = urlopts.copy()
                val_list = unfacet_urlopts.getlist(filter_val)
                val_list.remove(val)
                unfacet_urlopts.setlist(filter_val, val_list)
                # tuple of filter display value, url to remove it
                # - add details to label when the value doesn't make it obvious
                if filter_val in ['added by', 'modified by']:
                    label = '%s %s' % (filter_val, val)
                elif filter_val == 'fixity_check':
                    label = 'fixity check: %s' % 'valid' if val == 'pass' else 'invalid'
                elif val == missing_label:
                    label = '%s: null' % filter_val
                elif filter_val == 'access status':
                    # use access status abbreviation instead of numeric code
                    label = rights_access_terms_dict[val].abbreviation
                else:
                    label = val

                display_filters.append((label,
                                        unfacet_urlopts.urlencode()))

        # Update solr query to return values & counts for the
        # configured facet fields
        q = q.facet_by(searchform.facet_field_names.values(),
                       mincount=1, limit=15, sort='count',
                       missing=True)
        # NOTE: missing true displays count for items without any value
        # for the facet field (e.g., no access code set)

        # if there are any *keyword* terms, sort by relevance and display score
        # (for fielded search terms, items will either match or not, so relevance
        # is not as useful)
        if terms:
            # NOTE: possibly a change in sunburnt?
            # including score now requires specifying *all* fields that
            # should be returned
            q = q.sort_by('-score').field_limit([
                # common item information
                "object_type", "content_model", "pid", "label", "title",
                "creator", "created", "last_modified", "added_by",
                # collection
                "archive_short_name", "hasMember",
                # item
                "collection_id",
                # audio
                "part", "collection_label", "duration", "has_access_copy",
                "access_copy_mimetype", "access_copy_size", "source_id",
                # arrangement/disk image
                "simpleCollection_label", "rights", "state",
                # migrated / original
                "original_pid", "isDerivationOf", "hasDerivation",
                # format and size, used for disk images display (at least)
                "content_size", "content_format"
                ],
                score=True)
            ctx['show_relevance'] = True
        # then sort by most recently created
        # (primary sort when no search terms, secondary otherwise)
        q = q.sort_by('-created')

        # list of currently known types for display in results
        # FIXME: are these used anywhere?
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
        for display_name, field in searchform.facet_field_names.items():
            #do not display coll facet because it is redundant with the collection facet
            if display_name in ['coll', 'fixity_check']:
                continue
            if field in facet_fields and facet_fields[field]:
                show_facets = []
                # skip any display facet values that are already in effect
                for val in facet_fields[field]:
                    try:
                        if val[0] not in active_filters[display_name]:
                            show_facets.append(val)
                    except TypeError:
                        # when solr missing=True is turned on,
                        # last result is a count of items with no value
                        # for this field
                        if val is not 0 and field in searchform.show_missing_facets \
                          and missing_label not in active_filters[display_name]:
                            show_facets.append((missing_label, val))
                if show_facets:
                    facets[display_name] = show_facets

        ctx.update({
            'page': results,
            'show_pages': show_pages,
            # 'known_types': known_object_types,
            'search_opts': request.GET.urlencode(),
            'search_terms': terms,
            'search_info': search_info,
            'url_params': urlopts.urlencode(),
            'facets': facets,
            'active_filters': display_filters,
        })

    return TemplateResponse(request, 'repoadmin/results.html', ctx)


@user_passes_test_with_ajax(is_staff)
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
            for field, desc in KeywordSearch.field_descriptions.items()
        ]

    # otherwise, check if there is a field to look up values for
    else:

        term_prefix, sep, term_suffix = term.rpartition(' ')
        value_prefix = term_prefix + sep
        # parse the last search term
        try:
            # parse could error in some cases
            parsed_terms = parse_search_terms(term_suffix)
            field, prefix = parsed_terms[-1]
        except Exception:
            field, prefix = None, ''

        if prefix is None:
            prefix = ''

        # if field can be faceted, suggest terms
        if field in KeywordSearch.facet_fields.keys():
            facet_field = KeywordSearch.facet_fields[field]

            # date created is a special case
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

            elif field in ['added_by', 'user']:  # added_by or user
                sort = 'count'
                category = 'Users'
                result_fmt = '"%s" '


            # collection label
            if field == 'coll':
                sort = 'count'
                category = 'Collection'
                result_fmt = '%s '

                # if the term is numeric facet by source_id
                if prefix and prefix.isdigit():
                    facet_field = 'collection_source_id'

            solr = solr_interface()
            facetq = solr.query().paginate(rows=0)
            # filter by current user permssions
            # facetq = filter_by_perms(facetq, request.user)
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

    return HttpResponse(json_serializer.encode(suggestions),
                         content_type='application/json')


