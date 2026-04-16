#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download all Disk Image binary content directly from Fedora.

Uses the Fedora Resource Index to discover all DiskImage objects and
their collection membership, then streams each object's ``content``
datastream to a local directory tree organised by LIBSAFE Go container
ID (using the mapping in created_containers.csv).

Directory layout:
    <output_dir>/
        <container_id>/          # LIBSAFE Go container ID
            <pid>__<title>       # one file per disk image

Resume-safe: existing files whose size matches Fedora are skipped.

Usage:
    python download_diskimages.py \\
        --fedora-url https://fedora.example.edu/fedora/ \\
        --fedora-user keep \\
        --fedora-password SECRET \\
        --containers-csv created_containers.csv \\
        --output-dir ./diskimage_downloads
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import time

try:
    from urllib.request import Request, urlopen, HTTPBasicAuthHandler, \
        HTTPSHandler, build_opener
    from urllib.parse import urlencode, quote
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen, HTTPBasicAuthHandler, \
        HTTPSHandler, build_opener, HTTPError
    from urllib import urlencode, quote

# Fedora risearch SPARQL to get all disk images with their collections
SPARQL_DISK_IMAGES = (
    'select ?pid ?coll where { '
    '?pid <info:fedora/fedora-system:def/model#hasModel> '
    '<info:fedora/emory-control:DiskImage-1.0> . '
    '?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> '
    '?coll }'
)


def fedora_opener(fedora_url, user, password, ssl_context):
    """Build a urllib opener with basic auth for Fedora."""
    auth = HTTPBasicAuthHandler()
    auth.add_password('Fedora Repository Server', fedora_url, user, password)
    return build_opener(auth, HTTPSHandler(context=ssl_context))


def risearch(fedora_url, sparql, opener, ssl_context):
    """Run a SPARQL tuple query against the Fedora Resource Index."""
    params = urlencode({
        'type': 'tuples',
        'lang': 'sparql',
        'format': 'CSV',
        'limit': 100000,
        'query': sparql,
    })
    url = '%srisearch?%s' % (fedora_url, params)
    req = Request(url)
    resp = opener.open(req)
    body = resp.read().decode('utf-8')
    lines = body.strip().split('\n')
    if len(lines) < 2:
        return []
    headers = [h.strip('"') for h in lines[0].split(',')]
    rows = []
    for line in lines[1:]:
        vals = line.split(',')
        rows.append(dict(zip(headers, vals)))
    return rows


def get_mods_title(fedora_url, pid, opener):
    """Fetch the MODS title for a disk image object."""
    url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<mods:title>([^<]+)</mods:title>', xml)
        return m.group(1) if m else ''
    except Exception:
        return ''


def get_ds_size(fedora_url, pid, dsid, opener):
    """Get the size of a datastream from its profile."""
    url = '%sobjects/%s/datastreams/%s?format=xml' % (fedora_url, pid, dsid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<dsSize>(\d+)</dsSize>', xml)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def get_collection_source_id(fedora_url, coll_pid, opener, cache):
    """Get source_id from a collection's MODS (cached)."""
    if coll_pid in cache:
        return cache[coll_pid]
    url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, coll_pid)
    source_id = None
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<mods:identifier[^>]*type="ark"', xml)
        # source_id is in a dedicated field; look for the numeric id
        # In CollectionObject MODS, source_id is stored differently
        # Let's use the collection label instead
    except Exception:
        pass
    cache[coll_pid] = source_id
    return source_id


def download_content(fedora_url, pid, dest_path, opener):
    """Stream-download the content datastream from Fedora."""
    url = '%sobjects/%s/datastreams/content/content' % (fedora_url, pid)
    resp = opener.open(Request(url))
    downloaded = 0
    with open(dest_path, 'wb') as f:
        while True:
            chunk = resp.read(1024 * 1024)  # 1 MB
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
    return downloaded


def format_size(nbytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(nbytes) < 1024.0:
            return '%.1f %s' % (nbytes, unit)
        nbytes /= 1024.0
    return '%.1f PB' % nbytes


def build_collection_map(csv_path):
    """Map 'Manuscript Collection No. X' -> LIBSAFE Go container ID."""
    mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            ident = row.get('Identifier', '').strip()
            cid = row.get('Container ID', '').strip()
            if ident and cid:
                mapping[ident] = cid
    return mapping


def build_collection_pid_map(fedora_url, coll_pids, opener, id_to_container):
    """Map collection PID -> LIBSAFE Go container ID by reading each
    collection's MODS to get source_id, then matching to the CSV."""
    pid_map = {}
    for coll_pid in coll_pids:
        if coll_pid in pid_map:
            continue
        url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, coll_pid)
        try:
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            # source_id is <mods:identifier type="local">###</mods:identifier>
            # or in Keep it's mapped differently. Let's look for the title
            # and match, or extract source_id from the MODS
            # Actually, in Keep, source_id maps from mods:recordInfo/recordIdentifier
            # But let's try a simpler approach: extract the number from the
            # collection label/title and match
            title_match = re.search(r'<mods:title>([^<]+)</mods:title>', xml)
            title = title_match.group(1).strip() if title_match else ''

            # Look up by trying each identifier in our mapping
            found = False
            for ident, container_id in id_to_container.items():
                # Compare the title from mapping with the MODS title
                csv_title = None
                # We need to match the collection. The identifier is like
                # "Manuscript Collection No. 1000". We can extract 1000
                # and see if the MODS has a matching source_id.
                num_match = re.search(r'No\.\s*(\d+)', ident)
                if num_match:
                    source_num = num_match.group(1)
                    # Check if this number appears as source_id in the MODS
                    if ('<mods:recordInfo><mods:recordIdentifier source="'
                            in xml and source_num in xml):
                        pid_map[coll_pid] = container_id
                        found = True
                        break

            if not found:
                pid_map[coll_pid] = 'unmapped'
        except Exception:
            pid_map[coll_pid] = 'unmapped'

    return pid_map


def main():
    parser = argparse.ArgumentParser(
        description='Download all Disk Image content from Fedora'
    )
    parser.add_argument(
        '--fedora-url',
        default=os.environ.get('FEDORA_URL', ''),
        help='Fedora root URL (default: $FEDORA_URL)',
    )
    parser.add_argument('--fedora-user', default='keep')
    parser.add_argument('--fedora-password', required=True)
    parser.add_argument(
        '--solr-url',
        default=os.environ.get('SOLR_URL', ''),
        help='Solr URL (used for collection mapping; optional; default: $SOLR_URL)',
    )
    parser.add_argument(
        '--containers-csv', default='created_containers.csv',
        help='CSV mapping collections to LIBSAFE Go container IDs',
    )
    parser.add_argument(
        '--output-dir', default='diskimage_downloads',
        help='Output directory',
    )
    parser.add_argument(
        '--skip-download', action='store_true',
        help='Survey only: list objects and sizes without downloading',
    )
    parser.add_argument(
        '--limit', type=int, default=0,
        help='Limit number to download (0 = all)',
    )
    parser.add_argument(
        '--no-ssl-verify', action='store_true',
        help='Disable SSL certificate verification',
    )
    parser.add_argument(
        '--use-solr', action='store_true',
        help='Use Solr for collection mapping instead of Fedora MODS',
    )

    opts = parser.parse_args()
    if not (opts.fedora_url or '').strip():
        parser.error('Set FEDORA_URL or pass --fedora-url')
    fedora_url = opts.fedora_url.rstrip('/') + '/'

    # SSL
    ssl_ctx = ssl.create_default_context()
    if opts.no_ssl_verify:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    opener = fedora_opener(fedora_url, opts.fedora_user,
                           opts.fedora_password, ssl_ctx)

    # Load LIBSAFE Go container mapping
    print('Loading container mapping from %s ...' % opts.containers_csv)
    id_to_container = build_collection_map(opts.containers_csv)
    print('  %d collection identifiers mapped' % len(id_to_container))

    # Query Fedora Resource Index for all disk images + collections
    print('Querying Fedora Resource Index for disk images ...')
    rows = risearch(fedora_url, SPARQL_DISK_IMAGES, opener, ssl_ctx)
    print('  Found %d disk image objects' % len(rows))

    if not rows:
        return

    # Build collection PID -> LIBSAFE Go container ID mapping
    # by reading each collection's MODS from Fedora to get source_id
    coll_pids = set()
    for row in rows:
        coll_uri = row.get('coll', '')
        coll_pid = coll_uri.replace('info:fedora/', '')
        coll_pids.add(coll_pid)
    print('  Across %d unique collections' % len(coll_pids))

    print('Mapping collections to LIBSAFE Go containers via Fedora MODS ...')
    coll_pid_to_container = {}
    for coll_pid in sorted(coll_pids):
        url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, coll_pid)
        try:
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            m = re.search(
                r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>',
                xml
            )
            if m:
                source_id = m.group(1)
                formatted = 'Manuscript Collection No. %s' % source_id
                cid = id_to_container.get(formatted, 'unmapped')
                coll_pid_to_container[coll_pid] = cid
            else:
                coll_pid_to_container[coll_pid] = 'unmapped'
        except Exception:
            coll_pid_to_container[coll_pid] = 'unmapped'

    mapped = sum(1 for v in coll_pid_to_container.values() if v != 'unmapped')
    print('  Mapped %d / %d collections to containers' % (mapped, len(coll_pids)))

    # Prepare download
    os.makedirs(opts.output_dir, exist_ok=True)

    items = rows
    if opts.limit:
        items = rows[:opts.limit]

    total_size = 0
    download_count = 0
    skip_count = 0
    error_count = 0
    downloaded_bytes = 0

    for i, row in enumerate(items):
        pid_uri = row.get('pid', '')
        pid = pid_uri.replace('info:fedora/', '')
        coll_uri = row.get('coll', '')
        coll_pid = coll_uri.replace('info:fedora/', '')
        container_id = coll_pid_to_container.get(coll_pid, 'unmapped')

        # Get datastream size
        ds_size = get_ds_size(fedora_url, pid, 'content', opener)
        total_size += ds_size

        # Get title for filename
        title = get_mods_title(fedora_url, pid, opener)
        safe_title = re.sub(r'[^\w\-.]', '_', title) if title else pid.replace(':', '_')
        filename = '%s__%s' % (pid.replace(':', '_'), safe_title)

        if opts.skip_download:
            print('[%d/%d] %s  |  %s  |  container=%s  |  %s'
                  % (i + 1, len(items), pid, title, container_id,
                     format_size(ds_size)))
            continue

        # Create container directory
        container_dir = os.path.join(opts.output_dir, str(container_id))
        os.makedirs(container_dir, exist_ok=True)
        dest_path = os.path.join(container_dir, filename)

        # Resume: skip if file exists with matching size
        if os.path.exists(dest_path) and ds_size:
            if os.path.getsize(dest_path) == ds_size:
                print('[%d/%d] SKIP %s (%s)'
                      % (i + 1, len(items), pid, format_size(ds_size)))
                skip_count += 1
                continue

        print('[%d/%d] Downloading %s -> %s (%s)'
              % (i + 1, len(items), pid, filename, format_size(ds_size)))

        try:
            t0 = time.time()
            nbytes = download_content(fedora_url, pid, dest_path, opener)
            elapsed = time.time() - t0
            speed = nbytes / elapsed if elapsed > 0 else 0
            downloaded_bytes += nbytes
            download_count += 1
            print('  -> %s in %.1fs (%s/s)'
                  % (format_size(nbytes), elapsed, format_size(speed)))
        except Exception as e:
            print('  ERROR: %s' % e, file=sys.stderr)
            error_count += 1
            if os.path.exists(dest_path):
                os.remove(dest_path)

    print('\n' + '=' * 60)
    print('Total disk images:  %d' % len(items))
    print('Total size:         %s' % format_size(total_size))
    if not opts.skip_download:
        print('Downloaded:         %d (%s)' % (download_count,
              format_size(downloaded_bytes)))
        print('Skipped (exist):    %d' % skip_count)
        print('Errors:             %d' % error_count)


if __name__ == '__main__':
    main()
