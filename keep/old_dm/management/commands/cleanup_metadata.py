import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from pidservices.clients import parse_ark

from keep.audio.models import AudioObject
from eulxml.xmlmap.mods import Identifier

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for au in AudioObject.all():
            logger.info('examining AudioObject %s' % (au.pid,))
            self.cleanup_object(au)

        for coll in CollectionObject.all():
            logger.info('examining CollectionObject %s' % (coll.pid,))
            self.cleanup_object(coll)

    def cleanup_object(self, obj):
        old_mods = obj.mods.content.serialize(pretty=True)
        old_dc = obj.dc.content.serialize(pretty=True)

        mods = obj.mods.content
        # new objects will get these identifiers automatically. add them to
        # old objects for consistency.
        ark_access_uri = obj.default_target_data['access_uri']
        ark_idx = ark_access_uri.find('ark:')
        if not mods.ark:
            ark = Identifier(type='ark', text=ark_access_uri[ark_idx:])
            mods.identifiers.append(ark)
        if not mods.ark_uri:
            ark_uri = Identifier(type='uri', text=ark_access_uri)
            mods.identifiers.append(ark_uri)

        dc = obj.dc.content
        # these fields were all used only for findObjects search
        del dc.source_list
        del dc.relation_list
        del dc.format_list
        # for the rest, rely on the object to clean itself up.
        obj._update_dc()

        if obj.mods.isModified():
            new_mods = obj.mods.content.serialize(pretty=True)
            logger.debug('updating %s MODS from:\n%s== to:\n%s' %
                (obj.pid, old_mods, new_mods))

        if obj.dc.isModified():
            new_dc = obj.dc.content.serialize(pretty=True)
            logger.debug('updating %s DC from:\n%s== to:\n%s' % 
                (obj.pid, old_dc, new_dc))
