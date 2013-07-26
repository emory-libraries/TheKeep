from eulcm.xmlmap.boda import Rights
from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods

from keep.common.fedora import DigitalObject, Repository, LocalMODS
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
    # TODO:
    # NEW_OBJECT_VIEW = 'audio:view'

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

