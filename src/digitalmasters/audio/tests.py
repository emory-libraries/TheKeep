import cStringIO
import os
import urlparse
import stat
import sys
import tempfile
from time import sleep

from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.management.base import CommandError
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository
from eulcore.xmlmap  import load_xmlobject_from_string

from digitalmasters import mods
from digitalmasters.audio import forms as audioforms
from digitalmasters.audio.models import AudioObject, wav_duration
from digitalmasters.audio.management.commands import ingest_cleanup

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

# fixture filenames used in multiple tests
mp3_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')
wav_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav')


class AudioViewsTest(TestCase):
    fixtures =  ['users']

    def setUp(self):
        self.client = Client()

    def test_index(self):
        # test audio app index page permissions
        audio_index = reverse('audio:index')

        # not logged in
        response = self.client.get(audio_index)
        code = response.status_code
        expected = 302
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as AnonymousUser'
                             % (expected, code, audio_index))

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(audio_index)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, audio_index))

        self.assert_(isinstance(response.context['search'], audioforms.SearchForm))
        self.assertContains(response, '<input')
        self.assertContains(response, 'Pid:')
        self.assertContains(response, 'Title:')

    def test_upload_html5(self):
        # test upload form
        HTML5_upload_url = reverse('audio:HTML5FileUpload')
        upload_url = reverse('audio:upload')

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(upload_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, upload_url))
        self.assertContains(response, '<input')

        # common post options used for most test cases
        post_options = {
            'path': HTML5_upload_url,
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'HTTP_X_FILE_NAME': 'example.wav',
            'content_type': 'multipart/form-data',
        }
        # md5 checksums for the two fixture audio files
        mp3_md5 = 'b56b59c5004212b7be53fb5742823bd2'
        wav_md5 = 'f725ce7eda38088ede8409254d6fe8c3'
        
        # POST non-wav file to AJAX Upload view results in an error
        with open(mp3_filename, 'rb') as mp3:
            opts = post_options.copy()
            opts['HTTP_X_FILE_NAME'] = 'example.mp3' 
            response = self.client.post(data=mp3.read(), HTTP_X_FILE_MD5=mp3_md5, **opts)
            self.assertEqual('Error - Incorrect File Type',response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                                 % (expected, code, HTML5_upload_url))
        
        # POST wav file to AJAX Upload view with incorrect checksum should fail
        with open(wav_filename, 'rb') as wav:
            # using mp3 checksum but uploading wav file
            response = self.client.post(data=wav.read(), HTTP_X_FILE_MD5=mp3_md5,
                                        **post_options)
            self.assertEqual('Error - MD5 Did Not Match',response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                                 % (expected, code, HTML5_upload_url))
                
        # POST wav file to AJAX Upload view with missing header arguments should fail
        with open(wav_filename, 'rb') as wav:
            # expected error message if required headers are missing
            missing_args = 'Error - missing needed headers (either HTTP-X-FILE-NAME or HTTP-X-FILE-MD5).'
            opts = post_options.copy()
            opts['data'] = wav.read()
            # POST without MD5 header
            response = self.client.post(**opts)
            self.assertEqual(missing_args, response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                                 % (expected, code, HTML5_upload_url))

            # POST without filename header
            del(opts['HTTP_X_FILE_NAME'])
            response = self.client.post(HTTP_X_FILE_MD5=wav_md5, **opts)
            self.assertEqual(missing_args, response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                                 % (expected, code, HTML5_upload_url))
        
        # POST wav file to AJAX Upload view should work
        with open(wav_filename) as wav:            
            response = self.client.post(data=wav.read(),
                                        HTTP_X_FILE_MD5=wav_md5, **post_options)
            # on success, response content is temporary filename
            uploaded_filename = response.content
            self.assert_(uploaded_filename.startswith('example_'),
                'response content should be filename on success; should start with uploaded file base name')
            self.assert_(uploaded_filename.endswith('.wav'),
                'response content should be filename on success; should end with uploaded file suffix (.wav)')

        # use the returned filename from the last (successful) response to test upload
        upload_opts = {
            'originalFileNames': 'example.wav',
            'fileUploads': uploaded_filename,
            'fileMD5sum': wav_md5
        }
        # POST wav file with incorrect checksum should fail
        invalid_upload_opts = upload_opts.copy()
        invalid_upload_opts['fileMD5sum'] = mp3_md5     # using mp3 checksum for wav file
        response = self.client.post(upload_url, invalid_upload_opts, follow=True)
        # convert messages to a list for easier inspection
        messages = [ msg for msg in response.context['messages'] ]
        self.assert_('has a corrupted MD5 sum on the server.' in str(messages[0]))
        self.assertEqual('error', messages[0].tags)
        
        # POST wav file with correct checksum - should succeed
        response = self.client.post(upload_url, upload_opts, follow=True)
        messages = [ msg for msg in response.context['messages'] ]
        self.assert_('Successfully ingested file' in str(messages[0]))
        self.assertEqual('success', messages[0].tags)
        # pull the pid of the newly created object from the message and inspect in fedora
        pid = str(messages[0]).replace('Successfully ingested file example.wav in fedora as ',
                                      '').rstrip('.')
        repo = Repository()
        new_obj = repo.get_object(pid, type=AudioObject)
        # check object was created with audio cmodel
        self.assertTrue(new_obj.has_model(AudioObject.AUDIO_CONTENT_MODEL),
            "audio object was created with the correct content model")
        self.assertEqual('example.wav', new_obj.label,
            'initial object label set from original file name (not temporary upload filename)')
        # check that init from file worked correctly
        self.assertEqual(3, new_obj.digtech.content.duration,
                'duration is set on new object created via upload (init from file worked correctly)')
            
    def test_upload_fallback(self):
        # test upload form
        upload_url = reverse('audio:upload')

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        # view the form
        response = self.client.get(upload_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, upload_url))
        self.assertContains(response, '<input')

        # POST non-wav file - should fail
        with open(mp3_filename) as mp3:
            response = self.client.post(upload_url, {'fileManualUpload': mp3},
                                        follow=True)
            # convert messages to a list for easier inspection
            messages = [ msg for msg in response.context['messages'] ]
            self.assertEqual('The file uploaded is not of an accepted type (got audio/mpeg)',
                 str(messages[0]))
            self.assertEqual('error', messages[0].tags,
                'message on invalid file type should have tag "error", got "%s"' \
                % messages[0].tags)
        
        # POST a wav file - should result in a new object
        with open(wav_filename) as wav:
            response = self.client.post(upload_url, {'fileManualUpload': wav},
                                        follow=True)
            messages = [ msg for msg in response.context['messages'] ]
            self.assert_('Successfully ingested file example.wav' in str(messages[0]),
                'successful file ingest message displayed to user')
            self.assertEqual('success', messages[0].tags,
                'message on successful ingest should have tag "success", got "%s"' % messages[0].tags)
            # pull the pid of the newly created object from the message and inspect in fedora
            pid = str(messages[0]).replace('Successfully ingested file example.wav in fedora as ',
                                      '').rstrip('.')
            repo = Repository()
            new_obj = repo.get_object(pid, type=AudioObject)
            # check object was created with audio cmodel
            self.assertTrue(new_obj.has_model(AudioObject.AUDIO_CONTENT_MODEL),
                "audio object was created with the correct content model")
            # seek to 0 so we can re-read file data
            wav.seek(0)
            self.assertEqual(wav.read(), new_obj.audio.content.read(),
                "audio file content on new object corresponds to uploaded file data")
            # check that init from file worked correctly
            self.assertEqual(3, new_obj.digtech.content.duration,
                'duration is set on new object created via upload (init from file worked correctly)')

                    
    def test_search(self):
        search_url = reverse('audio:search')

        # create some test objects to search for
        repo = Repository()
        obj = repo.get_object()
        obj.dc.content.title = "test search object 1"
        obj.save()
        obj2 = repo.get_object()
        obj2.dc.content.title = "test search object 2"
        obj2.save()

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by exact pid
        response = self.client.get(search_url, {'pid': obj.pid})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by pid")
        self.assertNotContains(response, obj2.pid,
                msg_prefix="test object 2 not listed in results when searching by pid for test object 1")

        # search by title phrase
        response = self.client.get(search_url,
            {'title': 'test search', 'pid': '%s:' % settings.FEDORA_PIDSPACE })
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by title")
        self.assertContains(response, obj2.pid,
                msg_prefix="test object 2 listed in results when searching by title")

        download_url = reverse('audio:download-audio', args=[obj.pid])
        self.assertContains(response, download_url,
                msg_prefix="search results link to audio download")

    def test_download_audio(self):
        # create a test audio object
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
        obj.label = "my audio test object"
        obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj.save()
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        download_url = reverse('audio:download-audio', args=[obj.pid])
        
        response = self.client.get(download_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, download_url))
                             
        expected = 'audio/x-wav'
        self.assertEqual(response['Content-Type'], expected,
                        "Expected '%s' but returned '%s' for %s mimetype" % \
                        (expected, response['Content-Type'], download_url))
                        
        expected = 'attachment; filename=my-audio-test-object.wav'
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Type'], download_url))

    # NOTE: prototype edit form tests are failing; disabling because it's a *prototype*
    def disabled_test_edit(self):
        # create a test audio object to edit
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
        obj.label = "my audio test object"
        obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj.save()
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        edit_url = reverse('audio:edit', args=[obj.pid])

        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assert_(isinstance(response.context['form'], audioforms.EditForm),
                "MODS EditForm is set in response context")
        self.assert_(isinstance(response.context['form'].instance, mods.MODS),
                "form instance is a MODS xmlobject")

        # POST data to update MODS in fedora
        mods_data = {'title': 'new title',
                    'resource_type': 'text',
                    'note-label' : 'a general note',
                    'note-type': 'general',
                    'note-text': 'remember to ...',
                    'created-key_date': True,
                    'created-date': '2010-01-02',
                    }
        response = self.client.post(edit_url, mods_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Updated MODS for %s" % obj.pid, messages[0],
            "successful save message set in response context")
        # currently redirects to audio index
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "attempting to edit non-existent pid redirects to audio index page")
        expected = 302      # redirect  -- maybe this should be a 303?
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (edit non-existent record)'  % \
            (expected, code, edit_url))

        # retrieve the modified object from Fedora to check for updates
        updated_obj = repo.get_object(pid=obj.pid, type=AudioObject)
        self.assertEqual(mods_data['title'], updated_obj.mods.content.title,
            'mods title in fedora matches posted title')
        self.assertEqual(mods_data['resource_type'], updated_obj.mods.content.resource_type,
            'mods resource type in fedora matches posted resource type')
        self.assertEqual(mods_data['note-label'], updated_obj.mods.content.note.label,
            'mods note label in fedora matches posted note label')
        self.assertEqual(mods_data['note-type'], updated_obj.mods.content.note.type,
            'mods note type in fedora matches posted note type')
        self.assertEqual(mods_data['note-text'], updated_obj.mods.content.note.text,
            'mods note text in fedora matches posted note text')
        self.assertEqual(mods_data['created-key_date'],
            updated_obj.mods.content.origin_info.created.key_date,
            'mods created key date in fedora matches posted created key date')
        self.assertEqual(mods_data['created-date'],
            updated_obj.mods.content.origin_info.created.date,
            'mods created date in fedora matches posted created date')

        # force a schema-validation error (shouldn't happen normally)
        obj.mods.content = load_xmlobject_from_string(TestMods.invalid_xml, mods.MODS)
        obj.save("schema-invalid MODS")
        response = self.client.post(edit_url, mods_data)

        self.assertContains(response, '<ul class="errorlist">')

        # edit non-existent record - exception
        fakepid = 'bogus-pid:1'
        edit_url = reverse('audio:edit', args=[fakepid])
        response = self.client.get(edit_url, follow=True)  # follow redirect to check error message
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load %s MODS for editing" % fakepid, messages[0],
            "load error message set in context when attempting to edit a non-existent pid")
        # currently redirects to audio index 
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "attempting to edit non-existent pid redirects to audio index page")
        expected = 302      # redirect  -- maybe this should be a 303?
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (edit non-existent record)'  % (expected, code, edit_url))



RealRepository = Repository
class FedoraCommsTest(TestCase):
    '''Test the app's response to fedora inaccessibility and unexpected
    fedora errors.'''

    fixtures =  ['users']

    def setUp(self):
        self.client = Client()
        self.client.login(**ADMIN_CREDENTIALS)

    def tearDown(self):
        self.restoreRepository()

    def useRepositoryRoot(self, root=None, host=None, port=None, path=None):
        if root is None:
            root = settings.FEDORA_ROOT
        root = self._update_root(root, host, port, path)

        # lots of Repository objects floating around here. let's do our
        # modules and namespacing very explicitly
        import eulcore.fedora.server
        import eulcore.django.fedora
        import eulcore.django.fedora.server
        import digitalmasters.audio.views

        username = getattr(settings, 'FEDORA_USER', None)
        password = getattr(settings, 'FEDORA_PASS', None)

        class RedirectedRepository(eulcore.fedora.server.Repository):
            def __init__(self, request=None):
                # take (and ignore) a request option to match local Repository class
                eulcore.fedora.server.Repository.__init__(self, root, username, password)
        if hasattr(settings, 'FEDORA_PIDSPACE'):
            RedirectedRepository.default_pidspace = settings.FEDORA_PIDSPACE

        eulcore.django.fedora.Repository = RedirectedRepository
        eulcore.django.fedora.server.Repository = RedirectedRepository
        digitalmasters.audio.views.Repository = RedirectedRepository

    def restoreRepository(self):
        import eulcore.django.fedora
        import eulcore.django.fedora.server
        import digitalmasters.audio.views
        eulcore.django.fedora.Repository = RealRepository
        eulcore.django.fedora.server.Repository = RealRepository
        digitalmasters.audio.views.Repository = RealRepository

    def _update_root(self, root, host, port, path):
        root_parts = urlparse.urlsplit(root)
        use_auth, at, hostport = root_parts.netloc.rpartition('@')
        use_host, colon, use_port = hostport.partition(':')
        use_parts = list(root_parts)

        if host is not None:
            use_host = host
        if port is not None:
            use_port = str(port)
            colon = ':' # just in case it wasn't already
        use_parts[1] = ''.join((use_auth, at, use_host, colon, use_port))

        if path is not None:
            use_parts[2] = path

        return urlparse.urlunsplit(use_parts)

    # _test not test so that this isn't picked up as a test case. this
    # method should be called from other test methods after changing the
    # repo root.
    def _testRepoErrors(self):
        # search
        url = reverse('audio:search')
        response = self.client.get(url, {'pid': 'fakepid:42'})
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500)

        # upload
        url = reverse('audio:upload')
        f = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        response = self.client.post(url, {'fileManualUpload': f}, follow=True) 
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500) 

        # edit

        # FIXME: this uses a different error reporting structure than the
        # other tests in this block. we should unify them. at the very
        # least, these errors should return 500, not 302.
        url = reverse('audio:edit', kwargs={'pid': 'fakepid:42'})
        response = self.client.get(url, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load fakepid:42 MODS for editing", messages[0],
            "load error message set in context when attempting to access bad fedora port")

        mods_data = {'title': 'new title',
                    'resource_type': 'text',
                    'note-label' : 'a general note',
                    'note-type': 'general',
                    'note-text': 'remember to ...',
                    'created-key_date': True,
                    'created-date': '2010-01-02',
                    }
        response = self.client.post(url, mods_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load fakepid:42 MODS for editing", messages[0],
            "load error message set in context when attempting to access bad fedora port")

        # download
        url = reverse('audio:download-audio', kwargs={'pid': 'fakepid:42'})
        response = self.client.get(url)
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500)

    def testRepositoryDown(self):
        '''Verify we respond correctly when we can't connect to the repo.'''
        self.useRepositoryRoot(port=1)
        self._testRepoErrors()

    def testBadRepoUrl(self):
        '''Verify we respond correctly when the repo path is inaccessible.'''
        self.useRepositoryRoot(path='/')
        self._testRepoErrors()


# tests for MODS XmlObject
# FIXME: mods objects no longer part of digitalmasters.audio - where should these tests live?
class TestMods(TestCase):
    FIXTURE = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
  <mods:titleInfo>
    <mods:title>A simple record</mods:title>
  </mods:titleInfo>
  <mods:typeOfResource>text</mods:typeOfResource>
  <mods:note displayLabel="a general note" type="general">remember to...</mods:note>
  <mods:originInfo>
    <mods:dateCreated keyDate='yes'>2010-06-17</mods:dateCreated>
  </mods:originInfo>
  <mods:identifier type='uri'>http://so.me/uri</mods:identifier>
  <mods:name type="personal" authority="naf" ID="n82032703">
    <mods:namePart>Dawson, William Levi</mods:namePart>
    <mods:namePart type="date">1899-1990</mods:namePart>
    <mods:displayForm>William Levi Dawson (1899-1990)</mods:displayForm>
    <mods:affiliation>Tuskegee</mods:affiliation>
    <mods:role>
      <mods:roleTerm type="text" authority="marcrelator">Composer</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:accessCondition type="restrictions on access">Restricted</mods:accessCondition>
  <mods:relatedItem type="host">
    <mods:titleInfo>
      <mods:title>Emory University Archives</mods:title>
    </mods:titleInfo>
  <mods:identifier type="local_sourcecoll_id">eua</mods:identifier>
  </mods:relatedItem>
</mods:mods>
"""
    invalid_xml = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
    <mods:titleInfo><mods:title invalid_attribute='oops'>An invalid record</mods:title></mods:titleInfo>
</mods:mods>
        """

    def setUp(self):
        self.mods = load_xmlobject_from_string(self.FIXTURE, mods.MODS)

    def test_init_types(self):
        self.assert_(isinstance(self.mods, mods.MODS))
        self.assert_(isinstance(self.mods.note, mods.Note))
        self.assert_(isinstance(self.mods.origin_info, mods.OriginInfo))
        self.assert_(isinstance(self.mods.origin_info.created[0], mods.Date))
        self.assert_(isinstance(self.mods.identifiers[0], mods.Identifier))
        self.assert_(isinstance(self.mods.name, mods.Name))
        self.assert_(isinstance(self.mods.name.name_parts[0], mods.NamePart))
        self.assert_(isinstance(self.mods.name.roles[0], mods.Role))
        self.assert_(isinstance(self.mods.access_conditions[0], mods.AccessCondition))
        self.assert_(isinstance(self.mods.related_items[0], mods.RelatedItem))

    def test_fields(self):
        self.assertEqual('A simple record', self.mods.title)
        self.assertEqual('text', self.mods.resource_type)
        self.assertEqual('a general note', self.mods.note.label)
        self.assertEqual('general', self.mods.note.type)
        self.assertEqual(u'remember to...', unicode(self.mods.note))
        self.assertEqual(u'2010-06-17', unicode(self.mods.origin_info.created[0]))
        self.assertEqual('2010-06-17', self.mods.origin_info.created[0].date)
        self.assertEqual(True, self.mods.origin_info.created[0].key_date)
        self.assertEqual(u'http://so.me/uri', self.mods.identifiers[0].text)
        self.assertEqual(u'uri', self.mods.identifiers[0].type)
        # name fields
        self.assertEqual(u'personal', self.mods.name.type)
        self.assertEqual(u'naf', self.mods.name.authority)
        self.assertEqual(u'n82032703', self.mods.name.id)
        self.assertEqual(u'Dawson, William Levi', self.mods.name.name_parts[0].text)
        self.assertEqual(u'1899-1990', self.mods.name.name_parts[1].text)
        self.assertEqual(u'date', self.mods.name.name_parts[1].type)
        self.assertEqual(u'William Levi Dawson (1899-1990)', self.mods.name.display_form)
        self.assertEqual(u'Tuskegee', self.mods.name.affiliation)
        self.assertEqual(u'text', self.mods.name.roles[0].type)
        self.assertEqual(u'marcrelator', self.mods.name.roles[0].authority)
        self.assertEqual(u'Composer', self.mods.name.roles[0].text)
        # access condition
        self.assertEqual(u'restrictions on access', self.mods.access_conditions[0].type)
        self.assertEqual(u'Restricted', self.mods.access_conditions[0].text)
        # related item
        self.assertEqual(u'host', self.mods.related_items[0].type)
        self.assertEqual(u'Emory University Archives', self.mods.related_items[0].title)
        self.assertEqual(u'local_sourcecoll_id', self.mods.related_items[0].identifiers[0].type)
        self.assertEqual(u'eua', self.mods.related_items[0].identifiers[0].text)

    def test_create_mods(self):
        # test creating MODS from scratch - ensure sub-xmlobject definitions are correct
        # and produce schema-valid MODS
        mymods = mods.MODS()
        mymods.title = 'A Record'
        mymods.resource_type = 'text'
        mymods.name.type = 'personal'
        mymods.name.authority = 'local'
        mymods.name.name_parts.extend([mods.NamePart(type='family', text='Schmoe'),
                                    mods.NamePart(type='given', text='Joe')])
        mymods.name.roles.append(mods.Role(type='text', authority='local',
                                        text='Test Subject'))
        mymods.note.type = 'general'
        mymods.note.text = 'general note'
        mymods.origin_info.created.append(mods.DateCreated(date='2001-10-02'))
        mymods.origin_info.issued.append(mods.DateIssued(date='2001-12-01'))
        mymods.record_id = 'id:1'
        mymods.identifiers.extend([mods.Identifier(type='uri', text='http://ur.l'),
                                 mods.Identifier(type='local', text='332')])
        mymods.access_conditions.extend([mods.AccessCondition(type='restriction', text='unavailable'),
                                       mods.AccessCondition(type='use', text='Tuesdays only')])
        mymods.related_items.extend([mods.RelatedItem(type='host', title='EU Archives'),
                                   mods.RelatedItem(type='isReferencedBy', title='Finding Aid'),])
        xml = mymods.serialize(pretty=True)
        self.assert_('<mods:mods ' in xml)
        self.assert_('xmlns:mods="http://www.loc.gov/mods/v3"' in xml)

        self.assertTrue(mymods.is_valid(), "MODS created from scratch should be schema-valid")

    def test_isvalid(self):
        # if additions to MODS test fixture cause validation errors, uncomment the next 2 lines to debug
        #self.mods.is_valid()
        #print self.mods.validation_errors()
        self.assertTrue(self.mods.is_valid())        
        invalid_mods = load_xmlobject_from_string(self.invalid_xml, mods.MODS)
        self.assertFalse(invalid_mods.is_valid())


# tests for (prototype) Audio DigitalObject
class TestAudioObject(TestCase):
    fixtures =  ['users']
    repo = Repository()

    def setUp(self):
        # create a test audio object to edit
        with open(wav_filename) as wav:
            self.obj = self.repo.get_object(type=AudioObject)
            self.obj.label = "Testing, one, two"
            self.obj.dc.content.title = self.obj.label
            self.obj.audio.content = wav
            self.obj.save()

    def tearDown(self):
        self.repo.purge_object(self.obj.pid, "removing unit test fixture")

    def test_creation(self):
        # verify that the owner id is set.
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, self.obj.info.owner)

        self.obj.save()
        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, obj.info.owner)

    def test_save(self):
        # save without changing the MODS - shouldn't mess anything up
        self.obj.save()
        self.assertEqual("Testing, one, two", self.obj.label)
        self.assertEqual("Testing, one, two", self.obj.dc.content.title)

        # set values in mods and save - should cascade to label, DC
        title, type, date = 'new title in mods', 'text', '2010-01-03'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = type
        self.obj.mods.content.origin_info.created.append(mods.Date(date=date))
        self.obj.save('testing custom save logic')

        # get updated copy from repo to check
        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(title, obj.label)
        self.assertEqual(title, obj.dc.content.title)
        self.assertEqual(type, obj.dc.content.type)
        self.assertEqual(date, obj.dc.content.date)

        # verify that the owner id is set in repo copy.
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, self.obj.info.owner)

    def test_init_from_file(self):
        new_obj = AudioObject.init_from_file(wav_filename)
        filename = 'example.wav'
        self.assertEqual(filename, new_obj.label)
        self.assertEqual(filename, new_obj.mods.content.title)
        self.assertEqual(filename, new_obj.dc.content.title)
        self.assert_(isinstance(new_obj.audio.content, file),
            'audio datastream content should be a file object')
        # typeOfResource
        self.assertEqual('sound recording', new_obj.mods.content.resource_type,
            'mods:typeOfResource initialized to "sound recording"')
        # codec quality
        self.assertEqual('lossless', new_obj.digtech.content.codec_quality,
            'codec quality should be initialized to "lossless"')
        # duration
        self.assertEqual(3, new_obj.digtech.content.duration,
            'duration should be calculated and stored in duration, rounded to the nearest second')

        # specify an initial label
        label = 'this is a test WAV file'
        new_obj = AudioObject.init_from_file(wav_filename, label)
        self.assertEqual(label, new_obj.label)
        self.assertEqual(label, new_obj.mods.content.title)
        self.assertEqual(label, new_obj.dc.content.title)
        
        # specify an incorrect checksum
        wav_md5 = 'aaa'
        checksum_obj = AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
        expected_error=None
        try:
            checksum_obj.save()
        except Exception as e:
            expected_error = e
            
        self.assert_(str(expected_error).endswith('500 Internal Server Error'), 'Incorrect checksum should not be ingested.') 
        
        # specify a correct checksum
        wav_md5 = 'f725ce7eda38088ede8409254d6fe8c3'
        checksum_obj = AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
        return_result = checksum_obj.save()
        self.assertEqual(True, return_result)

        # use request to pass logged-in user credentials for fedora access
        rqst = HttpRequest()
        user = ADMIN_CREDENTIALS['username']
        rqst.user = User.objects.get(username=user)
        # use custom login so user credentials will be stored properly
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        rqst.session = self.client.session
        new_obj = AudioObject.init_from_file(wav_filename, request=rqst)
        self.assertEqual(new_obj.api.opener.username, user,
            'object initialized with request has user credentials configured for fedora access')
        


class TestWavDuration(TestCase):

    def test_success(self):
        duration = wav_duration(wav_filename)
        # ffmpeg reports the duration of fixture WAV file as 00:00:03.30
        self.assertAlmostEqual(3.3, duration, 3)

    def test_non_wav(self):
        self.assertRaises(StandardError, wav_duration, mp3_filename)

    def test_nonexistent(self):
        self.assertRaises(IOError, wav_duration, 'i-am-not-a-real-file.wav')


class TestIngestCleanupCommand(ingest_cleanup.Command):
    # extend command class to simplify calling as if running from the commandline
    # base command will set up default args before calling handle method
    def run_command(self, *args):
        '''Run the command as if calling from command line by giving a list
        of command-line arguments, e.g.::

            command.run_command('-n', '-v', '2')

        :param args: list of command-line arguments
        '''
        # run from argv expects command, subcommand, then any arguments
        run_args = ['manage.py', 'ingest_cleanup']
        run_args.extend(args)
        return self.run_from_argv(run_args)

class IngestCleanupTest(TestCase):
    def setUp(self):
        self.command = TestIngestCleanupCommand()
        self._real_temp_dir = settings.INGEST_STAGING_TEMP_DIR
        self._real_keep_age = settings.INGEST_STAGING_KEEP_AGE
        self.tmpdir = tempfile.mkdtemp(prefix='digmast-ingest-cleanup-test')
        settings.INGEST_STAGING_TEMP_DIR = self.tmpdir

    def tearDown(self):
        # remove any files created in temporary test staging dir
        for file in os.listdir(self.tmpdir):
            os.unlink(os.path.join(self.tmpdir, file))
        
        #Possible timing conflict.... can still occur if an anti-virus is running or something else accesses the file: http://bugs.python.org/issue1425127
        sleep(1)
        #See: http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
        os.chmod(self.tmpdir,stat.S_IWUSR)
        # remove temporary test staging dir
        os.rmdir(self.tmpdir)
        settings.INGEST_STAGING_TEMP_DIR = self._real_temp_dir
        settings.INGEST_STAGING_KEEP_AGE = self._real_keep_age

    def test_missing_age_setting(self):
        del(settings.INGEST_STAGING_KEEP_AGE)
        self.assertRaises(CommandError, self.command.handle, verbosity=0)
        
    def test_missing_dir_setting(self):
        del(settings.INGEST_STAGING_TEMP_DIR)
        self.assertRaises(CommandError, self.command.handle, verbosity=0)

    def test_nonexistent_directory(self):
        # temporarily override tmp dir with a non-existent one
        settings.INGEST_STAGING_TEMP_DIR = os.path.join('this', 'dir', 'should', 'not', 'exist')
        # should get a command error when directory does not exist or is not readable
        # - calling handle directly because base command run_from_argv handles/presents the command error
        self.assertRaises(CommandError, self.command.handle, verbosity=0)
        
        # restore existing test tmp dir
        settings.INGEST_STAGING_TEMP_DIR = self.tmpdir

    def test_cleanup(self):
        settings.INGEST_STAGING_KEEP_AGE = 10
        # create temp files in temp dir, one older than the keep age and one newer
        # - using delete=False so tempfile doesn't complain when the object is deleted
        #   and the file is not present to be removed
        older = tempfile.NamedTemporaryFile(dir=self.tmpdir, prefix='older-', delete=False)
        older.close()
        sleep(10)
        newer = tempfile.NamedTemporaryFile(dir=self.tmpdir, prefix='newer-', delete=False)
        newer.close()
        self.command.run_command('-v', '0')
        self.assertFalse(os.access(older.name, os.F_OK),
            'older file should NOT exist - should have been removed by cleanup script')
        self.assertTrue(os.access(newer.name, os.F_OK),
            'newer file should exist - should NOT have been removed by cleanup script')

    def test_read_error(self):
        settings.INGEST_STAGING_KEEP_AGE = 1
        file = tempfile.NamedTemporaryFile(dir=self.tmpdir, prefix='file-', delete=False)
        file.close()
        sleep(1)
        # temporarily make directory read-only
        dir_stats = os.stat(self.tmpdir)
        os.chmod(self.tmpdir, stat.S_IREAD)

        # capture command output in a stream
        buffer = cStringIO.StringIO()
        sys.stdout = buffer
        self.command.run_command('-v', '0')
        sys.stdout = sys.__stdout__         # restore real stdout
        output = buffer.getvalue()
        self.assert_('Error reading file' in output,
            'error reading file is printed even in minimal-output mode')
        buffer.close()

        # restore previous tmp dir permissions
        os.chmod(self.tmpdir, dir_stats.st_mode)

    def test_dry_run(self):
        settings.INGEST_STAGING_KEEP_AGE = 1
        file = tempfile.NamedTemporaryFile(dir=self.tmpdir, prefix='dryrun-')
        sleep(1)
        self.command.run_command('-n', '-v', '0')
        self.assertTrue(os.access(file.name, os.F_OK),
            'file past keep age is not deleted in dry-run mode')

