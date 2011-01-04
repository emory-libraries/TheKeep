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
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.management.base import CommandError
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository
from eulcore.xmlmap  import load_xmlobject_from_string

from digitalmasters import mods
from digitalmasters.audio import forms as audioforms
from digitalmasters.audio.models import AudioObject, AudioMods, wav_duration, \
        SourceTech, SourceTechMeasure, DigitalTech, TransferEngineer, \
        CodecCreator, Rights, AccessCondition
from digitalmasters.audio.management.commands import ingest_cleanup
from digitalmasters.collection.fixtures import FedoraFixtures
from digitalmasters.audio.tasks import convertWAVtoMP3

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

# fixture filenames used in multiple tests
mp3_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')
wav_filename = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav')


class AudioViewsTest(TestCase):
    fixtures =  ['users']

    # delete cached collections so test collections will be used
    cache.delete(audioforms._COLLECTION_OPTIONS_CACHE_KEY)
    client = Client()

    # collection fixtures are not modified, so only load & purge once
    rushdie = FedoraFixtures.rushdie_collection()
    rushdie.save()
    esterbrook = FedoraFixtures.esterbrook_collection()
    esterbrook.save()
    englishdocs = FedoraFixtures.englishdocs_collection()
    englishdocs.save()

    def setUp(self):        
        self.pids = []

    def tearDown(self):
        # purge any objects created by individual tests
        for pid in self.pids:
            FedoraFixtures.repo.purge_object(pid)

    def __del__(self):
        FedoraFixtures.repo.purge_object(self.rushdie.pid)
        FedoraFixtures.repo.purge_object(self.esterbrook.pid)
        FedoraFixtures.repo.purge_object(self.englishdocs.pid)

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
        #Add pid to be removed.
        self.pids.append(pid)

        repo = Repository()
        new_obj = repo.get_object(pid, type=AudioObject)
        # check object was created with audio cmodel
        self.assertTrue(new_obj.has_model(AudioObject.AUDIO_CONTENT_MODEL),
            "audio object was created with the correct content model")
        self.assertEqual('example.wav', new_obj.label,
            'initial object label set from original file name (not temporary upload filename)')
        # check that init from file worked correctly
        self.assertEqual(3, new_obj.digitaltech.content.duration,
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
            #Add pid to be removed.
            self.pids.append(pid)

            repo = Repository()
            new_obj = repo.get_object(pid, type=AudioObject)
            # check object was created with audio cmodel
            self.assertTrue(new_obj.has_model(AudioObject.AUDIO_CONTENT_MODEL),
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
        

    def test_compressed_audio_task(self):
            wav_md5 = 'f725ce7eda38088ede8409254d6fe8c3'
            obj = AudioObject.init_from_file(wav_filename,
                                             'test only',
                                              checksum=wav_md5)
            obj.save()
            
            #Add pid to be removed.
            self.pids.append(obj.pid)

            
            result = convertWAVtoMP3(obj.pid)
            self.assertEqual(result, "Successfully converted file")

            #Old test code that relys on a broker.
            #result = convertWAVtoMP3.delay(obj.pid)
            #self.assertEqual(result.get(), "Successfully converted file")
            #self.assertEqual(result.successful(), True,
                #"conversion of audio wav to compressed audio format did not succeed.")

                    
    def test_search(self):
        search_url = reverse('audio:search')

        # create some test objects to search for
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
        obj.mods.content.title = 'test search object 1'
        obj.mods.content.general_note.text = 'general note'
        obj.collection_uri = self.rushdie.uri
        obj.mods.content.origin_info.created.append(mods.DateCreated(date='1492-05'))
        obj.save()
        obj2 = repo.get_object(type=AudioObject)
        obj2.mods.content.title = 'test search object 2'
        obj2.mods.content.access_conditions.append(mods.AccessCondition(type='restriction',
                                                                    text='no photos'))
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
        self.assertContains(response, '''Displaying records
1 - 2
of 2''',
            msg_prefix='search results include total number of records found')

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

        # search by rights
        response = self.client.get(search_url, {'audio-rights': 'no photos'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        found = [o.pid for o in response.context['results']]
        self.assert_(obj.pid not in found,
                "test object 1 not listed in results when searching by rights")
        self.assert_(obj2.pid in found,
                "test object 2 listed in results when searching by rights")

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

    def test_download_audio(self):
        # create a test audio object
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
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
                        
        expected = 'attachment; filename=my-audio-test-object.wav'
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Type'], download_url))

    def test_edit(self):
        # create a test audio object to edit
        obj = AudioObject.init_from_file(wav_filename, "my audio test object")
        # pre-populate some data to check it is set in form instance
        obj.mods.content.general_note.text = 'Here is some general info about this item.'
        obj.mods.content.part_note.text = 'Side 1'
        obj.mods.content.origin_info.created.append(mods.DateCreated(date='1975-10-31'))
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1978-12-25'))
        # pre-populate source tech metadata so we can check it in form instance
        obj.sourcetech.content.note = 'source note'
        obj.sourcetech.content.related_files = '1-3'
        obj.sourcetech.content.sound_characteristics = 'mono'
        # speed in xml maps to a single custom field
        obj.sourcetech.content.speed.unit = 'rpm'
        obj.sourcetech.content.speed.aspect = 'phonograph disc'
        obj.sourcetech.content.speed.value = '120'
        # reel size also maps to a custom field
        obj.sourcetech.content.reel_size.value = '3'
        # pre-populate digital tech metadata
        obj.digitaltech.content.date_captured = '2008'
        obj.digitaltech.content.codec_quality = 'lossy'
        obj.digitaltech.content.note = 'technician details'
        obj.digitaltech.content.digitization_purpose = 'dawson exhibit'
        # retrieve test user object to use for transfer engineer - also used to test
        ldap_user = User.objects.get(username='ldap_user')
        # engineer & codec creator are initialized based on id values
        obj.digitaltech.content.transfer_engineer.id = ldap_user.username
        obj.digitaltech.content.codec_creator.id = '1'
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
        self.assert_(isinstance(response.context['form'].object_instance, AudioObject),
                "form instance is an AudioObject")
        self.assertContains(response, self.rushdie.pid)
        self.assertContains(response, self.esterbrook.pid)
        self.assertContains(response, self.englishdocs.pid)

        initial_data = response.context['form'].initial
        item_mods = obj.mods.content
        self.assertEqual(item_mods.title, initial_data['mods-title'],
            'object MODS title is pre-populated in form initial data')
        self.assertEqual(item_mods.general_note.text, initial_data['mods-general_note-text'],
            'object MODS general note is pre-populated in form initial data')
        self.assertEqual(item_mods.part_note.text, initial_data['mods-part_note-text'],
            'object MODS part note is pre-populated in form initial data')
        self.assertEqual(item_mods.origin_info.created[0].date, 
            initial_data['mods-origin_info-created-0-date'],
            'object MODS date created is pre-populated in form initial data')
        self.assertEqual(item_mods.origin_info.issued[0].date,
            initial_data['mods-origin_info-issued-0-date'],
            'object MODS date issued is pre-populated in form initial data')
        # source tech from object in initial data
        initial_data = response.context['form'].sourcetech.initial
        item_st = obj.sourcetech.content
        self.assertEqual(item_st.note, initial_data['st-note'])
        self.assertEqual(item_st.related_files, initial_data['st-related_files'])
        self.assertEqual(item_st.sound_characteristics, initial_data['st-sound_characteristics'])
        # semi-custom fields based on multiple values in initial data
        self.assertEqual('|'.join([item_st.speed.aspect, item_st.speed.value,
                                  item_st.speed.unit]), initial_data['st-_speed'])
        self.assertEqual(item_st.reel_size.value, initial_data['st-reel'])
        # digital tech from object initial data
        initial_data = response.context['form'].digitaltech.initial
        item_dt = obj.digitaltech.content
        self.assertEqual(item_dt.date_captured, initial_data['dt-date_captured'])
        self.assertEqual(item_dt.codec_quality, initial_data['dt-codec_quality'])
        self.assertEqual(item_dt.note, initial_data['dt-note'])
        self.assertEqual(item_dt.digitization_purpose, initial_data['dt-digitization_purpose'])
        self.assertEqual(ldap_user.id, initial_data['dt-engineer'])
        self.assertEqual(item_dt.codec_creator.id, initial_data['dt-hardware'])

        # POST data to update audio object in fedora
        audio_data = {'collection': self.rushdie.uri,
                    'mods-title': 'new title',
                    'mods-note-label' : 'a general note',
                    'mods-general_note-text': 'remember to ...',
                    'mods-part_note-text': 'side A',
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
                    'st-manufacturer': 'sony',
                    'st-sublocation': 'box 2',
                    'st-form': 'audio cassette',
                    'st-sound_characteristics': 'mono',
                    'st-housing': 'Open reel',
                    'st-stock': '60 minute cassette',
                    'st-reel': '3',
                    'st-_speed': 'tape|15/16|inches/sec',
                     # digital-tech data
                    'dt-digitization_purpose': 'patron request',
                    'dt-date_captured_year': '2010',
                    'dt-engineer': ldap_user.id,
                    'dt-hardware': '3',
                    }
        response = self.client.post(edit_url, audio_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Updated MODS for %s" % obj.pid, messages[0],
            "successful save message set in response context")
        # currently redirects to audio index
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "successful save redirects to audio index page")
        expected = 303      # redirect  -- maybe this should be a 303?
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (successfully saved)'  % \
            (expected, code, edit_url))

        # retrieve the modified object from Fedora to check for updates
        repo = Repository()
        updated_obj = repo.get_object(pid=obj.pid, type=AudioObject)
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
        self.assertEqual(audio_data['st-manufacturer'], st.manufacturer)
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
        self.assertEqual(audio_data['dt-date_captured_year'], dt.date_captured)        
        self.assertEqual('ldap', dt.transfer_engineer.id_type)
        self.assertEqual(ldap_user.username, dt.transfer_engineer.id)
        self.assertEqual(ldap_user.get_full_name(), dt.transfer_engineer.name)
        # codec creator - used id 3, which has two hardware fields
        hardware, software, version = CodecCreator.configurations[audio_data['dt-hardware']]
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
        updated_obj = repo.get_object(pid=obj.pid, type=AudioObject)
        dt = updated_obj.digitaltech.content
        # codec creator - id 4 only has one two hardware and no software version
        hardware, software, version = CodecCreator.configurations[data['dt-hardware']]
        self.assertEqual(data['dt-hardware'], dt.codec_creator.id)
        self.assertEqual(hardware[0], dt.codec_creator.hardware_list[0])
        self.assertEqual(1, len(dt.codec_creator.hardware_list)) # should only be one now
        self.assertEqual(software, dt.codec_creator.software)
        self.assertEqual(None, dt.codec_creator.software_version)

        # test logic for save and continue editing
        data = audio_data.copy()
        data['_save_continue'] = True   # simulate submit via 'save and continue' button
        response = self.client.post(edit_url, data)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual('Updated MODS for %s' % obj.pid, messages[0],
            'successful audio update message displayed to user on save and continue editing')
        self.assert_(isinstance(response.context['form'], audioforms.AudioObjectEditForm),
                "MODS EditForm is set in response context after save and continue editing")

        # force a schema-validation error (shouldn't happen normally)
        obj.mods.content = load_xmlobject_from_string(TestMods.invalid_xml, AudioMods)
        obj.save("schema-invalid MODS")
        response = self.client.post(edit_url, audio_data)
        self.assertContains(response, '<ul class="errorlist">')



        # TODO: add a field validation error & check that error message is displayed
        # to test that our custom templates don't lose any built-in functionality

        # edit non-existent record - exception  -- TODO: should actually be a 404
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
        expected = 303      # redirect
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (edit non-existent record)'  % (expected, code, edit_url))



# TODO: mock out the fedora connection and find a way to verify that we
# handle fedora outages appropriately

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

class SourceTechTest(TestCase):
    FIXTURE = '''<?xml version="1.0" encoding="UTF-8"?>
<st:sourcetech version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:st="http://pid.emory.edu/ns/2010/sourcetech"  xsi="http://pid.emory.edu/ns/2010/sourcetech/v1/sourcetech-1.xsd">
    <st:note type="general">Right channel has squeal throughout recording.</st:note>
    <st:note type="relatedFiles">a89, g3jll, 443b</st:note>
    <st:note type="conservationHistory">Repaired broken tape 2010-03-12</st:note>
    <st:manufacturer>Maxell</st:manufacturer>
    <st:speed>
        <st:measure type="speed" unit="inches/sec" aspect="tape">1.875</st:measure>
    </st:speed>
    <st:sublocation>box 3, folder 7</st:sublocation>
    <st:form type="sound">audio cassette</st:form>
    <st:soundChar>mono</st:soundChar>
    <st:stock>IMT C-60</st:stock>
    <st:housing type="sound">Plastic container</st:housing>
    <st:reelSize>
        <st:measure type="width" unit="inches" aspect="reel size">3</st:measure>
    </st:reelSize>
    <st:note type="technical">May be a duplicate of 222</st:note>
</st:sourcetech>'''

    def setUp(self):
        self.sourcetech = load_xmlobject_from_string(self.FIXTURE, SourceTech)

    def test_init_types(self):
        self.assert_(isinstance(self.sourcetech, SourceTech))
        self.assert_(isinstance(self.sourcetech.speed, SourceTechMeasure))
        self.assert_(isinstance(self.sourcetech.reel_size, SourceTechMeasure))

    def test_fields(self):
        # check field values correctly accessible from fixture
        self.assertEqual('Right channel has squeal throughout recording.', self.sourcetech.note_list[0])
        self.assertEqual('a89, g3jll, 443b', self.sourcetech.related_files)
        self.assertEqual('Repaired broken tape 2010-03-12', self.sourcetech.conservation_history_list[0])
        self.assertEqual('Maxell', self.sourcetech.manufacturer)
        self.assertEqual('inches/sec', self.sourcetech.speed.unit)
        self.assertEqual('tape', self.sourcetech.speed.aspect)
        self.assertEqual('1.875', self.sourcetech.speed.value)
        self.assertEqual(u'1.875', unicode(self.sourcetech.speed))
        self.assertEqual('box 3, folder 7', self.sourcetech.sublocation)
        self.assertEqual('audio cassette', self.sourcetech.form)
        self.assertEqual('mono', self.sourcetech.sound_characteristics)
        self.assertEqual('IMT C-60', self.sourcetech.stock)
        self.assertEqual('Plastic container', self.sourcetech.housing)
        self.assertEqual('inches', self.sourcetech.reel_size.unit)
        self.assertEqual('reel size', self.sourcetech.reel_size.aspect)
        self.assertEqual('3', self.sourcetech.reel_size.value)
        self.assertEqual(u'3', unicode(self.sourcetech.reel_size))
        self.assertEqual('May be a duplicate of 222', self.sourcetech.technical_note[0])

    def test_create(self):
        # test creating sourcetech metadata from scratch
        st = SourceTech()
        st.note_list.append('general note')
        st.related_fields = '1, 2, 3'
        st.conservation_history_list.append('loaned for digitization')
        st.manufacturer = 'Sony'
        st.speed.unit = 'rpm'
        st.speed.aspect = 'phonograph disc'
        st.speed.value = '120'
        st.sublocation = 'box 2'
        st.form = 'CD'
        st.sound_characteristics = 'stereo'
        st.stock = '60-min cassette'
        st.housing = 'Jewel case'
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
        self.digitaltech = load_xmlobject_from_string(self.FIXTURE, DigitalTech)

    def test_init_types(self):
        self.assert_(isinstance(self.digitaltech, DigitalTech))
        self.assert_(isinstance(self.digitaltech.transfer_engineer, TransferEngineer))
        self.assert_(isinstance(self.digitaltech.codec_creator, CodecCreator))

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
        dt = DigitalTech()
        dt.date_captured = '2010-01-01'
        dt.codec_quality = 'lossy'
        dt.duration = 33
        dt.note = 'Transferred slowly'
        dt.digitization_purpose = 'Dawson exhibit'
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
    <rt:accessCondition code="C108-UNRESTRICT">Under copyright; copy allowed by Sec. 108;  no contract restriction; only available within library</rt:accessCondition>
    <rt:copyrightholderName>Hughes, Carol</rt:copyrightholderName>
    <rt:copyrightDate encoding="w3cdtf">1923</rt:copyrightDate>
</rt:rights>'''

    def setUp(self):
        self.rights = load_xmlobject_from_string(self.FIXTURE, Rights)

    def test_init_types(self):
        self.assert_(isinstance(self.rights, Rights))
        self.assert_(isinstance(self.rights.access_condition, AccessCondition))

    def test_fields(self):
        # check field values correctly accessible from fixture
        self.assertEqual('C108-UNRESTRICT', self.rights.access_condition.code)
        self.assertEqual('Under copyright; copy allowed by Sec. 108;  no contract restriction; only available within library', self.rights.access_condition.text)
        self.assertEqual('Hughes, Carol', self.rights.copyright_holder_name)
        self.assertEqual('1923', self.rights.copyright_date)

    def test_create(self):
        # test creating digitaltech metadata from scratch
        rt = Rights()
        rt.access_condition.code = 'PD-UNRESTRICT'
        rt.access_condition.text = 'In public domain, no contract restriction'
        rt.copyright_holder_name = 'Mouse, Mickey'
        rt.copyright_date = '1928'

        # for now, just testing that all fields can be set without error
        self.assert_('<rt:rights' in rt.serialize())

        # TODO: validate against schema when we have one


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
        self.assert_(isinstance(obj.mods.content, AudioMods))

    def test_save(self):
        # save without changing the MODS - shouldn't mess anything up
        self.obj.save()
        self.assertEqual("Testing, one, two", self.obj.label)
        self.assertEqual("Testing, one, two", self.obj.dc.content.title)

        # set values in mods and save - should cascade to label, DC
        title, type, date = 'new title in mods', 'text', '2010-01-03'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = type
        self.obj.mods.content.origin_info.created.append(mods.DateCreated(date=date))
        self.obj.save('testing custom save logic')

        # get updated copy from repo to check
        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(title, obj.label)
        self.assertEqual(title, obj.dc.content.title)
        self.assertEqual(type, obj.dc.content.type)
        self.assertEqual(date, obj.dc.content.date)

        # verify that the owner id is set in repo copy.
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, self.obj.info.owner)

    def test_update_dc(self):
        # set values in MODS, RELS-EXT, digitaltech
        title, res_type = 'new title in mods', 'text'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = res_type
        cdate, idate = '2010-01-03', '2010-05-05'
        self.obj.mods.content.origin_info.created.append(mods.DateCreated(date=cdate))
        self.obj.mods.content.origin_info.issued.append(mods.DateIssued(date=idate))
        general_note = 'The Inspector General generally inspects'
        self.obj.mods.content.general_note.text = general_note
        dig_purpose = 'patron request'
        self.obj.digitaltech.content.digitization_purpose = dig_purpose
        restriction, use = ['personal photos unavailable', 'Tuesdays only']
        self.obj.mods.content.access_conditions.extend([
            mods.AccessCondition(type='restriction', text=restriction),
            mods.AccessCondition(type='use', text=use)])
        collection = 'collection:123'
        self.obj.collection_uri = 'collection:123'
        self.obj._update_dc()
        
        self.assertEqual(title, self.obj.dc.content.title)
        self.assertEqual(res_type, self.obj.dc.content.type)
        self.assert_(cdate in self.obj.dc.content.date_list)
        self.assert_(idate in self.obj.dc.content.date_list)
        self.assert_(general_note in self.obj.dc.content.description_list)
        self.assert_(dig_purpose in self.obj.dc.content.description_list)
        # currently using accessCondition type as a prefix in dc:rights
        self.assert_('restriction: ' + restriction in self.obj.dc.content.rights_list)
        self.assert_('use: ' + use in self.obj.dc.content.rights_list)

        # collection URI in dc:relation (for findObjects search)
        self.assertEqual('collection:123', self.obj.dc.content.relation)
        # cmodel in dc:format (for findObject search)
        self.assertEqual(self.obj.AUDIO_CONTENT_MODEL, self.obj.dc.content.format)

        # clear out data and confirm DC gets cleared out appropriately
        del(self.obj.mods.content.origin_info.created)
        del(self.obj.mods.content.origin_info.issued)
        del(self.obj.mods.content.general_note)
        del(self.obj.digitaltech.content.digitization_purpose)
        del(self.obj.mods.content.access_conditions)
        self.obj._update_dc()
        self.assertEqual([], self.obj.dc.content.date_list,
            'there should be no dc:date when dateCreated or dateIssued are not set in MODS')
        self.assertEqual([], self.obj.dc.content.description_list,
            'there should be no dc:description when general note in MODS and digitization ' +
            'purpose in digital tech are not set')
        self.assertEqual([], self.obj.dc.content.rights_list,
            'there should be no dc:rights when no MODS accessCondition is set')        
        
        
    def test_file_checksum(self):
        #This is just a sanity check that eulcore is working as expected with checksums.
        filename = 'example.wav'
        label = 'this is a test WAV file'
        #specify an incorrect checksum
        wav_md5 = 'aaa'
        obj = AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
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
        obj = AudioObject.init_from_file(wav_filename, label, checksum=wav_md5)
        return_result = obj.save()
        self.assertEqual(True, return_result)
        self.repo.purge_object(obj.pid, "removing unit test fixture")

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
        self.assertEqual('lossless', new_obj.digitaltech.content.codec_quality,
            'codec quality should be initialized to "lossless"')
        # duration
        self.assertEqual(3, new_obj.digitaltech.content.duration,
            'duration should be calculated and stored in duration, rounded to the nearest second')

        # specify an initial label
        label = 'this is a test WAV file'
        new_obj = AudioObject.init_from_file(wav_filename, label)
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
        new_obj = AudioObject.init_from_file(wav_filename, request=rqst)
        self.assertEqual(new_obj.api.opener.username, user,
            'object initialized with request has user credentials configured for fedora access')

    def test_collection(self):
        FAKE_COLLECTION = 'info:fedora/test:FakeCollection'

        self.obj.collection_uri = FAKE_COLLECTION
        self.obj.save()

        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(FAKE_COLLECTION, str(obj.collection_uri))


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

