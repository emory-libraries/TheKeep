from django.db import models
from django.contrib.auth.models import AnonymousUser


class ResearcherIP(models.Model):
    '''Model for IP addresses where anonymous users should be considered
    researchers (i.e., access from MARBL Reading Room).'''
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField('IP Address', max_length=30)

    class Meta:
        verbose_name = 'Researcher IP'

    def __unicode__(self):
        return '%s <%s>' % (self.name, self.ip_address)


class AnonymousResearcher(AnonymousUser):

    # default group membership of 'Patron' now set in
    # app config, since it can only be done after models are loaded

    def is_anonymous_researcher(self):
        return True

    @property
    def permissions(self):
        perms = []
        for g in self.groups:
            perms.extend(g.permissions.all())
        return perms

    def has_perm(self, perm):
        app_label, codename = perm.split('.')
        for perm in self.permissions:
            # django permission codes are tested on the *app* label
            # and not the model name
            if perm.content_type.app_label == app_label and \
              perm.codename == codename:
                return True
        return False

    def __str__(self):
        return 'AnonymousResearcher'