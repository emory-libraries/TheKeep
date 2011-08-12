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

class Series_Base(mods.RelatedItem):

    uri = xmlmap.StringField('mods:identifier[@type="uri"]',
            required=False, verbose_name='URI Identifier')

    base_ark = xmlmap.StringField('mods:identifier[@type="base_ark"]',
            required=False, verbose_name='base ark target of document')

    full_id = xmlmap.StringField('mods:identifier[@type="full_id"]',
            required=False, verbose_name='full id of this node')

    short_id = xmlmap.StringField('mods:identifier[@type="short_id"]',
            required=False, verbose_name='short id of this node')

class Series2(Series_Base):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series_Base,
        required=False,
        help_text='subseries')

class Series1(Series_Base):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series2,
        required=False,
        help_text='subseries')

class ArrangementMods(mods.MODS):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series1,
        required=False,
        help_text='series')

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



