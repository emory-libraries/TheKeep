.. _README:

README
======

Overview
--------

The Keep is a repository-based Django web application for managing digital
surrogates or "masters" of archival (and other) source materials.  For the first
phase of the project, The Keep is intended to handle audio materials only.

The Keep is intended to replace (eventually) the previous system that handled
some of this functionality, a Ruby-on-Rails application known as
"Digital Masters".

Components
----------

Collection
~~~~~~~~~~
Functionality for creating, editing, and searching Collection objects that are
used to aggregate item-level content, and roughly correspond (in most cases) to
a manuscript or archival collection.

Audio
~~~~~
Functionality for ingesting audio content (via single-file or batch upload) into
Fedora, editing metadata to describe the audio item, and searching across audio
items.

Accounts
~~~~~~~~
Custom login/logout functionality in support of passing user LDAP credentials
to Fedora so that objects in the repository will be accessed and updated
by the individual user rather than by a single site-wide account.
To Access MARBL materal a user will need the common | MARBL Allowed permission.
To Access Arrangement materal the user will need common | Arrangement Allowed permission
and and entry in the permit-keep-arrangement-admin.xml XACML policy.

Grant access to new / existing users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Change any Apache / firewall config that is necessary.

* Make sure the user is created in the database:

  - Check by logging in to the site and go to Admin > Users
  - If the userid does not exist, do one of the following:

      a. Go to Admin > Emory ldap user profiles and enter the USERID
         then click "Add username"
      b. run the following on the command line while in the keep
         environment::

          $ python ./manage.py inituser USERNAME

  - The user should now be in the list.

* For access to Audio only:

  * Go to Admin > Users > USERID

    - Make sure the **Active**" and the **Staff** flag is checked and
      the **Superuser** flag is NOT checked.
    - In the Permissions box make sure that *common | permissions |
      Access to MARBL material* is selected.
    - Save the user.

* For access to BoDA:

  - Go to Admin > Users > USERID
  - Make sure the **Active** and the **Staff** flag is checked and the
    **Superuser** flag is NOT checked.
  - In the Permissions box make sure that "common | permissions |
    Access to MARBL material" is selected.
  - In the Permissions box make sure that "common | permissions |
    Access to Arrangement material" is selected.
  - Save the user.
  - In Fedora go to the policies directory and then to
    thekeep-policies directory.
  - edit permit-keep-arrangement-admin.xml and add an entry for the
    USERID in the "Arrangement" section near the bottom of the file.
  - Reload policies.

Common
~~~~~~
Common code used by multiple components that does not clearly belong to a single
component is placed here.  This currently includes a customized Fedora Repository
server connection class (:class:`~keep.common.fedora.Repository`), which
has logic for accessing Fedora with the credentials of the currently-logged in
user, as well as utility methods.

System Dependencies
-------------------

The Keep requires the following network resources:

  * LDAP for user authentication
  * Fedora 3.4 with risearch enabled. It should be configured for FeSL LDAP
    authentication. Note that the localsettings.py requests Fedora user
    credentials; these are used by command line applications. Users logged
    into the web application use their own LDAP credentials when accessing
    Fedora.
  * A relational database for user and session information
  * Persistent ID manager for minting ARKs to use as object identifiers.
  * eXist-db XML database for auto-generating Fedora Collection objects
    from the corresponding EAD Finding Aids
  * RabbitMQ for brokering asynchronous tasks

-----

For more detailed information, including installation instructions and upgrade
notes, see :ref:`DEPLOYNOTES`.  For details about the features included in each release,
see :ref:`CHANGELOG`.  See :ref:`APP_MANAGEMENT` for documentation on application management steps that currently cannot be performed within the web application.


