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

        solr = solr_interface()
        base_search_opts = {
            # restrict to audio items by content model
            'content_model': AudioObject.AUDIO_CONTENT_MODEL,
            # restrict to items that have an access copy available
            'has_access_copy': True,
            # restrict to items that are allowed to be accessed
            'researcher_access': True,
        }
        # FIXME: researcher access filter could be removed for staff

        # start with a default query to add filters & search terms
        q = solr.query().filter(**base_search_opts)
        if search_terms:
            q = q.query(search_terms)
            q = q.sort_by('-score').field_limit(score=True)

        # TODO: restrict to researcher-accessible only!
        # (based on logged-in perms)
        # q = q.exclude(content_model=AudioObject.AUDIO_CONTENT_MODEL)

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

        ctx.update({
            'results': results,
            'search_opts': request.GET.urlencode(),
            'search_terms': search_terms,
        })

    return render(request, 'search/results.html', ctx)


