import logging
from sunburnt import sunburnt

from exceptions import ValueError
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.collection.models import CollectionObject
from keep.common import forms as commonforms
from keep.common.models import Rights
from keep.common.utils import PaginatedSolrSearch

@permission_required('is_staff')
def search(request):
    '''Search for  :class:`~keep.audio.models.AudioObject` by pid,
    title, description, collection, date, or rights.'''
    response_code = None
    form = commonforms.ItemSearch(request.GET, prefix='audio')
    ctx_dict = {'search': form}
    if form.is_valid():
        search_opts = {
            # restrict to objects in the configured pidspace
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        }

        # translate non-blank fields from the form to search terms
        for field, val in form.cleaned_data.iteritems():
            if not val:
                # skip blank fields
                continue

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

            # collection/archive objects are indexed as collection_id in solr
            elif field in ['collection', 'archive']:
                search_opts['%s_id' % field] = val

            # all other fields: solr search field = form field
            else:
                search_opts[field] = val
#               logging.info("%s=%s" % (field, val))

        # collect non-empty, non-default search terms to display to user on results page
        search_info = {}
        for field, val in form.cleaned_data.iteritems():
            key = form.fields[field].label  # use form display label when available
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field
            if val:     # if search value is not empty, selectively add it
                # for collections and archive, get collection object info
                if field in ['collection', 'archive']: # location = archive
                    search_info[key] = CollectionObject.find_by_pid(val)
                elif field == 'access_code':         # for rights, numeric code + abbreviation
                    if val != "0":
                        search_info[key] = '%s - %s' % (val, Rights.access_terms_dict[val].abbreviation)
                    else:
                        search_info[key] = '%s - %s' % ("", "No Verdict")
                elif field == "content_model":
                    search_info[key] = dict(form.format_options)[val]
                elif val != form.fields[field].initial:     # ignore default values
                    search_info[key] = val
        ctx_dict['search_info'] = search_info

        solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
        #Restrict to given content models content_models
        cm_query = solr.Q(solr.Q(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL) \
        | solr.Q(content_model=AudioObject.AUDIO_CONTENT_MODEL))


        # for now, sort by most recently created
        #Search for items with not verdict
        if search_opts.get("access_code") == "0":
            del search_opts['access_code'] # remove access_code from criteria
#           logging.info(search_opts)
            solrquery = solr.query(**search_opts).filter(cm_query).exclude(access_code__any=True).sort_by('-created')
        else:
#           logging.info(search_opts)
            solrquery = solr.query(**search_opts).filter(cm_query).sort_by('-created')

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