from digitalmasters.collection.forms import CollectionSearch

# TODO: move to collection 
def collection_search(request):
    "Template context processor: add the collection search form to context"
    return {'collection_search': CollectionSearch()}
