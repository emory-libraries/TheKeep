import logging
from sunburnt import sunburnt

from exceptions import ValueError
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.collection.models import CollectionObject, SimpleCollection
from keep.common import forms as commonforms
from keep.common.models import Rights
from keep.common.utils import PaginatedSolrSearch

@staff_member_required
def search(request):
    '''Search for  :class:`~keep.audio.models.AudioObject`  or :class:`~keep.arrangement.models.ArrangementObject`by pid,
    title, description, collection, date, or rights.'''
    response_code = None
    form = commonforms.ItemSearch(request.GET, prefix='audio')
    ctx_dict = {'search': form}
    if form.is_valid():
        solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
        search_opts = {
            # restrict to objects in the configured pidspace
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        }

        # translate non-blank fields from the form to search terms
        for field, val in form.cleaned_data.iteritems():
            if not val:
                # skip blank fields
                continue

            extra_solr_cleaned = val.lstrip('*?')
            if val != extra_solr_cleaned:
                if not extra_solr_cleaned:
                    messages.info(request, 'Ignoring search term "%s": Text fields can\'t start with wildcards.' % (val,))
                    form.cleaned_data[field] = ''
                    continue

                messages.info(request, 'Searching for "%s" instead of "%s": Text fields can\'t start with wildcards.' %
                              (extra_solr_cleaned, val))
                val = extra_solr_cleaned
                form.cleaned_data[field] = val

            # handle fields that need special logic
            if field == 'pid':
                # pid search field can now be object pid OR dm id
                # if the search string is purely numeric, it must be a dm1 id
                if val.isnumeric():
                    search_opts['dm1_id'] = val
                    # otherwise, search on fedora object pid
                else:
                    search_opts['pid'] = val
                    # add a wildcard if the search pid is the initial value
                    if val == form.fields['pid'].initial:
                        search_opts['pid'] += '*'

            # collection objects are indexed as collection_id in solr
            elif field in ['collection', 'simpleCollection']:
                search_opts['%s_id' % field] = val

            # all other fields: solr search field = form field
            else:
                search_opts[field] = val

        # collect non-empty, non-default search terms to display to user on results page
        search_info = {}
        for field, val in form.cleaned_data.iteritems():
            key = form.fields[field].label  # use form display label when available
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field
            if val:     # if search value is not empty, selectively add it
                # for collections get collection object info
                if field == 'collection':
                    search_info[key] = CollectionObject.find_by_pid(val)
                elif field == 'access_code':         # for rights, numeric code + abbreviation
                    search_info[key] = '%s - %s' % (val, Rights.access_terms_dict[val].abbreviation)
                elif field == "content_model":
                    search_info[key] = dict(form.format_options)[val]
                elif field == "simpleCollection":
                    search_info[key] = SimpleCollection.find_by_pid(val)
                elif val != form.fields[field].initial:     # ignore default values
                    search_info[key] = val
        ctx_dict['search_info'] = search_info

        #Restrict to given content models content_models
        cm_query = solr.Q(solr.Q(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL) \
        | solr.Q(content_model=AudioObject.AUDIO_CONTENT_MODEL))

        # for now, sort by most recently created

        #Search for items with not verdict
        #Remove access_code from criteria because 0 is not a valid value. Then exclude 
        #records with no access_code AKA verdict
        solrquery = solr.query(**search_opts).filter(cm_query).sort_by('-created')

        #Exclude results based on perms
        if not request.user.has_perm('common.marbl_allowed'):
            solrquery = solrquery.exclude(content_model=AudioObject.AUDIO_CONTENT_MODEL)
        if not request.user.has_perm('common.arrangement_allowed'):
            solrquery = solrquery.exclude(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL)


        # wrap the solr query in a PaginatedSolrSearch object
        # that knows how to translate between django paginator & sunburnt
        pagedsolr = PaginatedSolrSearch(solrquery)
        paginator = Paginator(pagedsolr, 30)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        ctx_dict.update({
            'results': results.object_list,
            'page': results,
            # pass search term query opts to view for pagination links
            'search_opts': request.GET.urlencode()
        })


    return render_to_response('common/search.html', ctx_dict,
        context_instance=RequestContext(request))
