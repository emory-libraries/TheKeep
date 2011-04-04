from django.conf import settings
from django.test import TestCase

from keep.collection.fixtures import FedoraFixtures
from keep.collection.models import CollectionObject
from keep.old_dm import models

class LocationTest(TestCase):
    marbl = models.Location(name='MARBL, Robert W. Woodruff Library, Emory University')
    eua_woodruff = models.Location(name='Emory Archives: Robert W. Woodruff Library')
    eua_healthsci = models.Location(name='Emory Archives: Woodruff Health Sciences Library')
    pitts = models.Location(name='Pitts Theology Library')
    business = models.Location(name='Goizueta Business Library')

    def setUp(self):
        # convert fixture objects into short-hand versions so we an easily identify them
        for obj in CollectionObject.top_level():
            if obj.label == 'Manuscript, Archives, and Rare Book Library':
                self.marbl_obj = obj
            elif obj.label == 'Emory University Archives':
                self.eua_obj = obj
            elif obj.label == 'Pitts Theology Library':
                self.pitts_obj = obj

    def test_corresponding_repository(self):
        self.assertEqual(self.marbl_obj.uri, self.marbl.corresponding_repository,
                         'MARBL location should correspond to MARBL Repository object')
        self.assertEqual(self.eua_obj.uri, self.eua_woodruff.corresponding_repository,
                         'EUA Woodruff location should correspond to EUA Repository Object')
        self.assertEqual(self.eua_obj.uri, self.eua_healthsci.corresponding_repository,
                         'EUA Health/Sci location should correspond to EUA Repository Object')
        self.assertEqual(self.pitts_obj.uri, self.pitts.corresponding_repository,
                         'Pitts location should correspond to Pitts Repository Object')
        self.assertEqual(None, self.business.corresponding_repository,
                         'Business library should return `None` for corresponding repository (none defined)')
        