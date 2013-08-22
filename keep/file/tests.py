from mock import Mock, patch
import os
from shutil import copyfile

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from eulfedora.server import Repository
from eullocal.django.taskresult.models import TaskResult

from keep.audio import models as audiomodels
from keep.audio.tests import ADMIN_CREDENTIALS, mp3_filename, wav_filename, \
    mp3_md5, wav_md5
from keep.collection.fixtures import FedoraFixtures
from keep.file.forms import UploadForm
from keep.file.models import DiskImage
from keep.file.utils import md5sum, sha1sum
from keep.testutil import KeepTestCase


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
class FileViewsTest(KeepTestCase):
    fixtures = ['users']

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
        copyfile(wav_filename, upload_filepath)
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
        copyfile(wav_filename, upload_filepath)     # re-copy file, now that is removed after ingest
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

            #upload same file but add a comment
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

        aff_file = os.path.join(settings.BASE_DIR, 'file', 'fixtures', 'test.aff')
        md5 = '7a0c337b817442796e5816afb731209b'

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
            self.assertEqual(md5, new_obj.provenance.content.object.checksums[0].digest)




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


class DiskImageTest(KeepTestCase):
    aff_file = os.path.join(settings.BASE_DIR, 'file', 'fixtures', 'test.aff')
    md5 = '7a0c337b817442796e5816afb731209b'
    sha1 = 'd7957b2845ad83df7de711cf8c6f418c22c67936'

    def test_init_from_file(self):
        label = 'My Disk Image'
        img = DiskImage.init_from_file(self.aff_file, label)
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
        self.assertEqual(self.md5, img.provenance.content.object.checksums[0].digest)
        self.assertEqual('MD5', img.provenance.content.object.checksums[0].algorithm)
        self.assertEqual(self.sha1, img.provenance.content.object.checksums[1].digest)
        self.assertEqual('SHA-1', img.provenance.content.object.checksums[1].algorithm)
        self.assertEqual('AFF', img.provenance.content.object.format.name)
        # for debugging invalid premis
        if not img.provenance.content.schema_valid():
            print img.provenance.content.serialize(pretty=True)
            print img.provenance.content.schema_validation_errors()

        self.assert_(img.provenance.content.schema_valid(),
            'generated premis should be schema-valid')

