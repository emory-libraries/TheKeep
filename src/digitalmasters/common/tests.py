from django.contrib.sites.models import Site
from django.test import TestCase

from digitalmasters.common.utils import absolutize_url

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