.. _APP_MANAGEMENT:

Application Management
**********************

Until we come up with a better solution, various application management processes will be documented here.

Purging Records from the Keep
=============================

The Keep web application does not currently support deletion, so on occasion developers may be asked to remove records (e.g., items that should not have been ingested or duplicate records).  To purge a Keep record, use the following process.

* Secure shell into the production deployed instance of the Keep, su to the keep user, and start the python console::

   $ python manage.py shell

* Initialize a repository connection to inspect and purge objects.  Retrieve the object by pid, but be sure to check the object label or other metadata to confirm it matches information provided about the object to be deleted::

   >>> from keep.common.fedora import Repository
   >>> from keep.audio.models import AudioObject
   >>> repo = Repository()
   >>> obj = repo.get_object('emory:bt0nm', type=AudioObject)
   >>> obj.label
   'record 5 side A.wav'
   >>> repo.purge_object(obj.pid, 'purge at user request - duplicate')
   True

* Update the corresponding ARK in the PID manager to mark the default target as inactive (either use the web admin and search by pid or or alternately use the Python pidman client in the django console if you are removing a large number of records).


