'''
Manage command for generating a list of test objects that can be
synchronized from production to QA to allow testing on a subset
of real data.

'''
from collections import defaultdict
import random

# from django.template.defaultfilters import filesizeformat, pluralize
from django.core.management.base import BaseCommand

from keep.common.fedora import Repository
from keep.common.utils import solr_interface
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.file.models import DiskImage
from keep.video.models import Video


class Command(BaseCommand):
    '''Select a list of pids for testing purposes.
    '''
    help = __doc__

    #: default verbosity level
    v_normal = 1

    collections = {
        'rushdie': 'emory:94k9k',
        'trethewey': 'emory:ghsdj',
        'mackey': 'emory:g1btw',
        'clifton': 'emory:94kf4',
        'grennan': 'emory:9k0st',
        'dawson': 'emory:94jz3'
    }


    def handle(self, *args, **kwargs):
        self.verbosity = kwargs.get('verbosity', self.v_normal)
        self.rushdie_files()
        self.disk_images()
        self.video()
        self.audio()

    def rushdie_files(self):
        self.stderr.write('Rushdie files')
        solr = solr_interface()

        ### individual rushdie files
        # select 100 individual rushdie files to simulate the way they
        # currently clutter up born-digital search in production
        q = solr.query(content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL,
                       collection_id=self.collections['rushdie']).field_limit('pid')
        self.stderr.write('Found %d Rushdie arrangement objects' % q.count())
        # over 6000 of these in production; pull a subset and randomize
        # to ensure diversity, get chunks from various points in the results
        pids = [r['pid'] for r in q[:100]]
        pids.extend([r['pid'] for r in q[1000:1100]])
        pids.extend([r['pid'] for r in q[2000:2100]])
        pids.extend([r['pid'] for r in q[3000:3100]])
        pids.extend([r['pid'] for r in q[4000:4100]])
        pids.extend([r['pid'] for r in q[5000:5100]])
        pids.extend([r['pid'] for r in q[6000:6100]])
        # then shuffle that and pick the first 100
        random.shuffle(pids)
        for p in pids[:100]:
            self.stdout.write(p)

    def disk_images(self):
        self.stderr.write('Disk images')
        ### disk images
        # representative sample of aff and ad1
        # DO NOT include anything in these collections:
        # Trethewey (ghsdj), Rushdie (94k9k), Mackey (g1btw),
        # Clifton (94kf4), and Grennan (9k0st)

        solr = solr_interface()
        repo = Repository()
        q = solr.query(content_model=DiskImage.DISKIMAGE_CONTENT_MODEL) \
                .exclude(collection_id=self.collections['trethewey']) \
                .exclude(collection_id=self.collections['rushdie']) \
                .exclude(collection_id=self.collections['mackey']) \
                .exclude(collection_id=self.collections['clifton']) \
                .exclude(collection_id=self.collections['grennan']) \
                .field_limit('pid')
        if self.verbosity >= self.v_normal:
            self.stderr.write('Found %d disk images not in restricted collections' % q.count())

        # currently there is no way to filter on format or size in either
        # solr or fedora risearch
        # so, go through individually and group them by type,
        # then sort by size and pick the smallest ones
        diskimgs_by_type = defaultdict(list)
        for result in q:
            diskimg = repo.get_object(result['pid'], type=DiskImage)
            if not diskimg.exists:
                if self.verbosity >= self.v_normal:
                    self.stderr.write('Referenced disk image %s does not exist or is inaccessible' \
                        % result['pid'])
                continue

            fmt = diskimg.provenance.content.object.format.name
            diskimgs_by_type[fmt].append(diskimg)

        for fmt, diskimages in diskimgs_by_type.items():
            if self.verbosity >= self.v_normal:
                self.stderr.write('Selecting %s disk images' % fmt)
            # sort on binary file size so we sync the smallest ones
            diskimages = sorted(diskimages, key=lambda diskimg: diskimg.content.size)
            # use the first 10 of each type
            for d in diskimages[:10]:
                self.stdout.write(d.pid)

    def video(self):
        self.stderr.write('Video')
        ### video
        # need a representative sample of all mime types
        # representative sample of old dm and native Keep objects
        #   (dm carries an access status of 11)
        # representative sample of different access codes
        # 5-10 collections represented
        # about 40 objects total (can be smallest size objects)

        # NOTE: there is currently no easy way to ensure we have
        # a representative sample of all mimetypes (master mimetypes are
        # not indexed, and there is too much content, so it would be too
        # slow to look in fedora.  Hopefully the diversity of codes and
        # old dm content will provide sufficient representation.

        solr = solr_interface()
        # desired minimum number of collections
        # (minimum since more may be added in order to find
        # representative objects by status)
        num_collections = 5
        # desired number of objects
        desired_total = 40

        pids = []
        collections = set()

        # find all video, and sort smallest first
        all_video = solr.query(content_model=Video.VIDEO_CONTENT_MODEL) \
               .field_limit(['pid', 'collection_id']).sort_by('access_copy_size')
        # master size is not indexed, but hopefully access copy
        # can serve as a proxy
        total_pids = all_video.count()

        if self.verbosity >= self.v_normal:
            self.stderr.write('Found %d total video objects' % all_video.count())
        facet_q = all_video.facet_by('collection_id', sort='count', mincount=1) \
                           .facet_by('access_code', sort='count', mincount=1) \
                           .paginate(rows=0)
        facets = facet_q.execute().facet_counts.facet_fields

        # pick the requested number of collections with the most items
        top_collections = [pid for (pid, count) in facets['collection_id']][:num_collections]
        # restrict query to video in those collections
        collection_filter = solr.Q()
        for coll in top_collections:
            collection_filter |= solr.Q(collection_id=coll)
        q = all_video.filter(collection_filter)
        self.stderr.write('Found %d total video objects in %d largest collections' \
            % (q.count(), num_collections))

        # Nothing here ensures we get content from all of these
        # collections, but hopefully the diversity of status codes
        # will help provide a reasonable distribution.

        # figure out some representative percentage based on our desired total
        # - by far the most content is old dm (93%), so don't use that %
        # first facet is old dm (largest total); facet is label, count
        old_dm_code =  facets['access_code'][0][0]
        old_dm_total = facets['access_code'][0][1]

        # get percentages based on the total *without* old dm
        for code, num in facets['access_code'][1:]:
            # determine number of pids to grab as a percentage
            # of half the desired number
            percent = float(num) / (total_pids - old_dm_total)
            # minimum of at least 1 per code
            num_pids = max(int((percent) * (desired_total/2)), 1)
            if self.verbosity >= self.v_normal:
                self.stderr.write('  Looking for %d pid(s) for access code %s' % \
                    (num_pids, code))
            # first try to find within the request collections
            pids_by_code = q.filter(access_code=code)
            # if no pids are found for this code in our collections,
            # look for them elsewhere
            if not pids_by_code.count():
                pids_by_code = all_video.filter(access_code=code)
            for r in pids_by_code[:num_pids]:
                pids.append(r['pid'])
                collections.add(r['collection_id'])

        # other codes will provide slightly more than half,
        # because we are rounding up; get the rest of the
        # requested objects from old dm
        remainder = desired_total - len(pids)
        for r in q.filter(access_code=old_dm_code)[:remainder]:
            pids.append(r['pid'])
            collections.add(r['collection_id'])

        if self.verbosity >= self.v_normal:
            self.stderr.write('Selected %d pids from %d collections' % \
                    (len(pids), len(collections)))

        for p in pids:
            self.stdout.write(p)

    def audio(self):
        self.stderr.write('Audio')
        ### audio
        # representative sample of all mime types
        # representative sample of old dm and native Keep objects
        #   (dm carries an access status of 11)
        # representative sample of different access codes
        # 10 collections represented
        #   (please include material from Dawson (94jz3)

        # NOTE: this is largely the same logic as for video

        solr = solr_interface()

        # desired number of collections
        # (could be adjusted some since more may be added in order to
        # find representative objects by status)
        num_collections = 10
        # desired number of objects
        desired_total = 100

        pids = []
        collections = set()

        # find all audioo, and sort smallest first
        all_audio = solr.query(content_model=AudioObject.AUDIO_CONTENT_MODEL) \
               .field_limit(['pid', 'collection_id']).sort_by('access_copy_size')
        # master size is not indexed, but hopefully access copy
        # can serve as a proxy
        total_pids = all_audio.count()

        if self.verbosity >= self.v_normal:
            self.stderr.write('Found %d total audio objects' % all_audio.count())
        facet_q = all_audio.facet_by('collection_id', sort='count', mincount=1) \
                           .facet_by('access_code', sort='count', mincount=1) \
                           .paginate(rows=0)
        facets = facet_q.execute().facet_counts.facet_fields

        # pick the requested number of collections with the most items
        top_collections = [pid for (pid, count) in facets['collection_id']][:num_collections]
        # restrict query to video in those collections
        # OR in the dawson collection
        # (dawson is *probably* included in those, but explicitly include
        # since it was requested)
        collection_filter = solr.Q(collection_id=self.collections['dawson'])
        for coll in top_collections:
            collection_filter |= solr.Q(collection_id=coll)
        q = all_audio.filter(collection_filter)
        self.stderr.write('Found %d total audio objects in %d largest collections (including dawson)' \
            % (q.count(), num_collections))

        # Nothing here ensures we get content from all of these
        # collections, but hopefully the diversity of status codes
        # will help provide a reasonable distribution.

        # calculate and find a representative percentage of items
        # for each status based on the desired total
        for code, num in facets['access_code']:
            # determine number of pids to grab as a percentage
            # of the desired number
            percent = float(num) / total_pids
            # minimum of at least 1 per code
            num_pids = max(int(percent * desired_total), 1)
            if self.verbosity >= self.v_normal:
                self.stderr.write('  Looking for %d pid(s) for access code %s' % \
                    (num_pids, code))
            # first try to find within the request collections
            pids_by_code = q.filter(access_code=code)
            # if no pids are found for this code in our collections,
            # look for them elsewhere
            if not pids_by_code.count():
                pids_by_code = all_audio.filter(access_code=code)
            for r in pids_by_code[:num_pids]:
                pids.append(r['pid'])
                collections.add(r['collection_id'])

        if self.verbosity >= self.v_normal:
            self.stderr.write('Selected %d pids from %d collections' % \
                    (len(pids), len(collections)))

        for p in pids:
            self.stdout.write(p)

