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

    ':class:`SubSeries`'

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

    _collection_uri = None

'''class Title(mods.Common):
    ROOT_NAME = 'title'
    XSD_SCHEMA = mods.MODS_SCHEMA
    xmlschema = mods._mods_xmlschema

    title = xmlmap.StringField('text()')
    'text description of rights access code'

class TitleInfo(mods.Common):
    ROOT_NAME = 'titleInfo'
    XSD_SCHEMA = mods.MODS_SCHEMA
    xmlschema = mods._mods_xmlschema

    title_info = xmlmap.NodeField('mods:title', Title,
        required=False,
        help_text='title')

class RelatedItem(mods.Common):
    ROOT_NAME = 'relatedItem'
    XSD_SCHEMA = mods.MODS_SCHEMA
    xmlschema = mods._mods_xmlschema

    type = xmlmap.SchemaField('@type', 'series', required=False)
    
    title_info = xmlmap.NodeField('mods:titleInfo', TitleInfo,
        required=False,
        help_text='titleInfo')

class ArrangementMods(mods.MODS):
    subseries = xmlmap.NodeField('mods:relatedItem', RelatedItem,
        required=True,
        help_text='subseries')
    ':class:`SubSeries`'
'''



