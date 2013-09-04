'''
Django module for uploading file content for ingest into the repository.

To start with, this module will only handle disk images.

Eventually, it should include functionality for editing metadata and
searching on any supported file objects.  If and where it makes sense,
logic common to all types of files should be shifted from
:mod:`keep.audio` into :mod:`keep.file`.

'''
