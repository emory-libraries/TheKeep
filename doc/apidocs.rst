:mod:`digitalmasters`
=====================

Collections
-----------
Django module for creating, editing, and searching Collection objects, which
are used to aggregate audio content.

Models
^^^^^^
.. automodule:: digitalmasters.collection.models
    :members:

Forms
^^^^^
.. automodule:: digitalmasters.collection.forms
    :members:

Views
^^^^^^
.. automodule:: digitalmasters.collection.views
    :members:

Management Commands/Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: digitalmasters.collection.management.commands.load_ead.Command
    :members:

Context Processors
^^^^^^^^^^^^^^^^^^
.. automodule:: digitalmasters.collection.context_processors
    :members:


Audio
-----
Django module for uploading audio content (either single files or in batches)
for ingest into the repository, with functionality for editing metadata, and
searching audio objects.

Models
^^^^^^
.. automodule:: digitalmasters.audio.models
    :members:

Forms
^^^^^
.. automodule:: digitalmasters.audio.forms
    :members:

Views
^^^^^^
.. automodule:: digitalmasters.audio.views
    :members:

Management Commands/Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: digitalmasters.audio.management.commands.ingest_cleanup
    :members:

Context Processors
^^^^^^^^^^^^^^^^^^
.. automodule:: digitalmasters.audio.context_processors
    :members:


Common code
-----------

.. automodule:: digitalmasters.common.models
    :members:

.. automodule:: digitalmasters.common.fedora
    :members:

.. automodule:: digitalmasters.common.utils
    :members:

.. automodule:: digitalmasters.mods
    :members:
