from digitalmasters.audio.forms import CollectionSearch

def collection_search(request):
    "Template context processor: add the collection search form to context"
    return {'collection_search': CollectionSearch()}
