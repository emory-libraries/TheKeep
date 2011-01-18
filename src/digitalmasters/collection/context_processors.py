from digitalmasters.collection.forms import CollectionSearch

def collection_search(request):
    '''Template context processor: add the collection search form
    (:class:`~digitalmasters.collection.forms.CollectionSearch`) to context
    so it is can be used on any page (e.g., in the site sidebar).'''
    return {'collection_search': CollectionSearch(prefix='collection')}
