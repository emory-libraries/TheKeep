import datetime
from mock import Mock, patch, MagicMock
import os
import shutil
import sunburnt
import tempfile
import bagit

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from eulfedora.server import Repository
from eullocal.django.taskresult.models import TaskResult
from eulxml.xmlmap import mods

from keep.audio import models as audiomodels
from keep.audio.tests import ADMIN_CREDENTIALS, mp3_filename, wav_filename, \
    mp3_md5, wav_md5
from keep.collection.fixtures import FedoraFixtures
from keep.file.forms import UploadForm, PremisEditForm, DiskImageEditForm, \
    largefile_staging_bags, LargeFileIngestForm
from keep.file.models import DiskImage, Application
from keep.file.utils import md5sum, sha1sum
from keep.testutil import KeepTestCase, mocksolr_nodupes


## Disk Image fixtures

aff_file = os.path.join(settings.BASE_DIR, 'file', 'fixtures', 'test.aff')
aff_md5 = '9d8daf0469a87dcfa65a29f5e107aac6'
aff_sha1 = '98d027edf2246917b2aede948039fcea1811461b'

ad1_file = os.path.join(settings.BASE_DIR, 'file', 'fixtures', 'test.ad1')
ad1_md5 = 'e1ec1ac3a9e1f5a1c577a1de6e1e5c38'
ad1_sha1 = '2d3065eb1b1ceeb618821e2cf776d36c9ba19e4a'


class TestChecksum(TestCase):
    # use mp3 file from audio test fixtures
    mp3_file = os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3')

    def test_md5sum(self):
        # md5 checksum
        md5 = 'b56b59c5004212b7be53fb5742823bd2'
        self.assertEqual(md5, md5sum(self.mp3_file))

        # test non-existent file
        # file errors are not caught by md5sum utility method but should be passed along
        self.assertRaises(IOError, md5sum, '/not/a/real/file.foo')

    def test_sha1(self):
        # sha1 checksum
        sha1 = '2b0a217cc23a6ce99ec90b67aee4058edc9f1bba'
        self.assertEqual(sha1, sha1sum(self.mp3_file))


# mock archives used to generate archives choices for form field
@patch('keep.collection.forms.CollectionObject.archives',
       new=Mock(return_value=FedoraFixtures.archives(format=dict)))
# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class FileViewsTest(KeepTestCase):
    fixtures = ['users', 'test-applications.json']

    def setUp(self):
        super(FileViewsTest, self).setUp()
        self.pids = []

        # collection fixtures are not modified, but there is no clean way
        # to only load & purge once
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.esterbrook = FedoraFixtures.esterbrook_collection()
        self.esterbrook.save()
        self.englishdocs = FedoraFixtures.englishdocs_collection()
        self.englishdocs.save()

        self.tempdir = tempfile.mkdtemp(prefix='keep-test-')

    def tearDown(self):
        super(FileViewsTest, self).tearDown()
        shutil.rmtree(self.tempdir)

    def test_upload_form(self):
        # test upload form
        upload_url = reverse('file:upload')

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        # on GET, should display the form
        response = self.client.get(upload_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, upload_url))
        self.assertNotEqual(None, response.context['form'])
        self.assert_(isinstance(response.context['form'], UploadForm))

        # collection is now required; posting without should re-display form with error
        response = self.client.post(upload_url, {'comment': 'foo'})
        self.assertNotEqual(None, response.context['form'])
        self.assertFalse(response.context['form'].is_valid())
        self.assertContains(response, 'You must choose a collection',
            msg_prefix='When form is posted without a collection, the error is displayed')

    def test_ajax_file_upload(self):
        # test uploading files via ajax
        upload_url = reverse('file:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # common post options used for most test cases
        post_options = {
            'path': upload_url,
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'HTTP_CONTENT_DISPOSITION': 'filename="example.wav"',
            'content_type': 'audio/wav',
            'X-CSRFToken': ''
        }
        # POST non-wav file to AJAX Upload view results in an error
        with open(mp3_filename, 'rb') as mp3:
            opts = post_options.copy()
            opts['HTTP_CONTENT_DISPOSITION'] = 'attachment; filename="example.mp3"'
            response = self.client.post(data=mp3.read(), HTTP_CONTENT_MD5=mp3_md5, **opts)
            self.assertEqual('File type audio/mpeg is not allowed', response.content)
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
            self.assertTrue(os.path.exists(upload_filepath + '.md5'),
                'MD5 file for temp file should exist in staging directory')
            with open(upload_filepath + '.md5') as md5file:
                self.assertEqual(wav_md5, md5file.read())

    def test_batch_upload(self):
        # test uploading files via ajax
        upload_url = reverse('file:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        # create files in staging dir to mimic results of ajax upload
        upload_filepath = os.path.join(settings.INGEST_STAGING_TEMP_DIR, 'example-01.wav')
        shutil.copyfile(wav_filename, upload_filepath)
        with open(upload_filepath + '.md5', 'w') as md5file:
            md5file.write(wav_md5)

        # use the returned filename from the last (successful) response to test upload
        upload_opts = {
            'filenames': 'example.wav',
            'uploaded_files': 'example-01.wav',
            'collection_0': self.rushdie.pid,
            'collection_1': self.rushdie.label,
            'comment': "This is a very interesting comment",
        }
        # POST wav file with correct checksum - should succeed
        response = self.client.post(upload_url, upload_opts)
        result = response.context['ingest_results'][0]
        self.assertTrue(result['success'],
            'success should be True in result for successful ingest')
        self.assertNotEqual(None, result['pid'],
            'pid should be set in result on success')
        self.assertEqual(wav_md5, result['checksum'],
                        'checksum should be included in result info')
        self.assertContains(response, wav_md5,
            msg_prefix='checksum should be reported on ingest results page')
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
        self.assertEqual(new_obj.collection.pid, self.rushdie.pid,
                         "New object should be a member of collection %s" % self.rushdie)
        #audit trail messages
        audit_trail = [a.message for a in new_obj.audit_trail.records]
        self.assertIn(upload_opts['comment'], audit_trail)

        # task result should have been created to track mp3 conversion
        self.assert_(isinstance(new_obj.conversion_result, TaskResult),
            'ingested object should have a conversion result to track mp3 generation')

        # POST wav file with an incorrect checksum should fail
        shutil.copyfile(wav_filename, upload_filepath)     # re-copy file, now that is removed after ingest
        with open(upload_filepath + '.md5', 'w') as md5file:
            md5file.write('bogus md5 checksum')

        response = self.client.post(upload_url, upload_opts)
        self.assert_('ingest_results' in response.context,
                     'response context should include a list of ingest results')
        result = response.context['ingest_results'][0]
        self.assertFalse(result['success'], 'success should be false on checksum mismatch')
        self.assert_('failed due to a checksum mismatch' in result['message'],
            'result should include explanatory message on failure')

    def test_upload_fallback(self):
        # test single-file upload
        upload_url = reverse('file:upload')
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # POST non-wav file - should fail
        with open(mp3_filename) as mp3:
            response = self.client.post(upload_url, {'file': mp3, 'collection_0':
                           self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
            result = response.context['ingest_results'][0]
            self.assertFalse(result['success'], 'success should be false on non-allowed type')
            self.assertEqual('''File type 'audio/mpeg' is not allowed''',
                            result['message'])

        # POST a wav file - should result in a new object
        with open(wav_filename) as wav:
            response = self.client.post(upload_url, {'file': wav,
                                                     'collection_0': self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
            result = response.context['ingest_results'][0]
            self.assertTrue(result['success'], 'success should be true for uploaded WAV')
            self.assertNotEqual(None, result['pid'],
                'result should include pid of new object on successful ingest')
            # Add pid to be removed.
            self.pids.append(result['pid'])

            repo = Repository()
            new_obj = repo.get_object(result['pid'], type=audiomodels.AudioObject)
            audit_messages = [a.message for a in new_obj.audit_trail.records]
            self.assertEqual(new_obj.collection.pid, self.rushdie.pid)
            # check object was created with audio cmodel
            self.assertTrue(new_obj.has_model(audiomodels.AudioObject.AUDIO_CONTENT_MODEL),
                "audio object was created with the correct content model")
            # seek to 0 so we can re-read file data
            wav.seek(0)
            orig_data = wav.read()

            fetched_data = new_obj.audio.content.getvalue()
            self.assertEqual(len(orig_data), len(fetched_data))
            self.assertEqual(orig_data, new_obj.audio.content.getvalue(),
                "audio file content on new object corresponds to uploaded file data")
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

            self.assertIn('initial repository ingest', audit_messages,
                          'Should have default message when no comment is present')

        # upload same file but add a comment
        with open(wav_filename) as wav:
            response = self.client.post(upload_url, {
                'file': wav, 'comment': "This is comment for the audit trail",
                'collection_0': self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
            result = response.context['ingest_results'][0]
            self.assertTrue(result['success'], 'success should be true for uploaded WAV')
            self.assertNotEqual(None, result['pid'],
                'result should include pid of new object on successful ingest')
            # Add pid to be removed.
            self.pids.append(result['pid'])

            repo = Repository()
            new_obj = repo.get_object(result['pid'], type=audiomodels.AudioObject)
            audit_messages = [a.message for a in new_obj.audit_trail.records]
            self.assertEqual(new_obj.collection.pid, self.rushdie.pid)

            self.assertIn('This is comment for the audit trail', audit_messages,
                          'Should have comment in audit trail')

    def test_upload_diskimage(self):
        # test specifics for disk image upload

        upload_url = reverse('file:upload')
        self.client.login(**ADMIN_CREDENTIALS)

        with open(aff_file) as aff:
            response = self.client.post(upload_url, {'file': aff, 'collection_0':
                           self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
            result = response.context['ingest_results'][0]
            self.assertTrue(result['success'], 'success should be true for uploaded AFF')
            self.assertNotEqual(None, result['pid'],
                'result should include pid of new object on successful ingest')
            # Add pid to be removed.
            self.pids.append(result['pid'])

            repo = Repository()
            new_obj = repo.get_object(result['pid'], type=DiskImage)
            # audit_messages = [a.message for a in new_obj.audit_trail.records]
            self.assertEqual(new_obj.collection.pid, self.rushdie.pid)
            # check object was created with disk image cmodel
            self.assertTrue(new_obj.has_model(DiskImage.DISKIMAGE_CONTENT_MODEL),
                "disk image object was created with the correct content model")

            # no audio access copy conversion task should have been queued
            self.assertEqual(0, TaskResult.objects.filter(object_id=new_obj.pid).count())

            # spot-check metadata init to confirm it ran
            self.assertEqual('software, multimedia', new_obj.mods.content.resource_type)
            self.assertEqual(aff_md5, new_obj.provenance.content.object.checksums[0].digest)

        # confirm AD1 also ingested as Disk Image
        with open(ad1_file) as ad1:
            response = self.client.post(upload_url, {'file': ad1, 'collection_0':
                           self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
            result = response.context['ingest_results'][0]
            self.assertTrue(result['success'], 'success should be true for uploaded AD1')
            self.assertNotEqual(None, result['pid'],
                'result should include pid of new object on successful ingest')
            # Add pid to be removed.
            self.pids.append(result['pid'])

            repo = Repository()
            new_obj = repo.get_object(result['pid'], type=DiskImage)
            self.assertTrue(new_obj.has_model(DiskImage.DISKIMAGE_CONTENT_MODEL),
                "AD1 ingested as disk image object")
            self.assertEqual(ad1_md5, new_obj.provenance.content.object.checksums[0].digest)

    def test_largefile_ingest(self):
        ingest_url = reverse('file:largefile-ingest')
        # use custom login so user credentials will be stored for fedora access
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)

        # on GET with no uploaded files, should display message and no form
        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            response = self.client.get(ingest_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, ingest_url))
        self.assert_('form' not in response.context,
            'form should not be set in response context when no files are available for ingest')
        self.assertTrue(response.context['no_files'])
        self.assertContains(response, '<p>No files are currently available for ingest.</p>',
            msg_prefix='response should indicate when no files are available for ingest',
            html=True)

        # construct a BagIt to test form display
        bag_path = tempfile.mkdtemp(dir=self.tempdir)
        bagit.make_bag(bag_path)

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            response = self.client.get(ingest_url)
        self.assertNotEqual(None, response.context['form'])
        self.assert_(isinstance(response.context['form'], LargeFileIngestForm))

        # collection & file are required; posting without should re-display form with errors
        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            response = self.client.post(ingest_url)
        self.assertNotEqual(None, response.context['form'])
        self.assertFalse(response.context['form'].is_valid())
        self.assertContains(response, 'You must choose a collection',
            msg_prefix='When form is posted without a collection, an error is displayed')
        self.assertContains(response, 'field is required',
            msg_prefix='When form is posted without a file selected, an error is displayed')
        # clean up first test bag
        shutil.rmtree(bag_path)

        # construct a BagIt and then post as selected file
        emptybag_path = tempfile.mkdtemp(dir=self.tempdir)
        # empty bag - valid but no disk image data
        bagit.make_bag(emptybag_path)

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            response = self.client.post(ingest_url, {'bag': emptybag_path, 'collection_0':
                self.rushdie.pid, 'collection_1': 'Rushdie Collection'})
        # should error because bagit does not contain a disk image file
        result = response.context['ingest_results'][0]
        self.assertFalse(result['success'])
        basename = os.path.basename(emptybag_path)
        self.assertEqual(basename, result['label'])
        self.assertEqual('No disk image content found in %s' % basename,
                         result['message'])

        # clean up
        shutil.rmtree(emptybag_path)

        # construct a BagIt and then post as selected file
        ad1bag_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture as payload
        shutil.copy(ad1_file, ad1bag_path)
        bagit.make_bag(ad1bag_path)

        # mock save method since we can't ingest test fixture via file uri
        self.saved_obj = None
        self.save_comment = None
        def mock_save(obj, msg):
            obj.pid = 'fakepid:1'
            obj.content.checksum = ad1_md5
            self.save_comment = msg
            self.saved_obj = obj

        # because we are mocking save and the view requests
        # a fresh copy of the object from fedora to compare checksums,
        # we have to mock repo.get_object
        def mockrepo_getobj(pid, **kwargs):
            if pid == self.rushdie.pid:
                return self.repo.get_object(self.rushdie.pid, **kwargs)
            else:
                return self.saved_obj

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            with patch('keep.file.models.DiskImage.save', new=mock_save):
                with patch('keep.file.views.Repository') as mockrepo:
                    mockrepo.return_value.get_object = mockrepo_getobj

                    response = self.client.post(ingest_url, {'bag': ad1bag_path, 'collection_0':
                        self.rushdie.pid, 'collection_1': 'Rushdie Collection',
                        'comment': 'ingest me!'})

        self.assertEqual('ingest me!', self.save_comment)

        # should create new disk image object & ingest into fedora
        # - summary info on ingested item should be displayed to user
        result = response.context['ingest_results'][0]
        self.assertTrue(result['success'],
            'success should be True in result for successful ingest')
        self.assertNotEqual(None, result['pid'],
            'pid should be set in result on success')
        self.assertEqual(ad1_md5, result['checksum'],
                        'checksum should be included in result info')
        self.assertContains(response, ad1_md5,
            msg_prefix='checksum should be reported on ingest results page')
        # add pid to be removed in tearDown
        self.pids.append(result['pid'])
        # bagit should be removed from large-file staging area
        self.assertFalse(os.path.isdir(bag_path),
            'BagIt should be removed on successful ingest')

        # form should not redisplay if no more files are available for ingest
        self.assert_('form' not in response.context,
            'form should not redisplay after ingest if no files are available for ingest')
        self.assertTrue(response.context['no_files'])
        self.assertContains(response, '<p>No more files are currently available for ingest.</p>',
            msg_prefix='response should indicate no more files are available for ingest',
            html=True)

        # inspect object as initialized (since save is simulated)
        # - should be created by logged in user
        self.assertEqual(ADMIN_CREDENTIALS['username'],
            self.saved_obj.api.opener.username)
        # - should be associated with collection
        # NOTE: this is failing because collection is None (because not ingested?)
        # self.assertEqual(self.rushdie.pid, self.saved_obj.collection.pid)
        # NOTE: can't test since this RELS-EXT isn't boot-strapped until ingest
        # self.assertTrue(self.saved_obj.has_model(DiskImage.DISKIMAGE_CONTENT_MODEL),
        #     "BagIt ingested via large-file workflow is disk image object")

        # test invalid checksum after ingest

        # reconstruct BagIt for posting (previous removed on success)
        bag_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture as payload
        shutil.copy(ad1_file, bag_path)
        bagit.make_bag(bag_path)

        self.saved_obj = None
        self.save_comment = None
        def mock_save_badchecksum(obj, msg):
            self.saved_obj = obj
            self.saved_obj.pid = 'fakepid:2'
            self.saved_obj.content.checksum = 'bogus md5'

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            with patch('keep.file.models.DiskImage.save', mock_save_badchecksum):
                with patch('keep.file.views.Repository') as mockrepo:
                    mockrepo.return_value.get_object = mockrepo_getobj

                    response = self.client.post(ingest_url, {'bag': bag_path, 'collection_0':
                        self.rushdie.pid, 'collection_1': 'Rushdie Collection',
                        'comment': 'ingest me!'})

        result = response.context['ingest_results'][0]
        self.assert_('checksum mismatch detected' in result['message'].lower())

    def test_duplicate_detection(self):
        # test that duplicate detected prevents ingest

        upload_url = reverse('file:upload')
        self.client.login(**ADMIN_CREDENTIALS)

        # mock solr to detect duplicates
        with patch('keep.common.fedora.solr_interface',
                   spec=sunburnt.SolrInterface) as mocksolr_interface:
            # mock sunburnt's fluid interface
            mocksolr = mocksolr_interface.return_value
            mocksolr.query = MagicMock()
            mocksolr.query.return_value = mocksolr.query
            for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                           'exclude']:
               getattr(mocksolr.query, method).return_value = mocksolr.query
            # set mock solr to indicate duplicate records
            mocksolr.query.count.return_value = 2

            # run again and inspect exception
            solr_result = [
                {'pid': 'audio:1', 'content_model': audiomodels.AudioObject.CONTENT_MODELS},
                {'pid': 'file:1', 'content_model': DiskImage.CONTENT_MODELS},
            ]
            mocksolr.query.__iter__.return_value = iter(solr_result)

            # ** test web upload with a single file
            with open(wav_filename) as wav:
                response = self.client.post(upload_url, {'file': wav,
                 'collection_0': self.rushdie.pid, 'collection_1': 'Rushdie Collection'})

            result = response.context['ingest_results'][0]

            self.assertEqual(False, result['success'],
                'ingest should fail when duplicates are detected')
            self.assert_('Detected 2 duplicate records' in result['message'],
                'error message should indicate the number of duplicate records detected')
            for res in solr_result:
                self.assert_(res['pid'] in result['message'],
                    'message should include pid of detected duplicate record')
            # should link to object, based on content model / object type
            self.assert_(reverse('audio:view', args=['audio:1']) in result['message'],
                'error message should include link to object based on detected type')
            self.assert_(reverse('file:view', args=['file:1']) in result['message'],
                'error message should include link to object based on detected type')

            # ** test duplicates also reported on large file / BagIt upload
            ingest_url = reverse('file:largefile-ingest')

            # construct test BagIt
            ad1bag_path = tempfile.mkdtemp(dir=self.tempdir)
            # copy in ad1 fixture as payload
            shutil.copy(ad1_file, ad1bag_path)
            bagit.make_bag(ad1bag_path)

            mocksolr.query.count.return_value = 1

            # run again and inspect exception
            solr_result = [
                {'pid': 'file:1', 'content_model': DiskImage.CONTENT_MODELS},
            ]
            mocksolr.query.__iter__.return_value = iter(solr_result)

            with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):

                response = self.client.post(ingest_url, {'bag': ad1bag_path, 'collection_0':
                    self.rushdie.pid, 'collection_1': 'Rushdie Collection'})

            result = response.context['ingest_results'][0]
            self.assertEqual(False, result['success'],
                'ingest should fail when a duplicate item is detected')
            self.assert_('Detected 1 duplicate record: ' in result['message'],
                'error message should indicate the number of duplicate records detected')
            for res in solr_result:
                self.assert_(res['pid'] in result['message'],
                    'message should include pid of detected duplicate record')
            # should link to object, based on content model / object type
            self.assert_(reverse('file:view', args=['file:1']) in result['message'],
                'error message should include link to object based on detected type')

    def test_edit(self):
        # ingest an object to test editing
        img = DiskImage.init_from_file(ad1_file, 'Important Disk Image')
        img.save()
        self.pids.append(img.pid)

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        edit_url = reverse('file:edit', args=[img.pid])
        # on GET, should display the form
        response = self.client.get(edit_url)
        # check response context
        self.assert_(isinstance(response.context['form'], DiskImageEditForm))
        self.assert_(isinstance(response.context['form'], DiskImageEditForm))
        self.assertContains(response, reverse('admin:file_application_changelist'),
            msg_prefix='edit form includes link to manage application list')

        # minimal required fields
        data = {
            'mods-title': 'updated disk image',
            'mods-abstract-text': 'longer description',
            # using W3C date field, so year/month/day submitted separately
            'mods-coveringdate_start_year': '2002',
            'mods-coveringdate_start_month': '05',
            'mods-coveringdate_start_day': '02',
            'mods-coveringdate_end_year': '2004',
            'mods-coveringdate_end_month': '03',
            'mods-coveringdate_end_day': '05',
            'collection_0': self.rushdie.pid,
            'collection_1': self.rushdie.label,
            'premis-application': '1',
            'premis-date': '2003-05-06',
            'rights-access': '10',
            'comment': 'update metadata via edit form',
        }

        # on POST, validate and update
        response = self.client.post(edit_url, data)
        # inspect updated object
        updated_img = self.repo.get_object(img.pid, type=DiskImage)
        # collection membership
        self.assertEqual(self.rushdie.pid, updated_img.collection.pid)
        # mods
        modsxml = updated_img.mods.content
        self.assertEqual(data['mods-title'], modsxml.title)
        self.assertEqual(data['mods-abstract-text'], modsxml.abstract.text)
        # print modsxml.serialize(pretty=True)
        start = '-'.join([data['mods-coveringdate_start_year'],
                          data['mods-coveringdate_start_month'],
                          data['mods-coveringdate_start_day']])
        self.assertEqual(start, modsxml.coveringdate_start)
        end = '-'.join([data['mods-coveringdate_end_year'],
                        data['mods-coveringdate_end_month'],
                        data['mods-coveringdate_end_day']])
        self.assertEqual(end, modsxml.coveringdate_end)
        # premis
        app = Application.objects.get(id=data['premis-application'])
        premis = updated_img.provenance.content
        self.assertEqual(data['premis-date'], unicode(premis.object.creating_application.date))
        self.assertEqual(app.name, unicode(premis.object.creating_application.name))
        self.assertEqual(app.version, unicode(premis.object.creating_application.version))
        # rights logic re-used, but make sure it was updated
        self.assertEqual(data['rights-access'], updated_img.rights.content.access_status.code)
        self.assertEqual(data['comment'], updated_img.audit_trail.records[-1].message)

        # TODO: test invalid post?

        # supplemental content links
        baggy_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture and create supplemental files
        text_content = 'some text about the disk image'
        shutil.copy(ad1_file, baggy_path)
        with open(os.path.join(baggy_path, 'info.txt'), 'w') as txtfile:
            txtfile.write(text_content)
        xml_content = '<xml/>'
        with open(os.path.join(baggy_path, 'extra.xml'), 'w') as xmlfile:
            xmlfile.write(xml_content)
        # convert to bagit
        bagit.make_bag(baggy_path)
        img = DiskImage.init_from_bagit(baggy_path, file_uri=False)
        img.save()
        self.pids.append(img.pid)

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        edit_url = reverse('file:edit', args=[img.pid])
        # on GET, should display the form
        response = self.client.get(edit_url)
        self.assertContains(response, 'Supplemental content:',
            msg_prefix='disk image with supplemental datastreams should list them')

        img = self.repo.get_object(img.pid, type=DiskImage)
        for ds in img.supplemental_content:
            self.assertContains(response, ds.label,
                msg_prefix='supplemental datastream %s label %s should be displayed' %
                (ds.id, ds.label))
            self.assertContains(response, reverse('file:raw-ds', args=(img.pid, ds.id)),
                msg_prefix='link to view/download supplemental datastream should be present')

    def test_manage_supplements(self):
        # ingest an object to test editing
        img = DiskImage.init_from_file(ad1_file, 'Important Disk Image')
        img.save()
        self.pids.append(img.pid)

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        manage_supplements_url = reverse('file:supplements', args=[img.pid])
        # on GET, should display the form
        response = self.client.get(manage_supplements_url)
        # no supplements; should display empty form (no initial data)
        self.assert_('formset' in response.context)
        self.assertEqual(0, len(response.context['formset'].initial_forms))

        # POST with no changes
        form_data = {
            'form-TOTAL_FORMS': 3,
            'form-INITIAL_FORMS': 0,
        }

        response = self.client.post(manage_supplements_url, form_data, follow=True)
        url, code = response.redirect_chain[0]
        self.assert_(url.endswith(reverse('file:edit', args=[img.pid])))
        self.assertEqual(303, code, 'should redirect with 303 See Other')
        messages = [str(msg) for msg in response.context['messages']]
        self.assertEqual('No changes made to supplemental content',
            messages[0])

        # - test POST data to add new supplemental datastreams
        tmpfile1 = tempfile.NamedTemporaryFile(delete=False)
        txt1 = 'Here is some supplemental content about an archival disk image'
        tmpfile1.write(txt1)
        tmpfile1.close()  # close to write contents so not detected as empty when posted
        tmpfile2 = tempfile.NamedTemporaryFile(delete=False)
        txt2 = '<xml><img>disk</img><metadata>something</metadata></xml>'
        tmpfile2.write(txt2)
        tmpfile2.close()
        data = form_data.copy()
        data.update({
            'form-0-label': 'some-file.txt',
            'form-0-dsid': '',
            'form-1-label': '',  # leaving blank to generate from filename
            'form-1-dsid': '',
        })
        with open(tmpfile1.name) as tmpfile1_data:
            with open(tmpfile2.name) as tmpfile2_data:
                data['form-0-file'] = tmpfile1_data
                data['form-1-file'] = tmpfile2_data

                response = self.client.post(manage_supplements_url, data, follow=True)

        url, code = response.redirect_chain[0]
        messages = [str(msg) for msg in response.context['messages']]
        self.assertEqual('Successfully added 2 supplemental files',
                         messages[0])
        # get object from fedora and check for supplemental datastreams
        updated_img = self.repo.get_object(img.pid, type=DiskImage)
        # should have added two supplementN datastreams
        self.assert_('supplement0' in updated_img.ds_list)
        self.assert_('supplement1' in updated_img.ds_list)
        supplements = list(updated_img.supplemental_content)
        self.assertEqual(2, len(supplements))
        self.assertEqual(data['form-0-label'], supplements[0].label,
            'datastream label should be set from form data if specified')
        self.assertEqual(txt1, supplements[0].content)
        self.assertEqual('text/plain', supplements[0].mimetype,
            'datastream mimetype is set based on detected content')
        self.assertEqual(md5sum(tmpfile1.name), supplements[0].checksum)
        self.assertEqual(os.path.basename(tmpfile2.name), supplements[1].label,
            'datastream label should be set from filename if not specified')
        self.assertEqual(txt2, supplements[1].content)
        self.assertEqual(md5sum(tmpfile2.name), supplements[1].checksum)

        os.unlink(tmpfile1.name)
        os.unlink(tmpfile2.name)

        # test initial form data for object with supplemental datastreams
        response = self.client.get(manage_supplements_url, data, follow=True)
        formset = response.context['formset']
        self.assertEqual(2, len(formset.initial_forms),
            'formset should have two initial forms when there are two supplemental datastreams')
        self.assertEqual(supplements[0].label, formset.initial_forms[0].initial['label'])
        self.assertEqual(supplements[0].id, formset.initial_forms[0].initial['dsid'])
        self.assertEqual(supplements[1].label, formset.initial_forms[1].initial['label'])
        self.assertEqual(supplements[1].id, formset.initial_forms[1].initial['dsid'])

        # update existing supplemental datastreams and add a new one

        tmpfile1_v2 = tempfile.NamedTemporaryFile(delete=False)
        txt1_v2 = 'Here is some *updated* content about an archival disk image'
        tmpfile1_v2.write(txt1_v2)
        tmpfile1_v2.close()
        tmpfile3 = tempfile.NamedTemporaryFile(delete=False)
        txt3 = 'third piece of content'
        tmpfile3.write(txt3)
        tmpfile3.close()
        data = form_data.copy()
        data.update({
            'form-INITIAL_FORMS': 2,
            'form-0-label': 'new-label.foo',  # s1: update label but not file
            'form-0-dsid': 'supplement0',
            'form-1-label': supplements[1].label,  # s2: update file but not label
            'form-1-dsid': 'supplement1',
            'form-2-label': '',              # s3: new supplemental file
            'form-2-dsid': '',
        })

        # test save error with valid post data
        with open(tmpfile1_v2.name) as tmpfile1v2_data:
            with open(tmpfile3.name) as tmpfile3_data:
                data['form-1-file'] = tmpfile1v2_data
                data['form-2-file'] = tmpfile3_data

                # patching md5sum to simulate checksum mismatch and force fedora error
                with patch('keep.file.views.md5sum') as mockmd5:
                    mockmd5.return_value = 'not-a-real-md5-sum'

                    response = self.client.post(manage_supplements_url, data)
                    messages = [str(msg) for msg in response.context['messages']]
                    self.assert_('Error saving' in messages[0])

        # test actual updates + additions
        with open(tmpfile1_v2.name) as tmpfile1v2_data:
            with open(tmpfile3.name) as tmpfile3_data:
                data['form-1-file'] = tmpfile1v2_data
                data['form-2-file'] = tmpfile3_data

                response = self.client.post(manage_supplements_url,
                    data, follow=True)

        messages = [str(msg) for msg in response.context['messages']]
        self.assertEqual('Successfully added 1 and updated 2 supplemental files',
                         messages[0])
        # inspect updates/additions
        updated_img = self.repo.get_object(img.pid, type=DiskImage)
        # should now have three supplementN datastreams
        self.assert_('supplement0' in updated_img.ds_list)
        self.assert_('supplement1' in updated_img.ds_list)
        supplements = list(updated_img.supplemental_content)
        self.assertEqual(3, len(supplements))
        self.assertEqual(data['form-0-label'], supplements[0].label,
            'datastream label should be updated from form data')
        self.assertEqual(txt1_v2, supplements[1].content,
            'datastream content should be updated from form data')
        # newly added datastream
        self.assertEqual(os.path.basename(tmpfile3.name), supplements[2].label)
        self.assertEqual(txt3, supplements[2].content)

        os.unlink(tmpfile1_v2.name)
        os.unlink(tmpfile3.name)


class UploadFormTest(TestCase):

    def test_validation(self):
        # no files (single or batch) - should be invalid
        form = UploadForm({'collection_0': 'some:pid',
                           'collection_1': 'a collection'})
        self.assertFalse(form.is_valid())
        self.assert_('No files were uploaded' in str(form._errors))

        # mismatch on uploaded file/filenames
        form = UploadForm(data={'collection_0': 'some:pid',
                                'collection_1': 'a collection',
                                'uploaded_files': ['one', 'two'],
                                'filenames': ['one.doc']})
        self.assertFalse(form.is_valid())
        self.assert_('Could not match uploaded files with original filenames'
                     in str(form._errors))

        # ok if file lists match
        form = UploadForm(data={'collection_0': 'some:pid',
                                'collection_1': 'a collection',
                                'uploaded_files': ['one'],
                                'filenames': ['one.doc']})
        self.assertTrue(form.is_valid())

    def test_files_to_ingest(self):
        form = UploadForm()
        mockuploadfile = Mock()
        mockuploadfile.temporary_file_path.return_value = '/tmp/tmp-1234'
        mockuploadfile.name = 'audio.file.wav'
        form.cleaned_data = {'file': mockuploadfile,
                             'uploaded_files': ['/tmp/tmp-567',
                                                '/tmp/tmp-89'],
                             'filenames': ['side-a.wav', 'side-b.wav']
                             }

        files = form.files_to_ingest()
        self.assertEqual(3, len(files))
        self.assertEqual(files[mockuploadfile.temporary_file_path()],
                         mockuploadfile.name)
        self.assertEqual(files[form.cleaned_data['uploaded_files'][0]],
                         form.cleaned_data['filenames'][0])
        self.assertEqual(files[form.cleaned_data['uploaded_files'][1]],
                         form.cleaned_data['filenames'][1])


class LargeFileStagingBagsTest(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='keep-test-')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_options(self):

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            # nothing in folder
            opts = largefile_staging_bags()
            self.assertEqual(1, len(opts),
                'select option list should only have one option when no bagit files are available')

            # create two bags
            bag1_path = tempfile.mkdtemp(dir=self.tempdir)
            bagit.make_bag(bag1_path)
            bag2_path = tempfile.mkdtemp(dir=self.tempdir)
            bagit.make_bag(bag2_path)
            # create a directory that is not a bagit
            nonbag_path = tempfile.mkdtemp(dir=self.tempdir)

            opts = largefile_staging_bags()
            self.assertEqual(3, len(opts),
                'option list should 3 entries when two bagit files are available')
            # inspect actual paths and labels that will be displayed to users
            paths = []
            labels = []
            for k, v in opts:
                paths.append(k)
                labels.append(v)
            self.assert_(bag1_path in paths)
            self.assert_(bag2_path in paths)
            self.assert_(nonbag_path not in paths)
            self.assert_(os.path.basename(bag1_path) in labels)
            self.assert_(os.path.basename(bag2_path) in labels)


# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class DiskImageTest(KeepTestCase):

    def setUp(self):
        # temp dir for constructing BagIt SIPs
        self.tempdir = tempfile.mkdtemp(prefix='keep-test-')
        self.repo = Repository()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_init_from_file(self):
        label = 'My Disk Image'
        mimetype = 'application/x-aff'
        img = DiskImage.init_from_file(aff_file, label,
                                       checksum=aff_md5, mimetype=mimetype)
        # label set on obj and dc:title
        self.assertEqual(label, img.label,
            'specified label should be set on object')
        self.assertEqual(label, img.dc.content.title,
            'specified label should be set as dc:title')
        # mods
        self.assertEqual('software, multimedia', img.mods.content.resource_type,
            'software, multimedia resource type should be preset in mods')
        self.assertEqual('born digital', img.mods.content.genres[0].text,
            'born digital should be set as mods genre')
        self.assertEqual('aat', img.mods.content.genres[0].authority)
        self.assert_(img.mods.content.schema_valid(),
            'generated mods should be schema-valid')
        # premis
        self.assertEqual('ark', img.provenance.content.object.id_type)
        self.assertEqual('', img.provenance.content.object.id)  # for now, since we don't yet have a pid
        self.assertEqual(aff_md5, img.provenance.content.object.checksums[0].digest)
        self.assertEqual('MD5', img.provenance.content.object.checksums[0].algorithm)
        self.assertEqual(aff_sha1, img.provenance.content.object.checksums[1].digest)
        self.assertEqual('SHA-1', img.provenance.content.object.checksums[1].algorithm)
        self.assertEqual('AFF', img.provenance.content.object.format.name)
        # content datastream
        self.assertEqual(aff_md5, img.content.checksum)
        self.assertEqual(mimetype, img.content.mimetype)

        # for debugging invalid premis
        if not img.provenance.content.schema_valid():
            print img.provenance.content.serialize(pretty=True)
            print img.provenance.content.schema_validation_errors()

        self.assert_(img.provenance.content.schema_valid(),
            'generated premis should be schema-valid')

        # AD1 - only difference should be format name & checksums
        img = DiskImage.init_from_file(ad1_file)
        self.assertEqual('AD1', img.provenance.content.object.format.name)
        self.assertEqual(ad1_md5, img.provenance.content.object.checksums[0].digest)
        self.assertEqual('MD5', img.provenance.content.object.checksums[0].algorithm)
        self.assertEqual(ad1_sha1, img.provenance.content.object.checksums[1].digest)
        # checksum and mimetype should be calculated and set on datastream
        self.assertEqual(ad1_md5, img.content.checksum)
        self.assertEqual('application/x-ad1', img.content.mimetype)

        # simulate ajax upload: label is original filename, file has alternate extension
        # create a temporary, actual file that ends with .upload
        tmpfile = tempfile.NamedTemporaryFile(suffix='.upload')

        img = DiskImage.init_from_file(tmpfile.name, 'DiskImage.aff')
        # object label & title should be filename without extension
        self.assertEqual('DiskImage', img.label)
        self.assertEqual('DiskImage', img.dc.content.title)
        self.assertEqual('DiskImage', img.mods.content.title)
        # format type should be AFF, not UPLOAD
        self.assertEqual('AFF', img.provenance.content.object.format.name)

        # content location
        ds_location = 'file:///some/ingest/path/DiskImage.aff'
        img = DiskImage.init_from_file(tmpfile.name, 'DiskImage.aff',
            content_location=ds_location)
        # content should not be set to open file
        self.assertEqual(None, img.content.content)
        # ds location should be set for fedora to ingest
        self.assertEqual(ds_location, img.content.ds_location)

    def test_init_from_bagit(self):

        # create bag with fixture as payload
        bag_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture as payload
        shutil.copy(ad1_file, bag_path)
        bagit.make_bag(bag_path)

        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            with self.settings(LARGE_FILE_STAGING_FEDORA_DIR=None):
                img = DiskImage.init_from_bagit(bag_path)

        # inspect resulting disk image object
        #  - initial label should be basename of BagIt
        self.assertEqual(os.path.basename(bag_path), img.label)
        mimetype = 'application/x-ad1'
        self.assertEqual(mimetype, img.content.mimetype,
            'content mimetype should be set based on disk image file in BagIt')
        self.assertEqual(ad1_md5, img.content.checksum,
            'content checksum should be set from BagIt data')
        # ds location should be file uri for disk image within BagIt
        ds_location = 'file://' + os.path.join(bag_path, 'data',
                                               os.path.basename(ad1_file))
        self.assertEqual(ds_location, img.content.ds_location)

        # fedora base path different than local
        fedora_staging_dir = '/fedora/server/path'
        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            with self.settings(LARGE_FILE_STAGING_FEDORA_DIR=fedora_staging_dir):
                img = DiskImage.init_from_bagit(bag_path)

        # ds location should be file uri for disk image within BagIt
        ds_location = 'file://' + os.path.join(fedora_staging_dir,
            os.path.basename(bag_path), 'data',
            os.path.basename(ad1_file))
        self.assertEqual(ds_location, img.content.ds_location)

        # disable file uri ingest
        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            img = DiskImage.init_from_bagit(bag_path, file_uri=False)
        # should be set as content file instead of ds location
        self.assertEqual(None, img.content.ds_location)
        self.assertNotEqual(None, img.content.content)

        # test invalid bag
        os.remove(os.path.join(bag_path, 'data', os.path.basename(ad1_file)))
        self.assertRaises(bagit.BagValidationError, DiskImage.init_from_bagit,
                          bag_path)

        # test valid bag with no disk image content
        nodata_bag_path = tempfile.mkdtemp(dir=self.tempdir)
        bagit.make_bag(nodata_bag_path)
        self.assertRaises(Exception, DiskImage.init_from_bagit,
                          nodata_bag_path)

    def test_init_from_bagit_supplement(self):
        # test creating disk image from bag with supplemental files
        baggy_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture and create supplemental files
        text_content = 'some text about the disk image'
        shutil.copy(ad1_file, baggy_path)
        with open(os.path.join(baggy_path, 'info.txt'), 'w') as txtfile:
            txtfile.write(text_content)
        xml_content = '<xml/>'
        with open(os.path.join(baggy_path, 'extra.xml'), 'w') as xmlfile:
            xmlfile.write(xml_content)
        baggy_bag = bagit.make_bag(baggy_path)
        img = DiskImage.init_from_bagit(baggy_path, file_uri=False)

        # actually save to fedora to test supplemental datastream
        # handling, since it is not the usual way we do things
        img.save('testing supplemental datastreams')

        # get fresh copy to inspect
        new_obj = self.repo.get_object(img.pid, type=DiskImage)
        self.assert_('supplement0' in new_obj.ds_list)
        self.assert_('supplement1' in new_obj.ds_list)

        # no guarantees what order they are added so figure out by label
        supplement0 = new_obj.getDatastreamObject('supplement0')
        supplement1 = new_obj.getDatastreamObject('supplement1')
        if supplement0.label == 'info.txt':
            txt_supplement = supplement0
            xml_supplement = supplement1
        else:
            txt_supplement = supplement1
            xml_supplement = supplement0

        # text file datastream
        self.assertEqual('text/plain', txt_supplement.mimetype)
        self.assertEqual(baggy_bag.entries['data/info.txt']['md5'],
                         txt_supplement.checksum)
        self.assertEqual(text_content, txt_supplement.content)
        # xml file datastream
        self.assertEqual('text/plain', xml_supplement.mimetype)
        # NOTE: mimetype magic doesn't distinguish xml from text
        self.assertEqual(baggy_bag.entries['data/extra.xml']['md5'],
                         xml_supplement.checksum)
        self.assertEqual(xml_content, xml_supplement.content)

        # supplemental file uri ingest
        img = DiskImage.init_from_bagit(baggy_path)
        s0 = img.getDatastreamObject('supplement0')
        s1 = img.getDatastreamObject('supplement1')
        s_locations = [s0.ds_location, s1.ds_location]
        path = 'file://%s/data/info.txt' % baggy_path
        self.assert_(path in s_locations,
            'file uri %s should be used for a supplemental datastream location' % path)
        path = 'file://%s/data/extra.xml' % baggy_path
        self.assert_(path in s_locations,
            'file uri %s should be used for a supplemental datastream location' % path)

        # fedora base path different than local
        fedora_staging_dir = '/fedora/server/path'
        with self.settings(LARGE_FILE_STAGING_DIR=self.tempdir):
            with self.settings(LARGE_FILE_STAGING_FEDORA_DIR=fedora_staging_dir):
                img = DiskImage.init_from_bagit(baggy_path)

        s0 = img.getDatastreamObject('supplement0')
        s1 = img.getDatastreamObject('supplement1')
        s_locations = [s0.ds_location, s1.ds_location]
        base_path = os.path.join(fedora_staging_dir, os.path.basename(baggy_path))
        self.assert_('file://%s/data/info.txt' % base_path in s_locations)
        self.assert_('file://%s/data/extra.xml' % base_path in s_locations)

    def test_update_dc(self):
        img = DiskImage.init_from_file(ad1_file)
        img.mods.content.title = 'AD1 Disk Image'
        img.mods.content.create_abstract()
        img.mods.content.abstract.text = 'long description of the image'
        img.mods.content.coveringdate_start = '2001-01-01'
        img.mods.content.coveringdate_end = '2004-12-31'
        img.rights.content.create_access_status()
        img.rights.content.access_status.text = 'rights & restrictions'

        img._update_dc()
        self.assertEqual(img.mods.content.title, img.label)
        self.assertEqual(img.mods.content.title, img.dc.content.title)
        self.assertEqual(img.mods.content.abstract.text, img.dc.content.description)
        self.assertEqual('%s:%s' % (img.mods.content.coveringdate_start,
                                    img.mods.content.coveringdate_end),
                         img.dc.content.coverage)
        self.assertEqual(img.rights.content.access_status.text, img.dc.content.rights)


    def test_index_data(self):
        # test custom data used for indexing objects in solr
        obj = self.repo.get_object(type=DiskImage)
        obj.pid = 'foo:1'
        obj.dc.content.title = 'ComputerName'
        # set an ark to confirm it is passed through to index data
        obj.mods.content.identifiers.append(
            mods.Identifier(type='uri', text='http://some.co/ark:/naan/1234')
        )
        obj.content.checksum = 'bogusmd5'

        # collection is an eulfedora.models.Relation, so patch on the class
        with patch('keep.file.models.DiskImage.collection') as mockcoll:
            mockcoll.pid = 'parent:1'
            mockcoll.uri = 'info:fedora/parent:1'
            mockcoll.label = 'mss collection'
            mockcoll.exists = True
            # should work with any id value including 0
            mockcoll.mods.content.source_id = 0

            desc_data = obj.index_data()
            self.assertEqual(obj.collection.uri, desc_data['collection_id'],
                             'parent collection object id should be set in index data')
            self.assertEqual(mockcoll.label, desc_data['collection_label'],
                             'parent collection object label should be set in index data')
            self.assertEquals(obj.collection.mods.content.source_id, desc_data['collection_source_id'],
                              'collection_source_id should be %s but is is %s' %
                              (obj.collection.mods.content.source_id, desc_data['collection_source_id']))

        self.assertEqual(obj.dc.content.title, desc_data['title'][0],
                         'default index data fields should be present in data (title)')
        self.assertEqual(obj.pid, desc_data['pid'],
                         'default index data fields should be present in data (pid)')
        self.assertEqual(obj.mods.content.ark_uri, desc_data['ark_uri'],
                         'ark uri should be present in index data')
        self.assertEqual(obj.content.checksum, desc_data['content_md5'],
                         'content datastream checksum should be included in index data')

    def test_supplemental_content(self):
        # test properties for interacting with supplemental file datastreams

        # image with no supplemental content
        img = DiskImage.init_from_file(ad1_file)
        img.save()
        self.assertFalse(img.has_supplemental_content)
        self.assertEqual([], list(img.supplemental_content))

        # create disk image from bag with supplemental files
        baggy_path = tempfile.mkdtemp(dir=self.tempdir)
        # copy in ad1 fixture and create supplemental files
        text_content = 'some text about the disk image'
        shutil.copy(ad1_file, baggy_path)
        with open(os.path.join(baggy_path, 'info.txt'), 'w') as txtfile:
            txtfile.write(text_content)
        xml_content = '<xml/>'
        with open(os.path.join(baggy_path, 'extra.xml'), 'w') as xmlfile:
            xmlfile.write(xml_content)
        # convert to bagit
        bagit.make_bag(baggy_path)
        img = DiskImage.init_from_bagit(baggy_path, file_uri=False)
        img.save()  # has to be saved to inspect datastreams
        img = self.repo.get_object(img.pid, type=DiskImage)
        self.assertTrue(img.has_supplemental_content)
        supplements = list(img.supplemental_content)
        self.assertEqual(2, len(supplements))


class PremisEditFormTest(TestCase):

    fixtures = ['test-applications.json']

    # use init from file as a convenient way to ensure working with valid premis
    img = DiskImage.init_from_file(ad1_file)
    instance = img.provenance.content
    today = datetime.date.today()

    def test_initial_data(self):
        # date and creating application not yet set in xml
        form = PremisEditForm(instance=self.instance)
        self.assert_('date' not in form.initial)
        self.assert_('application' not in form.initial)

        # set the editable fields
        app = Application.objects.get(name='bitcurator')
        self.instance.object.create_creating_application()
        self.instance.object.creating_application.name = app.name
        self.instance.object.creating_application.version = app.version

        self.instance.object.creating_application.date = self.today
        # on init, xml fields should propagate to initial form data
        form = PremisEditForm(instance=self.instance)
        self.assertEqual(app.id, form.initial['application'])
        self.assertEqual(self.today, form.initial['date'])

    def test_update_instance(self):
        form = PremisEditForm(instance=self.instance,
            data={'application': 1, 'date': self.today})
        self.assertTrue(form.is_valid())  # required before update instance will work

        # inspect updated xml
        updated = form.update_instance()
        app = Application.objects.get(id=1)
        self.assertEqual(app.name, updated.object.creating_application.name)
        self.assertEqual(app.version, updated.object.creating_application.version)
        self.assertEqual(self.today, updated.object.creating_application.date)



