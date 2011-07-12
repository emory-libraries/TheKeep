from collections import defaultdict, namedtuple
from contextlib import contextmanager
import csv
import logging
from optparse import make_option
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from keep.audio.models import AudioObject
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

AudioFile = namedtuple('AudioFile', 
        ('wav', 'm4a', 'md5', 'jhove'))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--csvoutput', '-c',
            help='''Output CSV data to the specified filename'''),
        )

    def handle(self, *args, **options):
        stats = defaultdict(int)

        with self.open_csv(options) as csvfile:
            if csvfile:
                FIELDS = ('pid', 'dm1_id', 'dm1_other_id',
                          'wav', 'm4a', 'md5', 'jhove')
                csvfile.writerow(FIELDS)

            for obj in self.audio_objects():
                stats['audio'] += 1
                mods = obj.mods.content
                old_id = mods.dm1_other_id or mods.dm1_id
                if not old_id:
                    logger.debug('%s: no DM1 id. skipping.' % (obj.pid,))
                    continue

                stats['dm1'] += 1
                logger.info('Found %s=%s %s' % (obj.pid, old_id, mods.title))
                paths = self.look_for_files(obj)
                if not paths:
                    logger.error("%s: couldn't predict path. skipping." % (obj.pid,))
                    continue
                logger.info('%s paths: %s' % (obj.pid, repr(paths)))

                if csvfile:
                    row_data = [ obj.pid, obj.mods.content.dm1_id,
                                 obj.mods.content.dm1_other_id ] + \
                                 list(paths)
                    csvfile.writerow(row_data)


        logger.debug('Total DM1 objects: %(dm1)d (of %(audio)d audio objects)' % stats)

    @contextmanager
    def open_csv(self, options):
        if options['csvoutput']:
            with open(options['csvoutput'], 'wb') as f:
                csvfile = csv.writer(f)
                yield csvfile
        else:
            yield None

    def audio_objects(self):
        repo = Repository()
        cmodel = AudioObject.AUDIO_CONTENT_MODEL
        return repo.get_objects_with_cmodel(cmodel, type=AudioObject)

    def look_for_files(self, obj):
        access_path = obj.old_dm_media_path()
        if not access_path:
            return
        basename, ext = os.path.splitext(access_path)

        return AudioFile(*(self.dm_path(basename, ext)
                           for ext in ('wav', 'm4a', 'wav.md5', 'wav.jhove')))

    def dm_path(self, basename, ext):
        rel_path = '%s.%s' % (basename, ext)
        abs_path = os.path.join(settings.MIGRATION_AUDIO_ROOT, rel_path)
        if os.path.exists(abs_path):
            logging.debug('found path: ' + abs_path)
            return abs_path
        else:
            logging.debug('missing path: ' + abs_path)
