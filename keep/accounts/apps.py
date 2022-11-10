from django.apps import AppConfig
from django.contrib.auth.models import Group

from keep.accounts.models import AnonymousResearcher

class AccountsConfig(AppConfig):
    name = 'keep.accounts'

    def ready(self):
        # Group can't be used until django has loaded models
        AnonymousResearcher._groups = Group.objects.filter(name='Patron').all()
