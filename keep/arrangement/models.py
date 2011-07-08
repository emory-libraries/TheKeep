from django.db import models
from rdflib import RDF
from keep.collection.models import SimpleCollection
from keep.common.rdfns import REPO

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
