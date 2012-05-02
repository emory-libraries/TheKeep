from datetime import date, timedelta
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
        q = solr.query(*terms)         
        
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
                q = q.query(term)
                terms.append(term)

            else:
                searchfield = searchform.allowed_fields[field]
                q = q.query(**{searchfield: val})
                search_info.update({field: val})

        # filter/facet  (display name => solr field)
        # NOTE: it would be nice to facet on 'archive_short_name',
        # but currently only collections have it indexed
        field_names = {
            'collection': 'collection_label',
            'added by': 'added_by_facet',
            'modified by': 'users_facet',
            'type': 'object_type',
            'access status': 'access_code',
        }
        # url opts for pagination & basis for removing active filters
        urlopts = request.GET.copy()

        display_filters = []
        active_filters = dict((field, []) for field in field_names.iterkeys())
        # filter the solr search based on any facets in the request
        for filter, facet_field in field_names.iteritems():
            # For multi-valued fields (author, subject), we could have multiple
            # filters on the same field; treat all facet fields as lists.
            for val in request.GET.getlist(filter):
                 # filter the current solr query
                q = q.filter(**{facet_field: val})
                 
                # add to list of active filters
                active_filters[filter].append(val)
                
                # also add to list for user display & removal
                # - copy the urlopts and remove the current value 
                unfacet_urlopts = urlopts.copy()
                val_list = unfacet_urlopts.getlist(filter)
                val_list.remove(val)
                unfacet_urlopts.setlist(filter, val_list)
                # tuple of filter display value, url to remove it
                # - add filter type where value doesn't make it obvious
                label = val
                if filter in ['added by', 'modified by']:
                    label = '%s %s' % (filter, val)
                    
                display_filters.append((label,
                                        unfacet_urlopts.urlencode()))


        # TODO: display rights access code with abbreviated name
        

        # Update solr query to return values & counts for configured facet fields
        q = q.facet_by(field_names.values(), mincount=1, limit=15, sort='count')
        # TODO: add support for missing=True for access_code

        # if there are any search terms, sort by relevance and display score
        if search_terms:
            q = q.sort_by('-score').field_limit(score=True)
            ctx['show_relevance'] = True
        # if no terms, sort by most recently created
        # (secondary sort when using relevance)
        q = q.sort_by('-created')
        
        known_object_types = ['audio', 'collection', 'born-digital']

        paginator = Paginator(q, 30)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        # convert facets for display to user;
        facets = {}
        facet_fields = results.object_list.facet_counts.facet_fields
        for display_name, field in field_names.iteritems():
            if field in facet_fields and facet_fields[field]:
                show_facets = []
            # skip any display facet values that are already in effect
            for val in facet_fields[field]:
                if val[0] not in active_filters[display_name]:
                    show_facets.append(val)
                if show_facets:
                    facets[display_name] = show_facets
            

        # calculate page links to show
        show_pages = pages_to_show(paginator, page)
        ctx.update({'page': results, 'show_pages': show_pages,
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
            

