'''

This Django application provides a combined search functionality
across the various disparate Repository objects managed by the
:mod:`keep`.  Currently, this includes the following objects apps and
objects:

- :mod:`keep.audio`

  - :class:`~keep.audio.models.AudioObject`
  
- :mod:`keep.arrangement`

  - :class:`~keep.arrangement.models.ArrangementObject`
  
- :mod:`keep.collection`

  - :class:`~keep.collection.models.CollectionObject`
  - :class:`~keep.collection.models.SimpleCollection`


Steps to add a new content type to this search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. New objects should include a unique human-readable ``object_type``
   in their Solr index data, which can be used for filtering results
   and customizing the display.
2. Create a new list-view template snippet (it is recommend to extend
   ``search/snippets/list-item.html``) in the app where the object
   is defined.
3. Add the new type to the list of ``known_object_types`` in
   :class:`~keep.search.views.keyword_search` and update the search
   template to render the new list-view template snippet.
4. Add a new icon (based on ``object_type``) to ``search.css``.


'''
