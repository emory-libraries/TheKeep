#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transfer Disk Image content and/or metadata from Fedora to LIBSAFE Go.

For each DiskImage object in Fedora:
  1. Queries the Resource Index for all PIDs + collection membership
  2. Maps collections to LIBSAFE Go container IDs (from created_containers.csv)
  3. Optionally downloads and uploads metadata datastreams
  4. Optionally downloads and uploads the content datastream
  5. Uploads files to the correct LIBSAFE Go container via the API

Usage:
    pip install requests   # if not already installed

    # Survey mode (no transfers, just list what would be done)
    python transfer_to_libsafego.py \\
        --fedora-password 'PASS' \\
        --no-ssl-verify \\
        --skip-transfer

    # Transfer metadata only
    python transfer_to_libsafego.py \\
        --fedora-password 'PASS' \\
        --no-ssl-verify \\
        --metadata-only \\
        --limit 10

    # Transfer content only (original behavior)
    python transfer_to_libsafego.py \\
        --fedora-password 'PASS' \\
        --no-ssl-verify \\
        --content-only \\
        --limit 1

    # Transfer both metadata and content
    python transfer_to_libsafego.py \\
        --fedora-password 'PASS' \\
        --no-ssl-verify

    # Transfer specific metadata datastreams only
    python transfer_to_libsafego.py \\
        --fedora-password 'PASS' \\
        --no-ssl-verify \\
        --metadata-only \\
        --datastreams MODS,DC,provenanceMetadata

Environment variables (optional defaults; no secrets in repo):
    FEDORA_URL, FEDORA_USER, LIBSAFE_GO_API_URL, LIBSAFE_GO_API_KEY
    CLI: --fedora-url, --libsafe-api-url, --libsafe-api-key override env.
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from collections import defaultdict

try:
    from urllib.request import Request, urlopen, HTTPBasicAuthHandler, \
        HTTPSHandler, build_opener
    from urllib.parse import urlencode
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen, HTTPBasicAuthHandler, \
        HTTPSHandler, build_opener, HTTPError
    from urllib import urlencode

import requests

# ---- Fedora defaults (override with --fedora-url / FEDORA_URL) ----
FEDORA_USER_DEFAULT = os.environ.get('FEDORA_USER', 'keep')

# ---- Fedora SPARQL ----
SPARQL = (
    'select ?pid ?coll where { '
    '?pid <info:fedora/fedora-system:def/model#hasModel> '
    '<info:fedora/emory-control:DiskImage-1.0> . '
    '?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> '
    '?coll }'
)

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB chunks for download


def make_opener(fedora_url, user, password, ssl_ctx):
    auth = HTTPBasicAuthHandler()
    auth.add_password('Fedora Repository Server', fedora_url, user, password)
    return build_opener(auth, HTTPSHandler(context=ssl_ctx))


def risearch(fedora_url, sparql, opener):
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'limit': 100000, 'query': sparql,
    })
    resp = opener.open(Request('%srisearch?%s' % (fedora_url, params)))
    lines = resp.read().decode('utf-8').strip().split('\n')
    headers = [h.strip('"') for h in lines[0].split(',')]
    return [dict(zip(headers, l.split(','))) for l in lines[1:]]


def get_mods_title(fedora_url, pid, opener):
    url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<mods:title>([^<]+)</mods:title>', xml)
        return m.group(1).strip() if m else ''
    except Exception:
        return ''


def get_ds_info(fedora_url, pid, dsid, opener):
    """Get datastream info - try profile first, fall back to content headers."""
    url = '%sobjects/%s/datastreams/%s?format=xml' % (fedora_url, pid, dsid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        size_m = re.search(r'<dsSize>(\d+)</dsSize>', xml)
        label_m = re.search(r'<dsLabel>([^<]*)</dsLabel>', xml)
        mime_m = re.search(r'<dsMIME>([^<]*)</dsMIME>', xml)
        return {
            'size': int(size_m.group(1)) if size_m else 0,
            'label': label_m.group(1) if label_m else '',
            'mimetype': mime_m.group(1) if mime_m else 'application/octet-stream',
        }
    except Exception:
        # Fallback: try to get size from content headers
        try:
            content_url = '%sobjects/%s/datastreams/%s/content' % (fedora_url, pid, dsid)
            req = Request(content_url)
            req.get_method = lambda: 'HEAD'
            resp = opener.open(req)
            size = int(resp.headers.get('Content-Length', 0))
            mimetype = resp.headers.get('Content-Type', 'application/octet-stream')
            return {'size': size, 'label': '', 'mimetype': mimetype}
        except:
            return {'size': 0, 'label': '', 'mimetype': 'application/octet-stream'}


def get_collection_source_id(fedora_url, coll_pid, opener):
    url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, coll_pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(
            r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>',
            xml
        )
        return m.group(1) if m else None
    except Exception:
        return None


def list_datastreams(fedora_url, pid, opener):
    """List all datastreams for an object."""
    url = '%sobjects/%s/datastreams?format=xml' % (fedora_url, pid)
    datastreams = []
    
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        
        # Parse datastream elements - they are self-closing tags
        for ds_match in re.finditer(
            r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',
            xml
        ):
            full_tag = ds_match.group(0)
            dsid = ds_match.group(1)
            
            # Extract datastream properties from the tag
            label_m = re.search(r'label="([^"]*)"', full_tag)
            mime_m = re.search(r'mimeType="([^"]*)"', full_tag)
            
            datastreams.append({
                'dsid': dsid,
                'label': label_m.group(1) if label_m else '',
                'mimetype': mime_m.group(1) if mime_m else ''
            })
    except Exception as e:
        print('  Error listing datastreams for %s: %s' % (pid, e), file=sys.stderr)
    
    return datastreams


def download_datastream(fedora_url, pid, dsid, opener, dest_path):
    """Download any datastream to a local file."""
    url = '%sobjects/%s/datastreams/%s/content' % (fedora_url, pid, dsid)
    try:
        resp = opener.open(Request(url))
        written = 0
        with open(dest_path, 'wb') as f:
            while True:
                chunk = resp.read(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                written += len(chunk)
        return written
    except Exception as e:
        print('  Error downloading %s/%s: %s' % (pid, dsid, e), file=sys.stderr)
        return 0


def build_collection_map(csv_path):
    mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            ident = row.get('Identifier', '').strip()
            cid = row.get('Container ID', '').strip()
            if ident and cid:
                mapping[ident] = cid
    return mapping


def format_size(n):
    for u in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(n) < 1024.0:
            return '%.1f %s' % (n, u)
        n /= 1024.0
    return '%.1f PB' % n


def download_fedora_ds(fedora_url, pid, dsid, opener, dest_path):
    """Download a Fedora datastream to a local file. Returns bytes written."""
    return download_datastream(fedora_url, pid, dsid, opener, dest_path)


def upload_to_libsafe(api_url, api_key, container_id, filepath, filename,
                       verify_ssl=True, subfolder=None):
    """Upload a file to LIBSAFE Go via the API.

    Uses POST /container/{id}/file/upload with multipart form data.
    If subfolder is specified, uploads to that path within the container.
    Returns the API response dict.
    """
    url = '%s/container/%s/file/upload' % (api_url, container_id)
    headers = {'Authorization': 'Bearer %s' % api_key}
    
    with open(filepath, 'rb') as f:
        # Prepare the multipart form data
        files = {'file': (filename, f)}
        
        # Add form fields including path if subfolder is specified
        data = {
            'fileName': filename,
            'chunkIndex': 0,  # Required field - single chunk upload
        }
        
        # If subfolder specified, add path parameter
        if subfolder:
            data['path'] = subfolder
        
        resp = requests.post(url, headers=headers, files=files, data=data,
                             verify=verify_ssl, timeout=7200)
    resp.raise_for_status()
    return resp.json()


def file_exists_in_container(api_url, api_key, container_id, filename,
                              verify_ssl=True, subfolder=None):
    """Check if a file already exists in a LIBSAFE Go container.

    Returns file info dict if exists, None otherwise.
    """
    # If subfolder specified, prepend to filename for path
    if subfolder:
        full_path = '%s/%s' % (subfolder, filename)
    else:
        full_path = filename
        
    url = '%s/container/%s/file/path/%s' % (api_url, container_id, full_path)
    headers = {'Authorization': 'Bearer %s' % api_key}
    try:
        resp = requests.get(url, headers=headers, verify=verify_ssl,
                            timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success') and data.get('result'):
                return data['result']
    except Exception:
        pass
    return None


def create_folder_in_container(api_url, api_key, container_id, folder_path,
                               verify_ssl=True):
    """Create a folder in a LIBSAFE Go container.
    
    Returns True if folder was created or already exists, False otherwise.
    """
    url = '%s/container/%s/folder' % (api_url, container_id)
    headers = {'Authorization': 'Bearer %s' % api_key}
    data = {'path': folder_path}
    
    try:
        resp = requests.post(url, headers=headers, json=data,
                           verify=verify_ssl, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            return result.get('success', False)
        # Check if folder already exists by trying to access it
        check_url = '%s/container/%s/file/path/%s' % (api_url, container_id, folder_path)
        check_resp = requests.get(check_url, headers=headers, verify=verify_ssl, timeout=30)
        return check_resp.status_code == 200
    except Exception as e:
        print('  Warning: Could not create/verify folder %s: %s' % (folder_path, e))
        return False


def analyze_transfer_log(log_path):
    """Analyze the transfer log to provide detailed status information.
    
    Returns a dict with statistics about completed transfers.
    """
    stats = {
        'total_pids': set(),
        'pids_with_content': set(),
        'pids_with_metadata': set(),
        'total_files': 0,
        'successful_files': 0,
        'failed_files': 0,
        'datastream_counts': defaultdict(int)
    }
    
    if not os.path.exists(log_path):
        return stats
    
    with open(log_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get('PID', '')
            ds = row.get('Datastream', '')
            status = row.get('Status', '')
            
            if pid and ds and ds != 'SURVEY':
                stats['total_pids'].add(pid)
                stats['total_files'] += 1
                
                if status in ('OK', 'EXISTS'):
                    stats['successful_files'] += 1
                    stats['datastream_counts'][ds] += 1
                    
                    if ds.lower() == 'content':
                        stats['pids_with_content'].add(pid)
                    elif ds.lower() in ('dc', 'mods', 'rels-ext', 'rights', 'provenancemetadata'):
                        stats['pids_with_metadata'].add(pid)
                elif status.startswith('ERROR'):
                    stats['failed_files'] += 1
    
    return stats


def load_completed_pids(log_path, transfer_mode='both'):
    """Load PIDs already completed from a previous transfer log.
    
    Args:
        log_path: Path to the transfer log CSV file
        transfer_mode: 'content' for content-only, 'metadata' for metadata-only, 
                      'both' for both content and metadata
    
    Returns:
        Set of PIDs that are considered complete based on the transfer mode
    """
    # Track what datastreams were successfully transferred for each PID
    pid_datastreams = defaultdict(set)
    
    if os.path.exists(log_path):
        with open(log_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Status') in ('OK', 'EXISTS'):
                    pid = row.get('PID', '')
                    ds = row.get('Datastream', row.get('Filename', ''))
                    if pid and ds and ds != 'SURVEY':
                        pid_datastreams[pid].add(ds.lower())
    
    # Determine which PIDs are complete based on transfer mode
    done = set()
    
    # Common metadata datastreams to check
    core_metadata = {'dc', 'mods', 'rels-ext', 'rights', 'provenancemetadata'}
    
    for pid, datastreams in pid_datastreams.items():
        if transfer_mode == 'content':
            # Content-only: PID is done if content was transferred
            if 'content' in datastreams:
                done.add(pid)
                
        elif transfer_mode == 'metadata':
            # Metadata-only: PID is done if core metadata was transferred
            # Consider done if at least DC, MODS, and RELS-EXT are present
            required_metadata = {'dc', 'mods', 'rels-ext'}
            if required_metadata.issubset(datastreams):
                done.add(pid)
                
        else:  # 'both'
            # Both: PID is done if content AND core metadata were transferred
            required_metadata = {'dc', 'mods', 'rels-ext'}
            if 'content' in datastreams and required_metadata.issubset(datastreams):
                done.add(pid)
    
    return done


def main():
    parser = argparse.ArgumentParser(
        description='Transfer Disk Images and/or Metadata from Fedora to LIBSAFE Go'
    )
    parser.add_argument(
        '--fedora-url',
        default=os.environ.get('FEDORA_URL', ''),
        help='Fedora base URL (default: $FEDORA_URL)',
    )
    parser.add_argument('--fedora-user', default=FEDORA_USER_DEFAULT)
    parser.add_argument('--fedora-password', required=True)
    parser.add_argument(
        '--libsafe-api-url',
        default=os.environ.get('LIBSAFE_GO_API_URL', ''),
        help='LibSafe Go API base URL ending in /api (default: $LIBSAFE_GO_API_URL)',
    )
    parser.add_argument(
        '--libsafe-api-key',
        default=os.environ.get('LIBSAFE_GO_API_KEY', ''),
        help='LibSafe Go bearer token (default: $LIBSAFE_GO_API_KEY)',
    )
    parser.add_argument('--containers-csv', default='created_containers.csv')
    parser.add_argument('--no-ssl-verify', action='store_true')
    parser.add_argument('--skip-transfer', action='store_true',
                        help='Survey only, do not transfer files')
    parser.add_argument('--limit', type=int, default=0,
                        help='Limit number of objects to process (0 = all)')
    parser.add_argument('--temp-dir', default=None,
                        help='Directory for temp files (default: system temp)')
    parser.add_argument('-o', '--output', default='transfer_log.csv',
                        help='Transfer log CSV')
    
    # New options for metadata handling
    parser.add_argument('--metadata-only', action='store_true',
                        help='Transfer metadata datastreams only, skip content')
    parser.add_argument('--content-only', action='store_true',
                        help='Transfer content only, skip metadata (original behavior)')
    parser.add_argument('--datastreams', default=None,
                        help='Comma-separated list of datastream IDs to transfer (e.g., MODS,DC,provenanceMetadata)')
    parser.add_argument('--skip-existing-metadata', action='store_true',
                        help='Skip metadata files that already exist in LIBSAFE Go')
    parser.add_argument('--use-pid-folders', action='store_true',
                        help='Organize files in PID-named subfolders within containers')

    opts = parser.parse_args()
    if not (opts.fedora_url or '').strip():
        print('Error: set FEDORA_URL or pass --fedora-url', file=sys.stderr)
        sys.exit(1)
    if not (opts.libsafe_api_url or '').strip() or not (opts.libsafe_api_key or '').strip():
        print(
            'Error: set LIBSAFE_GO_API_URL and LIBSAFE_GO_API_KEY '
            'or pass --libsafe-api-url and --libsafe-api-key',
            file=sys.stderr,
        )
        sys.exit(1)
    fedora_url = opts.fedora_url.rstrip('/') + '/'
    libsafe_api = opts.libsafe_api_url.rstrip('/')
    libsafe_key = opts.libsafe_api_key

    # Validate options
    if opts.metadata_only and opts.content_only:
        print('Error: Cannot use both --metadata-only and --content-only', file=sys.stderr)
        sys.exit(1)
    
    # If neither specified, transfer both (backward compatibility)
    transfer_metadata = not opts.content_only
    transfer_content = not opts.metadata_only
    
    # Parse datastream list if specified
    target_datastreams = None
    if opts.datastreams:
        target_datastreams = [ds.strip() for ds in opts.datastreams.split(',')]

    ssl_ctx = ssl.create_default_context()
    if opts.no_ssl_verify:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    opener = make_opener(fedora_url, opts.fedora_user,
                         opts.fedora_password, ssl_ctx)

    verify_ssl = not opts.no_ssl_verify

    # Load container mapping (collection identifier -> LIBSAFE Go container ID)
    print('Loading container mapping from %s ...' % opts.containers_csv)
    id_to_container = build_collection_map(opts.containers_csv)
    print('  %d collection identifiers mapped' % len(id_to_container))

    # Query Fedora for all disk images
    print('Querying Fedora Resource Index ...')
    rows = risearch(fedora_url, SPARQL, opener)
    print('  Found %d disk image objects' % len(rows))

    # Map collection PIDs to container IDs
    coll_pids = set()
    pid_to_coll = {}
    for r in rows:
        pid = r['pid'].replace('info:fedora/', '')
        coll = r['coll'].replace('info:fedora/', '')
        pid_to_coll[pid] = coll
        coll_pids.add(coll)
    print('  Across %d unique collections' % len(coll_pids))

    print('Mapping collections via Fedora MODS ...')
    coll_to_container = {}
    for coll_pid in sorted(coll_pids):
        source_id = get_collection_source_id(fedora_url, coll_pid, opener)
        if source_id:
            formatted = 'Manuscript Collection No. %s' % source_id
            container_id = id_to_container.get(formatted)
            if container_id:
                coll_to_container[coll_pid] = container_id
                print('  %s -> %s -> container %s' % (
                    coll_pid, formatted, container_id))
            else:
                coll_to_container[coll_pid] = None
                print('  %s -> %s -> NOT FOUND in CSV' % (
                    coll_pid, formatted))
        else:
            coll_to_container[coll_pid] = None
            print('  %s -> no source_id' % coll_pid)

    mapped = sum(1 for v in coll_to_container.values() if v is not None)
    print('  Mapped %d / %d collections' % (mapped, len(coll_pids)))

    # Load previously completed transfers for resume
    # Determine transfer mode for resume logic
    if transfer_metadata and not transfer_content:
        transfer_mode = 'metadata'
    elif transfer_content and not transfer_metadata:
        transfer_mode = 'content'
    else:
        transfer_mode = 'both'
    
    # Analyze existing log for better resume information
    if os.path.exists(opts.output) and not opts.skip_transfer:
        print('\nAnalyzing previous transfer log for resume...')
        log_stats = analyze_transfer_log(opts.output)
        if log_stats['total_pids']:
            print('  Previous transfers:')
            print('    - Total PIDs attempted: %d' % len(log_stats['total_pids']))
            print('    - PIDs with content transferred: %d' % len(log_stats['pids_with_content']))
            print('    - PIDs with metadata transferred: %d' % len(log_stats['pids_with_metadata']))
            print('    - Total files successfully transferred: %d' % log_stats['successful_files'])
            if log_stats['failed_files'] > 0:
                print('    - Failed file transfers: %d' % log_stats['failed_files'])
    
    done_pids = load_completed_pids(opts.output, transfer_mode)
    if done_pids:
        print('  Resume: %d PIDs will be skipped (completed %s transfer)' % (
            len(done_pids), transfer_mode))

    items = rows
    if opts.limit:
        items = rows[:opts.limit]

    total_size = 0
    transferred = 0
    skipped = 0
    errors = 0
    transferred_bytes = 0
    results = []
    start_time = time.time()

    for i, row in enumerate(items):
        pid = row['pid'].replace('info:fedora/', '')
        coll_pid = pid_to_coll.get(pid, '')
        container_id = coll_to_container.get(coll_pid)

        # Resume: skip already done PIDs based on transfer mode
        if pid in done_pids and not opts.skip_transfer:
            print('[%d/%d] SKIP (already completed %s transfer) %s' % (
                i + 1, len(items), transfer_mode, pid))
            skipped += 1
            continue

        if container_id is None:
            print('[%d/%d] SKIP (unmapped) %s' % (i + 1, len(items), pid))
            skipped += 1
            results.append((pid, '', '', 0, 'UNMAPPED'))
            continue

        # Get all datastreams for this object
        all_datastreams = list_datastreams(fedora_url, pid, opener)
        
        # Filter datastreams based on options
        datastreams_to_transfer = []
        
        if transfer_metadata:
            # Get metadata datastreams (everything except 'content')
            metadata_ds = [ds for ds in all_datastreams if ds['dsid'].lower() != 'content']
            
            # Further filter if specific datastreams requested
            if target_datastreams:
                metadata_ds = [ds for ds in metadata_ds if ds['dsid'] in target_datastreams]
            
            datastreams_to_transfer.extend(metadata_ds)
        
        if transfer_content:
            # Add content datastream if it exists
            content_ds = [ds for ds in all_datastreams if ds['dsid'].lower() == 'content']
            datastreams_to_transfer.extend(content_ds)
        
        if not datastreams_to_transfer:
            print('[%d/%d] SKIP (no matching datastreams) %s' % (i + 1, len(items), pid))
            skipped += 1
            continue
        
        # Show folder info if using PID folders
        if opts.use_pid_folders:
            folder_name = pid.replace(':', '_')
            print('[%d/%d] Processing %s -> Container %s/%s/ (%d datastreams)'
                  % (i + 1, len(items), pid, container_id, folder_name, len(datastreams_to_transfer)))
        else:
            print('[%d/%d] Processing %s -> container %s (%d datastreams)'
                  % (i + 1, len(items), pid, container_id, len(datastreams_to_transfer)))
        
        if opts.skip_transfer:
            if opts.use_pid_folders:
                print('  Folder: %s/' % pid.replace(':', '_'))
            for ds in datastreams_to_transfer:
                ds_info = get_ds_info(fedora_url, pid, ds['dsid'], opener)
                indent = '    ' if opts.use_pid_folders else '  '
                print('%s- %s: %s (%s)' % (indent, ds['dsid'], 
                                           ds['label'] or 'no label', 
                                           format_size(ds_info['size'])))
            results.append((pid, 'SURVEY', container_id or '', 0, 'SURVEY'))
            continue
        
        # Determine subfolder path if using PID folders
        subfolder = pid.replace(':', '_') if opts.use_pid_folders else None
        
        # Create folder if using PID folders and not in survey mode
        if subfolder and not opts.skip_transfer:
            folder_created = create_folder_in_container(
                libsafe_api, libsafe_key, container_id, subfolder,
                verify_ssl=verify_ssl
            )
            if not folder_created:
                print('  Warning: Could not create folder %s, files may upload to root' % subfolder)
        
        # Transfer each datastream
        for ds in datastreams_to_transfer:
            dsid = ds['dsid']
            
            # Create filename for this datastream
            if dsid.lower() == 'content':
                # For content, use descriptive naming
                ds_info = get_ds_info(fedora_url, pid, dsid, opener)
                if ds_info['label']:
                    # Use the label if available
                    ds_filename = ds_info['label']
                else:
                    # Otherwise use title-based naming
                    title = get_mods_title(fedora_url, pid, opener)
                    if title:
                        safe_title = re.sub(r'[^\w\-.]', '_', title)
                        ds_filename = '%s__%s' % (pid.replace(':', '_'), safe_title)
                    else:
                        # Fall back to just PID
                        ds_filename = '%s_content' % pid.replace(':', '_')
                
                # Ensure disk images have proper extensions if not present
                if not any(ds_filename.lower().endswith(ext) for ext in 
                          ['.img', '.iso', '.dd', '.dmg', '.ima', '.image', '.bin']):
                    # Add .img as default disk image extension
                    ds_filename = '%s.img' % ds_filename
                    
            else:
                # For metadata, create descriptive filename
                extension = {
                    'MODS': '.xml',
                    'DC': '.xml', 
                    'RELS-EXT': '.rdf',
                    'Rights': '.xml',
                    'provenanceMetadata': '.xml'
                }.get(dsid, '.txt' if 'supplement' in dsid.lower() else '.bin')
                
                # Simpler naming when using PID folders (no need to repeat PID)
                if opts.use_pid_folders:
                    # For supplemental files, use their labels if available
                    if 'supplement' in dsid.lower() and ds.get('label'):
                        ds_filename = '%s%s' % (ds['label'], extension)
                    else:
                        ds_filename = '%s%s' % (dsid, extension)
                else:
                    ds_filename = '%s_%s%s' % (pid.replace(':', '_'), dsid, extension)
            
            # Check if file already exists in LIBSAFE Go
            if opts.skip_existing_metadata or (dsid.lower() == 'content'):
                existing = file_exists_in_container(
                    libsafe_api, libsafe_key, container_id, ds_filename,
                    verify_ssl=verify_ssl, subfolder=subfolder
                )
                
                ds_info = get_ds_info(fedora_url, pid, dsid, opener)
                if existing and existing.get('size', 0) == ds_info['size'] and ds_info['size'] > 0:
                    if subfolder:
                        print('  SKIP (exists): %s/%s (%s)' % (
                            subfolder, ds_filename, format_size(ds_info['size'])))
                    else:
                        print('  SKIP (exists): %s/%s (%s)' % (
                            pid, dsid, format_size(ds_info['size'])))
                    skipped += 1
                    continue
            
            tmp_path = None
            try:
                # Download from Fedora to temp file
                t0 = time.time()
                tmp_fd, tmp_path = tempfile.mkstemp(
                    dir=opts.temp_dir, prefix='fedora_%s_' % dsid)
                os.close(tmp_fd)
                
                print('  Downloading %s ...' % dsid, end='', flush=True)
                dl_bytes = download_datastream(
                    fedora_url, pid, dsid, opener, tmp_path
                )
                
                if dl_bytes == 0:
                    print(' EMPTY/ERROR')
                    if tmp_path and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                    continue
                
                dl_time = time.time() - t0
                print(' %s in %.1fs' % (format_size(dl_bytes), dl_time))
                
                # Upload to LIBSAFE Go
                t1 = time.time()
                if subfolder:
                    print('    Uploading to Container %s/%s/%s ...' % (container_id, subfolder, ds_filename), end='', flush=True)
                else:
                    print('    Uploading to Container %s/%s ...' % (container_id, ds_filename), end='', flush=True)
                    
                result = upload_to_libsafe(
                    libsafe_api, libsafe_key, container_id,
                    tmp_path, ds_filename, verify_ssl=verify_ssl,
                    subfolder=subfolder
                )
                ul_time = time.time() - t1
                print(' ✓ done in %.1fs' % ul_time)
                
                transferred_bytes += dl_bytes
                transferred += 1
                total_size += dl_bytes
                
                results.append((pid, dsid, container_id, dl_bytes, 'OK'))
                
            except Exception as e:
                print('\n    ERROR: %s' % e, file=sys.stderr)
                errors += 1
                results.append((pid, dsid, container_id or '', 0, 'ERROR: %s' % e))
                
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        
        # Print summary for this PID
        pid_transferred = len([r for r in results if r[0] == pid and r[4] == 'OK'])
        if pid_transferred > 0:
            print('  ✓ Completed %s: %d files transferred' % (pid, pid_transferred))

    # Append results to log (for resume capability)
    write_header = not os.path.exists(opts.output) or opts.skip_transfer
    mode = 'w' if opts.skip_transfer else 'a'
    with open(opts.output, mode, newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(['PID', 'Datastream', 'Container ID', 'Size', 'Status'])
        for r in results:
            w.writerow(r)

    elapsed = time.time() - start_time
    print('\n' + '=' * 60)
    print('Total objects:   %d' % len(items))
    print('Total size:      %s' % format_size(total_size))
    if not opts.skip_transfer:
        print('Transferred:     %d (%s)' % (transferred,
              format_size(transferred_bytes)))
        print('Skipped:         %d' % skipped)
        print('Errors:          %d' % errors)
        if transferred > 0:
            avg_speed = transferred_bytes / elapsed if elapsed > 0 else 0
            print('Avg speed:       %s/s' % format_size(avg_speed))
            remaining = len(items) - i - 1
            if remaining > 0 and transferred > 0:
                avg_per_file = elapsed / transferred
                print('Est remaining:   %.0f min' % (
                    remaining * avg_per_file / 60))
    print('Elapsed:         %.1f min' % (elapsed / 60))
    print('Log written to:  %s' % opts.output)


if __name__ == '__main__':
    main()
