from keep.audio.forms import ItemSearch

def item_search(request):
    '''Template context processor: add the audio item search form
    (:class:`~keep.audio.forms.ItemSearch`) to context
    so it can be used on any page (e.g., in the site sidebar).'''
    return {'item_search': ItemSearch(prefix='audio')}
