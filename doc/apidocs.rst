:mod:`keep` Code Documentation for The Keep
===========================================

Collections
-----------
Django module for creating, editing, and searching Collection objects, which
are used to aggregate audio content.

Models
^^^^^^
.. automodule:: keep.collection.models
    :members:

Forms
^^^^^
.. automodule:: keep.collection.forms
    :members:

Views
^^^^^^
.. automodule:: keep.collection.views
    :members:

Management Commands/Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: keep.collection.management.commands.load_ead.Command
    :members:

Context Processors
^^^^^^^^^^^^^^^^^^
.. automodule:: keep.collection.context_processors
    :members:


Audio
-----
Django module for uploading audio content (either single files or in batches)
for ingest into the repository, with functionality for editing metadata, and
searching audio objects.

Models
^^^^^^
.. automodule:: keep.audio.models
    :members:

Forms
^^^^^
.. automodule:: keep.audio.forms
    :members:

Views
^^^^^^
.. automodule:: keep.audio.views
    :members:

Management Commands/Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: keep.audio.management.commands.ingest_cleanup
    :members:

Context Processors
^^^^^^^^^^^^^^^^^^
.. automodule:: keep.audio.context_processors
    :members:

Accounts
--------
This app adds custom login & logout views with supporting functionality to allow
accessing the repository as the user logged into the website.

Views
^^^^^^
.. automodule:: keep.accounts.views
    :members:


Common code
-----------

This is a module of common code and utility methods used by multiple apps.  It
is placed in a common module for convenience (including simplifying
running unit tests, since Django only knows how to test apps).

Fedora
^^^^^^
.. automodule:: keep.common.fedora
    :members:

MODS
^^^^
.. automodule:: keep.mods
    :members:

Utilities
^^^^^^^^^
.. automodule:: keep.common.utils
    :members:
