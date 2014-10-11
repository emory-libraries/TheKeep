import os

from django.conf import settings
from django.test import TestCase
from keep.video.models import Video
from django.test.utils import override_settings

import logging

logger = logging.getLogger(__name__)



vbag = os.path.join(settings.BASE_DIR, 'video', 'fixtures', '6452')

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
        
        self.assertEqual(v.label, '6452')
        self.assertEqual(v.dc.content.title, '6452')
        self.assertEqual(v.content.checksum, '2a21627d670bcef9e599e12b36d8c1a1')
        self.assertEqual(v.content.mimetype, 'video/mp4')
        self.assertEqual(v.mods.content.title, '6452')
        self.assertEqual(v.content.label, '6452')
        self.assertEqual(v.mods.content.resource_type, 'video recording')
        self.assertEqual(v.digitaltech.content.codec_quality, 'lossless')
        self.assertEqual(v.digitaltech.content.duration, 366)
        self.assertEqual(v.provenance.content.object.id_type, 'ark')
        self.assertEqual(v.provenance.content.object.id, '')
        self.assertEqual(v.provenance.content.object.type, 'p:file')
        self.assertEqual(v.provenance.content.object.composition_level, 0)
        self.assertEqual(v.provenance.content.object.checksums[0].algorithm, 'MD5')
        self.assertEqual(v.provenance.content.object.checksums[0].digest, '2a21627d670bcef9e599e12b36d8c1a1')
        self.assertEqual(v.provenance.content.object.checksums[1].algorithm, 'SHA-1')
        self.assertEqual(v.provenance.content.object.checksums[1].digest, '5b820424d811043e6b1fc0249564e0ef9c191592')
        self.assertEqual(v.provenance.content.object.format.name, 'MP4')
        self.assertEqual(v.content.ds_location, 'file://%s/data/6452.mp4' % vbag)

 




