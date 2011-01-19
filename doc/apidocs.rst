:mod:`digitalmasters` Code Documentation
========================================

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

Accounts
--------
This app adds custom login & logout views with supporting functionality to allow
accessing the repository as the user logged into the website.

Views
^^^^^^
.. automodule:: digitalmasters.accounts.views
    :members:


Common code
-----------

This is a module of common code and utility methods used by multiple apps.  It
is placed in a common module for convenience (including simplifying
running unit tests, since Django only knows how to test apps).

Fedora
^^^^^^
.. automodule:: digitalmasters.common.fedora
    :members:

MODS
^^^^
.. automodule:: digitalmasters.mods
    :members:

Utilities
^^^^^^^^^
.. automodule:: digitalmasters.common.utils
    :members:
