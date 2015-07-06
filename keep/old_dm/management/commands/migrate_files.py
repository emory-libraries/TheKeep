from collections import defaultdict, namedtuple
from contextlib import contextmanager
import csv
from datetime import datetime as dt
import logging
from optparse import make_option
import os
from sunburnt import sunburnt
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from eulfedora.util import RequestFailed, ChecksumMismatch

from keep.video.models import Video
from keep.common.fedora import Repository
from keep.file.utils import md5sum, sha1sum
from keep.common.models import PremisFixity, PremisObject
import urllib

logger = logging.getLogger(__name__)

VideoFile = namedtuple('VideoFile',
        ('mov', 'dv', 'mpg', 'm4v', 'mp4'))

class Command(BaseCommand):
    '''Migrate files for metadata-only items generated from the oldup
    Digital Masters database (using migrate_metadata) into the new
    Repository-based system.'''
    help = __doc__

    args = '<pid pid dm_id other_id pid ...>'
    option_list = BaseCommand.option_list + (
        make_option('--csvoutput', '-c',
            help='''Output CSV data to the specified filename'''),
        make_option('--max', '-m',
            type='int',
            help='''Stop after updating the specified number of items'''),
        make_option('--dry-run', '-n',
            default=False,
            action='store_true',
            help='Report on what would be done, but don\'t actually migrate anything'),
        )

    # text output to put in the CSV file for each file, based on the
    # return value from update_datastream
    file_ingest_status = {
        True: 'OK',
        False: 'FAIL',
        None: 'present'
    }

    mimetype={'dv': 'video/x-dv',
              'mov': 'video/quicktime',
              'mpg': 'video/mpeg',
              'm4v': 'video/x-m4v',
              'mp4': 'video/mp4'
    }

    def handle(self,  *pids, **options):
        stats = defaultdict(int)
        # limit to max number of items if specified
        max_items = None
        if 'max' in options and options['max']:
            max_items = options['max']
        # verbosity should be set by django BaseCommand standard options
        self.verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        self.v_normal = 1

        if options['dry_run']:
            if self.verbosity >= self.v_normal:
                self.stdout.write('Migration dry run. Video Objects and corresponding ' +
                         'file paths will be examined, but no files will be ' +
                         'migrated into Fedora. To migrate files, run ' +
                         'without the -n/--dry-run option.\n\n')

        
        self.claimed_files = set()

        # if there are any dm1 ids, convert them to fedora pids
        pids = self.dmids_to_pids(pids)

        with self.open_csv(options) as csvfile:
            if csvfile:
                FIELDS = ('pid', 'dm1_id', 'dm1_other_id',
                          'wav', 'm4a', 'md5', 'jhove',
                          'wav MD5', 'wav ingested', 'm4a ingested', 'jhove ingested')
                csvfile.writerow(FIELDS)

            for obj in self.video_objects(pids):
                stats['video'] += 1
                mods = obj.mods.content
                # only objects with a dm1 id will have files that need to be migrated
                old_id = mods.dm1_other_id or mods.dm1_id
                if not old_id:
                    if self.verbosity > self.v_normal:
                        self.stdout.write('%s: no DM1 id. skipping.\n' % (obj.pid,))
                    continue

                stats['dm1'] += 1
                if self.verbosity > self.v_normal:
                    self.stdout.write('Found %s (dm1 id %s) %s\n' % \
                                      (obj.pid, old_id,
                                      mods.title))
                paths = self.look_for_files(obj)
                if not paths:
                    self.stdout.write("Error on %s: couldn't predict path. skipping.\n" % \
                                      (obj.pid,))
                    continue

                master_path =  paths.dv or paths.mov or paths.mpg or paths.m4v
                if master_path:
                    master_path_md5 = master_path + ".md5"
                    master_path_sha1 = master_path + ".sha1"
                else:
                    master_path_md5 = None
                    master_path_sha1 = None
                try:
                    with open(master_path_md5) as f:
                        master_checksum = f.read().strip()
                except:
                    master_checksum = None
                try:
                    with open(master_path_sha1) as f:
                        master_sha1 = f.read().strip()
                except:
                    master_sha1 = None

                master_mimetype = self.mimetype[master_path.split(".")[-1]] if master_path else None

                access_path = paths.mp4
                if access_path:
                    access_path_md5 = access_path + ".md5"
                    access_path_sha1 = access_path + ".sha1"
                else:
                    access_path_md5 = None
                    access_path_sha1 = None
                try:
                    with open(access_path_md5) as f:
                        access_checksum = f.read().strip()
                except:
                    access_checksum = None
                try:
                    with open(access_path_sha1) as f:
                        access_sha1 = f.read().strip()
                except:
                    access_sha1 = None

                access_mimetype = self.mimetype[access_path.split(".")[-1]] if access_path else None

                file_info = []	# info to report in CSV file
                files_updated = 0
                # logic to actually add files to fedora objects
                # - only execute when not in dry-run mode
                if not options['dry_run']:
                    # keep track of any files that are migrated into fedora

                    #*************USE THIS LATER****************
                    # # if there is a stored MD5 checksum for the file, use that
                    # if paths.md5:
                    #     with open(paths.md5) as md5file:
                    #         wav_md5 = md5file.read().strip()
                    # # otherwise, let update_datastream calculate the MD5
                    # else:
                    #     wav_md5 = None
                    # file_info.append(wav_md5)
                    # # add the WAV file as contents of the primary audio datastream
                    # wav_updated = self.update_datastream(obj.audio, paths.wav, wav_md5)
                    # if wav_updated:	# True = successfully ingested/updated
                    #     files_updated += 1
                    # file_info.append(self.file_ingest_status[wav_updated])
                        
                    # Continue even if the WAV fails; it may have
                    # to be handled manually, but having the other
                    # files migrated should still be valuable
                    
                    # for newly ingested objects, audio file duration
                    # is calculated and stored at ingest; go ahead and
                    # do that for migration content, too
                    # obj.digitaltech.content.duration = '%d' % round(wav_duration(paths.wav))
                    # if obj.digitaltech.isModified():
                    #     if self.verbosity > self.v_normal:
                    #         self.stdout.write('Adding WAV file duration to DigitalTech')
                    #         obj.digitaltech.save('duration calculated from WAV file during migration')


                    if master_path:
                        # Set the correct mimetype
                        obj.content.mimetype = master_mimetype
                        master_updated = self.update_datastream(obj.content, master_path, master_checksum)
                        if master_updated:
                            files_updated += 1
                        file_info.append(self.file_ingest_status[master_updated])
                    else:
                        file_info.append('')	# blank to indicate no file

                    if access_path:
                        # Set the correct mimetype
                        obj.access_copy.mimetype = access_mimetype
                        access_updated = self.update_datastream(obj.access_copy, access_path, access_checksum, access_sha1)
                        if access_updated:
                            files_updated += 1
                            obj.mods.content.record_info.change_date = dt.now().isoformat()
                        file_info.append(self.file_ingest_status[access_updated])
                    else:
                        file_info.append('')	# blank to indicate no file

                    if master_checksum is None:
                        if self.verbosity > self.v_normal:
                            self.stdout.write('Calculating MD5 for %s\n' % master_path)
                        try:
                            master_checksum = md5sum(master_path)
                        except:
                            master_checksum = None

                    if master_checksum:
                        obj.provenance.content.create_object()
                        obj.provenance.content.object.id_type = 'ark'
                        obj.provenance.content.object.id = ''
                        obj.provenance.content.object.type = 'p:file'
                        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='MD5'))
                        obj.provenance.content.object.checksums[-1].digest = master_checksum

                    if master_sha1 is None:
                        if self.verbosity > self.v_normal:
                            self.stdout.write('Calculating SHA-1 for %s\n' % master_path)
                        try:
                            master_sha1 = sha1sum(master_path)
                        except:
                            master_sha1 = None

                    if master_sha1:
                        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='SHA-1'))
                        obj.provenance.content.object.checksums[-1].digest = master_sha1
                        obj.provenance.content.object.create_format()
                        obj.provenance.content.object.format.name = master_path.rsplit('.', 1)[1].upper() if master_path else None
                        obj.save("updated provenance mmetadata")

                if files_updated or options['dry_run']:
                    stats['updated'] += 1
                    stats['files'] += files_updated

                if csvfile:
                    row_data = [ obj.pid, obj.mods.content.dm1_id,
                                 obj.mods.content.dm1_other_id ] + \
                                 list(paths) + file_info
                    csvfile.writerow(row_data)

                # if a maximum was specified, check if we are at the limit
                # - it's a little bit arbitrary which count we use here; audio items?
                #   dm1 items? going with updated items as it seems the most useful
                if max_items is not None and stats['updated'] > max_items:
                    break

        # if we are not migrating everything (limited either by max or specified pids),
        # skip the unclaimed files check
        if max_items is not None or pids:
            if self.verbosity > self.v_normal:
                self.stdout.write('\nSkipping unclaimed file check because migration was limited\n')
        else:
            # look for any audio files not claimed by a fedora object
            self.check_unclaimed_files()

        if self.verbosity >= self.v_normal:
            self.stdout.write('\nTotal DM1 objects: %(dm1)d (of %(audio)d audio objects)\n' \
                              % stats)
            self.stdout.write('%(updated)d object(s) updated, %(files)d files migrated\n' \
                              % stats)
            self.stdout.write('Missing WAV file: %(no_wav)d\n' % stats)

    @contextmanager
    def open_csv(self, options):
        if options['csvoutput']:
            with open(options['csvoutput'], 'wb') as f:
                csvfile = csv.writer(f)
                yield csvfile
        else:
            yield None

    def video_objects(self, pids=list()):
        '''Find Video objects in the repository for files to be added.
        Takes an optional list of pids.  If specified, returns a
        generator of :class:`~keep.video.models.Video` instances
        for the specified pids.  Otherwise, returns all Fedora objects
        with the Video content model, as instances of AudioObject.
        '''
        repo = Repository()
        if pids:
            return (repo.get_object(pid, type=Video) for pid in pids)
        cmodel = Video.VIDEO_CONTENT_MODEL
        return repo.get_objects_with_cmodel(cmodel, type=Video)

    def look_for_files(self, obj):
        access_path = obj.old_dm_media_path()
        if not access_path:
            return
        basename, ext = os.path.splitext(access_path)

        return VideoFile(*[self.dm_path(basename, ext)
                           for ext in ('mov', 'dv', 'mpg', 'm4v', 'mp4')])

    def dm_path(self, basename, ext):
        for try_ext in self.ext_cap_variants(ext):
            rel_path = '%s.%s' % (basename, try_ext)
            abs_path = os.path.join(settings.MIGRATION_VIDEO_ROOT, rel_path)
            if os.path.exists(abs_path):
                if self.verbosity > self.v_normal:
                    self.stdout.write('  found path: %s\n' % abs_path)
                # keep track of files that belong to an object
                self.claimed_files.add(abs_path)
                return abs_path

        # otherwise, no match
        if self.verbosity > self.v_normal:
            self.stdout.write('  missing path: %s\n' % (abs_path,))

    def ext_cap_variants(self, ext):
        # Extensions are sometimes capitalized and sometimes not. For
        # multi-extension files, sometimes one will be capitalized and
        # another not. Recursively generate all possible capitalization
        # variants.
        first, dot, rest = ext.partition('.')
        if rest:
            variants = self.ext_cap_variants(rest)
            return ([ '%s.%s' % (first.lower(), v) for v in variants ] +
                    [ '%s.%s' % (first.upper(), v) for v in variants ])
        else:
            return [ first.lower(), first.upper() ]


    def check_unclaimed_files(self):
        '''Scan for any video files under the configured
        MIGRATION_VIDEO_ROOT directory that have not been claimed by
        an Video in Fedora.  This function will compare any file
        in a directory named "audio" at any depth under the migration
        root directory, and warn about any files that have not been
        already identified as corresponding to an Video.
        '''
        # should only be run after the main script logic has looked
        # for files and populated self.claimed_files
        if self.verbosity >= self.v_normal:
            self.stdout.write('Checking for unclaimed audio files\n')
        # traverse the configured migration directory
        for root, dirnames, filenames in os.walk(settings.MIGRATION_VIDEO_ROOT):
            # if we are in an audio directory, check the files
            base_path, current_dir = os.path.split(root)
            if current_dir == 'video':
                for f in sorted(filenames):
                    full_path = os.path.join(root, f)
                    # warn about any files not in the claimed set
                    if full_path not in self.claimed_files:
                        self.stdout.write('Warning: %s is unclaimed\n' % full_path)

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
                        self.stdout.write('Found too many pids for dm1 id %s: %s\n' % \
                                    (id, ', '.join(r['pid'] for r in result)))
                    else:
                        pids.add(result[0]['pid'])
                else:
                    self.stdout.write('Could not find a pid for dm1 id %s\n' % id)
            else:
                pids.add(id)
        return pids


    def update_datastream(self, ds, filepath, checksum=None, sha1=None):
        '''Update the contents of a single datastream in Fedora.  If
        the datastream already exists and the checksum matches the one
        passed in, no updates will be made.

        :param ds: :class:`eulfedora.models.DatastreamObject` the
            datastream to be updated
        :param filepath: full path to the file whose contents should
            be stored in the datastream
        :param checksum: the MD5 checksum for the file contents; if
            not specified, an MD5 checksum will be calculated for the
            file passed in

        :returns: True if the datastream was saved; None if no action
            was needed (datastream was already present with the
            expected checksum), or False if the update failed
        '''
        if checksum is None:
            if self.verbosity > self.v_normal:
                self.stdout.write('Calculating MD5 for %s\n' % filepath)
            try:
                checksum = md5sum(filepath)
            except:
                checksum = None

        # - if the content already exists with the correct checksum
        # (e.g., from a previous file migration run), skip it
        if ds.exists and ds.checksum == checksum:
            if self.verbosity > self.v_normal:
                self.stdout.write('%s already has %s datastream with the expected checksum; skipping\n' \
                                  % (ds.obj.pid, ds.id))
            return True
        
        # datastream does not yet exist or does not have the expected content
        # migrate the file into the repository
        else:
            location = filepath.replace(settings.MIGRATION_VIDEO_ROOT, settings.OLD_DM_MEDIA_ROOT)
            self.stdout.write('LOCATION: %s\n' % location)
            self.stdout.write('MD5: %s\n' % checksum)
            ds.ds_location = location
            #ds.checksum_type = 'MD5'
            #ds.checksum = checksum
            try:
                # save just this datastream
                success = ds.save('Migrated from legacy Digital Masters file %s\n' % \
                         filepath)
                if success:
                    if self.verbosity > self.v_normal:
                        self.stdout.write('Successfully updated %s/%s\n' \
                                      % (ds.obj.pid, ds.id))
                    return None
                else:
                    if self.verbosity >= self.v_normal:
                        self.stdout.write('Error updating %s/%s\n' \
                                          % (ds.obj.pid, ds.id))
            except RequestFailed as rf:
                self.stdout.write('Error saving %s/%s: %s\n' % \
                                  (ds.obj.pid, ds.id, rf))

        # FIXME: do we need to handle file read permission errors? 

        # successful update should already have returned - indicates some kind of error
        return False



                    
