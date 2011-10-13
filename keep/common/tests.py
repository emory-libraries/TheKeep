import logging
from os import path
from mock import Mock, MagicMock, patch
from sunburnt import sunburnt

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from eulfedora.models import XmlDatastream

from keep import mods
from keep.audio import models as audiomodels
from keep.collection.fixtures import FedoraFixtures
from keep.common.fedora import DigitalObject, LocalMODS, Repository
from keep.common.models import _DirPart, FileMasterTech, FileMasterTech_Base
from keep.common.utils import absolutize_url, md5sum
from keep.common.utils import PaginatedSolrSearch
from keep.testutil import KeepTestCase

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}


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
        self.obj.file_master.content.file.append(FileMasterTech_Base())
        self.obj.file_master.content.file[0].computer = "MyTestComputer"
        self.obj.file_master.content.file[0].path = "/path/to/some/file"


    def test_dirparts(self):
        parts = list(self.obj.file_master.content.file[0].dir_parts())
        self.assertEqual(unicode(parts[0]), 'path')
        self.assertEqual(unicode(parts[1]), 'to')
        self.assertEqual(unicode(parts[2]), 'some')


    def test_name(self):
        self.assertEqual(self.obj.file_master.content.file[0].name(), 'file')




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

# mock archives used to generate archives choices for form field
@patch('keep.collection.forms.CollectionObject.archives',
       new=Mock(return_value=FedoraFixtures.archives(format=dict)))

class SearchTest(KeepTestCase):
    fixtures =  ['users']

    client = Client()

    # set up a mock solr object for use in solr-based find methods
    mocksolr = MagicMock(sunburnt.SolrInterface)
    mocksolr.return_value = mocksolr
    # solr interface has a fluent interface where queries and filters
    # return another solr query object; simulate that as simply as possible
    mocksolr.query.return_value = mocksolr.query
    mocksolr.query.query.return_value = mocksolr.query
    mocksolr.query.paginate.return_value = mocksolr.query
    mocksolr.query.exclude.return_value = mocksolr.query
    mocksolr.query.__or__.return_value = mocksolr.query
    mocksolr.query.filter.return_value = mocksolr.query
    mocksolr.Q.return_value = mocksolr.query
    mocksolrpaginator = MagicMock(PaginatedSolrSearch)

    @patch('keep.common.views.sunburnt.SolrInterface', mocksolr)
    @patch('keep.common.views.PaginatedSolrSearch', new=Mock(return_value=mocksolrpaginator))
    @patch('keep.common.forms.CollectionObject')
    def test_search(self, mockcollobj):
        collections = [
            {'pid': 'pid:1', 'source_id': 1, 'title': 'mss 1'}
            ]
        mockcollobj.item_collections.return_value = collections

        search_url = reverse('common:search')

        # using a mock for sunburnt so we can inspect method calls,
        # simulate search results, etc.

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        self.mocksolrpaginator.count.return_value = 0
        self.mocksolrpaginator.__getitem__.return_value = None

        # search all items (no user-entered search terms)
        response = self.client.get(search_url)
        args, kwargs = self.mocksolr.query.call_args
        # default search args that should be included on every collection search
        self.assertEqual('%s:*' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'item search should be filtered by configured pidspace')
        # by default, results should be sorted most recently created
        self.mocksolr.query.sort_by.called_with('-created')

        # search by exact pid
        searchpid = 'pid:1'
        response = self.client.get(search_url, {'audio-pid': searchpid})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(searchpid, kwargs['pid'],
                         'item search should be filtered by pid')

        # search by DM id
        dm1_id = 20
        response = self.client.get(search_url, {'audio-pid': dm1_id})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(str(dm1_id), kwargs['dm1_id'],
                         'pid search for numeric dm1 id should search dm1_id field')
        self.assertNotEqual(str(dm1_id), kwargs['pid'],
                         'pid search for numeric dm1 id should NOT search pid field')
        # search by DM other id
        other_id =  '00000930'
        response = self.client.get(search_url, {'audio-pid': other_id})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(other_id, kwargs['dm1_id'],
                         'pid search for numeric other id should search dm1_id field')
        self.assertNotEqual(other_id, kwargs['pid'],
                         'pid search for numeric dm1 other id should NOT search pid field')

        # search by title phrase
        title_search = 'manuscript collection'
        response = self.client.get(search_url, {'audio-title': title_search})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(title_search, kwargs['title'],
                         'title search should filter on title field')
        self.assertPattern('title:.*%s' % title_search, response.content,
            msg_prefix='search results page should include search term (title)')
        self.assertNotContains(response, 'pid: ',
            msg_prefix='search results page should not include default search terms (pid)')
        self.assertNotContains(response, 'description: ',
            msg_prefix='search results page should not include empty search terms (description)')


        # search by note
        # (searches general note, digitization purpose, related files via solr copyfield)
        note = 'patron request'
        response = self.client.get(search_url, {'audio-notes': note})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(note, kwargs['notes'],
                         'notes search should search solr note field')

        self.assertPattern('notes:.*%s' % note, response.content,
            msg_prefix='search results page should include search term (note)')

        # search by date
        searchdate = '1492*'
        response = self.client.get(search_url, {'audio-date': searchdate})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(searchdate, kwargs['date'],
                         'date search should filter on date field')
        self.assertPattern('date:.*%s' % searchdate, response.content,
            msg_prefix='search results page should include search term (date)')

        # search by rights / access status
        access_code = '8'
        response = self.client.get(search_url, {'audio-access_code': access_code})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(access_code, kwargs['access_code'],
                         'rights/access status search should filter on access_code field')
        self.assertPattern('Rights:.*%s - Public Domain' % access_code, response.content,
            msg_prefix='search results page should include access status code and text)')

        # serch for NO Rights / Verdict
        access_code = '0'
        response = self.client.get(search_url, {'audio-access_code': access_code})
        args, kwargs = self.mocksolr.query.call_args
        self.assertTrue("access_code" not in kwargs,
                         'access_code field should NOT be in kwargs')
        args, kwargs = self.mocksolr.query.exclude.call_args
        self.assertEqual(kwargs["access_code__any"], True, "Any item with an access code should be excluded")

        # serch for format
        content_model = audiomodels.AudioObject.AUDIO_CONTENT_MODEL
        response = self.client.get(search_url, {'audio-content_model' : content_model})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(content_model, kwargs['content_model'])

        # collection
        collpid = '%s:1' % settings.FEDORA_PIDSPACE
        coll_info = {'pid': collpid, 'source_id': '1', 'title': 'Papers of Somebody Important'}
        colluri = 'info:fedora/%s' % collpid
        # modify item_collections so test pid will be in the form choice list
        mockcollobj.item_collections.return_value = [coll_info]
        # mock collection find by pid in the view for collection label look-up
        with patch('keep.audio.views.CollectionObject.find_by_pid', new=Mock(return_value=coll_info)):
            response = self.client.get(search_url, {'audio-collection':  colluri})
            args, kwargs = self.mocksolr.query.call_args
            self.assertEqual(colluri, kwargs['collection_id'],
                'collection search should filter on collection_id field')
            self.assertPattern('Collection:.*%s' % coll_info['title'], response.content,
                msg_prefix='search results page should include search term (collection by name)')

        # multiple fields
        # mock collection find by pid in the view for collection label look-up
        with patch('keep.audio.views.CollectionObject.find_by_pid', new=Mock(return_value=coll_info)):
            searchtitle = 'Moldy papers'
            searchdate = '1492*'
            response = self.client.get(search_url, {'audio-collection':  colluri,
                'audio-title': searchtitle, 'audio-date': searchdate})
            args, kwargs = self.mocksolr.query.call_args
            # all field should be in solr search
            self.assertEqual(colluri, kwargs['collection_id'])
            self.assertEqual(searchtitle, kwargs['title'])
            self.assertEqual(searchdate, kwargs['date'])
            # all fields should display to user
            self.assertPattern('Collection:.*%s' % coll_info['title'], response.content,
                msg_prefix='search results page should include all search terms used (collection)')
            self.assertPattern('date:.*%s' % searchdate, response.content,
                msg_prefix='search results page should include all search terms used (date)')
            self.assertPattern('title:.*%s' % searchtitle, response.content,
                msg_prefix='search results page should include all search terms used (title)')
