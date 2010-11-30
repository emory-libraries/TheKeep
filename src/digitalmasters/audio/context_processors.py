from digitalmasters.audio.forms import ItemSearch

def item_search(request):
    "Template context processor: add the audio item search form to context"
    return {'item_search': ItemSearch(prefix='audio')}
