#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create collection-level containers in LIBSAFE Go.

Reads the CSV produced by export_diskimage_collections and, for each row,
creates a data container via the LIBSAFE Go REST API and populates the
container metadata with:

    c_title      <- Collection title
    c_identifier <- ArchivesSpace-formatted source identifier

Usage:
    python create_libsafego_containers.py disk_image_collections.csv \\
        --api-url https://your-org.libnova.com \\
        --api-key YOUR_KEY \\
        --dry-run
"""

import argparse
import csv
import json
import sys
import time

try:
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
except ImportError:
    import urllib2 as urllib_request
    import urllib as urllib_parse

# ------------------------------------------------------------------
# Emory LIBSAFE Go defaults (discovered via API)
# ------------------------------------------------------------------
DEFAULTS = {
    'storage_id': 1,                # AWS S3
    'container_metadata_id': 5,     # Emory Archival Container Metadata
    'metadata_schema_id': 4,        # Emory Archival Object Metadata
    'workflow_id': 4,               # Rose Processing Workflow
    'workflow_step_id': 18,         # "Assign/update container metadata"
    'archival_structure_id': 7,     # Rose Library Manuscripts Node (MSS)
    'data_container_template_id': 2,  # Emory Archival Data Container
}


def create_container(api_url, api_key, name, opts):
    """POST /api/container -- create a new data container."""
    url = '%s/api/container' % api_url

    params = {'name': name}

    for key in [
        'storage_id',
        'container_metadata_id',
        'metadata_schema_id',
        'workflow_id',
        'workflow_step_id',
        'archival_structure_id',
        'data_container_template_id',
    ]:
        val = getattr(opts, key, None)
        if val is not None:
            params[key] = str(val)

    data = urllib_parse.urlencode(params).encode('utf-8')
    req = urllib_request.Request(url, data)
    req.add_header('Authorization', 'Bearer %s' % api_key)

    try:
        resp = urllib_request.urlopen(req)
        body = json.loads(resp.read().decode('utf-8'))
        if body.get('success'):
            return body['result']['id'], None
        return None, 'API error: %s' % body.get('msg', json.dumps(body))
    except Exception as e:
        return None, str(e)


def set_container_metadata(api_url, api_key, container_id, title, identifier):
    """PUT /api/container/{id}/metadata -- set c_title and c_identifier."""
    url = '%s/api/container/%s/metadata' % (api_url, container_id)

    payload = json.dumps({
        'metadata': [
            {'iecode': 'c_title', 'value': title, 'action': 'replace'},
            {'iecode': 'c_identifier', 'value': identifier, 'action': 'replace'},
        ]
    }).encode('utf-8')

    req = urllib_request.Request(url, payload, method='PUT')
    req.add_header('Authorization', 'Bearer %s' % api_key)
    req.add_header('Content-Type', 'application/json')

    try:
        resp = urllib_request.urlopen(req)
        body = json.loads(resp.read().decode('utf-8'))
        return body.get('success', False), None
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description='Create LIBSAFE Go collection containers from CSV'
    )
    parser.add_argument(
        'csv_file',
        help='Path to the input CSV (from export_diskimage_collections)',
    )
    parser.add_argument(
        '--api-url', required=True,
        help='LIBSAFE Go platform URL (e.g. https://your-org.libnova.com)',
    )
    parser.add_argument(
        '--api-key', required=True,
        help='LIBSAFE Go API key',
    )
    parser.add_argument(
        '--storage-id', type=int,
        default=DEFAULTS['storage_id'],
        help='Storage provider ID (default: %(default)s)',
    )
    parser.add_argument(
        '--container-metadata-id', type=int,
        default=DEFAULTS['container_metadata_id'],
        help='Container metadata schema ID (default: %(default)s)',
    )
    parser.add_argument(
        '--metadata-schema-id', type=int,
        default=DEFAULTS['metadata_schema_id'],
        help='Object metadata schema ID (default: %(default)s)',
    )
    parser.add_argument(
        '--workflow-id', type=int,
        default=DEFAULTS['workflow_id'],
        help='Workflow ID (default: %(default)s)',
    )
    parser.add_argument(
        '--workflow-step-id', type=int,
        default=DEFAULTS['workflow_step_id'],
        help='Initial workflow step ID (default: %(default)s)',
    )
    parser.add_argument(
        '--archival-structure-id', type=int,
        default=DEFAULTS['archival_structure_id'],
        help='Archival structure node ID (default: %(default)s)',
    )
    parser.add_argument(
        '--data-container-template-id', type=int,
        default=DEFAULTS['data_container_template_id'],
        help='Container template ID (default: %(default)s)',
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Show what would be created without making API calls',
    )
    parser.add_argument(
        '-o', '--output', default='created_containers.csv',
        help='Path for results CSV (default: %(default)s)',
    )
    parser.add_argument(
        '--delay', type=float, default=2.0,
        help='Seconds to wait between API calls (default: %(default)s)',
    )

    opts = parser.parse_args()
    api_url = opts.api_url.rstrip('/')
    api_key = opts.api_key

    # Read input CSV
    rows = []
    with open(opts.csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print('Read %d collections from %s' % (len(rows), opts.csv_file))

    if opts.dry_run:
        print('[DRY RUN] No API calls will be made.\n')

    created = 0
    failed = 0
    results = []

    for i, row in enumerate(rows):
        title = row.get('Title (c_title)', '').strip()
        identifier = row.get('Identifier (c_identifier)', '').strip()

        print('[%d/%d] %s  |  %s' % (i + 1, len(rows), title, identifier))

        if opts.dry_run:
            results.append((title, identifier, 'DRY-RUN'))
            continue

        # Step 1: create the container
        container_id, err = create_container(api_url, api_key, title, opts)
        if container_id is None:
            print('  FAILED: %s' % err, file=sys.stderr)
            results.append((title, identifier, 'ERROR'))
            failed += 1
            continue

        # Brief pause for the platform to provision the container
        time.sleep(opts.delay)

        # Step 2: set container metadata
        ok, err = set_container_metadata(
            api_url, api_key, container_id, title, identifier
        )
        if ok:
            print('  -> Created (ID %s)' % container_id)
            created += 1
        else:
            print('  -> Container %s created but metadata failed: %s'
                  % (container_id, err), file=sys.stderr)
            failed += 1

        results.append((title, identifier, str(container_id)))

        if i < len(rows) - 1:
            time.sleep(opts.delay)

    # Write results CSV
    with open(opts.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Identifier', 'Container ID'])
        for title, identifier, cid in results:
            writer.writerow([title, identifier, cid])

    print('\nDone. %d created, %d failed. Results in %s'
          % (created, failed, opts.output))


if __name__ == '__main__':
    main()
