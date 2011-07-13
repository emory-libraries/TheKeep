from django.db import models
from rdflib import RDF

from eulfedora.models import FileDatastream, XmlDatastream

from keep.collection.models import SimpleCollection
from keep.common.rdfns import REPO
from keep.common.fedora import DigitalObject, Repository
from keep.common.models import Rights, FileMasterTech

class Permissions(models.Model):
    class Meta:
        permissions = (
            ("marbl_allowed", "Access to MARBL collections is allowed."),
        )


class ProcessingBatch(SimpleCollection):
    def __init__(self, *args, **kwargs):
        super(ProcessingBatch, self).__init__(*args, **kwargs)

        #set RDF.type in rels_ext
        self.rels_ext.content.add((self.uri, RDF.type, REPO.ProcessingBatch))

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


