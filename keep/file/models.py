import os

from django.db import models
from eulcm.xmlmap.boda import Rights
from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods

from keep.common.fedora import DigitalObject, LocalMODS, Repository
from keep.collection.models import CollectionObject


##
## Fedora DiskImage
##

class DiskImage(DigitalObject):
    '''Fedora object for Disk Images.  Extends :class:`~keep.common.fedora.DigitalObject`.
    '''

    # NOTE about datastream naming conventions
    # Where a corresponding datastream id already exists within the Keep
    # (i.e. MODS for mods metadata), the same datastream id will be used
    # Where a Keep datastream id does not already exist, following
    # Hydra content model conventions, based on generic simple Hydra content model
    # For documentation on Hydra content models, see:
    #   https://wiki.duraspace.org/display/hydra/Hydra+objects%2C+content+models+%28cModels%29+and+disseminators
    #   https://wiki.duraspace.org/display/hydra/Hydra+objects%2C+content+models+%28cModels%29+and+disseminators#Hydraobjects%2Ccontentmodels%28cModels%29anddisseminators-genericContent

    DISKIMAGE_CONTENT_MODEL = 'info:fedora/emory-control:DiskImage-1.0'
    CONTENT_MODELS = [DISKIMAGE_CONTENT_MODEL]
    NEW_OBJECT_VIEW = 'file:view'

    allowed_mimetypes = ['', 'application/octet-stream']
    # once magic files are fixed, should be:
    # application/x-aff, application/x-ad1
    # NOTE: '' required for javascript, because browser does not detect
    # any mimetype at all


    collection = Relation(relsext.isMemberOfCollection, type=CollectionObject)
    ''':class:`~keep.collection.models.CollectionObject that this object belongs to,
    via `isMemberOfCollection` relation.
    '''

    mods = XmlDatastream("MODS", "MODS Metadata", LocalMODS, defaults={
                         'control_group': 'M',
                         'format': mods.MODS_NAMESPACE,
                         'versionable': True,
                         })
    '''descriptive metadata as MODS - :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`LocalMods`'''
    # note: using base local mods for now; may need to extend for disk images

    content = FileDatastream("content", "Master disk image file", defaults={
                             #'mimetype': 'audio/x-wav',
                             'versionable': True,  # ? (maybe)
                             })
    'master disk image binary content as :class:`~eulfedora.models.FileDatastream`'
    # TODO: coudl be one of several allowed mimetypes

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
                           defaults={
                               'control_group': 'M',
                               'versionable': True,
                           })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`'''

    # map datastream IDs to human-readable names for inherited history_events method
    # TODO (probably/eventually)
    # component_key = {
    #     'MODS': 'descriptive metadata',
    #     'DC': 'descriptive metadata',
    #     'Rights': 'rights metadata',
    #     'RELS-EXT': 'collection membership',  # TODO: revise when/if we add more relations
    # }

    @staticmethod
    def init_from_file(filename, initial_label=None, request=None, checksum=None):
        '''Static method to create a new :class:`DiskImage` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.

        :param filename: full path to the disk image file, as a string
        :param initial_label: optional initial label to use; if not specified,
            the base name of the specified file will be used
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param checksum: the checksum of the file being sent to fedora.
        :returns: :class:`DiskImage` initialized from the file
        '''
        if initial_label is None:
            initial_label, ext = os.path.splitext(os.path.basename(filename))

        repo = Repository(request=request)
        obj = repo.get_object(type=DiskImage)
        # set initial object label from the base filename
        obj.label = initial_label
        obj.dc.content.title = obj.label
        obj.content.content = open(filename)  # FIXME: at what point does/should this get closed?
        # Set the file checksum
        obj.content.checksum = checksum
        # Set disk image datastream label to filename
        obj.content.label = initial_label

        # descriptive/technical metadata todo

        return obj

    @models.permalink
    def get_absolute_url(self):
        'Absolute url to view this object within the site'
        return (DiskImage.NEW_OBJECT_VIEW, [str(self.pid)])



