from keep.repoadmin.forms import KeywordSearch

def search(request):
    '''Template context processor: add the keyword search form
    (:class:`~keep.repoadmin.forms.KeywordSearch`) to context
    so it can be used on any page (e.g., in the site sidebar).'''
    return {'admin_search': KeywordSearch()}

