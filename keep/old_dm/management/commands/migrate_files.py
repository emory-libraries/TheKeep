from collections import defaultdict
import logging
import sys
from django.core.management.base import BaseCommand
from keep.audio.models import AudioObject
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        stats = defaultdict(int)

        for obj in self.audio_objects():
            stats['audio'] += 1
            mods = obj.mods.content
            old_id = mods.dm1_other_id or mods.dm1_id
            if old_id:
                stats['dm1'] += 1
                logger.info('Found %s=%s %s' % (obj.pid, old_id, mods.title))
            else:
                logger.debug('%s: no DM1 id. skipping.' % (obj.pid,))

        logger.info('Total DM1 objects: %(dm1)d (of %(audio)d audio objects)' % stats)

    def audio_objects(self):
        repo = Repository()
        cmodel = AudioObject.AUDIO_CONTENT_MODEL
        return repo.get_objects_with_cmodel(cmodel, type=AudioObject)
