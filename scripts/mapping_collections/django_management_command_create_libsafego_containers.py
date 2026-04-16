# -*- coding: utf-8 -*-
"""Create collection-level containers in LIBSAFE Go.

Reads a CSV produced by :mod:`export_diskimage_collections` and, for each
row, creates a data container via the LIBSAFE Go REST API and populates
the container metadata with:

    c_title      ← Collection title
    c_identifier ← ArchivesSpace-formatted source identifier

A results CSV is written at the end mapping each collection to its new
LIBSAFE Go container ID.
"""

from __future__ import unicode_literals

import csv
import json
import time
import urllib
import urllib2

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Create LIBSAFE Go collection containers from a CSV of '
        'Disk Image collections (title and identifier).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            help='Path to the input CSV (from export_diskimage_collections)',
        )
        parser.add_argument(
            '--api-url',
            required=True,
            help='LIBSAFE Go platform URL (e.g. https://example.libnova.com)',
        )
        parser.add_argument(
            '--api-key',
            required=True,
            help='LIBSAFE Go API key (Bearer token value)',
        )
        parser.add_argument(
            '--container-metadata-id',
            type=int,
            default=None,
            help='Container metadata schema ID',
        )
        parser.add_argument(
            '--metadata-schema-id',
            type=int,
            default=None,
            help='Object metadata schema ID',
        )
        parser.add_argument(
            '--workflow-id',
            type=int,
            default=None,
            help='Workflow ID',
        )
        parser.add_argument(
            '--archival-structure-id',
            type=int,
            default=None,
            help='Archival structure node ID',
        )
        parser.add_argument(
            '--storage-id',
            type=int,
            default=None,
            help='Storage provider ID',
        )
        parser.add_argument(
            '--dry-run', '-n',
            action='store_true',
            help='Show what would be created without making API calls',
        )
        parser.add_argument(
            '-o', '--output', default='created_containers.csv',
            help='Path for results CSV (default: created_containers.csv)',
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=2.0,
            help='Seconds to wait between API calls (default: 2.0)',
        )

    # ------------------------------------------------------------------
    def handle(self, *args, **opts):
        csv_file = opts['csv_file']
        api_url = opts['api_url'].rstrip('/')
        api_key = opts['api_key']
        dry_run = opts['dry_run']
        output_path = opts['output']
        delay = opts['delay']
        verbosity = opts.get('verbosity', 1)

        rows = self._read_csv(csv_file)
        self.stdout.write('Read %d collections from %s' % (len(rows), csv_file))

        if dry_run:
            self.stdout.write('[DRY RUN] No API calls will be made.')

        created = 0
        failed = 0
        results = []

        for i, row in enumerate(rows):
            title = row.get('Title (c_title)', '').strip()
            identifier = row.get('Identifier (c_identifier)', '').strip()

            self.stdout.write(
                '[%d/%d] %s  |  %s' % (i + 1, len(rows), title, identifier)
            )

            if dry_run:
                results.append((title, identifier, 'DRY-RUN'))
                continue

            # Step 1 – create the container
            container_id = self._create_container(
                api_url, api_key, title, opts
            )
            if container_id is None:
                self.stderr.write('  FAILED to create container')
                results.append((title, identifier, 'ERROR'))
                failed += 1
                continue

            if verbosity >= 2:
                self.stdout.write('  -> Container ID: %s' % container_id)

            # Brief pause so the platform finishes provisioning
            time.sleep(delay)

            # Step 2 – populate container metadata (c_title, c_identifier)
            ok = self._set_container_metadata(
                api_url, api_key, container_id, title, identifier
            )
            if ok:
                self.stdout.write('  -> Created (ID %s)' % container_id)
                created += 1
            else:
                self.stderr.write(
                    '  -> Container %s created but metadata update failed'
                    % container_id
                )
                failed += 1

            results.append((title, identifier, str(container_id)))

            # polite pause before next request
            if i < len(rows) - 1:
                time.sleep(delay)

        # Write results CSV
        self._write_results(output_path, results)

        self.stdout.write(
            'Done. %d created, %d failed. Results in %s'
            % (created, failed, output_path)
        )

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _read_csv(path):
        rows = []
        with open(path, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows

    @staticmethod
    def _write_results(path, results):
        with open(path, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Identifier', 'Container ID'])
            for title, identifier, cid in results:
                writer.writerow([
                    title.encode('utf-8'),
                    identifier.encode('utf-8'),
                    str(cid).encode('utf-8'),
                ])

    # ------------------------------------------------------------------
    # API methods
    # ------------------------------------------------------------------

    def _create_container(self, api_url, api_key, name, opts):
        """POST /api/container — create a new data container."""
        url = '%s/api/container' % api_url

        params = {'name': name.encode('utf-8')}

        for opt_key, param_name in [
            ('storage_id', 'storage_id'),
            ('container_metadata_id', 'container_metadata_id'),
            ('metadata_schema_id', 'metadata_schema_id'),
            ('workflow_id', 'workflow_id'),
            ('archival_structure_id', 'archival_structure_id'),
        ]:
            val = opts.get(opt_key)
            if val is not None:
                params[param_name] = str(val)

        data = urllib.urlencode(params)
        req = urllib2.Request(url, data)
        req.add_header('Authorization', 'Bearer %s' % api_key)

        try:
            resp = urllib2.urlopen(req)
            body = json.loads(resp.read())
            if body.get('success'):
                return body['result']['id']
            self.stderr.write('  API response: %s' % json.dumps(body))
            return None
        except urllib2.HTTPError as e:
            self.stderr.write('  HTTP %d: %s' % (e.code, e.read()))
            return None
        except Exception as e:
            self.stderr.write('  Error: %s' % e)
            return None

    def _set_container_metadata(self, api_url, api_key, container_id,
                                title, identifier):
        """PUT /api/container/{id}/metadata — set c_title and c_identifier."""
        url = '%s/api/container/%s/metadata' % (api_url, container_id)

        payload = json.dumps({
            'metadata': [
                {
                    'iecode': 'c_title',
                    'value': title,
                    'action': 'replace',
                },
                {
                    'iecode': 'c_identifier',
                    'value': identifier,
                    'action': 'replace',
                },
            ]
        })

        req = urllib2.Request(url, payload)
        req.add_header('Authorization', 'Bearer %s' % api_key)
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'

        try:
            resp = urllib2.urlopen(req)
            body = json.loads(resp.read())
            return body.get('success', False)
        except urllib2.HTTPError as e:
            self.stderr.write('  Metadata HTTP %d: %s' % (e.code, e.read()))
            return False
        except Exception as e:
            self.stderr.write('  Metadata error: %s' % e)
            return False
