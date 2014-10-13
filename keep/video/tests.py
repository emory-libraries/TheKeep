import os

from django.conf import settings
from django.test import TestCase
from keep.video.models import Video
from django.test.utils import override_settings

import logging

logger = logging.getLogger(__name__)



vbag = os.path.join(settings.BASE_DIR, 'video', 'fixtures', 'BRIDGES_OF_THE_SPIRIT')

class VideoTest(TestCase):

    def setUp(self):
        self.pids = []

    def tearDown(self):
        # purge any objects created by individual tests
        for pid in self.pids:
            try:
                self.repo.purge_object(pid)
                logger.info('purging %s' % pid)
            except:
                logger.info('could not purge %s' % pid)

    def test_init_from_bagit(self):
        # This also tests init_from_file and get_default_pid also

        v = Video.init_from_bagit(vbag)
        
        self.assertEqual(v.label, 'BRIDGES_OF_THE_SPIRIT')
        self.assertEqual(v.dc.content.title, 'BRIDGES_OF_THE_SPIRIT')
        self.assertEqual(v.content.checksum, '0f40632ff448aaae6d42129278139fde')
        self.assertEqual(v.content.mimetype, 'video/x-msvideo')
        self.assertEqual(v.mods.content.title, 'BRIDGES_OF_THE_SPIRIT')
        self.assertEqual(v.content.label, 'BRIDGES_OF_THE_SPIRIT')
        self.assertEqual(v.mods.content.resource_type, 'video recording')
        self.assertEqual(v.digitaltech.content.codec_quality, 'lossless')
        self.assertEqual(v.digitaltech.content.duration, 732)
        self.assertEqual(v.provenance.content.object.id_type, 'ark')
        self.assertEqual(v.provenance.content.object.id, '')
        self.assertEqual(v.provenance.content.object.type, 'p:file')
        self.assertEqual(v.provenance.content.object.composition_level, 0)
        self.assertEqual(v.provenance.content.object.checksums[0].algorithm, 'MD5')
        self.assertEqual(v.provenance.content.object.checksums[0].digest, '0f40632ff448aaae6d42129278139fde')
        self.assertEqual(v.provenance.content.object.checksums[1].algorithm, 'SHA-1')
        self.assertEqual(v.provenance.content.object.checksums[1].digest, 'f8d05442238e4ddbcde4cc9ffbfa37dc86cf74a7')
        self.assertEqual(v.provenance.content.object.format.name, 'AVI')
        self.assertEqual(v.content.ds_location, 'file://%s/data/BRIDGES_OF_THE_SPIRIT.avi' % vbag)

        self.assertEqual(v.access_copy.label, 'BRIDGES_OF_THE_SPIRIT')
        self.assertEqual(v.access_copy.checksum, '74fbf1ce0afcd91787c0f5f76f218442')
        self.assertEqual(v.access_copy.mimetype, 'video/mp4')
        self.assertEqual(v.access_copy.ds_location, 'file://%s/data/BRIDGES_OF_THE_SPIRIT.mp4' % vbag)



 




