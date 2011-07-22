from collections import defaultdict, namedtuple
from contextlib import contextmanager
import csv
import logging
from optparse import make_option
import os
from sunburnt import sunburnt
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from keep.audio.models import AudioObject
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

AudioFile = namedtuple('AudioFile', 
        ('wav', 'm4a', 'md5', 'jhove'))

class Command(BaseCommand):
    '''Migrate files for metadata-only items generated from the old
    Digital Masters database (using migrate_metadata) into the new
    Repository-based system.'''
    help = __doc__

    args = '<pid pid dm_id other_id pid ...>'
    option_list = BaseCommand.option_list + (
        make_option('--csvoutput', '-c',
            help='''Output CSV data to the specified filename'''),
        make_option('--max', '-m',
            type='int',
            help='''Stop after processing the specified number of items'''),
        )

    def handle(self,  *pids, **options):
        stats = defaultdict(int)
        # limit to max number of items if specified
        max_items = None
        if 'max' in options and options['max']:
            max_items = options['max']
        
        self.claimed_files = set()

        # if there are any dm1 ids, convert them to fedora pids
        pids = self.dmids_to_pids(pids)

        with self.open_csv(options) as csvfile:
            if csvfile:
                FIELDS = ('pid', 'dm1_id', 'dm1_other_id',
                          'wav', 'm4a', 'md5', 'jhove')
                csvfile.writerow(FIELDS)

            for obj in self.audio_objects(pids):
                stats['audio'] += 1
                mods = obj.mods.content
                # only objects with a dm1 id will have files that need to be migrated
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
                if not paths.wav:
                    logger.error("%s=%s missing WAV file" % (obj.pid, old_id))
                    stats['no_wav'] += 1

                if csvfile:
                    row_data = [ obj.pid, obj.mods.content.dm1_id,
                                 obj.mods.content.dm1_other_id ] + \
                                 list(paths)
                    csvfile.writerow(row_data)

                if max_items is not None and stats['audio'] > max_items:
                    break

        # if we are not migrating everything (limited either by max or specified pids),
        # skip the unclaimed files check
        if max_items is not None or pids:
            logger.info('Skipping unclaimed file check, because migration was limited')
        else:
            # look for any audio files not claimed by a fedora object
            self.check_unclaimed_files()

        logger.debug('Total DM1 objects: %(dm1)d (of %(audio)d audio objects)' % stats)
        logger.debug('Missing WAV file: %(no_wav)d' % stats)

    @contextmanager
    def open_csv(self, options):
        if options['csvoutput']:
            with open(options['csvoutput'], 'wb') as f:
                csvfile = csv.writer(f)
                yield csvfile
        else:
            yield None

    def audio_objects(self, pids=list()):
        '''Find AudioObjects in the repository for files to be added.
        Takes an optional list of pids.  If specified, returns a
        generator of :class:`~keep.audio.models.AudioObject` instances
        for the specified pids.  Otherwise, returns all Fedora objects
        with the AudioObject content model, as instances of AudioObject.
        '''
        repo = Repository()
        if pids:
            return (repo.get_object(pid, type=AudioObject) for pid in pids)
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
            # keep track of files that belong to an object
            self.claimed_files.add(abs_path)
            return abs_path
        else:
            logging.debug('missing path: ' + abs_path)


    def check_unclaimed_files(self):
        '''Scan for any audio files under the configured
        MIGRATION_AUDIO_ROOT directory that have not been claimed by
        an AudioObject in Fedora.  This function will compare any file
        in a directory named "audio" at any depth under the migration
        root directory, and warn about any files that have not been
        already identified as corresponding to an AudioObject.  
        '''
        # should only be run after the main script logic has looked
        # for files and populated self.claimed_files
        logger.info('Checking for unclaimed audio files')
        # traverse the configured migration directory
        for root, dirnames, filenames in os.walk(settings.MIGRATION_AUDIO_ROOT):
            # if we are in an audio directory, check the files
            base_path, current_dir = os.path.split(root)
            if current_dir == 'audio':
                for f in filenames:
                    full_path = os.path.join(root, f)
                    # warn about any files not in the claimed set
                    if full_path not in self.claimed_files:
                        logger.warn('%s is unclaimed' % full_path)

    def dmids_to_pids(self, ids):
        '''Takes a list of ids with a mix of fedora object pids and
        dm1 ids or dm1 other ids, and looks up any dm1 ids in Solr to
        find the corresponding pid.  Returns a list of fedora object
        pids.'''

        pids = set()
        solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
        for id in ids:
            # purely numeric ids are expected to be dm1 id or other id
            if id.isdigit():
                # look up the dm1 id in solr and return just the object pid
                result = solr.query(dm1_id=id).field_limit('pid').execute()
                if result:
                    if len(result) > 1:
                        logger.warn('Found too many pids for dm1 id %s: %s' % \
                                    (id, ', '.join(r['pid'] for r in result)))
                    else:
                        pids.add(result[0]['pid'])
                else:
                    logger.warn('Could not find a pid for dm1 id %s' % id)
            else:
                pids.add(id)
        return pids
