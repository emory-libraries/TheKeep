from keep.search.forms import KeywordSearch

def search(request):
    '''Template context processor: add the keyword search form
    (:class:`~keep.search.forms.KeywordSearch`) to context
    so it can be used on any page (e.g., in the site sidebar).'''
    return {'keyword_search': KeywordSearch()}

