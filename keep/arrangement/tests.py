from rdflib import URIRef
import logging
import sys
from mock import Mock, MagicMock, patch
import os
from sunburnt import sunburnt

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from eulfedora.rdfns import relsext as relsextns, model as modelns
from eulcm.models import boda
from eulcm.xmlmap.boda import FileMasterTech_Base
from eulxml.xmlmap import cerp

from keep import __version__
from keep.arrangement.management.commands.migrate_rushdie import CONTENT_MODELS
from keep.arrangement.management.commands import migrate_rushdie
from keep.arrangement.models import ArrangementObject, RushdieArrangementFile, \
     ACCESS_ALLOWED_CMODEL, ACCESS_RESTRICTED_CMODEL, EmailMessage, Mailbox
from keep.collection.models import SimpleCollection, CollectionObject
from keep.collection.fixtures import FedoraFixtures
from keep.common.fedora import Repository
from keep.arrangement import forms as arrangementforms
from keep.testutil import KeepTestCase, mocksolr_nodupes



logger = logging.getLogger(__name__)

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

pdf_filename = os.path.join(settings.BASE_DIR, 'arrangement', 'fixtures', 'test.pdf')

class PermissionsCheckTest(TestCase):
    # FIXME: this test probably doesn't need to exist (testing built-in django functionality?)

    fixtures =  ['users']

    def test_permission_exists(self):
        marbl_perm = Permission.objects.get(codename='marbl_allowed')
        arrangement_perm = Permission.objects.get(codename='arrangement_allowed')

        #Test for permission on a sample fixture user
        marbl_user = get_user_model().objects.get(username__exact='marbl')
        marbl_user.user_permissions.clear()
        marbl_user.save()
        marbl_user.user_permissions.add(marbl_perm)
        marbl_user.user_permissions.add(arrangement_perm)
        marbl_user.save()
        self.assertTrue(marbl_user.has_perm('common.marbl_allowed'))
        self.assertTrue(marbl_user.has_perm('common.arrangement_allowed'))


# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class TestMigrateRushdie(TestCase):
    MM_FIXTURE ='''<macfs:document xmlns:macfs="info:fedora/emory-control:Rushdie-MacFsData-1.0">
  <macfs:md5>ffcf48e5df673fc7de985e1b859eeeec</macfs:md5>
  <macfs:file>
    <macfs:computer>Performa 5400</macfs:computer>
    <macfs:path>/Hard Disk/MIDNIGHT&apos;S CHILDREN/MISC. MATERIAL/x - the roles</macfs:path>
    <macfs:rawpath>L0hhcmQgRGlzay9NSUROSUdIVCdTIENISUxEUkVOL01JU0MuIE1BVEVSSUFML3ggLSB0aGUgcm9sZXM=</macfs:rawpath>
    <macfs:attributes>avbstclInmedz</macfs:attributes>
    <macfs:created>1997-01-19T19:29:32</macfs:created>
    <macfs:modified>1997-01-19T19:29:32</macfs:modified>
    <macfs:type>TEXT</macfs:type>
    <macfs:creator>ttxt</macfs:creator>
  </macfs:file>
</macfs:document>'''

    MA_FIXTURE ='''<marbl:analysis xmlns:marbl="info:fedora/emory-control:Rushdie-MarblAnalysis-1.0">
  <marbl:series>Writings by Rushdie</marbl:series>
  <marbl:subseries>Fiction</marbl:subseries>
  <marbl:verdict>As is</marbl:verdict>
</marbl:analysis>'''

    SERIES_FIXTURE = {'Writings by Rushdie':
              { 'series_info':
                   {'base_ark': 'http://testpid.library.emory.edu/ark:/25593/80mvk',
                        'id': 'rushdie1000_series2',
                        'short_id': 'series2',
                        'uri': 'https://findingaids.library.emory.edu/documents/rushdie1000/series2'},
              'subseries_info': {   'Fiction': {   'base_ark': 'http://testpid.library.emory.edu/ark:/25593/80mvk',
                                            'id': 'rushdie1000_subseries2.1',
                                            'short_id': 'subseries2.1',
                                            'uri': 'https://findingaids.library.emory.edu/documents/rushdie1000/series2/subseries2.1'}}}}

    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #Create a simple Collection
        self.sc = self.repo.get_object(type=SimpleCollection)
        self.sc.label = "SimpleCollection For Test"
        self.sc.save()
        self.pids.append(self.sc.pid)

        #Create a Master Collection
        self.mc = self.repo.get_object(type=CollectionObject)
        self.mc.label = "MasterCollection For Test"
        self.mc.save()
        self.pids.append(self.mc.pid)

        #Create a a DigitalObject
        self.digObj = self.repo.get_object(type=RushdieArrangementFile)
        self.digObj.label = "Object For Test"
        self.digObj.save()
        self.pids.append(self.digObj.pid)
        self.digObj.api.addDatastream(self.digObj.pid, "MARBL-MACTECH",
                                           "MARBL-MACTECH",  mimeType="application/xml", content= self.MM_FIXTURE)
        self.digObj.api.addDatastream(self.digObj.pid, "MARBL-ANALYSIS",
                                           "MARBL-ANALYSIS",  mimeType="application/xml", content= self.MA_FIXTURE)
        #Remove Arrangement model so it can be added later
        relation = (self.digObj.uriref, modelns.hasModel, "info:fedora/emory-control:Arrangement-1.0")
        self.digObj.rels_ext.content.remove(relation)
        self.digObj.save()


        #Setup Command
        self.cmd = migrate_rushdie.Command()
        self.cmd.verbosity = 1
        self.cmd.v_normal = 1
        self.cmd.v_none = 0
        self.cmd.simple_collection = self.sc
        self.cmd.stdout = sys.stdout
        self.cmd.CONTENT_MODELS = CONTENT_MODELS
        self.cmd.repo = self.repo

    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)


    def test__add_to_simple_collection(self):
        self.cmd._add_to_simple_collection(self.digObj)
        self.assertTrue((self.sc.uriref, relsextns.hasMember,
                     self.digObj.uriref) in self.sc.rels_ext.content, "%s shold be a member of the Simplecollection" % self.digObj.pid )


    def test__get_unique_objects(self):
        #duplicate pids are processed only once
        objs = self.cmd._get_unique_objects([self.digObj.pid, self.digObj.pid])
        self.assertEqual(len(objs), 1, "No dup pids should be processed")

    def test__convert_ds(self):
        obj = self.cmd._convert_ds(self.digObj, self.mc, self.SERIES_FIXTURE, False)
        #Check all fields are moved over correctly

        #filetech
        self.assertEqual(obj.filetech.content.file[0].md5, "ffcf48e5df673fc7de985e1b859eeeec")
        self.assertEqual(obj.filetech.content.file[0].computer, "Performa 5400")
        self.assertEqual(obj.filetech.content.file[0].path, "/Hard Disk/MIDNIGHT'S CHILDREN/MISC. MATERIAL/x - the roles")
        self.assertEqual(obj.filetech.content.file[0].rawpath, "L0hhcmQgRGlzay9NSUROSUdIVCdTIENISUxEUkVOL01JU0MuIE1BVEVSSUFML3ggLSB0aGUgcm9sZXM=")
        self.assertEqual(obj.filetech.content.file[0].attributes, "avbstclInmedz")
        self.assertEqual(obj.filetech.content.file[0].created, "1997-01-19T19:29:32")
        self.assertEqual(obj.filetech.content.file[0].modified, "1997-01-19T19:29:32")
        self.assertEqual(obj.filetech.content.file[0].type, "TEXT")
        self.assertEqual(obj.filetech.content.file[0].creator, "ttxt")
        #MODS
        self.assertEqual(obj.mods.content.series.title, "Fiction")
        self.assertEqual(obj.mods.content.series.uri, self.SERIES_FIXTURE["Writings by Rushdie"]["subseries_info"]["Fiction"]["uri"])
        self.assertEqual(obj.mods.content.series.base_ark, self.SERIES_FIXTURE["Writings by Rushdie"]["subseries_info"]["Fiction"]["base_ark"])
        self.assertEqual(obj.mods.content.series.full_id, self.SERIES_FIXTURE["Writings by Rushdie"]["subseries_info"]["Fiction"]["id"])
        self.assertEqual(obj.mods.content.series.short_id, self.SERIES_FIXTURE["Writings by Rushdie"]["subseries_info"]["Fiction"]["short_id"])
        self.assertEqual(obj.mods.content.series.series.title, "Writings by Rushdie")
        self.assertEqual(obj.mods.content.series.series.uri, self.SERIES_FIXTURE["Writings by Rushdie"]["series_info"]["uri"])
        self.assertEqual(obj.mods.content.series.series.base_ark, self.SERIES_FIXTURE["Writings by Rushdie"]["series_info"]["base_ark"])
        self.assertEqual(obj.mods.content.series.series.full_id, self.SERIES_FIXTURE["Writings by Rushdie"]["series_info"]["id"])
        self.assertEqual(obj.mods.content.series.series.short_id, self.SERIES_FIXTURE["Writings by Rushdie"]["series_info"]["short_id"])
        #Rights
        self.assertEqual(obj.rights.content.access_status.code, "2")
        #RELS-EXT
        self.assertTrue((obj.uriref, relsextns.isMemberOf, self.mc.uriref) in obj.rels_ext.content, "Object should have isMember relation to master collection")
        self.assertTrue((obj.uriref, modelns.hasModel, URIRef("info:fedora/emory-control:ArrangementAccessAllowed-1.0")) in obj.rels_ext.content, "Object should have Allowed Content Model")
        #Label and DS
        self.assertEqual(obj.label, "x - the roles", "Label should be set to last part of path")
        self.assertEqual(obj.owner, "thekeep-project", "owner should be set to 'thekeep-project'")
        self.assertEqual(obj.dc.content.title, "x - the roles", "DC title should be set to last part of path")
        #DataStreams
        #have to reload obj from repository to get DS update
        obj = self.repo.get_object(pid=obj.pid, type=ArrangementObject)
        self.assertFalse("MARBL-MACTECH" in obj.ds_list, "MARBL-MACTECH should have been removed")
        self.assertFalse("MARBL-ANALYSIS" in obj.ds_list, "MARBL-ANALYSIS should have been removed")

    def test_missing_series_info(self):
        #Remove subseries info from lookup
        series = self.SERIES_FIXTURE.copy()
        del series["Writings by Rushdie"]["subseries_info"]
        obj = self.cmd._convert_ds(self.digObj, self.mc, self.SERIES_FIXTURE, False)

        self.assertEqual(obj.mods.content.series.title, "Fiction")
        self.assertEqual(obj.mods.content.series.series.title, "Writings by Rushdie")


# mock solr used to avoid ingest failure to do pre-ingest duplicate checking
@patch('keep.common.fedora.solr_interface', new=mocksolr_nodupes())
class ArrangementViewsTest(KeepTestCase):
    fixtures =  ['users']

    client = Client()

    def setUp(self):
        super(ArrangementViewsTest, self).setUp()
        self.pids = []
        # collection fixtures are not modified, but there is no clean way
        # to only load & purge once
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.esterbrook = FedoraFixtures.esterbrook_collection()
        self.esterbrook.save()
        self.englishdocs = FedoraFixtures.englishdocs_collection()
        self.englishdocs.save()

        self.rushdie_obj = self.repo.get_object(type=RushdieArrangementFile)

        #Add Link pointing to the top level rushdie collection
        #relation = (self.rushdie_obj.uriref, model.isMemberOfCollection, "info:fedora/keep-athom09:349")
        #self.rushdie_obj.rels_ext.content.add(relation)

        self.rushdie_obj.label = "Test Rushdie Object"


        #Create some test filetech content
        filetech_1 = FileMasterTech_Base()
        filetech_1.md5 = 'bogus_md5_sum'
        filetech_1.local_id = '1'
        filetech_1.computer = 'Performa 5400'
        filetech_1.path = '/bogus/path/doesnotexist'
        filetech_1.rawpath = 'XYZ'
        filetech_1.attributes = 'abc'
        filetech_1.created = ''
        filetech_1.modified = ''
        filetech_1.type = 'TEXT'
        filetech_1.creator = 'ttxt'

        filetech_2 = FileMasterTech_Base()
        filetech_2.md5 = 'second_bogus_md5_sum'
        filetech_2.local_id = '2'
        filetech_2.computer = 'Performa 5300c'
        filetech_2.path = '/bogus/path/doesnotexist'
        filetech_2.rawpath = 'UVW'
        filetech_2.attributes = 'def'
        filetech_2.created = ''
        filetech_2.modified = ''
        filetech_2.type = 'PDF'
        filetech_2.creator = 'pdf'
        # FIXME: is filetech used in these tests at all?

        self.rushdie_obj.filetech.content.file.append(filetech_1)
        self.rushdie_obj.filetech.content.file.append(filetech_2)

        #Add a series objects
        self.rushdie_obj.mods.content.create_series()
        self.rushdie_obj.mods.content.series.title = 'subseries_title_value'

        self.rushdie_obj.mods.content.series.create_series()
        self.rushdie_obj.mods.content.series.series.title = 'series_title_vale'

        self.rushdie_obj.save()
        self.pids.append(self.rushdie_obj.pid)

        #create a mailbox
        self.mailbox = self.repo.get_object(type=Mailbox)
        self.mailbox.pid = 'mailbox:pid'
        self.mailbox.label = 'TestMailBox'

        # create email for test DO NOT INGEST this is used with mock for get_object return value
        self.email = self.repo.get_object(type=EmailMessage)
        self.email.pid = 'email:pid'
        self.email.cerp.content.from_list = ['sender@sendmail.com']
        self.email.cerp.content.to_list = ['guy1@friend.com', 'guy2@friend.com']
        self.email.cerp.content.subject_list = ['Interesting Subject']
        self.email.mailbox = self.mailbox
        h1 = cerp.Header()
        h1.name='Date'
        h1.value = 'Fri May 11 2012'
        self.email.cerp.content.headers.append(h1)


    def tearDown(self):
        super(ArrangementViewsTest, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            self.repo.purge_object(pid)

        self.repo.purge_object(self.rushdie.pid)
        self.repo.purge_object(self.esterbrook.pid)
        self.repo.purge_object(self.englishdocs.pid)

    @patch('keep.arrangement.views.TypeInferringRepository.get_object')
    def test_edit_form(self, mock_getobj):

        mock_getobj.return_value = self.rushdie_obj

        arrangement_data =  {
            u'fs-file-MAX_NUM_FORMS': [u''],
            u'fs-file-TOTAL_FORMS': [u'2'],
            u'fs-file-INITIAL_FORMS': [u'1'],

            u'mods-series-base_ark': [u'http://testpid.library.emory.edu/ark:/25593/80mvk'],
            u'mods-series-series-title': [u''],
            u'fs-file-0-attributes': [u'avbstclInmedz'],
            u'mods-series-series-short_id': [u''],
            u'rights-copyright_date_day': [u'DD'],
            u'fs-file-0-rawpath': [u'L01hY2ludG9zaCBIRC9MRVRURVJTL1RST01TTw=='],
            u'fs-file-0-md5': [u'796f7d0a4e8ac74632930f7b9b5c5e88'],
            u'fs-file-0-type': [u''],
            u'fs-file-0-computer': [u'PowerBook 5300c'],
            u'mods-series-uri': [u'https://findingaids.library.emory.edu/documents/rushdie1000/series4'],
            u'csrfmiddlewaretoken': [u'e04a7d70fa4d0c4e19906a3769f01ad9'],
            u'fs-file-0-modified': [u'3/4/1993 16:11'],
            u'rights-access_restriction_expiration_day': [u'DD'],
            u'fs-file-0-creator': [u'MWPR'],
            u'mods-series-short_id': [u'series4'],
            u'series_title_field': [u''],
            u'mods-series-series-uri': [u''],
            u'mods-series-series-full_id': [u''],
            u'_save_continue': [u'Save and continue editing'],
            u'fs-file-0-created': [u'3/4/1993 16:00'],
            u'fs-file-0-local_id': [u'242'],
            u'rights-copyright_date_year': [u'YYYY'],
            u'rights-access_restriction_expiration_year': [u'YYYY'],
            u'mods-series-full_id': [u'rushdie1000_series4'],
            u'mods-series-title': [u'Correspondence'],
            u'rights-access_restriction_expiration_month': [u'MM'],
            u'comment': [u''],
            u'rights-copyright_date_month': [u'MM'],
            u'mods-series-series-base_ark': [u''],
            u'rights-ip_note': [u''],
            u'fs-file-0-path': [u'/Macintosh HD/LETTERS/TROMSO'],
            u'rights-access': [u'10']
        }

        # test edit form
        edit_url = reverse('arrangement:edit', args=[self.rushdie_obj.pid])

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # on GET, should display the form
        response = self.client.get(edit_url, {'rights-access': '2'})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assertNotEqual(None, response.context['form'])
        self.assert_(isinstance(response.context['form'], arrangementforms.ArrangementObjectEditForm))

        # Check for filetech fields
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].md5)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].local_id)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].computer)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].path)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].rawpath)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].attributes)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].type)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[0].creator)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].md5)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].local_id)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].computer)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].path)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].rawpath)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].attributes)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].type)
        self.assertContains(response, self.rushdie_obj.filetech.content.file[1].creator)

        # Check for series fields
        self.assertContains(response, self.rushdie_obj.mods.content.series.title)
        self.assertContains(response, self.rushdie_obj.mods.content.series.series.title)

        # should display pdf file input for file object
        self.assertContains(response, '<input id="id_pdf" type="file" name="pdf" />',
            msg_prefix='edit form should display PDF file input for file object',
            html=True)
        # should display info about current pdf
        self.assertContains(response, '(no PDF)',
            msg_prefix='edit form should indicate object does not currently have a PDF')

        #TODO additional tests should be added

        response = self.client.post(edit_url, arrangement_data)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        obj = self.repo.get_object(type=ArrangementObject, pid=self.rushdie_obj.pid)

        # check audit trail (default message)
        self.assertEqual('update metadata', obj.audit_trail.records[-1].message)

        # test optional comment input
        data = arrangement_data.copy()
        data['comment'] = 'This is a comment'
        data['rights-access'] = 1 # need to change something to trigger a save
        response = self.client.post(edit_url, data)

        obj = self.repo.get_object(type=ArrangementObject, pid=self.rushdie_obj.pid)
        # check audit trail message
        self.assertEqual(data['comment'], obj.audit_trail.records[-1].message)

        # test uploading a PDF file
        with open(pdf_filename) as pdf:
            data = arrangement_data.copy()
            data['pdf'] = pdf
            response = self.client.post(edit_url, data)

        # check that PDF was saved to fedora (more tests on form update_instance method)
        with open(pdf_filename) as pdf:
            pdf_content = pdf.read()

        obj = self.repo.get_object(type=RushdieArrangementFile, pid=self.rushdie_obj.pid)
        self.assertEqual(pdf_content, obj.pdf.content.read())
        self.assertEqual('test.pdf', obj.pdf.label)

        # form display for item with a pdf should display pdf details
        response = self.client.get(edit_url)
        self.assertContains(response, 'test.pdf',
            msg_prefix='pdf filename should be displayed when object has a pdf')
        self.assertContains(response, reverse('arrangement:raw-ds', args=[self.rushdie_obj.pid, 'PDF']),
            msg_prefix='edit form should link to PDF view when object has a pdf')


    @patch('keep.arrangement.views.TypeInferringRepository')
    def test_view(self, mockrepo):
        # test generic view functionality (perms)
        mockrepo.return_value.get_object.return_value = self.email

        # non-authenticated user
        view_url = reverse('arrangement:view', kwargs={'pid': 'test:pid'})

        response = self.client.get(view_url)
        self.assertEqual(302, response.status_code,
            'non-authenticated user should not have acccess to view arrangement items')

        # authenticated user (WITH arrangement perms)
        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(view_url)
        self.assertEqual(200, response.status_code,
            'authenticated admin user can view arrangement item')

        # unsupported object type should 404
        fileobj = boda.RushdieFile(Mock())  # using mock for api
        mockrepo.return_value.get_object.return_value = fileobj
        response = self.client.get(view_url)
        self.assertEqual(404, response.status_code,
            'unsupported object types should 404')


    @patch('keep.arrangement.views.TypeInferringRepository.get_object')
    def test_view_email(self, mockget_obj):
        # test email message view specifics
        mockget_obj.return_value = self.email

        email_view_url = reverse('arrangement:view', kwargs={'pid': 'test:pid'})

        # authenticated user
        self.client.login(**ADMIN_CREDENTIALS)

        response = self.client.get(email_view_url)
        template_names = [t.name for t in response.templates]
        self.assert_('arrangement/email_view.html' in template_names,
            'email_view.html template should be used to render email message objects')

        # check for email content values
        self.assertContains(response, 'Interesting Subject',
            msg_prefix='email view should include message subject')
        self.assertContains(response, 'sender@sendmail.com',
            msg_prefix='email view should include message email address')
        self.assertContains(response, 'guy1@friend.com; guy2@friend.com',
            msg_prefix='email view should include message recipients')
        self.assertContains(response, 'Fri May 11 2012',
            msg_prefix='email view should include message date')

        self.assertContains(response, reverse('arrangement:edit', kwargs={'pid': 'email:pid'}),
            msg_prefix='email detail page should link to arrangement edit page')

    @patch('keep.arrangement.views.TypeInferringRepository.get_object')
    @patch('keep.arrangement.views.solr_interface')
    def test_view_mailbox(self, mocksolr, mockget_obj):
        mbox = boda.Mailbox(Mock())  # using mock for api
        mbox.pid = 'mailbox:pid'
        mbox.label = 'Email folder "In"'
        mockget_obj.return_value = mbox
        view_mailbox_url = reverse('arrangement:view', kwargs={'pid': 'mailbox:pid'})

        # authenticated user
        self.client.login(**ADMIN_CREDENTIALS)

        response = self.client.get(view_mailbox_url)
        template_names = [t.name for t in response.templates]
        self.assert_('arrangement/mailbox_view.html' in template_names,
            'mailbox_view.html template should be used to render email mailbox object')

        mocksolr.return_value.query.assert_called_with(isPartOf=mbox.uri)

        self.assertNotContains(response, reverse('arrangement:edit', kwargs={'pid': 'mailbox:pid'}),
            msg_prefix='mailbox detail page should NOT link to arrangement edit page')


class ArrangementObjectTest(KeepTestCase):

    def setUp(self):
        self.repo = Repository()
        self.pids = []

        # create test collection
        coll = self.repo.get_object(type=CollectionObject)
        coll.pid = '%s:parent-1' % settings.FEDORA_PIDSPACE
        coll.mods.content.source_id = '12345'
        coll.save()
        self.pids.append(coll.pid)

        #create test arrangement object
        self.arr = self.repo.get_object(type=ArrangementObject)
        self.arr.pid = 'foo:1'
        self.arr.collection = coll

    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)

    @patch('keep.arrangement.models.solr_interface', spec=sunburnt.SolrInterface)
    def test_by_arrangement_id(self, mocksolr):
        # no match
        self.assertRaises(ObjectDoesNotExist, ArrangementObject.by_arrangement_id,
                          42)
        solr = mocksolr.return_value
        solr.query.assert_called_with(arrangement_id=42,
                                      content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
        solr.query.return_value.field_limit.assert_called_with('pid')

        # too many matches
        solr.query.return_value.field_limit.return_value = [{'pid': 'pid:1'},
                                                            {'pid': 'pid:2'}]
        self.assertRaises(MultipleObjectsReturned, ArrangementObject.by_arrangement_id,
                          42)

        # one match
        solr.query.return_value.field_limit.return_value = [{'pid': 'pid:1'}]
        ao = ArrangementObject.by_arrangement_id(42)
        self.assert_(isinstance(ao, ArrangementObject))

        # custom repo object
        mockrepo = Mock()
        ao = ArrangementObject.by_arrangement_id(42, mockrepo)
        mockrepo.get_object.assert_called_with('pid:1', type=ArrangementObject)

    def test_arrangement_status(self):
        obj = ArrangementObject(Mock())
        obj.arrangement_status = 'processed'
        self.assertEqual('A', obj.state)
        self.assertEqual('processed', obj.arrangement_status)

        obj.arrangement_status = 'accessioned'
        self.assertEqual('I', obj.state)
        self.assertEqual('accessioned', obj.arrangement_status)

        value_error = None
        try:
            obj.arrangement_status = 'bogus'
        except ValueError:
            value_error = True

        self.assertTrue(value_error,
                        'attempting to assign an unknown status should raise a ValueError')

    def test_update_access_cmodel(self):
        obj = ArrangementObject(Mock())
        # no status set - should be set to restricted
        obj._update_access_cmodel()

        self.assert_((obj.uriref, modelns.hasModel, URIRef(ACCESS_RESTRICTED_CMODEL))
                     in obj.rels_ext.content)
        self.assert_((obj.uriref, modelns.hasModel, URIRef(ACCESS_ALLOWED_CMODEL))
                     not in obj.rels_ext.content)

        # set to status code 2 = access allowed
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = '2'

        obj._update_access_cmodel()

        self.assert_((obj.uriref, modelns.hasModel, URIRef(ACCESS_RESTRICTED_CMODEL))
                     not in obj.rels_ext.content)
        self.assert_((obj.uriref, modelns.hasModel, URIRef(ACCESS_ALLOWED_CMODEL))
                     in obj.rels_ext.content)

    def test_index_data(self):
        idx_data = self.arr.index_data()
        self.assertEqual('born-digital', idx_data['object_type'])
        self.assertEqual(self.arr.pid, idx_data['pid'])
        self.assertIn(self.arr.owner, idx_data['owner'])
        self.assertEquals(self.arr.collection.pid, idx_data['collection_id'])
        self.assertEquals(self.arr.collection.mods.content.source_id, idx_data['collection_source_id'])

    # Test the update_ark_label method in the keep.common.fedora
    # Note that this test is a simplified version of keep.common.fedora:ArkPidDigitalObject.test_update_ark_label
    # The udpate_ark_label here is an overriden method that is more specifc, and is used on Arrangement objects
    @patch('keep.arrangement.models.pidman')  # mock the pidman client (the API service)
    def test_update_ark_label(self, mockpidman):

        # Create a ArrangementObject
        arrangement_object = ArrangementObject(Mock())

        # Set a pid on the object so that it could internally generate a noid etc.
        arrangement_object.pid = "test:1234"

        # Simulate when the object doesn't exist (or hasn't been saved)
        # By default it appears as if it doesn't exist
        arrangement_object.update_ark_label()

        # What we should expect is that the update_ark_label is not called on pidman
        # Also there shouldn't be any errors
        # Use the mock assertFalse to check if a method is called or not
        self.assertFalse(mockpidman.get_ark.called)

        # Mock when the object exists (returns True)
        # Note: Need to set the Mock on the class and not the object because
        # this (exists) is a property method
        with patch.object(ArrangementObject, 'exists', new=Mock(return_value=True)):
            arrangement_object.update_ark_label()
            self.assertFalse(mockpidman.get_ark.called)

        # Set the label before the object exists so we don't trigger API calls
        arrangement_object.dc.content.title = "testpid"
        with patch.object(ArrangementObject, 'exists', new=Mock(return_value=True)):
            mockpidman.get_ark.return_value = {"name": arrangement_object.dc.content.title}
            arrangement_object.update_ark_label()
            mockpidman.get_ark.assert_called_with(arrangement_object.noid) # assert that it is called with a noid too
            self.assertFalse(mockpidman.update_ark.called)

            # When the label is different from that in Pidman
            mockpidman.get_ark.return_value = {"name": "another pid"}
            arrangement_object.update_ark_label()
            mockpidman.get_ark.assert_called_with(arrangement_object.noid) # assert that it is called with a noid too
            mockpidman.update_ark.assert_called_with(noid=arrangement_object.noid, name=arrangement_object.dc.content.title)

    def test_set_premis_object(self):
        mockapi = Mock()
        arrangement_object = ArrangementObject(mockapi)
        arrangement_object.pid = "test:1234"
        arrangement_object.mods.content.ark = 'ark:/1234/987'

        # return empty iterator for original data to checksum
        mockapi.getDatastreamDissemination.return_value = []
        with patch.object(arrangement_object, 'getDatastreamObject') as mockgetds:
            mockgetds.return_value.checksum = '123456789'
            mockgetds.return_value.mimetype = 'text/plain'
            arrangement_object.set_premis_object()

        self.assert_(arrangement_object.provenance.content.object)
        premis = arrangement_object.provenance.content
        # FIXME: placeholder tests for placeholder functionality,
        # should be updated to use ARK uri once that is implemented
        self.assertEqual('ark', premis.object.id_type)
        self.assertEqual(arrangement_object.mods.content.ark, premis.object.id)
        self.assertEqual('p:file', premis.object.type)
        self.assertEqual(0, premis.object.composition_level)
        self.assertEqual('MD5', premis.object.checksums[0].algorithm)
        self.assertEqual('123456789',
                         premis.object.checksums[0].digest)
        # sha1 for an empty file
        empty_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        self.assertEqual('SHA-1', premis.object.checksums[1].algorithm)
        self.assertEqual(empty_sha1,
                         premis.object.checksums[1].digest)
        # object format should be original mietype
        self.assertEqual('text/plain', premis.object.format.name)

        # generated premis should be valid
        self.assertTrue(premis.is_valid())

    def test_identifier_change_event(self):
        mockapi = Mock()
        mockapi.username = 'fedoraAdmin'
        arrangement_object = ArrangementObject(mockapi)
        arrangement_object.pid = 'test:1234'
        arrangement_object.mods.content.ark = 'ark:/1234/987'

        # set object premis so we can validate
        mockapi.getDatastreamDissemination.return_value = []
        with patch.object(arrangement_object, 'getDatastreamObject') as mockgetds:
            mockgetds.return_value.checksum = '123456789'
            mockgetds.return_value.mimetype = 'text/plain'
            arrangement_object.set_premis_object()

        arrangement_object.identifier_change_event('old-pid:1')
        premis = arrangement_object.provenance.content
        self.assertEqual(1, len(premis.events))
        event = premis.events[0]
        self.assertEqual('UUID', event.id_type)
        # id should be set, we don't care what it is exactly
        self.assert_(event.id)
        self.assertEqual('identifier assignment', event.type)
        self.assertEqual('program="keep"; version="%s"' % __version__,
                         event.detail)
        self.assertEqual('Pass', event.outcome)
        msg = 'Persistent identifier reassigned from %s to %s' % \
            ('old-pid:1', arrangement_object.pid)
        self.assertEqual(msg, event.outcome_detail)
        self.assertEqual('fedora user', event.agent_type)
        self.assertEqual('fedoraAdmin', event.agent_id)

        # generated premis should be valid
        self.assertTrue(premis.is_valid())


class EmailMessageTest(KeepTestCase):

    def setUp(self):
        self.repo = Repository()
        self.pids = []

        # test EmailMessage
        self.email = self.repo.get_object(type=EmailMessage)
        self.email.cerp.content.from_list = ['sender@sendmail.com']
        self.email.cerp.content.to_list = ['otherguy@friend.com']
        self.email.cerp.content.subject_list = ['Interesting Subject']

    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)

    def test_headers(self):
        h1 = cerp.Header()
        h1.name = "HEADER 1"
        h1.value = "value for header 1"
        h2 = cerp.Header()
        h2.name = "HEADER 2"
        h2.value = "value for header 2"
        self.email.cerp.content.headers.append(h1)
        self.email.cerp.content.headers.append(h2)
        self.assertEqual(self.email.headers['HEADER 1'], 'value for header 1')
        self.assertEqual(self.email.headers['HEADER 2'], 'value for header 2')


    def test_email_label(self):
        # no object label and one person in to field
        label = self.email.email_label()
        self.assertEqual('Email from sender@sendmail.com to otherguy@friend.com Interesting Subject',
                         label,
                         'Should construct label when it does not exist')

        # more then one person in to list
        self.email.cerp.content.to_list.append('additional.person@friend.com')
        label = self.email.email_label()
        self.assertEqual('Email from sender@sendmail.com to otherguy@friend.com et al. Interesting Subject',
                         label,
                         'only show first to email address when there are more than one')

        # no subject
        self.email.cerp.content.subject_list = []
        self.assertEqual('Email from sender@sendmail.com to otherguy@friend.com et al.',
                         self.email.email_label(),
                         'Display message without subject when no subject is present')

        # has a date
        date_header = cerp.Header()
        date_header.name = 'Date'
        date_header.value = 'Friday 13 200 13:00'
        self.email.cerp.content.headers.append(date_header)
        label = self.email.email_label()
        self.assertEqual('Email from sender@sendmail.com to otherguy@friend.com et al. on Friday 13 200 13:00',
                         label,
                         'only show first to email address when there are more than one')

        # object label already exists
        self.email.label = "label we want to keep"
        label = self.email.email_label()
        self.assertEqual(self.email.label, label, 'label should be preserved when it exists')

    def test_index_data(self):
        # NOTE: logic for creating the label is in the label test

        # test to make sure label exists in index data
        data = self.email.index_data()
        self.assertIn('label', data.keys())
        # mime_data does not exist, so no c
        self.assert_('content_md5' not in data,
                     'content_md5 should not be set when mime data does not exist')

        # patch mime data to test exists /cchecksum
        with patch.object(self.email, 'mime_data', Mock()) as mock_mime:
            mock_mime.exists = True
            mock_mime.checksum = 'test checksum value'

            data = self.email.index_data()
            self.assertEqual(self.email.mime_data.checksum, data['content_md5'])

    @patch('keep.arrangement.models.solr_interface', spec=sunburnt.SolrInterface)
    def test_by_checksum(self, mocksolr):
        # no match
        self.assertRaises(ObjectDoesNotExist, EmailMessage.by_checksum,
                          42)
        solr = mocksolr.return_value
        solr.query.assert_called_with(content_md5=42,
                                      content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
        solr.query.return_value.field_limit.assert_called_with('pid')

        # too many matches
        solr.query.return_value.field_limit.return_value = [{'pid': 'pid:1'},
                                                            {'pid': 'pid:2'}]
        self.assertRaises(MultipleObjectsReturned, EmailMessage.by_checksum,
                          42)

        # one match
        solr.query.return_value.field_limit.return_value = [{'pid': 'pid:1'}]
        em = EmailMessage.by_checksum(42)
        self.assert_(isinstance(em, EmailMessage))

        # custom repo object
        mockrepo = Mock()
        em = EmailMessage.by_checksum(42, mockrepo)
        mockrepo.get_object.assert_called_with('pid:1', type=EmailMessage)

    @patch('keep.arrangement.models.solr_interface', spec=sunburnt.SolrInterface)
    def test_by_message_id(self, mocksolr):
        # no match
        self.assertRaises(ObjectDoesNotExist, EmailMessage.by_message_id,
                          '<12345@message.com>')
        solr = mocksolr.return_value
        solr.query.assert_called_with(arrangement_id='<12345@message.com>',
                                      content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
        solr.query.return_value.field_limit.assert_called_with('pid')


#arrangementforms.ArrangementObjectEditForm))
#class ArrangementObjectEditFormTest(KeepTestCase):
class ArrangementObjectEditFormTest(TestCase):

    def test_update_instance(self):
        # test pdf update
        emailobj = EmailMessage(Mock())
        emailobj.pid = 'testemail:1'
        mock_upload = Mock()
        mock_upload.content_type = 'application/pdf'
        mock_upload.name = 'MyDocument.pdf'
        editform = arrangementforms.ArrangementObjectEditForm(instance=emailobj)
        editform.cleaned_data = {'pdf': mock_upload}

        editform.update_instance()
        # email has no pdf - should not error attempting to add one
        self.assertFalse(hasattr(emailobj, 'pdf'))

        fileobj = RushdieArrangementFile(Mock())
        fileobj.pid = 'testfile:1'
        editform = arrangementforms.ArrangementObjectEditForm(instance=fileobj)
        editform.cleaned_data = {'pdf': mock_upload}
        editform.update_instance()
        self.assertEqual(mock_upload.name, fileobj.pdf.label)
        self.assertEqual(mock_upload.content_type, fileobj.pdf.mimetype)
        self.assertEqual(mock_upload, fileobj.pdf.content)
