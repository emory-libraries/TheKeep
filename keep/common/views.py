from datetime import date
from exceptions import ValueError
from eulcommon.searchutil import pages_to_show
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.template.response import TemplateResponse

from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.video.models import Video
from keep.common import forms as commonforms
#from keep.common.models import Rights
from keep.common.utils import solr_interface
import unicodecsv


@staff_member_required
def search(request):
    '''Search for :class:`~keep.audio.models.AudioObject` or
    :class:`~keep.arrangement.models.ArrangementObject`by pid, title,
    description, collection, date, rights, etc.'''

    # if NO search terms are specified, return an advanced search page
    if not request.GET:
        return TemplateResponse(request, 'common/advanced-search.html',
                      {'searchform': commonforms.ItemSearch(prefix='audio')})

    form = commonforms.ItemSearch(request.GET, prefix='audio')

    ctx_dict = {'searchform': form}
    if form.is_valid():
        solr = solr_interface()
        # solr search options from posted data
        search_opts = form.search_options()
        # search term/value display info for user based on posted data
        ctx_dict['search_info'] = form.search_info()

        # solr query to restrict this search to appropriate content models
        cm_query = solr.Q(solr.Q(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL) \
                          | solr.Q(content_model=AudioObject.AUDIO_CONTENT_MODEL)\
                          | solr.Q(content_model=Video.VIDEO_CONTENT_MODEL))
        # for now, sort by most recently created
        solrquery = solr.query(**search_opts).filter(cm_query).sort_by('-created')


        # if user requested specific display fields, handle output display and formatting
        if form.cleaned_data['display_fields']:
            fields = form.cleaned_data['display_fields']
            # pid and content model are always needed to construct html search results
            solr_fields = fields + ['pid', 'content_model']
            solrquery = solrquery.field_limit(solr_fields)

            class FieldList(list):
                # extended list  object with pid and content model attributes
                def __init__(self, pid=None, content_model=None, values=[]):
                    super(FieldList, self).__init__(values)
                    if pid:
                        self.pid = pid
                    if content_model:
                        self.content_model = content_model
                    else:
                        self.content_model = []

            def field_list(**kwargs):
                # method to construct a custom solr result based on the requested field list
                l = FieldList(pid=kwargs.get('pid', None),
                              content_model=kwargs.get('content_model', None))
                for f in fields:
                    val = kwargs.get(f, '')
                    if solr.schema.fields[f].multi_valued:
                        val = '; '.join(val)
                    l.append(val)
                return l

            solrquery = solrquery.results_as(field_list)

            ctx_dict.update({
                'display_fields': fields,
                'display_labels': [commonforms.ItemSearch.display_field_opts[f] for f in fields]
                })

            # if CSV is requested with display_fields, return as csv before paginating

            if form.cleaned_data['output'] == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=Keep-report_%s.csv' \
                                           % date.today()
                writer = unicodecsv.writer(response)
                # write out list of field labels
                writer.writerow(ctx_dict['display_labels'])
                # then append all matching values
                # FIXME: csv output for very large results is VERY slow
                # TODO: append rows in chunks of 50-100, to handle
                # large result sets better - maybe use paginator?
                writer.writerows(solrquery)
                return response


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

        ctx_dict.update({
            'results': results.object_list,
            'page': results,
            'show_pages': show_pages,
            # pass search term query opts to view for pagination links
            'search_opts': request.GET.urlencode(),
        })

    return TemplateResponse(request, 'common/search.html', ctx_dict)
