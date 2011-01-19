from keep.collection.forms import CollectionSearch

def collection_search(request):
    '''Template context processor: add the collection search form
    (:class:`~keep.collection.forms.CollectionSearch`) to context
    so it can be used on any page (e.g., in the site sidebar).'''
    return {'collection_search': CollectionSearch(prefix='collection')}
