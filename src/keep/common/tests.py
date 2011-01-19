from os import path

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase

from keep.common.utils import absolutize_url, md5sum

class TestAbsolutizeUrl(TestCase):
    site = Site.objects.get_current()

    def test_domain_only(self):
        self.site.domain = 'example.com'
        self.site.save()
        self.assertEqual('http://example.com/foo/', absolutize_url('/foo/'))

    def test_domain_with_scheme(self):
        self.site.domain = 'http://example.com'
        self.site.save()
        self.assertEqual('http://example.com/foo/', absolutize_url('/foo/'))

class TestMd5Sum(TestCase):

    def test_md5sum(self):
        # use mp3 file from audio test fixtures
        mp3_filename = path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')
        # md5 checksum
        md5 = 'b56b59c5004212b7be53fb5742823bd2'
        self.assertEqual(md5, md5sum(mp3_filename))

        # test non-existent file
        # file errors are not caught by md5sum utility method but should be passed along
        self.assertRaises(IOError, md5sum, '/not/a/real/file.foo')
