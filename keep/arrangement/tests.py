from rdflib import URIRef
import logging
import sys
from mock import Mock, MagicMock, patch
from sunburnt import sunburnt

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.test import Client
from django.core.urlresolvers import reverse

from eulfedora.rdfns import relsext as relsextns
from eulfedora.rdfns import model

from keep.arrangement.management.commands.migrate_rushdie import CONTENT_MODELS
from  keep.arrangement.management.commands import migrate_rushdie
from keep.arrangement.models import ArrangementObject, Series1, Series2
from keep.collection.models import SimpleCollection, CollectionObject
from keep.common.fedora import Repository
from keep.arrangement import forms as arrangementforms
from keep.testutil import KeepTestCase
from keep.common.utils import PaginatedSolrSearch
from keep.collection.fixtures import FedoraFixtures

from keep.common.models import FileMasterTech_Base

logger = logging.getLogger(__name__)

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

class PermissionsCheckTest(TestCase):
    fixtures =  ['users']

    def test_permission_exists(self):
        marbl_perm = Permission.objects.get(codename='marbl_allowed')
        arrangement_perm = Permission.objects.get(codename='arrangement_allowed')

        #Test for permission on a sample fixture user
        marbl_user = User.objects.get(username__exact='marbl')
        marbl_user.user_permissions.clear()
        marbl_user.save()
        marbl_user.user_permissions.add(marbl_perm)
        marbl_user.user_permissions.add(arrangement_perm)
        marbl_user.save()
        self.assertTrue(marbl_user.has_perm('common.marbl_allowed'))
        self.assertTrue(marbl_user.has_perm('common.arrangement_allowed'))

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
        self.digObj = self.repo.get_object(type=ArrangementObject)
        self.digObj.label = "Object For Test"
        self.digObj.save()
        self.pids.append(self.digObj.pid)
        self.digObj.api.addDatastream(self.digObj.pid, "MARBL-MACTECH",
                                           "MARBL-MACTECH",  mimeType="application/xml", content= self.MM_FIXTURE)
        self.digObj.api.addDatastream(self.digObj.pid, "MARBL-ANALYSIS",
                                           "MARBL-ANALYSIS",  mimeType="application/xml", content= self.MA_FIXTURE)
        #Remove Arrangement model so it can be added later
        relation = (self.digObj.uriref, model.hasModel, "info:fedora/emory-control:Arrangement-1.0")
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
        self.assertTrue((obj.uriref, model.hasModel, URIRef("info:fedora/emory-control:ArrangementAccessAllowed-1.0")) in obj.rels_ext.content, "Object should have Allowed Content Model")
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

class ArrangementViewsTest(KeepTestCase):
    fixtures =  ['users']

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
    mocksolrpaginator = MagicMock(PaginatedSolrSearch)

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

        self.rushdie_obj = self.repo.get_object(type=ArrangementObject)

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
      
        self.rushdie_obj.filetech.content.file.append(filetech_1)
        self.rushdie_obj.filetech.content.file.append(filetech_2)

        #Add a series objects
        self.rushdie_obj.mods.content.create_series()
        self.rushdie_obj.mods.content.series.title = 'subseries_title_value'

        self.rushdie_obj.mods.content.series.create_series()
        self.rushdie_obj.mods.content.series.series.title = 'series_title_vale'

        self.rushdie_obj.save()
        self.pids.append(self.rushdie_obj.pid) 

    def tearDown(self):
        super(ArrangementViewsTest, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            self.repo.purge_object(pid)
        
        self.repo.purge_object(self.rushdie.pid)
        self.repo.purge_object(self.esterbrook.pid)
        self.repo.purge_object(self.englishdocs.pid)

    def test_edit_form(self):
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