from datetime import date, datetime, timedelta
from dateutil.tz import tzutc
import logging
from mock import Mock, MagicMock, patch
import os
import pytz
from sunburnt import sunburnt

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from eulfedora.models import XmlDatastream
from eulfedora.xml import AuditTrailRecord
from eulxml.xmlmap import mods

from keep.audio import models as audiomodels
from keep.collection.fixtures import FedoraFixtures
from keep.common.fedora import DigitalObject, LocalMODS, Repository, \
     AuditTrailEvent
from keep.common.forms import ItemSearch
from keep.common.models import _DirPart, FileMasterTech, FileMasterTech_Base
from keep.common.utils import absolutize_url, md5sum, solr_interface
from keep.common.templatetags import rights_extras
from keep.testutil import KeepTestCase

logger = logging.getLogger(__name__)

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
        mp3_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')
        # md5 checksum
        md5 = 'b56b59c5004212b7be53fb5742823bd2'
        self.assertEqual(md5, md5sum(mp3_filename))

        # test non-existent file
        # file errors are not caught by md5sum utility method but should be passed along
        self.assertRaises(IOError, md5sum, '/not/a/real/file.foo')


class TestSolrInterface(TestCase):

    def setUp(self):
        # save any solr settings and replace with test values
        self._solr_url = getattr(settings, 'SOLR_SERVER_URL', None)
        settings.SOLR_SERVER_URL = 'http://test.solr/'
        self._solr_ca_cert_path = getattr(settings, 'SOLR_CA_CERT_PATH', None)
        if self._solr_ca_cert_path:
            delattr(settings, 'SOLR_CA_CERT_PATH')

        self._http_proxy = os.getenv('HTTP_PROXY', None)
        del os.environ['HTTP_PROXY']

    def tearDown(self):
        # restore any solr settings
        if self._solr_url is None:
            delattr(settings, 'SOLR_SERVER_URL')
        else:
            settings.SOLR_SERVER_URL = self._solr_url
        
        if self._solr_ca_cert_path is None and hasattr(settings, 'SOLR_CA_CERT_PATH'):
            delattr(settings, 'SOLR_CA_CERT_PATH')
        else:
            settings.SOLR_CA_CERT_PATH = self._solr_ca_cert_path

        os.putenv('HTTP_PROXY', self._http_proxy)
        

    @patch('keep.common.utils.httplib2')
    @patch('keep.common.utils.sunburnt')
    def test_solr_interface(self, mocksunburnt, mockhttplib):
        # basic init with no options
        solr_interface()
        mockhttplib.Http.assert_called_once()
        # httplib2.Http should be initialized with defaults (no args)
        mockhttplib.Http.assert_called_with() 
        mocksunburnt.SolrInterface.assert_called_with(settings.SOLR_SERVER_URL,
                                                      http_connection=mockhttplib.Http.return_value)


    @patch('keep.common.utils.httplib2')
    @patch('keep.common.utils.sunburnt')
    def test_solr_interface(self, mocksunburnt, mockhttplib):
        # init with a ca cert
        settings.SOLR_CA_CERT_PATH = '/some/path/to/certs'
        solr_interface()
        # httplib should be initialized with ca_certs option
        mockhttplib.Http.assert_called_with(ca_certs=settings.SOLR_CA_CERT_PATH)


    @patch('keep.common.utils.httplib2')
    @patch('keep.common.utils.sunburnt')
    def test_solr_interface(self, mocksunburnt, mockhttplib):
        # init with an http proxy set in env
        os.environ['HTTP_PROXY'] = 'http://localhost:3128/'
        solr_interface()
        # proxy info should be configured & passed to httplib2
        mockhttplib.ProxyInfo.assert_called_with(proxy_type=mockhttplib.socks.PROXY_TYPE_HTTP_NO_TUNNEL,
                                              proxy_host='localhost', proxy_port=3128)
        mockhttplib.Http.assert_called_with(proxy_info=mockhttplib.ProxyInfo.return_value)

        # when solr url is http, no proxy should be set
        mockhttplib.reset()
        settings.SOLR_SERVER_URL = 'https://test.solr/'
        solr_interface()
        mockhttplib.ProxyInfo.assert_not_called()
        mockhttplib.Http.assert_called_with() # no args

        
        

# FIXME: why is this in keep.common instead of arrangement ?

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
        
    def test_history_events(self):
        obj = DcDigitalObject(Mock())
        with patch.object(DcDigitalObject, 'audit_trail') as mockaudit:
            # two api calls with same user + message, different components
            now = datetime.now(tz=tzutc())
            mockaudit.records = [
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='RELS-EXT'),
            ]
            # should collapse into one event
            self.assertEqual(1, len(obj.history_events()))

            # two api calls with different user
            mockaudit.records = [
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
                AuditTrailRecord(date=now, user='you', message='update',
                                 component='RELS-EXT'),
            ]
            # two different events
            self.assertEqual(2, len(obj.history_events()))

            # two api calls with same user but different message
            mockaudit.records = [
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
                AuditTrailRecord(date=now, user='me', message='change',
                                 component='RELS-EXT'),
            ]
            # two different events
            self.assertEqual(2, len(obj.history_events()))
            
            # two api calls with same user + message but repeated component
            mockaudit.records = [
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
            ]
            # two different events
            self.assertEqual(2, len(obj.history_events()))
        

            # two api calls with same user + message, different components,
            # but far enough in time they probably don't belong together
            mockaudit.records = [
                AuditTrailRecord(date=now, user='me', message='update',
                                 component='DC'),
                AuditTrailRecord(date=now + timedelta(seconds=10),
                                 user='me', message='update',
                                 component='RELS-EXT'),
            ]
            # should NOT be collapsed into one event
            self.assertEqual(2, len(obj.history_events()))


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
    mocksolr.query.sort_by.return_value = mocksolr.query
    mocksolr.query.paginate.return_value = mocksolr.query
    mocksolr.query.exclude.return_value = mocksolr.query
    mocksolr.query.__or__.return_value = mocksolr.query
    mocksolr.query.filter.return_value = mocksolr.query
    mocksolr.query.count.return_value = 0
    mocksolr.Q.return_value = mocksolr.query

    @patch('keep.common.views.solr_interface', mocksolr)
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

        # no request params at all - display advanced search form
        response = self.client.get(search_url)
        self.assertEqual('common/advanced-search.html',
            response.templates[0].name,
            'when no request parameters are given, advanced search page should be displayed')

        # no user-entered search terms - find all items 
        response = self.client.get(search_url, {'audio-title': ''})
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

        # minimal pagination test
        self.assert_('show_pages' in response.context,
                     'list of pagination pages to display should be set in response context')

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

        # search for format
        content_model = audiomodels.AudioObject.AUDIO_CONTENT_MODEL
        response = self.client.get(search_url, {'audio-content_model' : content_model})
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(content_model, kwargs['content_model'])

        # collection
        collpid = '%s:1' % settings.FEDORA_PIDSPACE
        coll_info = {'pid': collpid, 'source_id': '1', 'title': 'Papers of Somebody Important',
                     'collection_id': 'marbl:1'}
        colluri = 'info:fedora/%s' % collpid
        # modify item_collections so test pid will be in the form choice list
        mockcollobj.item_collections.return_value = [coll_info]
        # mock collection find by pid in the view for collection label look-up
        with patch('keep.common.forms.CollectionObject.find_by_pid',
                   new=Mock(return_value=coll_info)):
            response = self.client.get(search_url, {'audio-collection_0':  colluri})
            args, kwargs = self.mocksolr.query.call_args
            self.assertEqual(colluri, kwargs['collection_id'],
                'collection search should filter on collection_id field')
            self.assertPattern('collection:.*%s' % coll_info['title'], response.content,
                msg_prefix='search results page should include search term (collection by name)')

        # multiple fields
        # mock collection find by pid in the view for collection label look-up
        with patch('keep.audio.views.CollectionObject.find_by_pid',
                   new=Mock(return_value=coll_info)):
            searchtitle = 'Moldy papers'
            searchdate = '1492*'
            response = self.client.get(search_url, {'audio-collection_0':  colluri,
                'audio-title': searchtitle, 'audio-date': searchdate})
            args, kwargs = self.mocksolr.query.call_args
            # all field should be in solr search
            self.assertEqual(colluri, kwargs['collection_id'])
            self.assertEqual(searchtitle, kwargs['title'])
            self.assertEqual(searchdate, kwargs['date'])
            # all fields should display to user
            self.assertPattern('collection:.*%s' % coll_info['title'], response.content,
                msg_prefix='search results page should include all search terms used (collection)')
            self.assertPattern('date:.*%s' % searchdate, response.content,
                msg_prefix='search results page should include all search terms used (date)')
            self.assertPattern('title:.*%s' % searchtitle, response.content,
                msg_prefix='search results page should include all search terms used (title)')

    @patch('keep.common.views.solr_interface', mocksolr)
    def test_search_csv(self):
        # test advanced search with CSV output
        search_url = reverse('common:search')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        
        response = self.client.get(search_url, {'audio-display_fields': ['pid', 'title', 'description'],
                                                'audio-output': 'csv'})
        self.assertEqual('text/csv', response['Content-Type'],
                         'response should return text/csv content when csv output is requested')

        self.assert_('attachment; filename=' in response['Content-Disposition'],
                     'response should specify a default filename in content-disposition header')
        self.assert_(date.today().isoformat() in response['Content-Disposition'],
                     'default filename in content-disposition header should include current date')

        self.assertContains(response, ','.join(['PID', 'Title', 'General Note']),
                            msg_prefix='response should include human-readable column labels')

        # NOTE: not sure how to adapt solr mock to test actual
        # content, conversion to list, etc...


        # test validation - csv only valid with display fields
        response = self.client.get(search_url, {'audio-output': 'csv'})
        self.assertContains(response, 'You must select display fields for CSV output',
                            msg_prefix='validation error is displayed when CSV is selected without display fields')    


class ItemSearchTest(TestCase):

    @patch('keep.common.forms.CollectionObject')
    def test_search_options(self, mockcollection):
        # use a fake collection list
        mockcollection.item_collections.return_value = [
            {'pid': '%s:1' % settings.FEDORA_PIDSPACE, 'title': 'collection 1'},
            ]

        form_data = {'collection_0': 'info:fedora/%s:1' % settings.FEDORA_PIDSPACE,
                     'title': '*foo',
                     'notes': '?',
                     'pid': 'keep*',
                     'display_fields': ['pid', 'title'],
                     'output': 'html',
                     }
        f = ItemSearch(form_data)
        search_opts = f.search_options()
        self.assertEqual(form_data['collection_0'], search_opts['collection_id'],
                         'collection value should return collection_id search option')
        self.assertEqual(form_data['title'].lstrip('*'), search_opts['title'],
                         'leading wildcard should be removed')
        self.assertEqual(form_data['pid'], search_opts['pid'])
        self.assert_('notes' not in search_opts,
                     'wildcard-only search term should not be included in search options')
        self.assert_('display_fields' not in search_opts,
                     'display fields value should not be included in search options')
        self.assert_('output' not in search_opts,
                     'output value should not be included in search options')

        # numeric pid should search dm1 id instead of pid
        form_data['pid'] = '123'
        f = ItemSearch(form_data)
        search_opts = f.search_options()
        self.assertEqual(form_data['pid'], search_opts['dm1_id'],
                         'numeric pid value should search dm1_id field')
        self.assertNotEqual(form_data['pid'], search_opts['pid'],
                     'numeric pid value should not search pid field')
        
    @patch('keep.common.forms.CollectionObject')
    def test_search_info(self, mockcollection):
        mockcollection.item_collections.return_value = [
            {'pid': '%s:1' % settings.FEDORA_PIDSPACE, 'title': 'collection 1'},
        ]
        mockcollection.find_by_pid.return_value = 'my collection'

        f = ItemSearch()
        form_data = {'collection_0': 'info:fedora/%s:1' % settings.FEDORA_PIDSPACE,
                     'title': 'foo',
                     'display_fields': ['pid', 'title'],
                     'output': 'html',
                     'pid': f.fields['pid'].initial
                     }
        f = ItemSearch(form_data)
        search_info = f.search_info()
        self.assertEqual(mockcollection.find_by_pid.return_value,
                         search_info['collection'])
        self.assertEqual(form_data['title'], search_info['title'])
        self.assert_('pid' not in search_info,
                     'fields with initial/default value should not be included in search info')
        self.assert_('output' not in search_info,
                     'output formatting fields should not be included in search info')

        


class TestRightsExtrasTemplateTags(TestCase):

    def test_access_code_abbreviation(self):
        self.assertEqual('C108-a donor request',
                         rights_extras.access_code_abbreviation('1'))
        self.assertEqual('C108-a donor request',
                         rights_extras.access_code_abbreviation(1))
        self.assertEqual('Metadata only',
                         rights_extras.access_code_abbreviation('13'))
        # shouldn't error when there is no match
        self.assertEqual(None,
                         rights_extras.access_code_abbreviation('934'))
        self.assertEqual(None,
                         rights_extras.access_code_abbreviation('''obviously not
                         an access code'''))


class TestAuditTrailEvent(TestCase):

    def setUp(self):
        self.ingest = AuditTrailRecord(date=datetime.now(tz=tzutc()),
                                  user='admin',
                                  message='initial ingest',
                                  action='ingest')
        self.modify = AuditTrailRecord(date=datetime.now(tz=tzutc()),
                                       user='admin',
                                       message='update something',
                                       component='DC',
                                       action='modifyDatastream')

    def test_init(self):
        event = AuditTrailEvent(self.ingest)
        self.assertEqual(self.ingest.date, event.date)
        self.assertEqual(self.ingest.user, event.user)
        self.assertEqual(self.ingest.message, event.message)
        self.assertEqual([], event.components)
        self.assert_(self.ingest.action in event.actions)

    def test_add_record(self):
        event = AuditTrailEvent(self.ingest)
        event.add_record(self.modify)
        self.assertEqual(self.modify.date, event.date)
        self.assert_(self.modify.component in event.components)
        self.assert_(self.modify.action in event.actions)
        
    def test_component_names(self):
        event = AuditTrailEvent(self.modify, {'DC': 'dublin core'})
        self.assertEqual(set(['dublin core']), event.component_names())
    
    def action(self):
        ingest_event = AuditTrailEvent(self.ingest)
        self.assertEqual('ingest', ingest_event.action)

        modify_event = AuditTrailEvent(self.modify)
        self.assertEqual('modify', ingest_event.action)

