# -*- coding: utf-8 -*-
"""Export collections that contain Disk Image objects.

Queries Solr for every indexed Disk Image object, identifies the unique
parent collections, and writes a CSV with each collection's **Title** and
**Source Identifier** (formatted as an ArchivesSpace resource identifier,
e.g. ``Manuscript Collection No. 1045``).

CSV columns map to LIBSAFE Go IECodes:

    Title           → c_title
    Identifier      → c_identifier
"""

from __future__ import unicode_literals

import csv
from collections import OrderedDict

from django.core.management.base import BaseCommand

from keep.common.utils import solr_interface


CSV_HEADER = ['Title (c_title)', 'Identifier (c_identifier)']


class Command(BaseCommand):
    help = (
        'Export a CSV of collections containing Disk Image objects, '
        'with Title and Source Identifier formatted for ArchivesSpace / LIBSAFE Go.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output', default='disk_image_collections.csv',
            help='Path for output CSV (default: disk_image_collections.csv)',
        )

    def handle(self, *args, **opts):
        output_path = opts['output']
        verbosity = opts.get('verbosity', 1)

        solr = solr_interface()

        self.stdout.write('Querying Solr for Disk Image objects ...')

        # Query Solr for all disk image objects; retrieve only the
        # collection-level fields we need.
        q = solr.query(object_type='disk image') \
                .field_limit(['pid', 'collection_id',
                              'collection_label', 'collection_source_id']) \
                .paginate(start=0, rows=50000)
        results = q.execute()

        # Deduplicate by collection PID
        collections = OrderedDict()
        obj_count = 0

        for doc in results:
            obj_count += 1
            coll_pid = doc.get('collection_id', None)
            if not coll_pid or coll_pid in collections:
                continue

            title = doc.get('collection_label', '')
            source_id = doc.get('collection_source_id', None)

            # Format source_id as an ArchivesSpace resource identifier
            if source_id is not None:
                formatted_id = 'Manuscript Collection No. %s' % source_id
            else:
                formatted_id = ''

            collections[coll_pid] = {
                'title': title,
                'identifier': formatted_id,
            }

            if verbosity >= 2:
                self.stdout.write(
                    '  Collection: %s  [%s]' % (title, formatted_id)
                )

        self.stdout.write(
            'Found %d Disk Image object(s) across %d collection(s).'
            % (obj_count, len(collections))
        )

        with open(output_path, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_HEADER)

            for coll_pid, data in collections.items():
                writer.writerow([
                    data['title'].encode('utf-8'),
                    data['identifier'].encode('utf-8'),
                ])

        self.stdout.write(
            'CSV written to %s (%d collections)' % (output_path, len(collections))
        )
