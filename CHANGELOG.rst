.. _CHANGELOG:

CHANGELOG
=========

Release 2.7.5
-------------

* Updated pidman client to the current version of requests

Release 2.7.4
-------------

* Removed Record Info section from Video edit page


Release 2.7.3
-------------

* Making changes to celery backend
* Switching to a different RabbitMQ
* changing celery task to convert from wav to mp3


Release 2.7.2
-------------

* Keep reindex errors ( premis metadata version )
* Manage command for pids that don't have matching mimetypes
* ModsrecordChangeDate is not updating when pid is updated
* mov objects are not calculating the correct mimetype
* Updated to a specific version of celery because 4.0 is failing

Release 2.7.1
-------------

* Fixing Mods Dates errors
* Keep collection generation isn't working because the repository name for the Rose Library is incorrect.
* Testkeep is producing an error message for some audio objects.
* Bags with Iso disk images cannot be ingested into the Keep.
* INC02570212 - Keep configuration change: new codec creator
* Fixing indexing issue related to provenanceMetadata


Release 2.7
-----------

* As a staff user, when I'm viewing a Rushdie object with a reassigned pid, I
  want to be able to see PREMIS metadata documenting this change so that I
  understand the provenance of the object
* As a Keep administrator, I want Rushdie pids mismatched in Pidman to be
  assigned to a new pid within the Rushdie allocation range in Pidman
* As a Keep administrator, I want a one-time update of  pidman metadata for
  Rushdie objects (label/target) where objects exist in Fedora.

Release 2.6.5
-------------

* bugfix: Fix Keep load_ead script (generate Keep collections from EAD) to work
  with latest code updates
* As a collection manager, I want to be able to create new collections from
  finding aids so that the metadata for collections is consistent
* Update to existdb 2.2
* Update to use migrated taskresult in eulcommon and remove eullocal dependency
* Set up testkeep fedora content and pidqas so pid updates can be tested
* As a Keep administrator, I want a one-time update of ARK records in the Pid
  Manager to match current titles in the Keep so that the metadata is
  consistent in the two systems
* As a collection curator, when I edit an object title in the Keep, I want the
  Pidman title to automatically update in order to have accurate/matching
  information in Pidman
* bugfix: The Pidman rest api does not find pids in subdomains when searching
  by domain (requires Pidman 1.0.3)
* Resolve an issue in which Rushdie pids in Fedora do not match Pidman -
  Report on unused PIDS and missmatches

Release 2.6.4
-------------

* bugfix: researcher access permissions to view video revisited (updated
  to use `videoperms` instead of video)
* bugfix: Audio view now checks content models and will raise a 404
  for non audio, rather than incorrectly displaying video content
* Require latest eulfedora (1.6) for debug filter and retries
* Enable new eulfedora debug filter to keep fedora auth credentials from
  being displayed in stack traces and debug emails
* Enable django-debug-toolbar for development with eulfedora panel
* Regenerate accounts migrations and remove eullocal.emory_ldap dependency

Release 2.6.3 - Video Permissions
---------------------------------

* Browser warning removed (removed UnsupportedBrowserMiddleware middleware,
  which check for supported browsers and displayed a banner; browser
  support is no longer an issue)
* Video Permissions bug
* Audio timeout error
* Improved documentation for adding top-level collections
* Documentation for queuing batch-conversion of audio

Release 2.6.2 - MacMillan Law Library
-------------------------------------

* Adds Law Libary as a top-level collection

Release 2.6.1
-------------

* As a staff user, I want to be able to find objects with no collection
  or access status set so that I can identify and fix content that has
  been uploaded but not had any metadata added.
* Bugfix for error editing objects that include empty, non-existent
  xml datastreams (actual fix in eulfedora 1.5.1)
* Bugfix: catch and report problems with MediaInfo when getting video
  duration on ingest


Release 2.6 - Migrate Large AFF Disk Images + Video Improvements
----------------------------------------------------------------

* As a researcher, I want to be able to view video in full screen mode
  so that I can see the video more easily.
* Bugfix: Improve video playback on startup and skip (now using
  streaming response and Fedora range requests)
* As a repository administrator, I can migrate large AFF master
  disk images and add metadata that reflects these changes in order
  to update obsolete file formats in the repository.

Release 2.5 - Migrate AD1/AFF Disk Images to sustainable formats
----------------------------------------------------------------

* An administrator can migrate AD1 master files to TAR files generated
  by digital archives staff and add metadata that reflects this change
  in order to update obsolete file formats in the repository.
* An administrator can migrate the format of an AFF master composite
  file and add metadata that reflects this change in order to update
  obsolete file formats in the repository.
* An archivist can download a local copy of an image file in the lab
  for processing, arrangement, and description.
* As a staff user, when I'm viewing a migrated disk image object, I want
  to be able to access the original version (including metadata) that
  was migrated, so that I understand the provenance of the object.
* As a staff user, when I'm viewing the original version of a migrated
  disk image object, I want to be able to access the migrated version
  (including metadata) so that I can get to the most recent version.
* As a staff user, I want to filter search results by disk image, email,
  other born digital files, and format so that I can restrict results to
  a specific set of content.
* As a staff user, when my search results include migrated disk images,
  I want to see the original version grouped with the migrated version
  so that I understand that the files are related and I can tell which
  one is the most recent version.
* Bugfix: Primary target URI in pid manager for new Keep objects were
  being garbled.
* Bugfix: Fix video record download original file (now using streaming
  download)

Release 2.4.2
-------------

* Bugfix: correct logic for creating ARKs via PID manager so that
  the placeholder is not url-encoded and gets replaced properly with
  the newly-minted noid.


Release 2.4.1
-------------

* Support for running celery daemon on a separate server from the
  web application; modifies audio access copy conversion file handling
  on ingest to allow for celery and audio file conversions to run
  on a seprate server from the web UI where ingest is done.

Release 2.4 - Support additional disk image mimetypes
-----------------------------------------------------

* An archivist can upload .tar, E01, and .mbox files and associated
  metadata into the Keep as a part of a bag in order to ingest
  preservation-stable file formats for disk images and composite files.
* bugfix: prevent users from double-clicking ingest when uploading files
  and ingesting the same file twice.
* bugfix: make Keep frontend external dependencies configurable to
  support restricted access researcher machines.
* Upgrade to Django 1.8
* Migrate from eullocal to django-auth-ldap for LDAP login support

Release 2.3.1
-------------
* Changes to work with fedora 3.8: work around file uri checksum bug.

Release 2.3
-----------

* As a site user I will see a Site Down page when maintenance is being
  performed on the site or or other circumstances that will cause the
  site to be temporarily unavailable so that I will have a general
  idea of when I can use the site again.
* As a site user I will see a banner that displays an informative
  message on every page of the site so that I can be informed of future
  site maintenance or other events.
* As an application administrator, I want to generate a list of pids for
  testing so that I can verify the application works with a subset of
  representative but not sensitive real data.

Release 2.2.1 - Health Sciences Library
---------------------------------------
* Added Health Sciences Library

Release 2.2 - Ye'ol DM Video
----------------------------
* Migration scripts to migrate metadata and video files fromm DM to Keep


Release 2.1.3 - Hotfix-ish Filtering for Archive Collections
------------------------------------------------------------
* Filter archive collections for search results


Release 2.1.2 - Hotfix Add ETD Library
--------------------------------------
* Added library for ETD
* Fixed bug that prevented edit button for videos from displaying in collection view.


Release 2.1.1 - Bug-Fix - Large Master Conversion
-------------------------------------------------
* Fixed problem when convert large Audio files to MP3


Release 2.1 - Researcher Video Playback
---------------------------------------
* Enabled researcher video search and playback
* Fixed issue date and creation date bug
* Fixed index bug when file size is too large


Release 2.0 - Video Ingest
--------------------------
* Added ability for video ingest, search (by staff) and editing of metadata (by staff with appropriate permissions)
* Video objects include access copy in bagit package
* Larg File Upload SFTP server permissions and structure have been reworked to allow for different types of content
* Video objects are browseable  in collection view
* Now All staff can search for all types of content but viewing and editing metadata are still restricted by perms

Release 1.10
------------

* added dc_cleanup manage command
* added link to Keep Manual on dashboard for staff members
* added ability to upload 64bit wave files

Release 1.9.2
-------------

* bugfix release: workaround for Chrome v35 or later issue in recognizing
  MP3s as playable in HTML5

Release 1.9.1
-------------

* Bug fix: cleaner jplayer syntax for specifying mp3 or m4a audio file,
  to avoid issues with some versions of Chrome

Release 1.9
-----------

* As a user (researcher and archivist) of the Keep, I can see a note when
  I first access the application that informs me what browser I should use
  in order to avoid problems when playing audio incompatible with some browsers.
* As a staff user, I can see a visual indicator in the list views (search
  results and browse pages) that indicates whether an audio item is available
  to the public so that I can quickly see which items are inaccessible to
  non-staff users.
* As a researcher, I want to see a single audio item in a format consistent
  with the search results, so that I know where to look to find the same information.
* bugfix: error when LDAP fails is not obvious (generic 500?)
* bugfix: edit field sizes are too large for Sublocation, Tape Brand/Stock,
  and Part Note.
* bugfix: Keep does not support 32bit float wav files.
* bugfix: Django admin reassigns the staff flag if the user is an LDAP
  user even if an administrator removed the flag. (note: fixed in eullocal 0.21)


Release 1.8 - Permissions overhaul, Researcher Access, and Disk image/fixity improvements
-----------------------------------------------------------------------------------------

Permissions overhaul
^^^^^^^^^^^^^^^^^^^^

* As a Keep administrator, I can assign granular permissions to groups
  and individuals so that I can manage what users can view and do within
  the site.
* As a logged in staff user, I will be redirected to the dashboard page
  after saving a new or edited record, so that I can continue my work in
  the Keep.
* As a logged in archivist, I can see the item view page for items with
  any permissions status in order to see everything that is in the Keep.
* bugfix: permissions error redirects user to login page even if already
  logged in
* bugfix: dashboard facets should be filtered by user permissions
* bugfix: disk image objects are listed in search results for audio
  curation users

Researcher access
^^^^^^^^^^^^^^^^^

* As a researcher, I want to access and search the metadata for digitized
  audio recordings in The Keep in order to find materials relevant to my
  research.
* As a researcher viewing detailed metadata about an item, I want to be
  able to listen to the associated audio recording in order to conduct
  research.
* As a researcher viewing a list of search results, I can choose any
  item to view more detailed metadata about that item in order to find
  materials relevant to my research.
* As a researcher, I want to filter results based on collection name or
  number in order to find research materials that most closely relate to
  my research.
* As a researcher, I want to browse a paginated list of collections by
  owning repository in order to see groups of content.
* As a researcher, I can search across the collections by repository and
  collection number in order to quickly find a collection when I know
  exactly what I'm looking for.
* As a logged in archivist with edit permissions, I can move from the
  view page to the edit page in order to make updates.
* As a researcher, I want to browse a paginated list of materials by
  collection from a given repository in order to access materials related
  to my research.
* As a researcher, I want to filter results based on origin date by a single
  date, before or after a given date, or a specific date range in order to
  restrict results to a specific time period.
* As a researcher searching items, I will only find collections that include
  items I am allowed to use in order to avoid wasting time browsing collections
  for materials I'm unable to access.
* As a researcher, I can only access materials when in the MARBL Reading Room
  in order to protect MARBL copyright.
* As a researcher, I want to filter results based on owning library in order
  to find materials that most closely relate to my research.
* As a researcher, when I search using the advanced search filters, the
  filters will be displayed by default on the results page so I can see the
  filters that are active.
* As a researcher, I am unable to search or see digital objects that MARBL
  administrators have not made available to me.
* As a researcher when viewing search results, I can see the most up to date
  list of materials available to me in order to view the most updated and
  accurate materials.
* As a staff user, I can see a message that indicates when a audio item is
  inaccessible to patrons along with the rights code/override that governs
  this in order to distinguish between objects available to researchers
  and those available only to staff.

Disk Image and fixity improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* A repository administrator can configure a script to periodically check
  content checksums in order to identify integrity issues so that they can
  be dealt with. (implemented in eulfedora)
* A repository administrator will receive an email notification if the system
  encounters bad or missing checksums so that they can then resolve any
  integrity issues. (implemented in eulfedora)
* A repository admin can view fixity check results for individual objects
  in the premis data stream (for objects where premis exists) in order to
  view a more detailed result and the history. (implemented in eulfedora)
* As a Keep user, when I log in I want to see on the home page a count of
  any objects that have failed a fixity check in the last 30 days and be
  able to view metadata records for those objects so that I can follow up
  and/or document as needed.
* An archivist can ingest an .iso as a disk image for preservation,
  storage, and data management when content can't be converted to AFF or AD1.
* As an archivist, I can view and edit necessary metadata fields within
  disk image Keep records so that I can manage digital assets.
* Only processing archivists in digital archives and university archives
  can view and edit metadata records to ensure the security of unprocessed
  digital archives materials.
* bugfix: disk image ingest returns a 500 error if bagit data filenames
  contain whitespace


Release 1.7.1 - streamlined large file ingest
---------------------------------------------

* bugfix: streamline disk image ingest to avoid timeout errors
  (now requires bagit input with both MD5 and SHA1 checksums; no checksums
  are calculated by the Django app during disk image ingest)


Release 1.7 - large file ingest workflow, duplicate detection
-------------------------------------------------------------

* An archivist can upload a large file and its checksum into a staging
  area, so it can be selected for ingest into the Repository without
  having to upload large files in the web interface.
* An archivist can select a file uploaded to the staging area for ingest,
  so that content too large for web upload can be ingested into the repository.
* When archivist selects an uploaded file for ingest, any supplemental
  files in bagit will be ingested and associated with disk image object
  in order to allow staff to assess and document contents of image.
* Archivist can view the supplemental file name (as file title) in the
  metadata record for the disk image and view or download the supplemental
  file, in order to review the content in the file.
* Archivist can add supplemental files (and edit file names) associated
  with an ingested composite file in order to maintain security, chain
  of custody, and appraisal information about the digital object.
* When a data curator attempts to ingest content via the Keep, they will
  receive an alert if the file is already present in the repository, so
  that staff can avoid duplicating digital objects in the Keep.

Release 1.6 - support Disk Images ingest via web upload
-------------------------------------------------------

* Updated to Django 1.5
* An archivist can upload a disk image file via the Keep web interface
  to ingest it into the repository, in order to secure and preserve the
  data and to provide archival access for triage and processing.
* After uploading a disk image file (or batch of disk image files), an
  archivist should see a list of original file names and corresponding
  checksums so that they can verify data authenticity.
* When an archivist uploads a disk image file via the Keep, record
  identifiers and other standardized fields will be automatically stored
  in the metadata record, so that an archivist does not have to enter
  them manually.
* Archivist can search and discover metadata records for ingested disk
  images so that they can view, download and/or edit disk images as part
  of processing.
* An archivist can enter minimal required metadata after upload when
  ingesting a disk image file, in order to document custodial history.
* An archivist can add and edit entries in the controlled list of
  imaging software used for disk image metadata, so that new systems can
  be added as needed.


Release 1.5.2
-------------

* Archivist can view status of process after changing the status of a
  "simple collection" in the Keep, so they can tell whether or not all
  items in the collection were updated.  (correction to previous implementation)
* bugfix: marking an object as processed via "simple collection" Keep edit
  will now leave an audit trail message
* Django 1.4 cleanup: settings & templates, cache configuration example
  in ``localsettings.py.dist``


Release 1.5.1
-------------

* Added a new Codec Creator entry for audio

Release 1.5
-----------

* A logged in user can see a checksum for binary file content on the record
  detail page (currently edit page), in order to verify file authenticity.
* A logged in user can search file content by checksum, in order to match
  ingested content with original metadata.
* A logged in user can identify email records and see high-level email
  information in Keep search results, so that email can be distinguished
  from other types of files.
* When a user clicks on an email record in the search results, they are
  taken to a brief view page so that they can see information about the
  email instead of loading the default arrangement edit form which does
  not entirely apply to email.
* A system administrator or developer can run a script to import verdict
  and series information (in a CSV file) for the processed 5300c files into
  the repository, so that verdict and series decisions do not have to be
  entered one at a time.
* A system administrator or developer can run a script to ingest 5300c email
  messages into the repository, so that email verdicts can be imported and
  email content can eventually be made accessible to researchers.
* A system administrator or developer can run a script to add item level
  content for non-email files to 5300c metadata-only records in the repository,
  so that processed file content can be made accessible to users for research
  purposes.
* A system administrator or developer can run a script to import verdict
  information from a CSV file for 5300c email messages, so that verdicts from
  messages sorted in the emulation can be applied to repository items.
* Recently added items on site home page now includes a list of collections
  with items added in the past 30 days.
* Administrative users receive notification when the number of available
  iTunes feeds changes, so that they can update the researcher kiosk.

Bug fixes:
 * Corrected item level search results link to parent collection
 * Search audio/arrangement items (old search) by collection (broken after change
   to auto-complete collection input)
 * Corrected sorting for recently added items by day (on site home page)



Release 1.4.2
-------------

* Make Archive required in the collection create and edit forms.
* Prevent the creation of collections with duplicate Source Id in the same
  Archive.


Release 1.4.1
-------------

* Correct a bug in the access link URL for downloading MP4/M4A version
  of audio items in the new combined search.
* Users can view the duration for audio items in the search display in
  HH:MM:SS format rather than in total seconds, so that duration can
  be easily understood.


Release 1.4 - search, audit trail, and collection enhancements
--------------------------------------------------------------

* A logged in user can perform a simple keyword search to quickly find
  any records in the repository that contain the relevant keywords, so
  that any type of item can be found in a single search.
* A logged in user can search for records by the user who uploaded
  them, in order to easily find records they created or items uploaded
  by a specific user.
* A logged in user can search for records by creation date, in order to
  easily find recent items or items uploaded on a specific date.
* A user can filter keyword search results by type
  (collection/audio/born-digital), collection, rights status, or
  upload user so that they can easily narrow a large result set to the
  items they are interested in.
* When ingesting a composite file or batch of files, an archivist or
  curator can enter an optional log message for auditing purposes.
* An archivist can make an optional comment when making metadata
  changes using any edit form, so that the audit trail will be a more
  useful record of changes made to an object.
* Logged in users can quickly select a collection on edit, upload and
  audo/arrangement search form by typing any part of the collection
  name or number and choosing from matching suggestions.
* An archivist or curator uploading files for ingest must associate
  them with an archival collection, so that the content is linked to
  the appropriate collection from the point of ingest.
* An archivist can view a human-readable version of the Fedora audit
  trail for an item in order to review the history of all actions on a
  file since ingest.
* When a user attempts to upload a file without choosing a collection
  they see an error message, so that they don't waste time uploading
  files without setting a required field.
* Only authorized users, within the born-digital archives group, can
  access born-digital archival objects and metadata via the combined
  search.
* Updated to use Django staticfiles app to manage static site content.
* Added support for a beta warning to be displayend in test/staging
  sites; turn on via **ENABLE_BETA_WARNING** setting.

Release 1.3
-----------

* A user browsing search results can navigate through paginated
  results by just a few pagination links, so that they can access all
  results without being overwhelmed by pagination links.
* A logged in user can use the item search form to select specific
  fields and an output mode (html or csv), in order to dynamically
  generate a report on a specific group of items.
* Updated to Django 1.3.1, Solr 3.3, httplib2 0.7.4
* 'old-dm' migration code has been removed.


Release 1.2.2
--------------

* Update to the MD5 javascript implementation: now correctly
  calculates checksums for files >2GB.

Release  1.2.1
--------------
 * Require eulfedora 0.18.1 to avoid missing checksums on XML and RDF
   datastreams.


Release  1.2 - Verdict App
--------------------------
* Branched Keep code and added arrangement app
* Added load_arrangement management command
* Added SimpleCollection in collection.models
* Moved Rights and supporting models from audio app to common app
* Added FileMasterTech class in common app
* Added function to update all ArrangementObjects based on SimpleCollection status
* Added content modle fixtures AccessAllowed.xml and AccessRestricted.xml in arrangement/initial_objects
* Added migrate_rushdie manage command
* Added ability to ItemSearch to search for Arrangements and Audio
* Added ability to Item Search to fiter by Format (contenet_model)
* Added ability to Item Search to fiter by SimpleCollection
* Updated and added xacml policies
* Updated permission checking for existing keep views and new Arrangement views
* Added settings.json.dist example fab settings file
* Changed project to use django logging insted of logging.conf style

Release 1.1.1
-------------

Fix several bugs in 1.1.0:

 * Sort collections by archive in collection browse.
 * Remove archive objects from collection browse.
 * Include appropriate collection data in audio feed entries.
 * Use eullocal templates for task package.

Release 1.1.0 - Metadata Migration
----------------------------------

Migrate all metadata for audio files from the existing Digital Masters
database to the new system so that existing users can transition to
use the new system entirely in place of the old one for audio
metadata.

* A system administrator can run a script that reads metadata from
  audio records in the old database and generates clear logs of items
  and metadata in the old system. Stakeholders can review this log to
  identify changes needed in either the source data or the processing.
* A system administrator can run the metadata log script to
  transform and migrate legacy system data into reposited metadata in
  the new system. (Logging “Dry run” functionality will still be
  available with a command-line option.)
* Metadata experts and archivists can view all migrated fields in the
  audio edit interface so that they can verify it and copy it to new
  fields.
* Users will be able to view and find migrated Audio File metadata by
  association with a Collection object, based on either the collection
  number (if location is MARBL and if an MSS collection number is
  assigned) or the location (unnumbered collections for MARBL, EU
  Archives or Oxford) in the legacy system data.
* A user can designate "trash" records in the old database that should
  not be reposited in the new system, by including the word "delete"
  (not case sensitive) in the title field. The migration script will
  not create an object to migrate metadata to, and the transaction log
  will record a special "delete" error condition.
* Users will see legacy system filename identifiers on the audio item
  edit page for migrated records (where audio files stored in the
  repository would normally be available for listening), so that they
  will be able to locate the audio files that are not yet available in
  the repository. (Note that future milestones will migrate this audio
  into the repository.)
* Archivists can use the web interface to search for migrated metadata
  using newly migrated critical file metadata.
* Researchers at the MARBL A/V kiosk see migrated records once (and
  only once) in the kiosk interface.
* A curator can select "Vendor" and "Unknown" (non-LDAP identities)
  from the list of Transfer Engineer choices.
* A curator can record correct speed metadata for digitized
  microcassettes.
* Librarians and preservation specialists can see in the legacy
  Digital Masters interface whether any particular record's metadata
  has been migrated to The Keep and into what PID for easy
  verification.

Additionally, this milestone includes updates to take advantage of
EULindexer functionality and use Solr for searching:

* Users who browse or search for collections receive their results in
  under 1 second for a faster user experience and more efficient
  workflow.
* Users who browse or search for audio items receive their results in
  under 1 second for a faster user experience and more efficient
  workflow.
* When MARBL Kiosk requests audio items feeds, it receives results in
  under 1 second, so that iTunes can harvest available items without
  timing out.


Release 1.0.4
-------------
Date: May 2011

* Update to Javascript MD5 checksum uploader code to work with the most
  recent versions of Firefox 4 and Google Chrome due to changes in
  HTML5 Blob.slice specification.


Release 1.0.3
-------------

* Update to a newer version of eulcore for revised default pid logic;
  include the object label as a pid name when generating a new ARK for
  an object pid.
* Added a log message when ingesting new audio objects so that an
  audit trail mesage will be saved in Fedora.
* Convenience short-cut search links on the home page to fixnd items
  uploaded today, yesterday, and in the current month.

Release 1.0.2
-------------

* Update to Fedora XACML policy for production environment.

.. _Release1-0:

Release 1.0 - Min Items, part IV
---------------------------------
Date: March 2011

Changes and fixes to Min items I-III that were needed for an initial production release.

* A curator will see a message, “Changes not saved,” if they attempt to save changes to a metadata record but the
  changes are not saved because of validation errors.
* When editing an audio file, drop-down selectors should default to blank, even when a nonblank selection is required.
* When a user (staff or public) downloads a file, the filename given to the downloaded file (copy of archival
  master, or derived use copy format) will be based on the "noid" part of the PID number.
* When a user searches for audio items, the “Rights” field should search the numeric rt:accessStatus/@code and should
  be called “Rights code.”
* A curator has an easy way (within a single-click or so) to find the most recently created items (new uploads) so
  that they can easily perform initial metadata on them. (Reversing the current item default search, which
  returns all items in chronological order, is expected to be an easy way to provide this.)
* The Collection metadata edit form will make field labels and field contents visually distinct to the user by use of
  different fonts, in the same way that the Audio File edit form does.
* Users creating or editing Collection metadata will not be required to add a Name element. If a Name element is
  created, adding a Role and/or Role term will be optional as well.
* A curator will have sufficient room to input and view a fairly long title for an item.
* A curator or archivist can select from revised rights access status codes (numeric),
  displayed with mnemonic abbreviations.
* A curator or archivist can add an "IP Note" field to Rights metadata.
* An archivist can over-ride an access status code that would grant access to the public to digitized file through
  the MARBL Kiosk, by selecting a checkbox in the form.  Checking the box will cause "Deny access" to appear in red
  letters next to the field.
* A curator can choose from revised selections for the Source Tech Housing field; new choices are jewel case;
  plastic container; paper sleeve; cardboard sleeve; cardboard box; other; none.
* A curator can choose from 2 additional selections for Source Technical - Reel Size: "not applicable",
  and " 4" " (four inches) and the field will no longer be required.
* A curator can choose from revised selections for Source Technical - Recording Speed: aspect term "cylinder disk"
  should be changed to "phono cylinder" in the drop-down list and in the metadata.
* A curator will no longer be required to enter metadata in the Source Technical Sublocation field.
* A curator will no longer be required to enter metadata in the Digital Technical  Digitization Purpose field.
* The Digital Technical Transfer Engineer field will no longer be a required field (until non-LDAP choices are
  available).
* Change label for Collection search result column from MSS# to Col. No., to better reflect meaning for users.
* Change label for Collection search result column from "Collection" to "Repository" to better reflect its revised
  meaning.
* In Collection search results, if there is no mods:title element (or it is empty) in a record retrieved by the
  search, users will see “(no title present)” as a hyperlink to the record,  so that they can access the record
  to add a title.
* Metadata specialists and archivists will have access to links to view MODS, DC and RELS-EXT datastreams at
  the top of the Collection metadata editing form so that they can view the XML for Collection objects.
* When a user creates a new Collection object, the object will be available within a short time (less than 2 minutes)
  in drop-down selections for the Audio Files Search by Collection and Audio Files Edit, Collection choice.
* A user can search for Audio Files by Date Uploaded in order to enable date-based report generation. The Audio Files
  input box for Date Captured should no longer appear to users, as it is no longer needed.


Release 0.9 - Min Items, part III
---------------------------------
Date: February 2011

**NOT FOR PRODUCTION RELEASE**

Digital technical metadata and rights metadata for audio items; automated
access-copy audio file generation; support for batch upload of large files.

* An authenticated user can log out of the Euterpe interface from any screen.
* A curator can use a web form to associate a digitized audio file with basic
  “stub” digital technical metadata.
* A curator can use a web form to associate a digitized audio file with basic
  “stub” rights metadata.
* When a new audio file is uploaded, the system automatically generates access
  copies in mp3 format to support kiosk access.
* Web users can listen to uploaded audio, linked from both the metadata view/edit
  views and search results.
* A researcher can use the MARBL A/V kiosk to search metadata in the system and
  listen to the audio.
* A curator can upload large files via drag & drop batch upload.
* Project rebranded as "The Keep".


Release 0.8 - Min Items, part II
--------------------------------
Date: December 2010

**NOT FOR PRODUCTION RELEASE**

Minor enhancement to search functionality, use of ARKs for Fedora object pids,
and audio items now contain source technical metadata.

* A user searching for collections by fields other than Manuscript Number will
  not have the default “MSS” in that box interfere with their search.
* The search interface contains a tool tip with documentation for
  case sensitive and wildcard searching for both collection and item search.
* Web users can search for stub records by keyword, associated manuscript
  collection, and date created.
* Web users can select file records from search results to view or edit file
  metadata.
* A curator can use a web form to associate a digitized audio file with basic
  “stub” source technical metadata.
* Web users can identify files by ARK in both the metadata view/edit views and
  search results so that they can easily reference these ARKs in external systems.
* Web users searching for files can see a count of matching records for simple
  report generation.
* Web users navigating to the collection browse page see the page load in under
  5 seconds.



Release 0.7 - Min Items, part I
-------------------------------
Date: December 2010

**NOT FOR PRODUCTION RELEASE**

Support for audio file uploads and basic descriptive metadata for for newly
digitized sound recordings.

* A curator can ingest a batch of digitized audio files so that he doesn’t
  have to pause his workflow for several minutes for each one to upload
  individually.
* When a curator ingests audio files, additional metadata is generated from
  the file’s content and stored in reposited metadata to maintain accurate
  records.
* A curator can use a web form to associate a digitized audio file with
  basic “stub” descriptive metadata.
* A system administrator deploying the application can run a script to
  create a pre-selected list of collection objects based on the
  corresponding Finding Aids EAD XML for those collections.


Release 0.6
-------------
Date: October 2010

**NOT FOR RELEASE TO PRODUCTION**

Support for basic, production-ready user interface for adding and
managing the Fedora digital collection objects that will ultimately
contain digital master items.

* An editor can create a collection object, associate it with a
  top-level collection, and enter basic initial metadata, so that the
  collection can be described and assigned objects.
* An editor can edit complete initial metadata so that the collection
  MODS can describe the full range of available metadata.
* An editor can update descriptive metadata for a collection to keep
  collection metadata up-to-date.
* An editor can search for a collection by title, manuscript number,
  creator, and top-level collection to locate one for editing or to
  check if a particular collection exists before creating it.
* An editor can view a hierarchical list of collections to locate one
  for editing or to understand the organization of collections.
* When any user creates or modifies a collection, the repository
  permanently associates that action with the user for preservation
  and auditing.
* When an editor saves changes on a collection, they can choose to
  continue editing or return to the default view.


Prototype ingest/editing
------------------------
Date: September 2010

**NOT FOR RELEASE TO PRODUCTION**

Prototype system that includes the simplest implementation of a
metadata editor interface and content ingest. This includes a simple
content model, ingest of a single sound file, and simple indexing, and
uses LDAP authentication for library staff.

* Users can log into the application with their Emory User ID so they
  can be authorized if appropriate.
* Admins can assign roles and permissions to users to maintain
  security and workflow in the application. (built-in Django
  functionality)
* Editors can upload and ingest a sound file in wave format so
  metadata can be created for the ingest item.
* Editors can add or edit metadata to an ingested sound file from a
  selected mods subset to describe the sound file.
* Editors can search ingested content by PID or Title so they can find
  an item to modify or create metadata.
* Editors can download ingested audio files for review to assist them
  in creating metadata.
* Editors receive error messages pertaining to metadata validation
  when editing records to ensure data quality and consistency.
* The application logs and displays error messages related to
  interaction with Fedora for troubleshooting and communication.
* Developers can create django forms related to XML objects to ease
  the development of editing interfaces.
* Developers can link an XML Object with an XML schema so objects can
  be validated.
