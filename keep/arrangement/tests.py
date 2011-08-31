import logging
import sys
from django.test import TestCase
from django.contrib.auth.models import User

from eulfedora.rdfns import relsext as relsextns

from keep.arrangement.management.commands.migrate_rushdie import CONTENT_MODELS
from  keep.arrangement.management.commands import migrate_rushdie
from keep.arrangement.models import ArrangementObject
from keep.collection.models import SimpleCollection
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

class PermissionsCheckTest(TestCase):
    fixtures =  ['users']

    def test_permission_exists(self):
        #Test for permission on a sample fixture user
        marbl_user = User.objects.get(username__exact='marbl')
        self.assertTrue(marbl_user.has_perm('arrangement.marbl_allowed'))

        #Test for permission not existing on a sample fixture user.
        non_marbl_user = User.objects.get(username__exact='nonmarbl')
        self.assertFalse(non_marbl_user.has_perm('arrangement.marbl_allowed'))

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

    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #Create a a simple Collection
        self.sc = self.repo.get_object(type=SimpleCollection)
        self.sc.label = "SimpleCollection For Test"
        self.sc.save()
        self.pids.append(self.sc.pid)

        #Create a a DigitalObject
        self.digObj = self.repo.get_object(type=ArrangementObject)
        self.digObj.label = "Object For Test"
        self.digObj.save()
        self.pids.append(self.digObj.pid)
        self.digObj.api.addDatastream(self.digObj.pid, "MARBL-MACTECH",
                                           "MARBL-MACTECH",  mimeType="application/xml", content= self.MM_FIXTURE)


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
        obj = self.cmd._convert_ds(self.digObj, False)
        #Check all fields are moved over correctly
        self.assertEqual(obj.filetech.content.file[0].md5, "ffcf48e5df673fc7de985e1b859eeeec")
        self.assertEqual(obj.filetech.content.file[0].computer, "Performa 5400")
        self.assertEqual(obj.filetech.content.file[0].path, "/Hard Disk/MIDNIGHT'S CHILDREN/MISC. MATERIAL/x - the roles")
        self.assertEqual(obj.filetech.content.file[0].rawpath, "L0hhcmQgRGlzay9NSUROSUdIVCdTIENISUxEUkVOL01JU0MuIE1BVEVSSUFML3ggLSB0aGUgcm9sZXM=")
        self.assertEqual(obj.filetech.content.file[0].attributes, "avbstclInmedz")
        self.assertEqual(obj.filetech.content.file[0].created, "1997-01-19T19:29:32")
        self.assertEqual(obj.filetech.content.file[0].modified, "1997-01-19T19:29:32")
        self.assertEqual(obj.filetech.content.file[0].type, "TEXT")
        self.assertEqual(obj.filetech.content.file[0].creator, "ttxt")
        #have to reload obj from repository to get DS update
        obj = self.repo.get_object(pid=obj.pid, type=ArrangementObject)
        self.assertFalse("MARBL-MACTECH" in obj.ds_list, "MARBL-MACTECH should have been removed")

