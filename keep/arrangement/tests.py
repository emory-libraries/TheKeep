"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

class PermissionsCheckTest(TestCase):
    fixtures =  ['users']

    def test_permission_exists(self):
        #Test for permission on a sample fixture user
        marbl_user = User.objects.get(username__exact='marbl')
        self.assertTrue(marbl_user.has_perm('arrangement.marbl_allowed'))

        #Test for permission not existing on a sample fixture user.
        non_marbl_user = User.objects.get(username__exact='nonmarbl')
        self.assertFalse(non_marbl_user.has_perm('arrangement.marbl_allowed'))

