import sys
from django.test import TestCase
from django.contrib.auth.models import User

from eulfedora.rdfns import relsext as relsextns

from keep.arrangement.management.commands.migrate_rushdie import CONTENT_MODELS
from  keep.arrangement.management.commands import migrate_rushdie
from keep.collection.models import SimpleCollection
from keep.common.fedora import Repository

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
    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #Create a a simple Collection
        self.sc = self.repo.get_object(type=SimpleCollection)
        self.sc.label = "SimpleCollection For Test"
        self.sc.save()
        self.pids.append(self.sc.pid)

        #Create a a DigitalObject
        self.digObj = self.repo.get_object()
        self.digObj.label = "Object For Test"
        self.digObj.save()
        self.pids.append(self.digObj.pid)

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
        self.assertTrue((self.sc.uriref, relsextns.hasMember, self.digObj.uriref) in self.sc.rels_ext.content)


    def test__get_unique_objects(self):
        #duplicate pids are processed only once
        objs = self.cmd._get_unique_objects([self.digObj.pid, self.digObj.pid])
        self.assertEqual(len(objs), 1)

