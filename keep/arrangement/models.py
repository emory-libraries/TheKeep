from django.db import models

from eulfedora.models import FileDatastream, XmlDatastream
from eulxml import xmlmap

from keep import mods
from keep.common.fedora import DigitalObject, Repository
from keep.common.models import Rights, FileMasterTech

class Permissions(models.Model):
    class Meta:
        permissions = (
            ("marbl_allowed", "Access to MARBL collections is allowed."),
        )

class ArrangementMods(mods.MODS):
    subseries = xmlmap.NodeField('mods:relatedItem', mods.RelatedItem,
        required=True,
        help_text='subseries')

class ArrangementObject(DigitalObject):
    ARRANGEMENT_CONTENT_MODEL = 'info:fedora/emory-control:Arrangement-1.0'
    CONTENT_MODELS = [ ARRANGEMENT_CONTENT_MODEL ]
    NEW_OBJECT_VIEW = 'arrangement:index'

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`'''

    filetech = XmlDatastream("FileMasterTech", "File Technical Metadata", FileMasterTech ,defaults={
            'control_group': 'M',
            'versionable': True,
        })

    mods = XmlDatastream('MODS', 'MODS Metadata', ArrangementMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    'MODS :class:`~eulfedora.models.XmlDatastream` with content as :class:`ArrangementMods`'

    _collection_uri = None



