from os import path
from mock import Mock, patch

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase

from eulfedora.models import XmlDatastream

from keep import mods
from keep.common.fedora import DigitalObject, LocalMODS, Repository
from keep.common.models import _DirPart, FileMasterTech
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


class Test_DirPart(TestCase):

    def  test_unicode(self):
        dir_part = _DirPart('computer', 'base', 'fileName')
        self.assertEqual('fileName', unicode(dir_part))



    def  test_path(self):
        dir_part = _DirPart('computer', 'base', 'fileName')
        self.assertEqual('/computerbasefileName/', dir_part.path())


class TestFileMasterTech(TestCase):

    def setUp(self):
        self.repo = Repository()
        self.obj = self.repo.get_object(type=Obj4Test)
        self.obj.file_master.content.computer = "MyTestComputer"
        self.obj.file_master.content.path = "/path/to/some/file"


    def test_dirparts(self):
        parts = list(self.obj.file_master.content.dir_parts())
        self.assertEqual(unicode(parts[0]), 'path')
        self.assertEqual(unicode(parts[1]), 'to')
        self.assertEqual(unicode(parts[2]), 'some')


    def test_name(self):
        self.assertEqual(self.obj.file_master.content.name(), 'file')




class Obj4Test(DigitalObject):
    file_master = XmlDatastream("FileMasterTech", "Test DS for FileMasterTech", FileMasterTech, defaults={
            'control_group': 'M',
            'versionable': True,
        })



# extend Keep DigitalObject with to test ARK init logic
class DcDigitalObject(DigitalObject):
    NEW_OBJECT_VIEW = 'audio:view'    # required for minting pid


# extend Keep DigitalObject with a MODS datastream to test ARK init logic
class ModsDigitalObject(DcDigitalObject):
    mods = XmlDatastream('MODS', 'MODS Metadata', LocalMODS, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })


class DigitalObjectTest(TestCase):
    naan = '123'
    noid = 'bcd'
    testark = 'http://p.id/ark:/%s/%s' % (naan, noid)

    @patch('keep.common.fedora.pidman')
    def test_get_default_pid(self, mockpidman):
        mockpidman.create_ark.return_value = self.testark
        
        digobj = DcDigitalObject(Mock())
        digobj.label = 'my test object'
        pid = digobj.get_default_pid()
        self.assertEqual('%s:%s' % (settings.FEDORA_PIDSPACE, self.noid), pid)
        # test/inspect mockpidman.create_ark arguments?

        # generated ARK should be stored in dc:identifier
        self.assert_(self.testark in digobj.dc.content.identifier_list)

        
    @patch('keep.common.fedora.pidman')
    def test_get_default_pid__mods(self, mockpidman):
        # mods variant
        mockpidman.create_ark.return_value = self.testark
        
        digobj = ModsDigitalObject(Mock())
        pid = digobj.get_default_pid()

        # generated ARK should be stored in MODS in two forms
        self.assertEqual(2, len(digobj.mods.content.identifiers))
        # map mods:identifier to a dictionary so we can inspect by type
        id_by_type = dict((id.type, id.text) for id in digobj.mods.content.identifiers)
        self.assertEqual('ark:/%s/%s' % (self.naan, self.noid),
            digobj.mods.content.ark,
            'short-form ARK should be stored in mods:identifier with type "ark"')
        self.assertEqual(self.testark, digobj.mods.content.ark_uri,
            'resolvable ARK should be stored in mods:identifier with type "uri"')

        # generated ark should not be stored in dc:identifier
        self.assert_(self.testark not in digobj.dc.content.identifier_list)


    def test_ark_access_uri(self):
        # dc
        dcobj = DcDigitalObject(Mock())
        # not set in dc
        self.assertEqual(None, dcobj.ark_access_uri)
        dcobj.dc.content.identifier_list.extend([
            'http://some.other/uri/foo/',
            self.testark
            ])
        self.assertEqual(self.testark, dcobj.ark_access_uri)

        # mods
        modsobj = ModsDigitalObject(Mock())
        # not set in mods
        self.assertEqual(None, modsobj.ark_access_uri)
        modsobj.mods.content.identifiers.extend([
            mods.Identifier(type='uri', text='http://yet.an/other/url'),
            mods.Identifier(type='uri', text=self.testark)
            ])
        self.assertEqual(self.testark, modsobj.ark_access_uri)
       
