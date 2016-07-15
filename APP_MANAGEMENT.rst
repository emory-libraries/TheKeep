.. _APP_MANAGEMENT:

Application Management
**********************

Until we come up with a better solution, various application management processes will be documented here.

Purging Records from the Keep
=============================

The Keep web application does not currently support deletion, so on occasion
developers may be asked to remove records (e.g., items that should not have
been ingested or duplicate records).  To purge a Keep record, use the
following process.

* Secure shell into the production deployed instance of the Keep, su to the
  keep user, and start the python console::

   $ python manage.py shell

* Initialize a repository connection to inspect and purge objects.  Retrieve
  the object by pid, but be sure to check the object label or other metadata
  to confirm it matches information provided about the object to be
  deleted::

   >>> from keep.common.fedora import Repository
   >>> from keep.audio.models import AudioObject
   >>> repo = Repository()
   >>> obj = repo.get_object('emory:bt0nm', type=AudioObject)
   >>> obj.label
   'record 5 side A.wav'
   >>> repo.purge_object(obj.pid, 'purge at user request - duplicate')
   True

* Update the corresponding ARK in the PID manager to mark the default target
  as inactive (either use the web admin and search by pid or or alternately
  use the Python pidman client in the django console if you are removing a
  large number of records).

Regenerating Audio Access Copies
================================

Normally The Keep will automatically generate access copies for audio
objects it ingests. Occasionally, though, this process fails or needs to be
rerun. Future versions of the web application will expose functionality for
some users to request regeneration of these access copies. In the meantime,
they can also be regenerated from the command line::

   $ python manage.py generate_access_copy <pid> <pid>

If you need to do a larger batch, or queue access copy generation for objects
based on a Fedora query or Solr search, you can also do that in the
python console like this::

  from eulfedora.server import Repository
  from keep.audio.models import AudioObject
  from keep.audio.tasks import queue_access_copy

  obj = repo.get_object(result['pid'], type=AudioObject)
  queue_access_copy(obj)




Creating a new top-level collection AKA Archive AKA Repository
==============================================================

There is no user interface for creating or managing the top-level
collections (including the MARBL, EUA, or Pitts collection objects), so
when a new one is needed it will need to be created manually.

  1. Get the full name and a short-hand name for the archive to be created.
  2. Use the PID manager to create a new ARK for the object.  The ARK target
     should be the Keep collection URL based on the short name of the library
     that you will enter later, e.g. https://keep.library.emory.edu/collections/marbl/
     or https://keep.library.emory.edu/collections/oxford/
  3. Copy one of the existing initial object fixtures (``keep/collection/fixtures/initial_objects``)
     and update the pid, full name, and short name everywhere they appear and add the new
     fixture to version control.

     3a. You may want to ingest the object in a development or staging Fedora Repository
        as a sanity check before committing to version control or creating in production.

  4. Add the new pid to the **PID_ALIASES** in :mod:`keep.settings`.
  5. Ingest the new object using ``python manage.py syncrepo`` or the
     Fedora Admin interface.  The empty collection should now be accessible
     at the collections url you created based on the short label.  (It won't show
     up in the `Collections by Library <https://keep.library.emory.edu/collections/>`_
     listing until it includes content.)  When you deploy a new release including
     a fixture, you should also document this step in the deploy notes.


.. NOTE::

  This procedure is also documented in Emory Service Now Knowledge Base
  as article KB05198.
