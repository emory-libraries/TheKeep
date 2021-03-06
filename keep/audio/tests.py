import cStringIO
from datetime import datetime
import logging
import json
from mock import Mock, patch
import os
from shutil import copyfile
import stat
import sys
from subprocess import call
from sunburnt import sunburnt
import tempfile
from time import sleep
from unittest import skipIf
import wave

from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.core.management.base import CommandError
from django.test import Client, TestCase

from eulfedora.server import Repository
from eulfedora.models import DigitalObjectSaveFailure
from eulcommon.djangoextras.taskresult.models import TaskResult
from eulfedora.util import RequestFailed, ChecksumMismatch
from eulxml.xmlmap import load_xmlobject_from_string
from eulxml.xmlmap import mods

from keep.accounts.models import ResearcherIP
from keep.audio import forms as audioforms, models as audiomodels
from keep.audio.management.commands import ingest_cleanup
from keep.audio.tasks import convert_wav_to_mp3
from keep.audio.templatetags import audio_extras
from keep.collection.fixtures import FedoraFixtures
from keep.collection.models import CollectionObject
from keep.common.models import SourceTechMeasure, TransferEngineer, CodecCreator
from keep.testutil import KeepTestCase, mocksolr_nodupes

logger = logging.getLogger(__name__)

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



# mock archives used to generate archives choices for form field
@patch('keep.collection.forms.CollectionObject.archives',
       new=Mock(return_value=FedoraFixtures.archives(format=dict)))
# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class AudioViewsTest(KeepTestCase):
    fixtures = ['users', 'initial_groups']

    client = Client()

    # set up a mock solr object for use in solr-based find methods
    mocksolr = Mock(sunburnt.SolrInterface)
    mocksolr.return_value = mocksolr
    # solr interface has a fluent interface where queries and filters
    # return another solr query object; simulate that as simply as possible
    mocksolr.query.return_value = mocksolr.query
    mocksolr.query.query.return_value = mocksolr.query
    mocksolr.query.paginate.return_value = mocksolr.query
    mocksolr.query.exclude.return_value = mocksolr.query

    def setUp(self):
        super(AudioViewsTest, self).setUp()
        self.pids = []
        # store settings that may be changed when testing podcast feed pagination
        self._template_context_processors = getattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS', None)

        # collection fixtures are not modified, but there is no clean way
        # to only load & purge once
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.esterbrook = FedoraFixtures.esterbrook_collection()
        self.esterbrook.save()
        self.englishdocs = FedoraFixtures.englishdocs_collection()
        self.englishdocs.save()

    def tearDown(self):
        super(AudioViewsTest, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            try:
                self.repo.purge_object(pid)
            except:
                logger.info('could not purge %s' % pid)

        if self._template_context_processors is not None:
            settings.TEMPLATE_CONTEXT_PROCESSORS = self._template_context_processors
        else:
            del settings.TEMPLATE_CONTEXT_PROCESSORS

        # TODO: remove any test files created in staging dir
        # FIXME: should we create & remove a tmpdir instead of using actual staging dir?

        self.repo.purge_object(self.rushdie.pid)
        self.repo.purge_object(self.esterbrook.pid)
        self.repo.purge_object(self.englishdocs.pid)

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

        expected = 'attachment; filename="%s.wav"' % obj.noid
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Disposition'], download_url))

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

        download_url = reverse('audio:download-compressed-audio', args=[obj.pid, 'mp3'])

        response = self.client.get(download_url)
        code = response.status_code
        expected = 404
        self.assertEqual(code, expected,
                         'Expected %s but returned %s for %s as admin for non-existent audio file'
                         % (expected, code, download_url))

        # Set a compressed audio stream.
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

        expected = 'attachment; filename="%s.mp3"' % obj.noid
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Disposition'], download_url))

        # logout to test guest/researcher access
        self.client.logout()
        response = self.client.get(download_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, download_url, got))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to audio download view should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()
        # object not researcher-accessible; should still not get access
        response = self.client.get(download_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as researcher, got %s' % \
            (expected, download_url, got))

        # update object with researcher-accessible status code
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = 2
        obj.save()

        # request does not include http range header; should still not get access
        response = self.client.get(download_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as researcher without http range, got %s' % \
            (expected, download_url, got))

        response = self.client.get(download_url, HTTP_RANGE='bytes=0-')
        expected, got = 206, response.status_code
        self.assertEqual(expected, got, 'Expected %s but returned %s for %s as patron with http range in request'
                             % (expected, got, download_url))
        # spot-check response object
        expected = 'audio/mpeg'
        self.assertEqual(response['Content-Type'], expected,
                        "Expected '%s' but returned '%s' for %s mimetype" % \
                        (expected, response['Content-Type'], download_url))
        researchip.delete()

        # log back in as admin to test errors
        self.client.login(**ADMIN_CREDENTIALS)

        # attempt to download mp3 as m4a - should 404
        m4a_download_url = reverse('audio:download-compressed-audio', args=[obj.pid, 'm4a'])
        response = self.client.get(m4a_download_url)
        code = response.status_code
        expected = 404
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (MP3 datastream as M4A)'
                             % (expected, code, m4a_download_url))

        # pretend mp3 datastream is actually m4a
        obj.compressed_audio.mimetype = 'audio/mp4'
        obj.compressed_audio.save('set mimetype to mp4')
        response = self.client.get(m4a_download_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (M4A'
                             % (expected, code, m4a_download_url))
        expected = 'attachment; filename="%s.m4a"' % obj.noid
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Disposition'], download_url))

        # attempt to download m4a as mp3 - should 404
        response = self.client.get(download_url)
        code = response.status_code
        expected = 404
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (M4A datastream as MP3)'
                             % (expected, code, download_url))

    @patch('keep.common.utils.solr_interface')  # for index page redirect
    def test_edit(self, mocksolr):
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
        ldap_user = get_user_model().objects.get(username='ldap_user')
        audio_curator = Group.objects.get(name='Audio Curator')
        ldap_user.groups.add(audio_curator)

        # engineer & codec creator are initialized based on id values
        obj.digitaltech.content.create_transfer_engineer()
        obj.digitaltech.content.transfer_engineer.id = ldap_user.username
        obj.digitaltech.content.transfer_engineer.id_type = TransferEngineer.LDAP_ID_TYPE
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

        # mock collection item_collections so test collection will be based on fixture collections
        collection_choices = list(
            {'pid': coll.pid, 'source_id': coll.mods.content.source_id, 'title': coll.label}
            for coll in [self.rushdie, self.esterbrook, self.englishdocs])
        with patch('keep.collection.forms.CollectionObject.item_collections',
                   new=Mock(return_value=collection_choices)):
            response = self.client.get(edit_url)
            expected, code = 200, response.status_code
            self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                                 % (expected, code, edit_url))
            self.assert_(isinstance(response.context['form'], audioforms.AudioObjectEditForm),
                    "MODS EditForm is set in response context")
            self.assert_(isinstance(response.context['form'].object_instance, audiomodels.AudioObject),
                    "form instance is an AudioObject")
            # edit form no longer contains collection pids (auto-complete instead of drop-down)

            # audio datastream links
            self.assertContains(response, reverse('audio:download-audio', kwargs={'pid': obj.pid}),
                                msg_prefix='edit page should link to audio datastream when available')
            self.assertContains(response, 'original audio',
                                msg_prefix='edit page should link to original audio datastream when available')
            self.assertNotContains(response, reverse('audio:download-compressed-audio',
                                kwargs={'pid': obj.pid, 'extension': 'mp3' }),
                                msg_prefix='edit page should not link to non-existent comprresed audio')
            # purge audio datastream to simulate a metadata migration object with no master audio
            purged = obj.api.purgeDatastream(obj.pid, audiomodels.AudioObject.audio.id)
            response = self.client.get(edit_url)
            self.assertNotContains(response, reverse('audio:download-audio', kwargs={'pid': obj.pid}),
                                msg_prefix='edit page should not link to non-existent audio datastream')
            self.assertContains(response, 'original audio',
                                msg_prefix='edit page should display original audio as unavailable')

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
            self.assertEqual('%s|%s' % (TransferEngineer.LDAP_ID_TYPE, ldap_user.username),
                             initial_data['engineer'])
            self.assertEqual(item_dt.codec_creator.id, initial_data['hardware'])
            # rights in initial data
            initial_data = response.context['form'].rights.initial
            item_rights = obj.rights.content
            self.assertEqual(item_rights.access_status.code, initial_data['access'])
            self.assertEqual(item_rights.copyright_holder_name, initial_data['copyright_holder_name'])
            self.assertEqual(item_rights.copyright_date, initial_data['copyright_date'])

            # POST data to update audio object in fedora
            audio_data = {'collection_0': self.rushdie.uri,
                          'collection_1': self.rushdie.label,
                        'mods-title': u'new title \u2026',
                        'mods-note-label': 'a general note',
                        #'mods-general_note-text': u'remember to ... with some unicode \u1f05',
                        'mods-general_note-text': u'remember to',
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
                        'dt-engineer': '%s|%s' % (TransferEngineer.LDAP_ID_TYPE,
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
            messages = [str(msg) for msg in response.context['messages']]
            self.assert_(messages[0].startswith("Successfully updated"),
                "successful save message set in response context")
            # currently redirects to audio index
            (redirect_url, code) = response.redirect_chain[0]
            self.assert_(reverse('site-index') in redirect_url,
                "successful save redirects to audio index page")
            expected = 303      # redirect
            self.assertEqual(code, expected,
                'Expected %s but returned %s for %s (successfully saved)' % \
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
            self.assertEqual(self.rushdie.uriref, updated_obj.collection.uriref,
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
            self.assertEqual(TransferEngineer.LDAP_ID_TYPE, dt.transfer_engineer.id_type)
            self.assertEqual(ldap_user.username, dt.transfer_engineer.id)
            self.assertEqual(ldap_user.get_full_name(), dt.transfer_engineer.name)
            # codec creator - used id 3, which has two hardware fields
            hardware, software, version = CodecCreator.configurations[audio_data['dt-hardware']]
            self.assertEqual(audio_data['dt-hardware'], dt.codec_creator.id)
            self.assertEqual(hardware[0], dt.codec_creator.hardware_list[0])
            self.assertEqual(hardware[1], dt.codec_creator.hardware_list[1])
            self.assertEqual(software, dt.codec_creator.software)
            self.assertEqual(version, dt.codec_creator.software_version)

            #check audit trail has default edit message when no comment is provided
            audit_trail = [a.message for a in obj.audit_trail.records]
            self.assertEqual("update metadata", audit_trail[-1])

            #add comment to metadata and check the response
            data = audio_data.copy()
            data['comments-comment'] = 'This is a very interesting comment'
            data['dt-hardware'] = '4'  # make a change so the obj will save
            response = self.client.post(edit_url, data)

            # get the latest copy of the object
            updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
            audit_trail = [a.message for a in updated_obj.audit_trail.records]
            self.assertEqual("This is a very interesting comment", audit_trail[-1])

            # change data and confirm codec creator is updated correctly
            data = audio_data.copy()
            data['dt-hardware'] = '4'  # only one hardware, no software version
            response = self.client.post(edit_url, data)
            # get the latest copy of the object
            updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
            dt = updated_obj.digitaltech.content
            # codec creator - id 4 only has one two hardware and no software version
            hardware, software, version = CodecCreator.configurations[data['dt-hardware']]
            self.assertEqual(data['dt-hardware'], dt.codec_creator.id)
            self.assertEqual(hardware[0], dt.codec_creator.hardware_list[0])
            self.assertEqual(1, len(dt.codec_creator.hardware_list))  # should only be one now
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
            messages = [str(msg) for msg in response.context['messages']]
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
            messages = [str(msg) for msg in response.context['messages']]
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
            obj.digitaltech.content.transfer_engineer.id_type = TransferEngineer.DM_ID_TYPE
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
            self.assertEqual(obj.digitaltech.content.transfer_engineer.id,
                             updated_obj.digitaltech.content.transfer_engineer.id)
            self.assertEqual(obj.digitaltech.content.transfer_engineer.id_type,
                             updated_obj.digitaltech.content.transfer_engineer.id_type)
            self.assertEqual(obj.digitaltech.content.transfer_engineer.name,
                             updated_obj.digitaltech.content.transfer_engineer.name)
            # test local transfer engineer options
            # - when displaying the form, local options should be available
            response = self.client.get(edit_url)
            for local_id, local_name in TransferEngineer.local_engineers.iteritems():
                self.assertContains(response, '%s|%s' % (TransferEngineer.LOCAL_ID_TYPE,
                                                         local_id),
                    msg_prefix='select id should be listed for local transfer engineer %s' % local_name)
                self.assertContains(response, local_name,
                    msg_prefix='local transfer engineer name %s should be listed' % local_name)

            # save a record with a local transfer engineer
            data['dt-engineer'] = 'local|vendor1'
            response = self.client.post(edit_url, data)
            # id type, id, and name should all be set to local engineer info
            updated_obj = repo.get_object(pid=obj.pid, type=audiomodels.AudioObject)
            self.assertEqual(TransferEngineer.LOCAL_ID_TYPE,
                             updated_obj.digitaltech.content.transfer_engineer.id_type)
            self.assertEqual('vendor1', updated_obj.digitaltech.content.transfer_engineer.id)
            self.assertEqual('Vendor', updated_obj.digitaltech.content.transfer_engineer.name)

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
        ldap_user = get_user_model().objects.get(username='ldap_user')
        audio_curator = Group.objects.get(name='Audio Curator')
        ldap_user.groups.add(audio_curator)

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        edit_url = reverse('audio:edit', args=[obj.pid])

        # POST data to update audio object in fedora
        audio_data = {'collection_0': self.rushdie.uri,
                      'collection_1': self.rushdie.label,
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
                    'dt-engineer': '%s|%s' % (TransferEngineer.LDAP_ID_TYPE,
                                              ldap_user.username),
                    'dt-hardware': '3',
                    # rights metadata
                    'rights-access': 8,   # public domain
        }

        coll_info = {'pid': self.rushdie.pid, 'source_id': '1000', 'title': self.rushdie.label}
        # mock collection item_collections so test collection will be in edit form choices
        with patch('keep.collection.forms.CollectionObject.item_collections',
                   new=Mock(return_value=[coll_info])):
            response = self.client.post(edit_url, audio_data, follow=True)
            print response
            # currently redirects to audio index
            (redirect_url, code) = response.redirect_chain[0]
            self.assert_(reverse('site-index') in redirect_url,
                         "successful save redirects to audio index page")

            messages = [str(msg) for msg in response.context['messages']]
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

        # NOTE: as of 2013/07, response content is failing
        # this view is a thin wrapper around an eulfedora generic view,
        # so mainly we need to test that the correct datastreams are
        # configured and accessible.
        # response content tests disabled.

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
        # self.assertContains(response, '<mods:title>%s</mods:title>' % \
        #                     obj.mods.content.title)

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
        # self.assertContains(response, obj.AUDIO_CONTENT_MODEL)
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
        content = ' '.join(response.streaming_content)
        self.assertTrue('<st:sourcetech' in content)
        self.assertTrue(obj.sourcetech.content.note in content)
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
        content = ' '.join(response.streaming_content)
        self.assertTrue('<dt:digitaltech' in content)
        self.assertTrue(obj.digitaltech.content.date_captured in content)

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

    def test_view(self):
        # create a test audio object to display
        obj = audiomodels.AudioObject.init_from_file(wav_filename, "my audio test object")
        obj.mods.content.ark_uri = 'http://pid.co/ark:/12345/4sr46'
        obj.mods.content.create_part_note()
        obj.mods.content.part_note.text = 'Side 1'
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date='1975-10-31'))
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1978-12-25'))
        # pre-populate digital tech metadata
        obj.digitaltech.content.duration = 75
        obj.collection = self.esterbrook
        # set non-researcher accessible code
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = 9
        obj.rights.content.access_status.text = 'PD - Restricted by Donor or MARBL'
        # NOTE: possibly also test override flag?
        obj.save()
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)

        # TEMPORARY: requires login for now, until permissions are sorted
        self.client.login(**ADMIN_CREDENTIALS)

        view_url = reverse('audio:view', args=[obj.pid])
        response = self.client.get(view_url)
        self.assertContains(response, obj.label,
            msg_prefix='audio view page should include object label')
        self.assertContains(response, obj.collection.label,
            msg_prefix='audio view page should include object collection label')
        self.assertContains(response, obj.collection.mods.content.source_id,
            msg_prefix='audio view page should include object collection number')
        # TODO: test edit link only displayed if user has perms
        # NOTE: dates are converted to human-readable equivalent
        self.assertContains(response, 'Dec 25, 1978',
            msg_prefix='date issued should be displayed in human-readable form when present in metadata')
        self.assertContains(response, 'Oct 31, 1975',
            msg_prefix='date created should be displayed in human-readable form when present in metadata')
        self.assertContains(response, obj.mods.content.part_note.text,
            msg_prefix='part note should be displayed when present')
        self.assertContains(response, '1 minute, 15 seconds',
            msg_prefix='duration should be displayed in human-readable form')
        self.assertContains(response, obj.mods.content.ark_uri.replace('http://pid.co/', ''),
            msg_prefix='ARK URI (short form) should be displayed')
        self.assertContains(response, obj.get_access_url(),
            msg_prefix='access audio url should be present on view page for playback')
        # warning that item is not researcher-accessible
        self.assertContains(response, 'This item is not accessible to researchers.',
            msg_prefix='warning should be displayed for content that is not researcher-accessible')
        self.assertContains(response, obj.rights.content.access_status.code,
            msg_prefix='non-researcher-accessible content should show access status code')
        self.assertContains(response, obj.rights.content.access_status.text,
            msg_prefix='non-researcher-accessible content should show access status text')

        # logout to test guest/researcher access
        self.client.logout()
        response = self.client.get(view_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, view_url, got))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to audio view should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()
        response = self.client.get(view_url)
        # should still redirect if object is not researcher-accessible
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as researcher, got %s' % \
            (expected, view_url, got))

        # update object with researcher-accessible status code
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = 2
        obj.save()
        response = self.client.get(view_url)
        # spot-check that page renders
        self.assertContains(response, obj.label,
            msg_prefix='researcher-accessible audio view page should display to patron')

        researchip.delete()

    def test_audit_trail(self):
        # create a test audio object with ingest message
        obj = audiomodels.AudioObject.init_from_file(wav_filename, "my audio test object")
        obj.mods.content.title = 'test audio object'
        obj.save('audit trail test')
        # add pid to list for clean-up in tearDown
        self.pids.append(obj.pid)

        self.client.login(**ADMIN_CREDENTIALS)

        audit_url = reverse('audio:audit-trail', kwargs={'pid': obj.pid})
        response = self.client.get(audit_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (raw audit trail xml)' \
                % (expected, got, audit_url))
        self.assertContains(response, 'justification>audit trail test</audit')

    def test_tasks(self):
        # test view method for queuing tasks (access copy conversion)
        self.client.login(**ADMIN_CREDENTIALS)
        tasks_url = reverse('audio:tasks', args=[self.rushdie.pid])

        # anything but a POST is currently invalid
        response = self.client.get(tasks_url)
        self.assertEqual(405, response.status_code)   # method not allowed

        # POST unsupported task type
        bogus_task = 'stand on your head'
        response = self.client.post(tasks_url, {'task': bogus_task})
        self.assertContains(response, 'Task "%s" is not supported' % bogus_task,
            status_code=500)

        # supported task type
        gen_access = 'generate access copy'

        # mock repo / object to simulate errors, success
        with patch('keep.audio.views.Repository') as mockrepo:
            mockobj = mockrepo.return_value.get_object.return_value
            # non-existent object
            mockobj.exists = False
            response = self.client.post(tasks_url, {'task': gen_access})
            self.assertEqual(404, response.status_code,
                'view should 404 when object does not exist')

            # exists but is not audio
            mockobj.exists = True
            mockobj.has_requisite_content_models = False
            response = self.client.post(tasks_url, {'task': gen_access})
            self.assertEqual(404, response.status_code,
                'view should 404 when object is not an audio object')

            # exists and is audio
            mockobj.has_requisite_content_models = True
            with patch('keep.audio.views.queue_access_copy') as mock_qac:
                # success
                response = self.client.post(tasks_url, {'task': gen_access})
                self.assertContains(response, 'Successfully queued access copy conversion')
                # queue method should be called
                self.assertEqual(1, mock_qac.call_count)

                # error message
                mockobj = mockrepo.return_value.get_object.side_effect = Exception('timed out')
                response = self.client.post(tasks_url, {'task': gen_access})
                self.assertContains(response, 'Error queueing access copy conversion (timed out)')

# TODO: mock out the fedora connection and find a way to verify that we
# handle fedora outages appropriately

# tests for MODS XmlObject
# FIXME: mods objects no longer part of keep.audio - where should these tests live?
class TestMods(KeepTestCase):
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
        super(TestMods, self).setUp()
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
                                   mods.RelatedItem(type='isReferencedBy', title='Finding Aid')])
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


class TestModsTypedNote(KeepTestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        super(TestModsTypedNote, self).setUp()
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


class TestModsDate(KeepTestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        super(TestModsDate, self).setUp()
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


class TestModsOriginInfo(KeepTestCase):
    # node fields tested in main mods test case; testing custom is_empty logic here

    def setUp(self):
        super(TestModsOriginInfo, self).setUp()
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


class SourceTechTest(KeepTestCase):
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
        super(SourceTechTest, self).setUp()
        self.sourcetech = load_xmlobject_from_string(self.FIXTURE, audiomodels.SourceTech)

    def test_init_types(self):
        self.assert_(isinstance(self.sourcetech, audiomodels.SourceTech))
        self.assert_(isinstance(self.sourcetech.speed, SourceTechMeasure))
        self.assert_(isinstance(self.sourcetech.reel_size, SourceTechMeasure))

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


class DigitalTechTest(KeepTestCase):
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
        super(DigitalTechTest, self).setUp()
        self.digitaltech = load_xmlobject_from_string(self.FIXTURE, audiomodels.DigitalTech)

    def test_init_types(self):
        self.assert_(isinstance(self.digitaltech, audiomodels.DigitalTech))
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


# TODO: move into eulcm.boda

# class RightsXmlTest(KeepTestCase):
#     FIXTURE =  '''<?xml version="1.0" encoding="UTF-8"?>
# <rt:rights version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rt="http://pid.emory.edu/ns/2010/rights"  xsi="http://pid.emory.edu/ns/2010/sourcetech/v1/rights-1.xsd">
#     <rt:accessStatus code="2">Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement</rt:accessStatus>
#     <rt:copyrightholderName>Hughes, Carol</rt:copyrightholderName>
#     <rt:copyrightDate encoding="w3cdtf">1923</rt:copyrightDate>
#     <rt:ipNotes>Written permission required.</rt:ipNotes>
# </rt:rights>'''

#     def setUp(self):
#         super(RightsXmlTest, self).setUp()
#         self.rights = load_xmlobject_from_string(self.FIXTURE, audiomodels.Rights)

#     def test_init_types(self):
#         self.assert_(isinstance(self.rights, audiomodels.Rights))
#         self.assert_(isinstance(self.rights.access_status, commonmodels.AccessStatus))

#     def test_fields(self):
#         # check field values correctly accessible from fixture
#         self.assertEqual('2', self.rights.access_status.code)
#         self.assertEqual('Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement',
#             self.rights.access_status.text)
#         self.assertEqual('Hughes, Carol', self.rights.copyright_holder_name)
#         self.assertEqual('1923', self.rights.copyright_date)
#         self.assertEqual('Written permission required.', self.rights.ip_note)
#         self.assertEqual(False, self.rights.block_external_access)

#     def test_create(self):
#         # test creating digitaltech metadata from scratch
#         rt = audiomodels.Rights()
#         rt.create_access_status()
#         rt.access_status.code = 8    # public domain
#         rt.access_status.text = 'In public domain, no contract restriction'
#         rt.copyright_holder_name = 'Mouse, Mickey'
#         rt.copyright_date = '1928'
#         rt.ip_note = 'See WATCH list for copyright contact info'
#         rt.block_external_access = True

#         # quick sanity check
#         self.assertTrue('<rt:rights' in rt.serialize())

#         # also, did block_external_access actually create its subelement?
#         self.assertTrue('<rt:externalAccess>deny</' in rt.serialize())

#         # TODO: more fields tests; validate against schema when we have one


# tests for Audio DigitalObject
# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class TestAudioObject(KeepTestCase):
    fixtures = ['users']
    repo = Repository()

    def setUp(self):
        super(TestAudioObject, self).setUp()
        self.pids = []
        # create a test audio object to edit
        with open(wav_filename) as wav:
            self.obj = self.repo.get_object(type=audiomodels.AudioObject)
            self.obj.label = "Testing, one, two"
            self.obj.dc.content.title = self.obj.label
            self.obj.audio.content = wav
            self.obj.save()
            self.pids.append(self.obj.pid)

        # collection fixture
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.pids.append(self.rushdie.pid)

    def tearDown(self):
        super(TestAudioObject, self).tearDown()

        for pid in self.pids:
            try:
                self.repo.purge_object(pid, "removing unit test fixture")
            except RequestFailed:
                logger.warn('Failed to purge test fixture %s' % pid)

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
        self.obj.mods.content.title = ' '.join(['this is the song that never ends' for i in range(0, 10)])
        # save will cause an exception if the object label is not truncated correctly
        self.obj.save()

    def test_save_and_update_dc(self):
        # check that update_dc is only called when it ought to be

        with patch.object(self.obj, '_update_dc') as mock_update_dc:
            # nothing modified - update_dc should not be called
            self.obj.save()
            self.assertEqual(0, mock_update_dc.call_count)

            # if any one of these datastreams is modified, update_dc should
            # be called on save

            # mods
            with patch.object(self.obj.mods, 'isModified', new=Mock(return_value=True)):
                try:
                    self.obj.save()
                except DigitalObjectSaveFailure:
                    # generating a digitalobject save failure - ignore
                    pass
                self.assertEqual(1, mock_update_dc.call_count)
            mock_update_dc.reset_mock()

            # rels-ext
            with patch.object(self.obj.rels_ext, 'isModified', new=Mock(return_value=True)):
                self.obj.save()
                self.assertEqual(1, mock_update_dc.call_count)
            mock_update_dc.reset_mock()

            # digital tech
            with patch.object(self.obj.digitaltech, 'isModified', new=Mock(return_value=True)):
                try:
                    self.obj.save()
                except DigitalObjectSaveFailure:
                    pass
                self.assertEqual(1, mock_update_dc.call_count)
            mock_update_dc.reset_mock()

            # rights
            with patch.object(self.obj.rights, 'isModified', new=Mock(return_value=True)):
                try:
                    self.obj.save()
                except DigitalObjectSaveFailure:
                    pass
                self.assertEqual(1, mock_update_dc.call_count)

    def test_update_dc(self):
        # set values in MODS, RELS-EXT, digitaltech
        title, res_type = 'new title in mods', 'text'
        self.obj.mods.content.title = title
        self.obj.mods.content.dm1_id = '1001'
        self.obj.mods.content.dm1_other_id = '000004'
        self.obj.mods.content.resource_type = res_type
        cdate, idate = '2010-01-03', '2010-05-05'
        self.obj.mods.content.create_origin_info()
        self.obj.mods.content.origin_info.created.append(mods.DateCreated(date=cdate))
        self.obj.mods.content.origin_info.issued.append(mods.DateIssued(date=idate))
        general_note = 'The Inspector General generally inspects'
        self.obj.mods.content.create_general_note()
        self.obj.mods.content.general_note.text = general_note
        # names
        namepartxml = mods.NamePart(text='Dawson, William Levi')
        rolexml = mods.Role(type='text', authority='marcrelator',
                            text='Composer')
        namexml = mods.Name(type='personal', authority='naf')
        namexml.name_parts.append(namepartxml)
        namexml.roles.append(rolexml)
        self.obj.mods.content.names.append(namexml)
        namepartxml = mods.NamePart(text='American Symphony Orchestra')
        rolexml = mods.Role(type='text', authority='marcrelator',
                            text='Performer')
        namexml = mods.Name(type='corporate', authority='naf')
        namexml.name_parts.append(namepartxml)
        namexml.roles.append(rolexml)
        self.obj.mods.content.names.append(namexml)
        related_files = '1000, 2011'
        self.obj.sourcetech.content.related_files = related_files
        dig_purpose = 'patron request'
        self.obj.digitaltech.content.digitization_purpose = dig_purpose
        self.obj.rights.content.create_access_status()
        self.obj.rights.content.access_status.code = '8'
        self.obj.rights.content.access_status.text = 'Material is in public domain'
        self.obj.collection = self.obj.get_object(self.rushdie.uri)
        self.obj._update_dc()

        self.assertEqual(title, self.obj.dc.content.title)
        # dm1 ids no longer need to be in dc:identifier (indexed & searched via solr)
        self.assert_(self.obj.mods.content.dm1_id not in self.obj.dc.content.identifier_list)
        self.assert_(self.obj.mods.content.dm1_other_id not in self.obj.dc.content.identifier_list)
        self.assertEqual(res_type, self.obj.dc.content.type)
        for name in self.obj.mods.content.names:
            self.assert_(unicode(name) in self.obj.dc.content.creator_list)
        self.assert_(cdate in self.obj.dc.content.date_list)
        self.assert_(idate in self.obj.dc.content.date_list)
        # object creation date no longer needed in dc:date for searching
        self.assert_(self.obj.created.strftime('%Y-%m-%d') not in self.obj.dc.content.date_list,
                 'object creation date for ingested object should no longer be included in dc:date')
        self.assert_(general_note in self.obj.dc.content.description_list)
        # related files should no longer be in dc:description
        self.assert_(related_files not in self.obj.dc.content.description_list)
        # currently using rights access condition text (no code) in dc:rights
        # should only be one in dc:rights - mods access condition not included
        self.assertEqual(1, len(self.obj.dc.content.rights_list))
        access = self.obj.rights.content.access_status
        self.assert_(access.code not in self.obj.dc.content.rights)
        self.assertEqual(access.text, self.obj.dc.content.rights)

        # clear out data and confirm DC gets cleared out appropriately
        del(self.obj.mods.content.origin_info.created)
        del(self.obj.mods.content.origin_info.issued)
        del(self.obj.mods.content.general_note)
        del(self.obj.mods.content.names)  # FIXME: does this work?
        del(self.obj.sourcetech.content.related_files)
        del(self.obj.rights.content.access_status)
        self.obj._update_dc()
        self.assertEqual([], self.obj.dc.content.date_list,
            'there should be no dc:date when dateCreated or dateIssued are not set in MODS')
        self.assertEqual([], self.obj.dc.content.description_list,
            'there should be no dc:description when general note in MODS, digitization ' +
            'purpose in digital tech, and related files in source tech are not set')
        self.assertEqual([], self.obj.dc.content.rights_list,
            'there should be no dc:rights when no Rights access_status is set')
        self.assertEqual([], self.obj.dc.content.creator_list,
            'there should be no dc:creator when no creator names are set')
        self.assertEqual([], self.obj.dc.content.identifier_list,
             'there should be no dc:identifiers when no identifiers are set')

        # un-ingested object - should not error
        obj = self.repo.get_object(type=audiomodels.AudioObject)
        obj._update_dc()

    @patch('keep.audio.models.CollectionObject')
    def test_index_data(self, mockcollobj):
        # test custom data used for indexing objects in solr

        mockmss = Mock(CollectionObject)
        mockmss.label = 'mss collection'
        mockmss.collection_id = 'archive:pid'
        mockarchive = Mock(CollectionObject)
        mockarchive.label = 'MARBL'

        colls = [mockmss, mockarchive]

        def get_coll(*args, **kwargs):
            return colls.pop(0)
        # collection object will be initialized twice - once for
        # collection this item belongs to, once for repository the
        # collection belongs to.
        mockcollobj.side_effect = get_coll

        # create mock collection object with minimal data
        coll = Mock(CollectionObject)
        coll.pid = 'parent:1'
        coll.exists = True
        # should work with any id value including 0
        coll.mods.content.source_id = 0

        obj = self.repo.get_object(type=audiomodels.AudioObject)
        obj.pid = 'foo:1'
        obj.dc.content.title = 'audio item'

        # collection is an eulfedora.models.Relation, so patch on the AudioObject class
        with patch('keep.audio.models.AudioObject.collection', new=coll):
            desc_data = obj.index_data()

            self.assertEqual(obj.collection.pid, desc_data['collection_id'],
                             'parent collection object id should be set in index data')
            self.assertEqual(mockmss.label, desc_data['collection_label'],
                          'parent collection object label should be set in index data')
            # NB: as of 2011-08-23, eulindexer doesn't support automatic
            # reindexing of audio objects when their collection changes. as a
            # result, archive_id and archive_label may be stale. disable
            # indexing them until eulindexer supports those chained updates.
            # check CollectionObject use
            # get all args for collection object initializations
            args, kwargs = mockcollobj.call_args
            self.assert_(obj.collection.uri in args,
                         'object.collection.uri %s should be used to initialize a CollectionObject for collection info' \
                         % obj.collection.uri)
            self.assertEquals(obj.collection.mods.content.source_id, desc_data['collection_source_id'],
                              'collection_source_id should be %s but is is %s' %
                              (obj.collection.mods.content.source_id, desc_data['collection_source_id']))

        self.assertEqual(obj.dc.content.title, desc_data['title'][0],
                         'default index data fields should be present in data (title)')
        self.assertEqual(obj.pid, desc_data['pid'],
                         'default index data fields should be present in data (pid)')
        self.assert_('dm1_id' not in desc_data,
                     'dm1_id should not be included in index data when list is empty')
        self.assert_('digitization_purpose' not in desc_data,
                     'digitization_purpose should not be included in index data when it is empty')
        self.assert_('part' not in desc_data,
                     'part should not be included in index data when it is empty')
        self.assertEqual(False, desc_data['researcher_access'],
                     'researcher_access should be false when it access is not set in rights md')
        self.assertEqual(False, desc_data['has_original'],
                     'has_original should be false when object has no ingested original datastream')
        self.assertEqual(False, desc_data['has_access_copy'],
                     'has_access_copy should be false when object has no ingested access datastream')
        self.assert_('access_copy_size' not in desc_data,
                     'access_copy_size should not be included in index data when access ds does not exist')
        self.assert_('access_copy_mimetype' not in desc_data,
                     'access_copy_mimetype should not be included in index data when access ds does not exist')
        self.assert_('duration' not in desc_data,
                     'duration should not be included in index data unless set in digitaltech')
        self.assert_('date_issued' not in desc_data,
                     'date_issued should not be included in index data when it is not set')
        self.assert_('related_files' not in desc_data,
                         'related_files should not be set when not present in sourcetech')
        self.assert_('sublocation' not in desc_data,
                         'sublocation should not be set when not present in sourcetech')
        self.assert_('ip_note' not in desc_data,
                         'ip_note should not be set when not present in rights metadata')
        self.assert_('copyright_date' not in desc_data,
                         'copyright_date should not be set when not present in rights metadata')

        # additional fields that could be present
        obj.mods.content.dm1_id = '0103'
        obj.mods.content.dm1_other_id = '000004993'
        obj.digitaltech.content.digitization_purpose_list.append('patron request')
        obj.mods.content.create_part_note()
        obj.mods.content.part_note.text = 'Side 1'
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.issued.append(mods.DateIssued(date='1978-12-25'))
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = '8'
        obj.rights.content.block_external_access = False
        obj.rights.content.copyright_date = '2001-05'
        obj.rights.content.ip_note = 'donor agreement caveat'
        obj.compressed_audio.info.size = 13546
        obj.compressed_audio.mimetype = 'application/mpeg'
        obj.digitaltech.content.duration = 36
        obj.sourcetech.content.related_files = '1000, 2011'
        obj.sourcetech.content.sublocation = 'Box 3'

        # reset mock collection objects to be returned
        colls = [mockmss, mockarchive]

        desc_data = obj.index_data()
        self.assert_(obj.mods.content.dm1_id in desc_data['dm1_id'],
                         'dm1 id should be included in index data when set')
        self.assert_(obj.mods.content.dm1_other_id in desc_data['dm1_id'],
                         'dm1 id should be included in index data when set')
        self.assert_(obj.digitaltech.content.digitization_purpose_list[0] in desc_data['digitization_purpose'],
                         'digitization purpose should be included in index data when set')
        self.assertEqual(obj.mods.content.part_note.text, desc_data['part'],
                         'part note should be included in index data when set')
        self.assertEqual(obj.rights.content.access_status.code, desc_data['access_code'],
                         'access code should be included in index data when set')
        self.assertEqual(obj.researcher_access, desc_data['researcher_access'],
                         'researcher_access should be set based on access code & override')
        self.assertEqual(obj.rights.content.copyright_date, desc_data['copyright_date'],
                         'copyright date should be included in index data when set')
        self.assertEqual(obj.rights.content.ip_note, desc_data['ip_note'],
                         'ip_note should be included in index data when set')
        self.assertEqual(obj.sourcetech.content.related_files, desc_data['related_files'][0],
                         'related_files should be set when present in sourcetech')
        self.assertEqual(obj.sourcetech.content.sublocation, desc_data['sublocation'],
                         'sublocation should be set when present in sourcetech')

        # error if data is not serializable as json
        self.assert_(json.dumps(desc_data))

        colls = [mockmss, mockarchive]
        # pretend access copy exists in fedora
        with patch.object(obj.compressed_audio, 'exists', new=True):
            desc_data = obj.index_data()
            self.assertEqual(True, desc_data['has_access_copy'],
                         'has_access_copy should be true when object has an access datastream')
            self.assertEqual(obj.compressed_audio.info.size, desc_data['access_copy_size'],
                         'access_copy_size should match compressed audio datastream size')
            self.assertEqual(obj.compressed_audio.mimetype, desc_data['access_copy_mimetype'],
                         'access_copy_mimetype should match compressed audio datastream mimetype')
            self.assertEqual(obj.digitaltech.content.duration, desc_data['duration'],
                         'duration should match digitaltech duration value')
            self.assert_(unicode(obj.mods.content.origin_info.issued[0]) in desc_data['date_issued'],
                         'date_issued should not be set based on mods origin_info.issued')
            self.assert_(json.dumps(desc_data))

        colls = [mockmss, mockarchive]
        # pretend original exists in fedora
        with patch.object(obj, 'audio') as mockaudio:
            mockaudio.exists = True
            mockaudio.checksum = 'test audio MD5'
            desc_data = obj.index_data()
            self.assertEqual(True, desc_data['has_original'],
                             'has_original should be true when object has original audio datastream')
            self.assertEqual(mockaudio.checksum, desc_data['content_md5'])

    def test_file_checksum(self):
        #This is just a sanity check that eulfedora is working as expected with checksums.
        filename = 'example.wav'
        label = 'this is a test WAV file'
        #specify an incorrect checksum
        bad_md5 = 'aaa'
        obj = audiomodels.AudioObject.init_from_file(wav_filename, label, checksum=bad_md5)
        expected_error = None
        try:
            obj.save()
            #Purge if it somehow did not error on the save.
            self.repo.purge_object(obj.pid, "removing unit test fixture")
        except RequestFailed as e:
            expected_error = e

        self.assert_(isinstance(expected_error, ChecksumMismatch),
            'attempting to save with invalid checksum should raise a ChecksumMismatch exception')

        # specify a correct checksum
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
        rqst.user = get_user_model().objects.get(username=user)
        # use custom login so user credentials will be stored properly
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        rqst.session = self.client.session
        new_obj = audiomodels.AudioObject.init_from_file(wav_filename, request=rqst)
        # NOTE: when eulfedora switches to requests-backed API, this will need to change:
        #  self.assertEqual(new_obj.api.username, user,
        self.assertEqual(new_obj.api.username, user,
            'object initialized with request has user credentials configured for fedora access')

    def test_collection(self):
        FAKE_COLLECTION = 'info:fedora/test:FakeCollection'

        self.obj.collection = self.repo.get_object(FAKE_COLLECTION)
        self.obj.save()

        obj = self.repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertEqual(FAKE_COLLECTION, obj.collection.uri)

        self.obj.collection_uri = None
        self.assertEqual(None, self.obj.collection_uri)

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

    def test_access_file_extension(self):
        # object created in fixture has no access copy
        self.assertEqual(None, self.obj.access_file_extension())
        self.obj.compressed_audio.mimetype = 'audio/mpeg'
        self.obj.compressed_audio.exists = True		# not really (cheat)
        self.assertEqual('mp3', self.obj.access_file_extension())
        self.obj.compressed_audio.mimetype = 'audio/mp4'
        self.assertEqual('m4a', self.obj.access_file_extension())


# check if mediainfo is installed on this system
mediainfo_unavailable = (call(['which', 'mediainfo']) != 0)


class TestWavDuration(KeepTestCase):

    def test_success(self):
        duration = audiomodels.wav_duration(wav_filename)
        # ffmpeg reports the duration of fixture WAV file as 00:00:03.30
        self.assertAlmostEqual(3.3, duration, 3)

    def test_non_wav(self):
        self.assertRaises(StandardError, audiomodels.wav_duration, mp3_filename)

    def test_nonexistent(self):
        self.assertRaises(IOError, audiomodels.wav_duration, 'i-am-not-a-real-file.wav')

    @skipIf(mediainfo_unavailable, 'mediainfo is not installed')
    def test_mediainfo(self):
        # mock wav error to test mediainfo logic
        with patch('keep.audio.models.wave.open') as mockwaveopen:
            mockwaveopen.side_effect = wave.Error
            duration = audiomodels.wav_duration(wav_filename)
            # duration reported by MediaInfo is more exact than the one calculated
            # from the wav framerate, so we can compare directly
            self.assertAlmostEqual(3.299, duration)


# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
# @patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())

@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class TestWavMP3DurationCheck(KeepTestCase):

    def setUp(self):
        super(TestWavMP3DurationCheck, self).setUp()

        # somehow setup seems to not be covered by class-level patch (?)
        with patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes()):
            # create an audio object to test conversion with
            self.obj = audiomodels.AudioObject.init_from_file(wav_filename,
                                         'test wav/mp3 duration checks',  checksum=wav_md5)
            self.obj.save()
            self.pids = [self.obj.pid]

    def tearDown(self):
        super(TestWavMP3DurationCheck, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            self.repo.purge_object(pid)

    def test_compare_local_files(self):
        # compare wav with equivalent mp3
        self.assertTrue(audiomodels.check_wav_mp3_duration(wav_file_path=wav_filename,
                                                           mp3_file_path=mp3_filename),
                        'matching wav and mp3 should pass duration check')
        # compare alternate wav with original mp3
        self.assertFalse(audiomodels.check_wav_mp3_duration(wav_file_path=alternate_wav_filename,
                                                           mp3_file_path=mp3_filename),
                        'non-matching wav and mp3 should not pass duration check')

        # pass non-mp3 file as mp3
        self.assertRaises(Exception, audiomodels.check_wav_mp3_duration, None, wav_filename,
                                                           alternate_wav_filename)
        # pass non-existent file
        self.assertRaises(Exception, audiomodels.check_wav_mp3_duration, None,
                          '/tmp/my/very/bogus/file.wav', '/tmp/my/very/bogus/file.mp3')

    def test_compare_object_datastreams(self):
        # initially has no mp3
        self.assertFalse(audiomodels.check_wav_mp3_duration(self.obj.pid),
            'wav/mp3 duration check should fail when object has no access datastream and filename is not specified')

        # compare with local mp3
        self.assertTrue(audiomodels.check_wav_mp3_duration(self.obj.pid, mp3_file_path=mp3_filename),
            'wav/mp3 duration check pass for object and matching local mp3')

        # add mp3 to object
        with open(mp3_filename) as mp3_file:
            self.obj.compressed_audio.content = mp3_file
            self.obj.compressed_audio.checksum = mp3_md5
            self.obj.save('adding compressed audio to test audio duration check')

            self.assertTrue(audiomodels.check_wav_mp3_duration(self.obj.pid),
                'wav/mp3 duration check should pass for matching wav/mp3 datastreams on object')

            # compare mp3 on object to local wav files
            self.assertTrue(audiomodels.check_wav_mp3_duration(self.obj.pid, wav_file_path=wav_filename),
                'duration should match for mp3 datastream on object and matching local wav file')

            self.assertFalse(audiomodels.check_wav_mp3_duration(self.obj.pid,
                                                                wav_file_path=alternate_wav_filename),
                'duration should not match for mp3 datastream on object and non-matching local wav file')


#def check_wav_mp3_duration(obj_pid=None,wav_file_path=None,mp3_file_path=None):


class TestModsEditForm(KeepTestCase):
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


# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class SourceAudioConversions(KeepTestCase):
    def setUp(self):
        super(SourceAudioConversions, self).setUp()

        # somehow setup seems to not be covered by class-level patch (?)
        with patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes()):
            # create an audio object to test conversion with
            self.obj = audiomodels.AudioObject.init_from_file(wav_filename,
               'test only',  checksum=wav_md5)
            self.obj.save()
            self.pids = [self.obj.pid]

    def tearDown(self):
        super(SourceAudioConversions, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            try:
                self.repo.purge_object(pid)
            except RequestFailed:
                logger.warn('Failed to purge %s in tear down' % pid)

    def test_wav_to_mp3(self):
        result = convert_wav_to_mp3(self.obj.pid)
        self.assertEqual(result, "Successfully converted file")

        # inspect the object in fedora to confirm that the audio was added
        repo = Repository()
        obj = repo.get_object(self.obj.pid, type=audiomodels.AudioObject)
        self.assertTrue(obj.compressed_audio.exists,
           'compressed audio datastream should exist in Fedora after mp3 conversion')

        #Verify the wav and mp3 durations match.
        comparison_result = audiomodels.check_wav_mp3_duration(self.obj.pid)
        self.assertTrue(comparison_result,
            "duration for WAV and generated MP3 datastreams should match.")

        # any other settings/info on the mp3 datastream that should be checked?

    def test_wav_to_mp3_localfile(self):
        #test conversion when path to local wav file is specified.
        result = convert_wav_to_mp3(self.obj.pid, use_wav=wav_filename)
        self.assertEqual(result, "Successfully converted file")

        self.assertTrue(os.path.exists(wav_filename),
            'local wav file should not be removed if we did not request removal')

        #Verify the wav and mp3 durations match.
        comparison_result = audiomodels.check_wav_mp3_duration(self.obj.pid, wav_file_path=wav_filename)
        self.assertTrue(comparison_result,
             "duration for MP3 should match WAV file it was generated from.")

        # copy wav file so we can test removing it
        wav_copy = os.path.join(settings.INGEST_STAGING_TEMP_DIR, 'example-01.wav')
        copyfile(wav_filename, wav_copy)
        result = convert_wav_to_mp3(self.obj.pid, use_wav=wav_copy, remove_wav=True)
        self.assertFalse(os.path.exists(wav_copy),
            'local wav file should be removed when requested')

    def test_nonexistent(self):
        # test with invalid pid
        self.assertRaises(RequestFailed, convert_wav_to_mp3, 'bogus:DoesNotExist')

        # test with invalid file.
        self.assertRaises(IOError, convert_wav_to_mp3, self.obj.pid, "CompletelyBogusFile.wav")

    def test_non_matching_checksum(self):
        #Use the alternate wav file to kick off an incorrect checksum match.
        self.assertRaises(Exception, convert_wav_to_mp3, self.obj.pid, alternate_wav_filename)

    def test_changing_wav_file(self):
        with open(alternate_wav_filename) as alt_audio:
            self.obj.audio.content = alt_audio
            self.obj.audio.checksum = alternate_wav_md5
            self.obj.save()

            result = convert_wav_to_mp3(self.obj.pid)
            self.assertEqual(result, "Successfully converted file")

            #Verify it no longer matches the original wav file.
            comparison_result = audiomodels.check_wav_mp3_duration(self.obj.pid,
                wav_file_path=wav_filename)
            self.assertFalse(comparison_result,
                "MP3 generated from alternate WAV should not match duration of original WAV")

            #Verify the new wav and mp3 durations match.
            comparison_result = audiomodels.check_wav_mp3_duration(self.obj.pid,
                wav_file_path=alternate_wav_filename)
            self.assertTrue(comparison_result,
                 "MP3 should match duration of the WAV file it was generated from.")


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


class IngestCleanupTest(KeepTestCase):
    def setUp(self):
        super(IngestCleanupTest, self).setUp()
        self.command = TestIngestCleanupCommand()
        self._real_temp_dir = settings.INGEST_STAGING_TEMP_DIR
        self._real_keep_age = settings.INGEST_STAGING_KEEP_AGE
        self.tmpdir = tempfile.mkdtemp(prefix='digmast-ingest-cleanup-test')
        settings.INGEST_STAGING_TEMP_DIR = self.tmpdir

    def tearDown(self):
        super(IngestCleanupTest, self).tearDown()
        # remove any files created in temporary test staging dir
        for file in os.listdir(self.tmpdir):
            os.unlink(os.path.join(self.tmpdir, file))

        #Possible timing conflict.... can still occur if an anti-virus is running or something else accesses the file: http://bugs.python.org/issue1425127
        sleep(1)
        #See: http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
        os.chmod(self.tmpdir, stat.S_IWUSR)
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


class TestAudioExtrasTemplateTags(TestCase):

    def test_seconds_duration(self):
        self.assertEqual('0:00:01',
                         audio_extras.seconds_duration(1))
        self.assertEqual('0:00:01',
                         audio_extras.seconds_duration('1'))
        self.assertEqual('0:01:05',
                         audio_extras.seconds_duration(65))
        self.assertEqual('3:22:17',
                         audio_extras.seconds_duration((3 * 60 * 60) + (22 * 60) + 17))
        self.assertEqual('16:21:13',
                         audio_extras.seconds_duration((16 * 60 * 60) + (21 * 60) + 13))
        self.assertEqual('',
                         audio_extras.seconds_duration(''))

    def test_natural_seconds(self):
        self.assertEqual('1 second',
                         audio_extras.natural_seconds(1))
        self.assertEqual('1 second',
                         audio_extras.natural_seconds('1'))
        self.assertEqual('1 minute, 5 seconds',
                         audio_extras.natural_seconds(65))
        self.assertEqual('1 minute',
                         audio_extras.natural_seconds(60))
        self.assertEqual('1 hour',
                         audio_extras.natural_seconds(60 * 60))
        self.assertEqual('1 hour, 7 seconds',
                         audio_extras.natural_seconds((60 * 60) + 7))
        self.assertEqual('3 hours, 22 minutes, 17 seconds',
                         audio_extras.natural_seconds((3 * 60 * 60) + (22 * 60) + 17))
        self.assertEqual('16 hours, 21 minutes, 13 seconds',
                         audio_extras.natural_seconds((16 * 60 * 60) + (21 * 60) + 13))
        self.assertEqual('',
                         audio_extras.natural_seconds(''))


