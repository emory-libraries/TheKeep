import cStringIO
from datetime import date
import os
from shutil import copyfile
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
from eulcore.django.taskresult.models import TaskResult
from eulcore.django.test import TestCase as EulDjangoTestCase
from eulcore.fedora.util import RequestFailed
from eulcore.xmlmap  import load_xmlobject_from_string

from keep import mods
from keep.audio import forms as audioforms
from keep.audio import models as audiomodels
from keep.audio.management.commands import ingest_cleanup
from keep.collection.fixtures import FedoraFixtures
from keep.collection.models import CollectionObject
from keep.audio.tasks import convert_wav_to_mp3

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

# fixture filenames used in multiple tests
mp3_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')
wav_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav')
alternate_wav_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example2.wav')
# MD5 checksums for fixture files
# md5 checksums for the two fixture audio files
mp3_md5 = 'b56b59c5004212b7be53fb5742823bd2'
wav_md5 = 'f725ce7eda38088ede8409254d6fe8c3'
alternate_wav_md5 = '736e0d8cd4dec9e02cd25283e424bbd5'

class AudioViewsTest(EulDjangoTestCase):
    fixtures =  ['users']

    client = Client()

    def setUp(self):        
        self.pids = []
        # store setting that may be changed when testing podcast feed pagination
        self.max_per_podcast = getattr(settings, 'MAX_ITEMS_PER_PODCAST_FEED', None)

        # collection fixtures are not modified, but there is no clean way
        # to only load & purge once
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.esterbrook = FedoraFixtures.esterbrook_collection()
        self.esterbrook.save()
        self.englishdocs = FedoraFixtures.englishdocs_collection()
        self.englishdocs.save()

    def tearDown(self):
        # purge any objects created by individual tests
        for pid in self.pids:
            FedoraFixtures.repo.purge_object(pid)
        # restore podcast pagination setting
        if self.max_per_podcast is not None:
            settings.MAX_ITEMS_PER_PODCAST_FEED = self.max_per_podcast
        elif hasattr(settings, 'MAX_ITEMS_PER_PODCAST_FEED'):
            # if not originally set but added by a test, remove the setting
            del settings.MAX_ITEMS_PER_PODCAST_FEED

        # TODO: remove any test files created in staging dir
        # FIXME: should we create & remove a tmpdir instead of using actual staging dir?
        
        FedoraFixtures.repo.purge_object(self.rushdie.pid)
        FedoraFixtures.repo.purge_object(self.esterbrook.pid)
        FedoraFixtures.repo.purge_object(self.englishdocs.pid)

        # refresh cached collections after objects are deleted
        CollectionObject.item_collections(refresh_cache=True)

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

    def test_upload_form(self):
        # test upload form
        upload_url = reverse('audio:upload')

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        # on GET, should display the form
        response = self.client.get(upload_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, upload_url))
        self.assertNotEqual(None, response.context['form'])
        self.assert_(isinstance(response.context['form'], audioforms.UploadForm))
        # is this sufficient? anything else to test here?

    def test_ajax_file_upload(self):
        # test uploading files via ajax
        upload_url = reverse('audio:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # common post options used for most test cases
        post_options = {
            'path': upload_url,
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'HTTP_CONTENT_DISPOSITION': 'filename="example.wav"',
            'content_type': 'audio/wav',
        }
        # POST non-wav file to AJAX Upload view results in an error
        with open(mp3_filename, 'rb') as mp3:
            opts = post_options.copy()
            opts['HTTP_CONTENT_DISPOSITION'] = 'attachment; filename="example.mp3"'
            response = self.client.post(data=mp3.read(), HTTP_CONTENT_MD5=mp3_md5, **opts)
            self.assertEqual('File type audio/mpeg is not allowed',response.content)
            code = response.status_code
            expected = 415  # unsupported media type
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                                 % (expected, code, upload_url))
        
        # POST wav file to AJAX Upload view with incorrect checksum should fail
        with open(wav_filename, 'rb') as wav:
            # using mp3 checksum but uploading wav file
            response = self.client.post(data=wav.read(), HTTP_CONTENT_MD5=mp3_md5,
                                        **post_options)
            self.assertEqual('Checksum mismatch; uploaded data may be incomplete or corrupted',
                response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected,
                'Expected %s but returned %s for %s with invalid MD5'
                     % (expected, code, upload_url))
                
        # POST wav file to AJAX Upload view with missing header arguments should fail
        with open(wav_filename, 'rb') as wav:
            # post without checksum
            opts = post_options.copy()
            opts['data'] = wav.read()
            # POST without MD5 header
            response = self.client.post(**opts)
            self.assertEqual('Content-MD5 header is required', response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected,
                'Expected %s but returned %s for %s without Content-MD5 header'
                        % (expected, code, upload_url))

            # POST without filename header
            del(opts['HTTP_CONTENT_DISPOSITION'])
            response = self.client.post(HTTP_CONTENT_MD5=wav_md5, **opts)
            self.assertEqual('Content-Disposition header is required', response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected,
                'Expected %s but returned %s for %s without Content-Disposition header'
                         % (expected, code, upload_url))

            # POST with content-disposition but no filename
            opts['HTTP_CONTENT_DISPOSITION'] = 'attachment'
            response = self.client.post(HTTP_CONTENT_MD5=wav_md5, **opts)
            self.assertEqual('Content-Disposition header must include filename', response.content)
            code = response.status_code
            expected = 400
            self.assertEqual(code, expected,
                'Expected %s but returned %s for %s with invalid Content-Disposition header'
                         % (expected, code, upload_url))
        
        # POST wav file to AJAX Upload view should work
        with open(wav_filename) as wav:            
            response = self.client.post(data=wav.read(),
                                        HTTP_CONTENT_MD5=wav_md5, **post_options)
            # on success, response content is temporary filename
            uploaded_filename = response.content
            self.assert_(uploaded_filename.startswith('example_'),
                'response content should be filename on success; should start with uploaded file base name')
            self.assert_(uploaded_filename.endswith('.wav'),
                'response content should be filename on success; should end with uploaded file suffix (.wav)')
            expected = 'text/plain'
            self.assertEqual(response['Content-Type'], expected,
                        "Expected '%s' but returned '%s' for %s mimetype" % \
                        (expected, response['Content-Type'], upload_url))
            
            # temp files should exist in staging dir
            upload_filepath = os.path.join(settings.INGEST_STAGING_TEMP_DIR,
                                                         uploaded_filename)
            self.assertTrue(os.path.exists(upload_filepath),
                'temp file returned in should exist in staging directory')
            self.assertTrue(os.path.exists(upload_filepath +  '.md5'),
                'MD5 file for temp file should exist in staging directory')
            with open(upload_filepath + '.md5') as md5file:
                self.assertEqual(wav_md5, md5file.read())

    def test_batch_upload(self):
        # test uploading files via ajax
        upload_url = reverse('audio:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        # create files in staging dir to mimic results of ajax upload
        upload_filepath = os.path.join(settings.INGEST_STAGING_TEMP_DIR, 'example-01.wav')
        copyfile(wav_filename, upload_filepath)
        with open(upload_filepath + '.md5', 'w') as md5file:
            md5file.write(wav_md5)

        # use the returned filename from the last (successful) response to test upload
        upload_opts = {
            'originalFileNames': 'example.wav',
            'fileUploads': 'example-01.wav',
        }
        # POST wav file with correct checksum - should succeed
        response = self.client.post(upload_url, upload_opts)
        result = response.context['ingest_results'][0]
        self.assertTrue(result['success'],
            'success should be True in result for successful ingest')
        self.assertNotEqual(None, result['pid'],
            'pid should be set in result on success')
        # add pid to be removed in tearDown
        self.pids.append(result['pid'])

        repo = Repository()
        new_obj = repo.get_object(result['pid'], type=audiomodels.AudioObject)
        # check object was created with audio cmodel
        self.assertTrue(new_obj.has_model(audiomodels.AudioObject.AUDIO_CONTENT_MODEL),
            "audio object was created with the correct content model")
        self.assertEqual('example.wav', new_obj.label,
            'initial object label set from original file name (not temporary upload filename)')
        # check that init from file worked correctly
        self.assertEqual(3, new_obj.digitaltech.content.duration,
                'duration is set on new object created via upload (init from file worked correctly)')

        # task result should have been created to track mp3 conversion
        self.assert_(isinstance(new_obj.conversion_result, TaskResult),
            'ingested object should have a conversion result to track mp3 generation')
            
        # POST wav file with an incorrect checksum should fail
        copyfile(wav_filename, upload_filepath)     # re-copy file, now that is removed after ingest
        with open(upload_filepath + '.md5', 'w') as md5file:
            md5file.write('bogus md5 checksum')
        response = self.client.post(upload_url, upload_opts)
        result = response.context['ingest_results'][0]
        self.assertFalse(result['success'], 'success should be false on checksum mismatch')
        self.assert_('failed due to a checksum mismatch' in result['message'],
            'result should include explanatory message on failure')

    def test_upload_fallback(self):
        # test single-file upload 
        upload_url = reverse('audio:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # POST non-wav file - should fail
        with open(mp3_filename) as mp3:
            response = self.client.post(upload_url, {'audio': mp3})
            result = response.context['ingest_results'][0]
            self.assertFalse(result['success'], 'success should be false on non-allowed type')
            self.assertEqual('''File type 'audio/mpeg' is not allowed''',
                            result['message'])
        
        # POST a wav file - should result in a new object
        with open(wav_filename) as wav:
            response = self.client.post(upload_url, {'audio': wav})
            result = response.context['ingest_results'][0]
            self.assertTrue(result['success'], 'success should be true for uploaded WAV')
            self.assertNotEqual(None, result['pid'],
                'result should include pid of new object on successful ingest')
            # Add pid to be removed.
            self.pids.append(result['pid'])

            repo = Repository()
            new_obj = repo.get_object(result['pid'], type=audiomodels.AudioObject)
            # check object was created with audio cmodel
            self.assertTrue(new_obj.has_model(audiomodels.AudioObject.AUDIO_CONTENT_MODEL),
                "audio object was created with the correct content model")
            # seek to 0 so we can re-read file data
            wav.seek(0)
            orig_data = wav.read()

            fetched_data = new_obj.audio.content.getvalue()
#           NB: fedora bug https://jira.duraspace.org/browse/FCREPO-774
#           truncates datastreams fetched through the rest api, causing
#           these next two checks to fail. we're temporarily replacing them
#           with the two checks that follow them. the fedora developers
#           expect a fix to that bug in fedora 3.4.2, to be released in jan
#           2010. once that's installed in testing we should put back the
#           original checks.

#            self.assertEqual(len(orig_data), len(fetched_data))
#            self.assertEqual(orig_data, new_obj.audio.content.getvalue(),
#                "audio file content on new object corresponds to uploaded file data")
            self.assertEqual(len(orig_data), new_obj.audio.info.size)
            # for now check only that the truncated fetched_data matches the
            # beginning of orig_data.
            self.assertEqual(orig_data[:len(fetched_data)], fetched_data,
                "audio file content on new object corresponds to uploaded file data")

            # check that init from file worked correctly
            self.assertEqual(3, new_obj.digitaltech.content.duration,
                'duration is set on new object created via upload (init from file worked correctly)')

            # task result should have been created to track mp3 conversion
            self.assert_(isinstance(new_obj.conversion_result, TaskResult),
                'ingested object should have a conversion result to track mp3 generation')

                    
    def test_search(self):
        search_url = reverse('audio:search')

        # create some test objects to search for
        repo = Repository()
        obj = repo.get_object(type=audiomodels.AudioObject)
        obj.mods.content.title = 'test search object 1'
        obj.mods.content.create_general_note()
        obj.mods.content.general_note.text = 'general note'
        obj.collection_uri = self.rushdie.uri
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date='1492-05'))
        obj.save()
        obj2 = repo.get_object(type=audiomodels.AudioObject)
        obj2.mods.content.title = 'test search object 2'
        obj2.rights.content.create_access_status()
        obj2.rights.content.access_status.code = 8
        obj2.rights.content.access_status.text = 'public domain'
        obj2.save()
        # add pids to list for clean-up in tearDown
        self.pids.extend([obj.pid, obj2.pid])
        
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by exact pid
        response = self.client.get(search_url, {'audio-pid': obj.pid})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by pid")
        self.assert_(obj2.pid not in found,
                "test object 2 not listed in results when searching by pid for test object 1")
        self.assertContains(response, '''Displaying record
1
of 1''',
            msg_prefix='search results include total number of records found')

        # search by title phrase
        response = self.client.get(search_url,
            {'audio-title': 'test search', 'audio-pid': '%s:' % settings.FEDORA_PIDSPACE })
        found = [o.pid for o in response.context['results']]
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by title")
        self.assert_(obj2.pid in found,
                "test object 2 listed in results when searching by title")
        self.assertPattern('Displaying records.*1 - 2.*of 2', response.content,
            msg_prefix='search results include total number of records found')
        self.assertPattern('title:.*test search', response.content,
            msg_prefix='search results page should include search term (title)')
        self.assertNotContains(response, 'pid: ',
            msg_prefix='search results page should not include default search terms (pid)')
        self.assertNotContains(response, 'description: ',
            msg_prefix='search results page should not include empty search terms (description)')

        download_url = reverse('audio:download-audio', args=[obj.pid])
        self.assertContains(response, download_url,
                msg_prefix="search results link to audio download")

        # search by description
        response = self.client.get(search_url, {'audio-description': 'general note'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by description")
        self.assert_(obj2.pid not in found,
                "test object 2 not listed in results when searching by description")
        self.assertPattern('description:.*general note', response.content,
            msg_prefix='search results page should include search term (description)')

        # search by date
        response = self.client.get(search_url, {'audio-date': '1492*'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by date")
        self.assert_(obj2.pid not in found,
                "test object 2 not listed in results when searching by date")
        self.assertPattern('date:.*1492\*', response.content,
            msg_prefix='search results page should include search term (date)')

        # search by rights
        response = self.client.get(search_url, {'audio-rights': '8'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid not in found,
                "test object 1 not listed in results when searching by rights")
        self.assert_(obj2.pid in found,
                "test object 2 listed in results when searching by rights")
        self.assertPattern('rights:.*8 - Public Domain', response.content,
            msg_prefix='search results page should include search term (rights)')

        # collection
        response = self.client.get(search_url, {'audio-collection':  self.rushdie.uri})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by collection")
        self.assert_(obj2.pid not in found,
                "test object 2 not listed in results when searching by collection")
        self.assert_(self.rushdie.pid not in found,
                "collection object not listed in results when searching by collection")
        self.assertPattern('Collection:.*%s' % self.rushdie.label, response.content,
            msg_prefix='search results page should include search term (collection by name)')

        # multiple fields
        response = self.client.get(search_url, {'audio-collection':  self.rushdie.uri,
            'audio-title': 'search', 'audio-date': '1492*'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid in found,
                "test object 1 listed in results when searching by collection + title + date")
        self.assert_(obj2.pid not in found,
                "test object 2 not listed in results when searching by collection + title + date")
        self.assertPattern('Collection:.*%s' % self.rushdie.label, response.content,
            msg_prefix='search results page should include all search terms used (collection)')
        self.assertPattern('date:.*1492\*', response.content,
            msg_prefix='search results page should include all search terms used (date)')
        self.assertPattern('title:.*test search', response.content,
            msg_prefix='search results page should include all search terms used (title)')

        # by default, list most recently created items first
        obj3 = repo.get_object(type=audiomodels.AudioObject)
        obj3.label = "most recent upload"
        obj3.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj3.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj3.pid)
        # default search
        response = self.client.get(search_url)
        found = [o.pid for o in response.context['results']]
        self.assert_(len(found) >= 3,
            'default search should find at least 3 items')
        self.assertEqual(found[0], obj3.pid,
            'most recently created object should be listed first in search results')

    def test_download_audio(self):
        # create a test audio object
        repo = Repository()
        obj = repo.get_object(type=audiomodels.AudioObject)
        obj.label = "my audio test object"
        obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)
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
                        
        expected = 'attachment; filename=%s.wav' % obj.noid
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Type'], download_url))

    def test_download_compressed_audio(self):
        # create a test audio object
        obj = audiomodels.AudioObject.init_from_file(wav_filename,
                                             'my audio test object',
                                              checksum=wav_md5)
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        download_url = reverse('audio:download-compressed-audio', args=[obj.pid])

        response = self.client.get(download_url)
        code = response.status_code
        expected = 404
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin for non-existent audio file'
                             % (expected, code, download_url))

        #Set a compressed audio stream.
        result = convert_wav_to_mp3(obj.pid)
        self.assertEqual(result, "Successfully converted file")
        
        response = self.client.get(download_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, download_url))
                             
        expected = 'audio/mpeg'
        self.assertEqual(response['Content-Type'], expected,
                        "Expected '%s' but returned '%s' for %s mimetype" % \
                        (expected, response['Content-Type'], download_url))
                        
        expected = 'attachment; filename=%s.mp3' % obj.noid
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Type'], download_url))

    def test_edit(self):
        # create a test audio object to edit
        obj = audiomodels.AudioObject.init_from_file(wav_filename, "my audio test object")
        # pre-populate some data to check it is set in form instance
        obj.mods.content.create_general_note()
        obj.mods.content.general_note.text = 'Here is some general info about this item.'
        obj.mods.content.create_part_note()
        obj.mods.content.part_note.text = 'Side 1'
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date='1975-10-31'))
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1978-12-25'))
        # descriptive metadata migration fields
        obj.mods.content.dm1_id = '20'
        obj.mods.content.dm1_other_id = '00000040'
        obj.mods.content.create_dm1_abstract_note()
        obj.mods.content.dm1_abstract_note.text = '''Includes a short commentary intro.'''
        obj.mods.content.create_dm1_content_note()
        obj.mods.content.dm1_content_note.text = '''content notes here'''
        obj.mods.content.create_dm1_toc_note()
        obj.mods.content.dm1_toc_note.text = '''TOC notes here.'''        
        obj.mods.content.resource_type = 'sound recording'
        namepartxml = mods.NamePart(text='Dawson, William Levi')
        rolexml = mods.Role(type='text', authority='marcrelator',
                            text='Composer')
        namexml = mods.Name(type='personal', authority='naf')
        namexml.name_parts.append(namepartxml)
        namexml.roles.append(rolexml)
        obj.mods.content.names.append(namexml)
        namepartxml = mods.NamePart(text='American Symphony Orchestra')
        rolexml = mods.Role(type='text', authority='marcrelator',
                            text='Performer')
        namexml = mods.Name(type='corporate', authority='naf')
        namexml.name_parts.append(namepartxml)
        namexml.roles.append(rolexml)
        obj.mods.content.names.append(namexml)
        obj.mods.content.genres.extend([
            mods.Genre(text='Sound recordings', authority='aat'),
            mods.Genre(text='Radio programs', authority='aat'),
        ])
        lang = mods.Language()
        lang.terms.append(mods.LanguageTerm(type='code',
            authority='iso639-2b', text='eng'))
        obj.mods.content.languages.append(lang)
        namepartxml = mods.NamePart(text='Dawson, William Levi')
        rolexml = mods.Role(type='text', authority='marcrelator',
                            text='Composer')
        namexml = mods.Name(type='personal', authority='naf')
        namexml.name_parts.append(namepartxml)
        namexml.roles.append(rolexml)
        obj.mods.content.subjects.extend([
            mods.Subject(authority='lcsh', geographic='Africa, West'),
            mods.Subject(authority='lcsh', topic='Radio Programs, Musical'),
            mods.Subject(authority='local', title='Frontiers of faith (Television series)'),
            mods.Subject(authority='naf', name=namexml),
        ])
        # pre-populate source tech metadata so we can check it in form instance
        obj.sourcetech.content.note = 'source note'
        obj.sourcetech.content.related_files = '1-3'
        obj.sourcetech.content.sound_characteristics = 'mono'
        # speed in xml maps to a single custom field
        obj.sourcetech.content.create_speed()
        obj.sourcetech.content.speed.unit = 'rpm'
        obj.sourcetech.content.speed.aspect = 'phonograph disc'
        obj.sourcetech.content.speed.value = '120'
        # reel size also maps to a custom field
        obj.sourcetech.content.create_reel_size()
        obj.sourcetech.content.reel_size.value = '3'
        # pre-populate digital tech metadata
        obj.digitaltech.content.codec_quality = 'lossy'
        obj.digitaltech.content.note = 'technician details'
        obj.digitaltech.content.digitization_purpose = 'dawson exhibit'
        # retrieve test user object to use for transfer engineer - also used to test
        ldap_user = User.objects.get(username='ldap_user')
        # engineer & codec creator are initialized based on id values
        obj.digitaltech.content.create_transfer_engineer()
        obj.digitaltech.content.transfer_engineer.id = ldap_user.username
        obj.digitaltech.content.transfer_engineer.id_type = audiomodels.TransferEngineer.LDAP_ID_TYPE
        obj.digitaltech.content.create_codec_creator()
        obj.digitaltech.content.codec_creator.id = '1'
        # pre-populate rights metadata
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = 10   # undetermined
        obj.rights.content.access_status.text = 'Rights status unknown; no access to files or metadata'
        obj.rights.content.copyright_holder_name = 'User, Example'
        obj.rights.content.copyright_date = '1978'
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)
        
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        edit_url = reverse('audio:edit', args=[obj.pid])

        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assert_(isinstance(response.context['form'], audioforms.AudioObjectEditForm),
                "MODS EditForm is set in response context")
        self.assert_(isinstance(response.context['form'].object_instance, audiomodels.AudioObject),
                "form instance is an AudioObject")
        self.assertContains(response, self.rushdie.pid)
        self.assertContains(response, self.esterbrook.pid)
        self.assertContains(response, self.englishdocs.pid)

        initial_data = response.context['form'].mods.initial
        item_mods = obj.mods.content
        self.assertEqual(item_mods.title, initial_data['title'],
            'object MODS title is pre-populated in form initial data')
        self.assertEqual(item_mods.general_note.text, initial_data['general_note-text'],
            'object MODS general note is pre-populated in form initial data')
        self.assertEqual(item_mods.part_note.text, initial_data['part_note-text'],
            'object MODS part note is pre-populated in form initial data')
        self.assertEqual(item_mods.origin_info.created[0].date, 
            initial_data['origin_info-created-0-date'],
            'object MODS date created is pre-populated in form initial data')
        self.assertEqual(item_mods.origin_info.issued[0].date,
            initial_data['origin_info-issued-0-date'],
            'object MODS date issued is pre-populated in form initial data')
        self.assertEqual(item_mods.dm1_id, initial_data['dm1_id'],
            'object MODS DM1 id is pre-populated in form initial data')
        self.assertEqual(item_mods.dm1_other_id, initial_data['dm1_other_id'],
            'object MODS DM1 other id is pre-populated in form initial data')
        self.assertEqual(item_mods.resource_type, initial_data['resource_type'],
            'object MODS resource type is pre-populated in form initial data')
        self.assertEqual(item_mods.dm1_abstract_note.text, initial_data['dm1_abstract_note-text'],
            'object MODS DM1 abstract note is pre-populated in form initial data')
        self.assertEqual(item_mods.dm1_content_note.text, initial_data['dm1_content_note-text'],
            'object MODS DM1 content note is pre-populated in form initial data')
        self.assertEqual(item_mods.dm1_toc_note.text, initial_data['dm1_toc_note-text'],
            'object MODS DM1 toc note is pre-populated in form initial data')
        # some migrated fields are display-only, not part of the form
        for name in item_mods.names:
            self.assertContains(response, name.name_parts[0].text,
               msg_prefix='creator name part %s should display on the edit form' % name.name_parts[0].text)
            self.assertContains(response, name.roles[0].text,
               msg_prefix='creator name role %s should display on the edit form' % name.roles[0].text)
            self.assertContains(response, name.type,
               msg_prefix='creator name type %s should display on the edit form' % name.type)
            self.assertContains(response, name.authority,
               msg_prefix='creator name authority %s should display on the edit form' % name.authority)
        for genre in item_mods.genres:
            expected_val = '%s [%s]' % (genre.text, genre.authority)
            self.assertContains(response, expected_val,
                msg_prefix='response should include genre text & authority %s' % expected_val)
        for lang in item_mods.languages:
            expected_val = '%s [%s]' % (lang.terms[0].text, lang.terms[0].authority)
            self.assertContains(response, expected_val,
                msg_prefix='response should include language value and authority %s' % expected_val)

        # test subjects by type in order: geographic, topic, title, name
        expected_val = '<b>Geographic:</b> %s' % item_mods.subjects[0].geographic
        self.assertContains(response, expected_val,
           msg_prefix='response should include geographic subject %s' % expected_val)
        expected_val = '[%s]' % item_mods.subjects[0].authority
        self.assertContains(response, expected_val,
           msg_prefix='response should include geographic subject authority %s' % expected_val)
        expected_val = '<b>Topic:</b> %s' % item_mods.subjects[1].topic
        self.assertContains(response, expected_val,
           msg_prefix='response should include topic subject %s' % expected_val)
        expected_val = '[%s]' % item_mods.subjects[1].authority
        self.assertContains(response, expected_val,
           msg_prefix='response should include topic subject authority %s' % expected_val)
        expected_val = '<b>Title:</b> %s' % item_mods.subjects[2].title
        self.assertContains(response, expected_val,
           msg_prefix='response should include title subject %s' % expected_val)
        expected_val = '[%s]' % item_mods.subjects[2].authority
        self.assertContains(response, expected_val,
           msg_prefix='response should include title subject authority %s' % expected_val)
        expected_val = '<b>Name:</b> %s' % unicode(item_mods.subjects[3].name)
        self.assertContains(response, expected_val,
           msg_prefix='response should include name subject %s' % expected_val)
        expected_val = '[%s]' % item_mods.subjects[3].authority
        self.assertContains(response, expected_val,
           msg_prefix='response should include name subject authority %s' % expected_val)
        
        # source tech from object in initial data
        initial_data = response.context['form'].sourcetech.initial
        item_st = obj.sourcetech.content
        self.assertEqual(item_st.note, initial_data['note'])
        self.assertEqual(item_st.related_files, initial_data['related_files'])
        self.assertEqual(item_st.sound_characteristics, initial_data['sound_characteristics'])
        # semi-custom fields based on multiple values in initial data
        self.assertEqual('|'.join([item_st.speed.aspect, item_st.speed.value,
                                  item_st.speed.unit]), initial_data['_speed'])
        self.assertEqual(item_st.reel_size.value, initial_data['reel'])
        # digital tech from object initial data
        initial_data = response.context['form'].digitaltech.initial
        item_dt = obj.digitaltech.content
        self.assertEqual(item_dt.codec_quality, initial_data['codec_quality'])
        self.assertEqual(item_dt.note, initial_data['note'])
        self.assertEqual(item_dt.digitization_purpose, initial_data['digitization_purpose'])
        self.assertEqual('%s|%s' % (audiomodels.TransferEngineer.LDAP_ID_TYPE, ldap_user.username),
                         initial_data['engineer'])
        self.assertEqual(item_dt.codec_creator.id, initial_data['hardware'])
        # rights in initial data
        initial_data = response.context['form'].rights.initial
        item_rights = obj.rights.content
        self.assertEqual(item_rights.access_status.code, initial_data['access'])
        self.assertEqual(item_rights.copyright_holder_name, initial_data['copyright_holder_name'])
        self.assertEqual(item_rights.copyright_date, initial_data['copyright_date'])

        # POST data to update audio object in fedora
        audio_data = {'collection': self.rushdie.uri,
                    'mods-title': 'new title',
                    'mods-note-label' : 'a general note',
                    'mods-general_note-text': 'remember to ...',
                    'mods-part_note-text': 'side A',
                    'mods-resource_type': 'sound recording',
                    # 'management' form data is required for django to process formsets/subforms
                    'mods-origin_info-issued-INITIAL_FORMS': '0',
                    'mods-origin_info-issued-TOTAL_FORMS': '1',
                    'mods-origin_info-issued-MAX_NUM_FORMS': '',
                    'mods-origin_info-issued-0-date_year': '2010',
                    'mods-origin_info-issued-0-date_month': '01',
                    'mods-origin_info-issued-0-date_day': '11',
                    'mods-origin_info-created-INITIAL_FORMS': '0',
                    'mods-origin_info-created-TOTAL_FORMS': '1',
                    'mods-origin_info-created-MAX_NUM_FORMS': '',
                    'mods-origin_info-created-0-date_year': '1980',
                    'mods-origin_info-created-0-date_month': '03',
                    # source-tech data now required for form submission
                    'st-note': 'general note',
                    'st-related_files': '1-3',
                    'st-conservation_history': 'on loan',
                    'st-sublocation': 'box 2',
                    'st-form': 'audio cassette',
                    'st-sound_characteristics': 'mono',
                    'st-housing': 'cardboard box',
                    'st-stock': '60 minute cassette',
                    'st-reel': '3',
                    'st-_speed': 'tape|15/16|inches/sec',
                    # digital-tech data
                    'dt-digitization_purpose': 'patron request',
                    'dt-engineer': '%s|%s' % (audiomodels.TransferEngineer.LDAP_ID_TYPE,
                                              ldap_user.username),
                    'dt-hardware': '3',
                    # rights metadata
                    'rights-access': '8',       # public domain
                    'rights-copyright_holder_name': 'Mouse, Mickey',
                    'rights-copyright_date_year': '1942',
                    'rights-block_external_access': '1',
                    'rights-ip_note': 'Written permission required',
        }
        response = self.client.post(edit_url, audio_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_(messages[0].startswith("Successfully updated"),
            "successful save message set in response context")
        # currently redirects to audio index
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "successful save redirects to audio index page")
        expected = 303      # redirect
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (successfully saved)'  % \
            (expected, code, edit_url))

        # retrieve the modified object from Fedora to check for updates
        repo = Repository()
        updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(audio_data['mods-title'], updated_obj.mods.content.title,
            'mods title in fedora matches posted title')        
        self.assertEqual(audio_data['mods-general_note-text'], updated_obj.mods.content.general_note.text,
            'mods general note text in fedora matches posted note text')
        self.assertEqual(audio_data['mods-part_note-text'], updated_obj.mods.content.part_note.text,
            'mods part note text in fedora matches posted note text')
        # date issued and created are multi-part fields
        issued = '-'.join([audio_data['mods-origin_info-issued-0-date_year'],
            audio_data['mods-origin_info-issued-0-date_month'],
            audio_data['mods-origin_info-issued-0-date_day']])
        self.assertEqual(issued, updated_obj.mods.content.origin_info.issued[0].date,
            'mods issued date in fedora matches posted issued date')
        created = '-'.join([audio_data['mods-origin_info-created-0-date_year'],
            audio_data['mods-origin_info-created-0-date_month']])
        self.assertEqual(created, updated_obj.mods.content.origin_info.created[0].date,
            'mods date created in fedora matches posted date created')
        self.assertEqual(self.rushdie.uriref, updated_obj.collection_uri,
            'collection id in fedora matches posted collection')

        # check that source tech fields were updated correctly
        st = updated_obj.sourcetech.content
        self.assertEqual(audio_data['st-note'], st.note)
        self.assertEqual(audio_data['st-related_files'], st.related_files)
        self.assertEqual(audio_data['st-conservation_history'], st.conservation_history)
        self.assertEqual(audio_data['st-form'], st.form)
        self.assertEqual(audio_data['st-sound_characteristics'], st.sound_characteristics)
        self.assertEqual(audio_data['st-housing'], st.housing)
        self.assertEqual(audio_data['st-stock'], st.stock)
        # reel size has custom logic
        self.assertEqual(audio_data['st-reel'], st.reel_size.value)
        self.assertEqual('inches', st.reel_size.unit)
        # speed has custom logic - 15/16 inches/sec gets split into two fields
        self.assertEqual('tape', st.speed.aspect)
        self.assertEqual('15/16', st.speed.value)
        self.assertEqual('inches/sec', st.speed.unit)

        # check that digital tech fields were updated correctly
        dt = updated_obj.digitaltech.content
        self.assertEqual(audio_data['dt-digitization_purpose'], dt.digitization_purpose)
        self.assertEqual(audiomodels.TransferEngineer.LDAP_ID_TYPE, dt.transfer_engineer.id_type)
        self.assertEqual(ldap_user.username, dt.transfer_engineer.id)
        self.assertEqual(ldap_user.get_full_name(), dt.transfer_engineer.name)
        # codec creator - used id 3, which has two hardware fields
        hardware, software, version = audiomodels.CodecCreator.configurations[audio_data['dt-hardware']]
        self.assertEqual(audio_data['dt-hardware'], dt.codec_creator.id)
        self.assertEqual(hardware[0], dt.codec_creator.hardware_list[0])
        self.assertEqual(hardware[1], dt.codec_creator.hardware_list[1])
        self.assertEqual(software, dt.codec_creator.software)
        self.assertEqual(version, dt.codec_creator.software_version)

        # change data and confirm codec creator is updated correctly
        data = audio_data.copy()
        data['dt-hardware'] = '4' # only one hardware, no software version
        response = self.client.post(edit_url, data)
        # get the latest copy of the object 
        updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
        dt = updated_obj.digitaltech.content
        # codec creator - id 4 only has one two hardware and no software version
        hardware, software, version = audiomodels.CodecCreator.configurations[data['dt-hardware']]
        self.assertEqual(data['dt-hardware'], dt.codec_creator.id)
        self.assertEqual(hardware[0], dt.codec_creator.hardware_list[0])
        self.assertEqual(1, len(dt.codec_creator.hardware_list)) # should only be one now
        self.assertEqual(software, dt.codec_creator.software)
        self.assertEqual(None, dt.codec_creator.software_version)

        # check that rights fields were updated correctly
        rights = updated_obj.rights.content
        self.assertEqual(audio_data['rights-access'], rights.access_status.code)
        self.assertTrue(rights.access_status.text.endswith('in public domain'))
        self.assertEqual(audio_data['rights-copyright_holder_name'], rights.copyright_holder_name)
        self.assertEqual(audio_data['rights-copyright_date_year'], rights.copyright_date)
        self.assertTrue(rights.block_external_access)
        self.assertEqual(audio_data['rights-ip_note'], rights.ip_note)

        # test logic for save and continue editing
        data = audio_data.copy()
        data['_save_continue'] = True   # simulate submit via 'save and continue' button
        response = self.client.post(edit_url, data)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_(messages[0].startswith("Successfully updated"),
            'successful audio update message displayed to user on save and continue editing')
        self.assert_(isinstance(response.context['form'], audioforms.AudioObjectEditForm),
                "MODS EditForm is set in response context after save and continue editing")

        # sending blank origin info dates should remove them from mods
        data = audio_data.copy()
        data.update({
            'mods-origin_info-issued-0-date_year': '',
            'mods-origin_info-issued-0-date_month': '',
            'mods-origin_info-issued-0-date_day': '',
            'mods-origin_info-created-INITIAL_FORMS': '0',
            'mods-origin_info-created-TOTAL_FORMS': '1',
            'mods-origin_info-created-MAX_NUM_FORMS': '',
            'mods-origin_info-created-0-date_year': '',
            'mods-origin_info-created-0-date_month': '',
        })
        response = self.client.post(edit_url, data)
        # get the latest copy of the object
        updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
        self.assertFalse(updated_obj.mods.content.origin_info)
        # get a page to clear any session messages
        response = self.client.get(edit_url)
        
        # validation errors - post incomplete/bogus data & check for validation errors
        data = audio_data.copy()
        data.update({
            'mods-title': '',       # title is required
            'mods-origin_info-issued-0-date_year': 'abcf',  # not a year 
        })
        response = self.client.post(edit_url, data)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_(messages[0].startswith("Your changes were not saved due to a validation error"),
            "form validation error message set in response context")
        self.assertContains(response, 'This field is required',
            msg_prefix='required error message displayed (empty title)')
        self.assertContains(response, 'Enter a date in one of these formats',
            msg_prefix='date validation error message displayed')

        # sending blank engineer should remove from digital tech
        data = audio_data.copy()
        data['dt-engineer'] = ''
        response = self.client.post(edit_url, data)
        # get the latest copy of the object
        updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
        self.assertFalse(updated_obj.digitaltech.content.transfer_engineer)

        # test editing record with migrated legacy DM user transfer engineer
        # engineer & codec creator are initialized based on id values
        obj.digitaltech.content.create_transfer_engineer()
        obj.digitaltech.content.transfer_engineer.id = 2100
        obj.digitaltech.content.transfer_engineer.id_type = audiomodels.TransferEngineer.DM_ID_TYPE
        obj.digitaltech.content.transfer_engineer.name = 'Historic User'
        obj.save()
        # get the form - non-LDAP user should be listed & selected
        response = self.client.get(edit_url)
        transf_eng = obj.digitaltech.content.transfer_engineer
        select_id = '%s|%s' % (transf_eng.id_type, transf_eng.id)
        self.assertContains(response, select_id,
            msg_prefix='records with a legacy DM transfer engineer should include the legacy id options')
        self.assertContains(response, transf_eng.name,
            msg_prefix='records with a legacy DM transfer engineer should include the legacy name in options')
        self.assertContains(response, '<option value="%s|%s" selected="selected">%s' % \
           (transf_eng.id_type, transf_eng.id, transf_eng.name),
            msg_prefix='records with a legacy DM transfer engineer should display the legacy id as selected')
        # post the legacy user id - data should look as before
        data = audio_data.copy()
        data['dt-engineer'] = select_id
        response = self.client.post(edit_url, data)
        # id type, id, and name should all be set to legacy user information
        updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(updated_obj.digitaltech.content.transfer_engineer.id,
                         obj.digitaltech.content.transfer_engineer.id)
        self.assertEqual(updated_obj.digitaltech.content.transfer_engineer.id_type,
                         obj.digitaltech.content.transfer_engineer.id_type)
        self.assertEqual(updated_obj.digitaltech.content.transfer_engineer.name,
                         obj.digitaltech.content.transfer_engineer.name)


        # force a schema-validation error (shouldn't happen normally)
        # NOTE: invalid mods test should happen after all other tests that modify this object
        obj.mods.content = load_xmlobject_from_string(TestMods.invalid_xml, audiomodels.AudioMods)
        obj.save("schema-invalid MODS")
        response = self.client.post(edit_url, audio_data)
        self.assertContains(response, '<ul class="errorlist">')
        
        # edit non-existent record should 404
        fakepid = 'bogus-pid:1'
        edit_url = reverse('audio:edit', args=[fakepid])
        response = self.client.get(edit_url)  # follow redirect to check error message
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (edit non-existent object)' \
                % (expected, got, edit_url))

        # attempt to edit non-audio object should 404
        edit_url = reverse('audio:edit', args=[self.rushdie.pid])
        response = self.client.get(edit_url)
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (edit non-audio object)' \
                % (expected, got, edit_url))

        # how to test fedora permission denied scenario?

    def test_edit_min_fields(self):
        # verify that we can get away with filling in only required fields.

        # create a test audio object to edit
        obj = audiomodels.AudioObject.init_from_file(wav_filename, "my audio test object")
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)

        # retrieve test user object to use for transfer engineer - also used to test
        ldap_user = User.objects.get(username='ldap_user')

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        edit_url = reverse('audio:edit', args=[obj.pid])

        # POST data to update audio object in fedora
        audio_data = {'collection': self.rushdie.uri,
                    'mods-title': 'new title',
                    'mods-resource_type': 'sound recording',
                    # 'management' form data is required for django to process formsets/subforms
                    'mods-origin_info-issued-INITIAL_FORMS': '0',
                    'mods-origin_info-issued-TOTAL_FORMS': '0',
                    'mods-origin_info-issued-MAX_NUM_FORMS': '',
                    'mods-origin_info-created-INITIAL_FORMS': '0',
                    'mods-origin_info-created-TOTAL_FORMS': '0',
                    'mods-origin_info-created-MAX_NUM_FORMS': '',
                    'st-sublocation': 'box 3',
                    'st-housing': 'other',
                    'st-_speed': 'other|other|other',
                    # digital-tech data
                    'dt-digitization_purpose': 'avoid nuclear war',
                    'dt-engineer': '%s|%s' % (audiomodels.TransferEngineer.LDAP_ID_TYPE,
                                              ldap_user.username),
                    'dt-hardware': '3',
                    # rights metadata
                    'rights-access': 8,   # public domain
        }

        response = self.client.post(edit_url, audio_data, follow=True)

        # currently redirects to audio index
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "successful save redirects to audio index page")

        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_(messages[0].startswith("Successfully updated"),
            "successful save message set in response context")

        # we'll assume (for now) that the fields were saved correctly: this
        # should be verified in test_edit

    def test_raw_datastream(self):
        # create a test audio object to edit
        obj = audiomodels.AudioObject.init_from_file(wav_filename, "my audio test object")
        obj.mods.content.title = 'test audio object'
        obj.sourcetech.content.note = 'source note'
        # pre-populate digital tech metadata
        obj.digitaltech.content.date_captured = '2008'
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)

        self.client.login(**ADMIN_CREDENTIALS)

        # MODS
        ds_url = reverse('audio:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'MODS'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (MODS datastream)' \
                % (expected, got, ds_url))
        expected, got = 'text/xml', response['Content-Type']
        self.assertEqual(expected, got,
            'Expected %s but returned %s for mimetype on %s (MODS datastream)' \
                % (expected, got, ds_url))
        self.assertContains(response, '<mods:title>%s</mods:title>' % \
                            obj.mods.content.title)
        # RELS-EXT
        ds_url = reverse('audio:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'RELS-EXT'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (RELS-EXT datastream)' \
                % (expected, got, ds_url))
        expected, got = 'application/rdf+xml', response['Content-Type']
        self.assertEqual(expected, got,
            'Expected %s but returned %s for mimetype on %s (RELS-EXT datastream)' \
                % (expected, got, ds_url))
        self.assertContains(response, obj.AUDIO_CONTENT_MODEL)
        # Source Tech
        ds_url = reverse('audio:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'SourceTech'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (SourceTech datastream)' \
                % (expected, got, ds_url))
        expected, got = 'text/xml', response['Content-Type']
        self.assertEqual(expected, got,
            'Expected %s but returned %s for mimetype on %s (SourceTech datastream)' \
                % (expected, got, ds_url))
        self.assertContains(response, '<st:sourcetech')
        self.assertContains(response, obj.sourcetech.content.note)
        # Digital Tech
        ds_url = reverse('audio:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'DigitalTech'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (DigitalTech datastream)' \
                % (expected, got, ds_url))
        expected, got = 'text/xml', response['Content-Type']
        self.assertEqual(expected, got,
            'Expected %s but returned %s for mimetype on %s (DigitalTech datastream)' \
                % (expected, got, ds_url))
        self.assertContains(response, '<dt:digitaltech')
        self.assertContains(response, obj.digitaltech.content.date_captured)

        # not testing bogus datastream id because url config currently does not
        # allow it

         # non-existent record should 404
        fakepid = 'bogus-pid:1'
        ds_url = reverse('audio:raw-ds', kwargs={'pid': fakepid, 'dsid': 'MODS'})
        response = self.client.get(ds_url)  # follow redirect to check error message
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (datastream on non-existent object)' \
                % (expected, got, ds_url))

        # object without requested datastream 404
        # (currently view does not check cmodels for efficiency reasons)
        ds_url = reverse('audio:raw-ds', kwargs={'pid': self.rushdie.pid, 'dsid': 'SourceTech'})
        response = self.client.get(ds_url)
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (datastream non-audio object)' \
                % (expected, got, ds_url))



    def test_podcast_feed(self):
        feed_url = reverse('audio:podcast-feed', args=[1])

        # create some test objects to show up in the feed
        repo = Repository()
        obj = repo.get_object(type=audiomodels.AudioObject)
        obj.mods.content.title = 'Dylan Thomas reads anthology'
        obj.mods.content.create_part_note()
        obj.mods.content.part_note.text = 'Side A'
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1976-05'))
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = 8 # public domain
        obj.collection_uri = self.rushdie.uri
        obj.compressed_audio.content = open(mp3_filename)
        obj.save()
        obj2 = repo.get_object(type=audiomodels.AudioObject)
        obj2.mods.content.title = 'Patti Smith Live in New York'
        obj2.compressed_audio.content = open(mp3_filename)
        obj2.rights.content.create_access_status()
        obj2.rights.content.access_status.code = 8 # public domain
        obj2.collection_uri = self.esterbrook.uri
        obj2.save()
        obj3 = repo.get_object(type=audiomodels.AudioObject)
        obj3.mods.content.title = 'No Access copy'
        obj3.rights.content.create_access_status()
        obj3.rights.content.access_status.code = 8 # public domain
        obj3.save()
        obj4 = repo.get_object(type=audiomodels.AudioObject)
        obj4.rights.content.create_access_status()
        obj4.rights.content.access_status.code = 10 # undetermined
        obj4.compressed_audio.content = open(mp3_filename)
        obj4.save()
        obj5 = repo.get_object(type=audiomodels.AudioObject)
        obj5.compressed_audio.content = open(mp3_filename)
        obj5.save()
        obj6 = repo.get_object(type=audiomodels.AudioObject)
        obj6.mods.content.title = 'Moses reads Ten Commandments'
        obj6.compressed_audio.content = open(mp3_filename)
        obj6.rights.content.create_access_status()
        obj6.rights.content.access_status.code = 8 # public domain
        obj6.rights.content.block_external_access = True
        obj6.collection_uri = self.esterbrook.uri
        obj6.save()
        # add pids to list for clean-up in tearDown
        self.pids.extend([obj.pid, obj2.pid, obj3.pid, obj4.pid, obj5.pid,
                          obj6.pid])

        response = self.client.get(feed_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                             % (expected, code, feed_url))        
        self.assertContains(response, obj.pid,
            msg_prefix='pid for first test object should be included in feed')
        self.assertContains(response, obj2.pid,
            msg_prefix='pid for second test object should be included in feed')
        self.assertNotContains(response, obj3.pid,
            msg_prefix='pid for test object with no access copy should NOT be included in feed')
        self.assertNotContains(response, obj4.pid,
            msg_prefix='pid for test object with restricted access rights should NOT be included in feed')
        self.assertNotContains(response, obj4.pid,
            msg_prefix='pid for test object without rights information should NOT be included in feed')
        self.assertNotContains(response, obj6.pid,
            msg_prefix='pid for test object with negative override should NOT be included in feed')
        self.assertContains(response, obj.mods.content.title,
            msg_prefix='title for first test object should be included in feed')
        self.assertContains(response, obj2.mods.content.title,
            msg_prefix='title for second test object should be included in feed')
        self.assertContains(response, '%s - %s' % (self.rushdie.mods.content.source_id,
            self.rushdie.mods.content.title),
            msg_prefix='collection title & number for first test object should be included in feed')
        self.assertContains(response, '%s - %s' % (self.esterbrook.mods.content.source_id,
            self.esterbrook.mods.content.title),
            msg_prefix='collection title & number for second test object should be included in feed')         
        self.assertContains(response, obj.mods.content.part_note.text,
            msg_prefix='part note for first test object should be included in feed')
        self.assertContains(response, 'May 1976',
            msg_prefix='dateIssued should be included in feed')

        # test pagination
        settings.MAX_ITEMS_PER_PODCAST_FEED = 1
        response = self.client.get(feed_url)
        self.assertContains(response, obj.pid,
            msg_prefix='pid for first test object should be included in paginated feed')
        self.assertNotContains(response, obj2.pid,
            msg_prefix='pid for second test object should not be included in paginated feed')
        feed2_url = reverse('audio:podcast-feed', args=[2])
        response = self.client.get(feed2_url)
        self.assertNotContains(response, obj.pid,
            msg_prefix='pid for first test object should not be included in second paginated feed')
        self.assertContains(response, obj2.pid,
            msg_prefix='pid for second test object should be included in second paginated feed')

    def test_podcast_feed_list(self):
        feed_list_url = reverse('audio:feed-list')
        # must be logged in as staff to view
        self.client.login(**ADMIN_CREDENTIALS)

        # create some test objects to show up in the feeds
        repo = Repository()
        obj = repo.get_object(type=audiomodels.AudioObject)
        obj.mods.content.title = 'Dylan Thomas reads anthology'
        obj.mods.content.create_part_note()
        obj.mods.content.part_note.text = 'Side A'
        obj.collection_uri = self.rushdie.uri
        obj.compressed_audio.content = open(mp3_filename)
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1976-05'))
        obj.save()
        obj2 = repo.get_object(type=audiomodels.AudioObject)
        obj2.mods.content.title = 'Patti Smith Live in New York'
        obj2.compressed_audio.content = open(mp3_filename)
        obj2.collection_uri = self.esterbrook.uri
        obj2.save()
        # add pids to list for clean-up in tearDown
        self.pids.extend([obj.pid, obj2.pid])

        # set high enough we should only have one feed
        settings.MAX_ITEMS_PER_PODCAST_FEED = 2000
        response = self.client.get(feed_list_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s'
                             % (expected, code, feed_list_url))
        self.assertContains(response, reverse('audio:podcast-feed', args=[1]))
        self.assertNotContains(response, reverse('audio:podcast-feed', args=[2]))
        # set pagination low enough that we get more than one feed
        settings.MAX_ITEMS_PER_PODCAST_FEED = 1
        response = self.client.get(feed_list_url)
        self.assertContains(response, reverse('audio:podcast-feed', args=[1]))
        self.assertContains(response, reverse('audio:podcast-feed', args=[2]))

# TODO: mock out the fedora connection and find a way to verify that we
# handle fedora outages appropriately

# tests for MODS XmlObject
# FIXME: mods objects no longer part of keep.audio - where should these tests live?
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
        self.assert_(isinstance(self.mods.origin_info.created[0], mods.DateCreated))
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
        self.assertEqual('remember to...', self.mods.note.text)
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
        mymods.create_name()
        mymods.name.type = 'personal'
        mymods.name.authority = 'local'
        mymods.name.name_parts.extend([mods.NamePart(type='family', text='Schmoe'),
                                    mods.NamePart(type='given', text='Joe')])
        mymods.name.roles.append(mods.Role(type='text', authority='local',
                                        text='Test Subject'))
        mymods.create_note()
        mymods.note.type = 'general'
        mymods.note.text = 'general note'
        mymods.create_origin_info()
        mymods.origin_info.created.append(mods.DateCreated(date='2001-10-02'))
        mymods.origin_info.issued.append(mods.DateIssued(date='2001-12-01'))
        mymods.create_record_info()
        mymods.record_info.record_id = 'id:1'
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

class TestModsTypedNote(TestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        self.note = mods.TypedNote()
        self.note.type = 'general'

    def test_is_empty(self):
        # initial note object should be considered empty (type only)
        self.assertTrue(self.note.is_empty())

    def test_is_empty__extra_attribute(self):
        # set an attribute besides type
        self.note.label = "Note"        
        self.assertFalse(self.note.is_empty())

    def test_is_empty_text(self):
        # set text value
        self.note.text = 'here is some general info'
        self.assertFalse(self.note.is_empty())

class TestModsDate(TestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        self.date = mods.DateCreated() 

    def test_is_empty(self):
        # starting fixture should be considered empty (no date)
        self.assertTrue(self.date.is_empty())

    def test_is_empty_with_attributes(self):
        # should be empty with attributes but no date value
        self.date.keydate = True
        self.assertTrue(self.date.is_empty())

    def test_is_empty_date_value(self):
        # set date value
        self.date.date = '1066'
        self.assertFalse(self.date.is_empty())

class TestModsOriginInfo(TestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        self.origin_info = mods.OriginInfo()

    def test_is_empty(self):
        # starting object should be considered empty (no date elements at all)
        self.assertTrue(self.origin_info.is_empty())

    def test_is_empty_with_empty_dates(self):
        self.origin_info.created.append(mods.DateCreated())
        self.assertTrue(self.origin_info.is_empty())
        self.origin_info.issued.append(mods.DateIssued())
        self.assertTrue(self.origin_info.is_empty())

    def test_is_empty_date_values(self):
        self.origin_info.created.append(mods.DateCreated(date='300'))
        self.assertFalse(self.origin_info.is_empty())
        self.origin_info.issued.append(mods.DateIssued(date='450'))
        self.assertFalse(self.origin_info.is_empty())



class SourceTechTest(TestCase):
    FIXTURE = '''<?xml version="1.0" encoding="UTF-8"?>
<st:sourcetech version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:st="http://pid.emory.edu/ns/2010/sourcetech"  xsi="http://pid.emory.edu/ns/2010/sourcetech/v1/sourcetech-1.xsd">
    <st:note type="general">Right channel has squeal throughout recording.</st:note>
    <st:note type="relatedFiles">a89, g3jll, 443b</st:note>
    <st:note type="conservationHistory">Repaired broken tape 2010-03-12</st:note>
    <st:speed>
        <st:measure type="speed" unit="inches/sec" aspect="tape">1.875</st:measure>
    </st:speed>
    <st:sublocation>box 3, folder 7</st:sublocation>
    <st:form type="sound">audio cassette</st:form>
    <st:soundChar>mono</st:soundChar>
    <st:stock>IMT C-60</st:stock>
    <st:housing type="sound">plastic container</st:housing>
    <st:reelSize>
        <st:measure type="diameter" unit="inches" aspect="reel size">3</st:measure>
    </st:reelSize>
    <st:note type="technical">May be a duplicate of 222</st:note>
</st:sourcetech>'''

    def setUp(self):
        self.sourcetech = load_xmlobject_from_string(self.FIXTURE, audiomodels.SourceTech)

    def test_init_types(self):
        self.assert_(isinstance(self.sourcetech, audiomodels.SourceTech))
        self.assert_(isinstance(self.sourcetech.speed, audiomodels.SourceTechMeasure))
        self.assert_(isinstance(self.sourcetech.reel_size, audiomodels.SourceTechMeasure))

    def test_fields(self):
        # check field values correctly accessible from fixture
        self.assertEqual('Right channel has squeal throughout recording.', self.sourcetech.note_list[0])
        self.assertEqual('a89, g3jll, 443b', self.sourcetech.related_files)
        self.assertEqual('Repaired broken tape 2010-03-12', self.sourcetech.conservation_history_list[0])
        self.assertEqual('inches/sec', self.sourcetech.speed.unit)
        self.assertEqual('tape', self.sourcetech.speed.aspect)
        self.assertEqual('1.875', self.sourcetech.speed.value)
        self.assertEqual(u'1.875', unicode(self.sourcetech.speed))
        self.assertEqual('box 3, folder 7', self.sourcetech.sublocation)
        self.assertEqual('audio cassette', self.sourcetech.form)
        self.assertEqual('mono', self.sourcetech.sound_characteristics)
        self.assertEqual('IMT C-60', self.sourcetech.stock)
        self.assertEqual('plastic container', self.sourcetech.housing)
        self.assertEqual('inches', self.sourcetech.reel_size.unit)
        self.assertEqual('reel size', self.sourcetech.reel_size.aspect)
        self.assertEqual('3', self.sourcetech.reel_size.value)
        self.assertEqual(u'3', unicode(self.sourcetech.reel_size))
        self.assertEqual('May be a duplicate of 222', self.sourcetech.technical_note[0])

    def test_create(self):
        # test creating sourcetech metadata from scratch
        st = audiomodels.SourceTech()
        st.note_list.append('general note')
        st.related_fields = '1, 2, 3'
        st.conservation_history_list.append('loaned for digitization')
        st.create_speed()
        st.speed.unit = 'rpm'
        st.speed.aspect = 'phonograph disc'
        st.speed.value = '120'
        st.sublocation = 'box 2'
        st.form = 'CD'
        st.sound_characteristics = 'stereo'
        st.stock = '60-min cassette'
        st.housing = 'jewel case'
        st.create_reel_size()
        st.reel_size.unit = 'inches'
        st.reel_size.value = '5'
        st.technical_note.append('Recorded at Rockhill recording studio.')

        # for now, just testing that all fields can be set without error
        self.assert_('<st:sourcetech' in st.serialize())

        # TODO: validate against schema when we have one

class DigitalTechTest(TestCase):
    FIXTURE = '''<?xml version="1.0" encoding="UTF-8"?>
<dt:digitaltech version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dt="http://pid.emory.edu/ns/2010/digitaltech"  xsi="http://pid.emory.edu/ns/2010/digitaltech/v1/digitaltech-1.xsd">
    <dt:dateCaptured encoding="w3cdtf">2010-11-29T05:13:01-05:00</dt:dateCaptured>
    <dt:codecQuality>lossless</dt:codecQuality>
    <dt:duration>
        <dt:measure type="time" unit="seconds" aspect="duration of playing time">186</dt:measure>
    </dt:duration>
    <dt:note type="general">Interview ends at 00:33:50.  Tape silent until end.</dt:note>
    <dt:note type="purpose of digitization">patron request</dt:note>
    <dt:codecCreator>
        <dt:codecCreatorID>1</dt:codecCreatorID>
        <dt:hardware>MAC G4</dt:hardware>
        <dt:software>DigiDesign ProTools LE</dt:software>
        <dt:softwareVersion>5.2</dt:softwareVersion>
    </dt:codecCreator>
    <dt:transferEngineer id="tbunn" idType="ldap">Trey Bunn</dt:transferEngineer>
</dt:digitaltech>'''

    def setUp(self):
        self.digitaltech = load_xmlobject_from_string(self.FIXTURE, audiomodels.DigitalTech)

    def test_init_types(self):
        self.assert_(isinstance(self.digitaltech, audiomodels.DigitalTech))
        self.assert_(isinstance(self.digitaltech.transfer_engineer, audiomodels.TransferEngineer))
        self.assert_(isinstance(self.digitaltech.codec_creator, audiomodels.CodecCreator))

    def test_fields(self):
        # check field values correctly accessible from fixture
        self.assertEqual('2010-11-29T05:13:01-05:00', self.digitaltech.date_captured)
        self.assertEqual('lossless', self.digitaltech.codec_quality)
        self.assertEqual(186, self.digitaltech.duration)
        self.assertEqual('Interview ends at 00:33:50.  Tape silent until end.',
            self.digitaltech.note)
        self.assertEqual('patron request', self.digitaltech.digitization_purpose)
        self.assertEqual('1', self.digitaltech.codec_creator.id)
        self.assertEqual('MAC G4', self.digitaltech.codec_creator.hardware)
        self.assertEqual('DigiDesign ProTools LE', self.digitaltech.codec_creator.software)
        self.assertEqual('5.2', self.digitaltech.codec_creator.software_version)
        self.assertEqual('tbunn', self.digitaltech.transfer_engineer.id)
        self.assertEqual('ldap', self.digitaltech.transfer_engineer.id_type)
        self.assertEqual('Trey Bunn', self.digitaltech.transfer_engineer.name)

    def test_create(self):
        # test creating digitaltech metadata from scratch
        dt = audiomodels.DigitalTech()
        dt.date_captured = '2010-01-01'
        dt.codec_quality = 'lossy'
        dt.duration = 33
        dt.note = 'Transferred slowly'
        dt.digitization_purpose = 'Dawson exhibit'
        dt.create_codec_creator()
        dt.codec_creator.id = '2'
        dt.codec_creator.hardware = 'Dell Optiplex'
        dt.codec_creator.software = 'iTunes'
        dt.codec_creator.sotfware_version = '9'

        # for now, just testing that all fields can be set without error
        self.assert_('<dt:digitaltech' in dt.serialize())

        # TODO: validate against schema when we have one


class RightsXmlTest(TestCase):
    FIXTURE =  '''<?xml version="1.0" encoding="UTF-8"?>
<rt:rights version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rt="http://pid.emory.edu/ns/2010/rights"  xsi="http://pid.emory.edu/ns/2010/sourcetech/v1/rights-1.xsd">
    <rt:accessStatus code="2">Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement</rt:accessStatus>
    <rt:copyrightholderName>Hughes, Carol</rt:copyrightholderName>
    <rt:copyrightDate encoding="w3cdtf">1923</rt:copyrightDate>
    <rt:ipNotes>Written permission required.</rt:ipNotes>
</rt:rights>'''

    def setUp(self):
        self.rights = load_xmlobject_from_string(self.FIXTURE, audiomodels.Rights)

    def test_init_types(self):
        self.assert_(isinstance(self.rights, audiomodels.Rights))
        self.assert_(isinstance(self.rights.access_status, audiomodels.AccessStatus))

    def test_fields(self):
        # check field values correctly accessible from fixture
        self.assertEqual('2', self.rights.access_status.code)
        self.assertEqual('Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement',
            self.rights.access_status.text)
        self.assertEqual('Hughes, Carol', self.rights.copyright_holder_name)
        self.assertEqual('1923', self.rights.copyright_date)
        self.assertEqual('Written permission required.', self.rights.ip_note)
        self.assertEqual(False, self.rights.block_external_access)

    def test_create(self):
        # test creating digitaltech metadata from scratch
        rt = audiomodels.Rights()
        rt.create_access_status()
        rt.access_status.code = 8    # public domain
        rt.access_status.text = 'In public domain, no contract restriction'
        rt.copyright_holder_name = 'Mouse, Mickey'
        rt.copyright_date = '1928'
        rt.ip_note = 'See WATCH list for copyright contact info'
        rt.block_external_access = True

        # quick sanity check
        self.assertTrue('<rt:rights' in rt.serialize())

        # also, did block_external_access actually create its subelement?
        self.assertTrue('<rt:externalAccess>deny</' in rt.serialize())

        # TODO: more fields tests; validate against schema when we have one


# tests for Audio DigitalObject
class TestAudioObject(TestCase):
    fixtures =  ['users']
    repo = Repository()

    def setUp(self):
        # create a test audio object to edit
        with open(wav_filename) as wav:
            self.obj = self.repo.get_object(type=audiomodels.AudioObject)
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
        obj = self.repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, obj.info.owner)
        self.assert_(isinstance(obj.mods.content, audiomodels.AudioMods))

    def test_save(self):
        # save without changing the MODS - shouldn't mess anything up
        self.obj.save()
        self.assertEqual("Testing, one, two", self.obj.label)
        self.assertEqual("Testing, one, two", self.obj.dc.content.title)

        # set values in mods and save - should cascade to label, DC
        title, type, date = 'new title in mods', 'text', '2010-01-03'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = type
        self.obj.mods.content.create_origin_info()
        self.obj.mods.content.origin_info.created.append(mods.DateCreated(date=date))
        self.obj.save('testing custom save logic')

        # get updated copy from repo to check
        obj = self.repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(title, obj.label)
        self.assertEqual(title, obj.dc.content.title)
        self.assertEqual(type, obj.dc.content.type)
        self.assertEqual(date, obj.dc.content.date)

        # verify that the owner id is set in repo copy.
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, self.obj.info.owner)

        # test saving with a title longer than 255 characters
        self.obj.mods.content.title = ' '.join(['this is the song that never ends' for i in range(0,10)])
        # save will cause an exception if the object label is not truncated correctly
        self.obj.save()

    def test_update_dc(self):
        # set values in MODS, RELS-EXT, digitaltech
        title, res_type = 'new title in mods', 'text'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = res_type
        cdate, idate = '2010-01-03', '2010-05-05'
        self.obj.mods.content.create_origin_info()
        self.obj.mods.content.origin_info.created.append(mods.DateCreated(date=cdate))
        self.obj.mods.content.origin_info.issued.append(mods.DateIssued(date=idate))
        general_note = 'The Inspector General generally inspects'
        self.obj.mods.content.create_general_note()
        self.obj.mods.content.general_note.text = general_note
        dig_purpose = 'patron request'
        self.obj.digitaltech.content.digitization_purpose = dig_purpose
        self.obj.rights.content.create_access_status()
        self.obj.rights.content.access_status.code = '8'
        self.obj.rights.content.access_status.text = 'Material is in public domain'
        collection = 'collection:123'
        self.obj.collection_uri = collection
        self.obj._update_dc()
        
        self.assertEqual(title, self.obj.dc.content.title)
        self.assertEqual(res_type, self.obj.dc.content.type)
        self.assert_(cdate in self.obj.dc.content.date_list)
        self.assert_(idate in self.obj.dc.content.date_list)
        self.assert_(self.obj.created.strftime('%Y-%m-%d') in self.obj.dc.content.date_list,
                 'object creation date for ingested object should be included in dc:date in YYYY-MM-DD format')
        self.assert_(general_note in self.obj.dc.content.description_list)
        self.assert_(dig_purpose in self.obj.dc.content.description_list)
        # currently using rights access condition code & text in dc:rights
        # should only be one in dc:rights - mods access condition not included
        self.assertEqual(1, len(self.obj.dc.content.rights_list))
        access = self.obj.rights.content.access_status
        self.assert_(self.obj.dc.content.rights.startswith('%s: ' % access.code))
        self.assert_(self.obj.dc.content.rights.endswith(access.text))        

        # collection URI in dc:relation (for findObjects search)
        self.assertEqual(collection, self.obj.dc.content.relation)
        # cmodel in dc:format (for findObject search)
        self.assertEqual(self.obj.AUDIO_CONTENT_MODEL, self.obj.dc.content.format)

        # clear out data and confirm DC gets cleared out appropriately
        del(self.obj.mods.content.origin_info.created)
        del(self.obj.mods.content.origin_info.issued)
        del(self.obj.mods.content.general_note)
        del(self.obj.digitaltech.content.digitization_purpose)
        del(self.obj.rights.content.access_status)
        self.obj._update_dc()
        self.assertEqual(1, len(self.obj.dc.content.date_list),
            'there should only be one dc:date (object creation) when dateCreated or dateIssued are not set in MODS')
        self.assertEqual([], self.obj.dc.content.description_list,
            'there should be no dc:description when general note in MODS and digitization ' +
            'purpose in digital tech are not set')
        self.assertEqual([], self.obj.dc.content.rights_list,
            'there should be no dc:rights when no Rights access_status is set')

        # un-ingested object - should not error, should get current date
        obj = self.repo.get_object(type=audiomodels.AudioObject)
        obj._update_dc()
        self.assert_(date.today().strftime('%Y-%m-%d') in obj.dc.content.date_list,
             'current date should be set in dc:date for un-ingested object')
               
    def test_file_checksum(self):
        #This is just a sanity check that eulcore is working as expected with checksums.
        filename = 'example.wav'
        label = 'this is a test WAV file'
        #specify an incorrect checksum
        wav_md5 = 'aaa'
        obj = audiomodels.AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
        expected_error=None
        try:
            obj.save()
            #Purge if it somehow did not error on the save.
            self.repo.purge_object(obj.pid, "removing unit test fixture")
        except Exception as e:
            expected_error = e
            
        self.assert_(str(expected_error).endswith('500 Internal Server Error'), 'Incorrect checksum should not be ingested.') 
        
        # specify a correct checksum
        wav_md5 = 'f725ce7eda38088ede8409254d6fe8c3'
        obj = audiomodels.AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
        return_result = obj.save()
        self.assertEqual(True, return_result)
        self.repo.purge_object(obj.pid, "removing unit test fixture")

    def test_init_from_file(self):
        new_obj = audiomodels.AudioObject.init_from_file(wav_filename)
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
        self.assertEqual('lossless', new_obj.digitaltech.content.codec_quality,
            'codec quality should be initialized to "lossless"')
        # duration
        self.assertEqual(3, new_obj.digitaltech.content.duration,
            'duration should be calculated and stored in duration, rounded to the nearest second')

        # specify an initial label
        label = 'this is a test WAV file'
        new_obj = audiomodels.AudioObject.init_from_file(wav_filename, label)
        self.assertEqual(label, new_obj.label)
        self.assertEqual(label, new_obj.mods.content.title)
        self.assertEqual(label, new_obj.dc.content.title)
        
        # use request to pass logged-in user credentials for fedora access
        rqst = HttpRequest()
        user = ADMIN_CREDENTIALS['username']
        rqst.user = User.objects.get(username=user)
        # use custom login so user credentials will be stored properly
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        rqst.session = self.client.session
        new_obj = audiomodels.AudioObject.init_from_file(wav_filename, request=rqst)
        self.assertEqual(new_obj.api.opener.username, user,
            'object initialized with request has user credentials configured for fedora access')

    def test_collection(self):
        FAKE_COLLECTION = 'info:fedora/test:FakeCollection'

        self.obj.collection_uri = FAKE_COLLECTION
        self.obj.save()

        obj = self.repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(FAKE_COLLECTION, str(obj.collection_uri))

    def test_conversion_result(self):
        self.assertEqual(None, self.obj.conversion_result)
        conv1 = TaskResult(label='genmp3', object_id=self.obj.pid,
            url=self.obj.get_absolute_url(), task_id='foo')
        conv1.save()
        sleep(1)    # ensure different task creation times
        conv2 = TaskResult(label='genmp3', object_id=self.obj.pid,
            url=self.obj.get_absolute_url(), task_id='bar')
        conv2.save()
        self.assertEqual(conv2, self.obj.conversion_result)

class TestWavDuration(TestCase):

    def test_success(self):
        duration = audiomodels.wav_duration(wav_filename)
        # ffmpeg reports the duration of fixture WAV file as 00:00:03.30
        self.assertAlmostEqual(3.3, duration, 3)

    def test_non_wav(self):
        self.assertRaises(StandardError, audiomodels.wav_duration, mp3_filename)

    def test_nonexistent(self):
        self.assertRaises(IOError, audiomodels.wav_duration, 'i-am-not-a-real-file.wav')


class TestModsEditForm(TestCase):
    MIN_DATA = {
        'mods-title': 'new title',
        'mods-general_note-text': '',
        'mods-part_note-text': '',
        'mods-resource_type': 'sound recording',
        # 'management' form data is required for django to process formsets/subforms
        'mods-origin_info-issued-INITIAL_FORMS': '0',
        'mods-origin_info-issued-TOTAL_FORMS': '1',
        'mods-origin_info-issued-MAX_NUM_FORMS': '',
        'mods-origin_info-issued-0-date_year': '',
        'mods-origin_info-created-INITIAL_FORMS': '0',
        'mods-origin_info-created-TOTAL_FORMS': '1',
        'mods-origin_info-created-MAX_NUM_FORMS': '',
        'mods-origin_info-created-0-date_year': '',
    }

    def test_no_extra_fields(self):
        # don't create any extra fields when updating instance with minimal required fields
        # NOTE: fields may be present when binding the form, but empty fields
        # should be removed before the instance is finally updated
        m = audiomodels.AudioMods()
        form = audioforms.ModsEditForm(instance=m, data=self.MIN_DATA, prefix='mods')
        self.assertTrue(form.is_valid())
        inst = form.update_instance()
        self.assertEqual(2, len(inst.node.getchildren()),
                         'minimal record should only have 2 fields (title, resource type)')

    def test_clean_on_update(self):
        # POST data to update audio object in fedora
        m = audiomodels.AudioMods()
        form = audioforms.ModsEditForm(data=self.MIN_DATA, instance=m, prefix='mods')
        self.assertTrue(form.is_valid())
        inst = form.update_instance()
        self.assertEqual(None, inst.general_note)
        self.assertEqual(None, inst.part_note)
        self.assertEqual(None, inst.origin_info)

        # set values - ensure they do not get removed
        data = self.MIN_DATA.copy()
        data.update({
            'mods-general_note-text': 'gen',
            'mods-part_note-text': 'side a',
            'mods-origin_info-issued-0-date_year': '2000',
            'mods-origin_info-created-0-date_year': '',
        })
        form = audioforms.ModsEditForm(data, instance=m, prefix='mods')
        form.is_valid()
        inst = form.update_instance()
        self.assertNotEqual(None, inst.general_note)
        self.assertNotEqual(None, inst.part_note)
        self.assertNotEqual(None, inst.origin_info)
        self.assertEqual(0, len(inst.origin_info.created))
        self.assertEqual(1, len(inst.origin_info.issued))

        # remove a pre-existing date by sending empty string for date value
        # originInfo sholud not be present with empty dates
        data['mods-origin_info-issued-0-date_year'] = ''
        form = audioforms.ModsEditForm(data, instance=m, prefix='mods')
        form.is_valid()
        inst = form.update_instance()
        self.assertEqual(None, inst.origin_info)

class SourceAudioConversions(TestCase):
    def setUp(self):
        # create an audio object to test conversion with
        self.obj = audiomodels.AudioObject.init_from_file(wav_filename,
                                         'test only',  checksum=wav_md5)
        self.obj.save()
        self.pids = [self.obj.pid]

    def tearDown(self):
        # purge any objects created by individual tests
        for pid in self.pids:
            FedoraFixtures.repo.purge_object(pid)

    def test_wav_to_mp3(self):
        result = convert_wav_to_mp3(self.obj.pid)
        self.assertEqual(result, "Successfully converted file")

        # inspect the object in fedora to confirm that the audio was added
        repo = Repository()
        obj = repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertTrue(obj.compressed_audio.exists)

        #Verify the wav and mp3 durations match.
        comparison_result = audiomodels.wav_and_mp3_duration_comparator(self.obj.pid)
        self.assertTrue(comparison_result, "WAV and MP3 durations did not match.")

        # any other settings/info on the mp3 datastream that should be checked?

    def test_wav_to_mp3_localfile(self):
        #test conversion when wav file on hard-disk is specified.
        result = convert_wav_to_mp3(self.obj.pid, use_wav=wav_filename)
        self.assertEqual(result, "Successfully converted file")

        self.assertTrue(os.path.exists(wav_filename),
            'specified wav file should not be removed if we did not request removal')

        #Verify the wav and mp3 durations match.
        comparison_result = audiomodels.wav_and_mp3_duration_comparator(self.obj.pid, wav_file_path=wav_filename)
        self.assertTrue(comparison_result, "WAV and MP3 durations did not match.")

        # copy wav file so we can test removing it
        wav_copy = os.path.join(settings.INGEST_STAGING_TEMP_DIR, 'example-01.wav')
        copyfile(wav_filename, wav_copy)
        result = convert_wav_to_mp3(self.obj.pid, use_wav=wav_copy, remove_wav=True)
        self.assertFalse(os.path.exists(wav_copy),
            'specified wav file should be removed when requested')

    def test_nonexistent(self):
        # test with invalid pid
        self.assertRaises(RequestFailed, convert_wav_to_mp3, 'bogus:DoesNotExist')

        # test with invalid file.
        self.assertRaises(IOError, convert_wav_to_mp3, self.obj.pid, "CompletelyBogusFile.wav")

    def test_non_matching_checksum(self):
        #Use the alternate wav file to kick off an incorrect checksum match.
        self.assertRaises(Exception, convert_wav_to_mp3, self.obj.pid, alternate_wav_filename)

    def test_changing_wav_file(self):
        self.obj.audio.content = open(alternate_wav_filename)  # FIXME: at what point does/should this get closed?
        self.obj.audio.checksum=alternate_wav_md5
        self.obj.save()
        
        result = convert_wav_to_mp3(self.obj.pid)
        self.assertEqual(result, "Successfully converted file")

        #Verify it no longer matches the original wav file.
        comparison_result = audiomodels.wav_and_mp3_duration_comparator(self.obj.pid, wav_file_path=wav_filename)
        self.assertFalse(comparison_result, "WAV and MP3 durations did not match.")

        #Verify the new wav and mp3 durations match.
        comparison_result = audiomodels.wav_and_mp3_duration_comparator(self.obj.pid, wav_file_path=alternate_wav_filename)
        self.assertTrue(comparison_result, "WAV and MP3 durations did not match.")
        

    # TODO: test failures, error handling, etc.
    # - trigger tempfile error - make temp dir non-writable

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

