:mod:`keep` Code Documentation for The Keep
===========================================

.. automodule:: keep


Collection
----------
.. automodule:: keep.collection

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
.. autoclass:: keep.collection.management.commands.repair_arks.Command

Context Processors
^^^^^^^^^^^^^^^^^^
.. automodule:: keep.collection.context_processors
    :members:

Arrangement
-----------
.. automodule:: keep.arrangement
   :members:

Models
^^^^^^
.. automodule:: keep.arrangement.models
    :members:

Forms
^^^^^
.. automodule:: keep.arrangement.forms
    :members:

Views
^^^^^^
.. automodule:: keep.arrangement.views
    :members:

Management Commands/Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: keep.arrangement.management.commands.migrate_rushdie
    :members:

.. automodule:: keep.arrangement.management.commands.load_arrangement
    :members:


Audio
-----
.. automodule:: keep.audio
    :members:

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

.. automodule:: keep.audio.management.commands.generate_access_copy
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
.. automodule:: keep.common

Fedora
^^^^^^
.. automodule:: keep.common.fedora
    :members:

Models
^^^^^^
.. automodule:: keep.common.models
    :members:


Utilities
^^^^^^^^^
.. automodule:: keep.common.utils
    :members:


Search
------

.. automodule:: keep.search


Forms
^^^^^
.. automodule:: keep.search.forms
    :members:

Views
^^^^^^
.. automodule:: keep.search.views
    :members:

