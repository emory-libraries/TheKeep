#!/usr/bin/env python3
"""
Transfer metadata to LibSafe Go by processing one container at a time.
This avoids the hanging issue by querying only PIDs for each specific collection.
"""

import os
import sys
import csv
import re
import ssl
import time
import tempfile
from urllib.request import Request, urlopen, HTTPBasicAuthHandler, HTTPSHandler, build_opener
from urllib.parse import urlencode
import requests
import urllib3
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings()


def _require_env(name):
    v = (os.environ.get(name) or '').strip()
    if not v:
        sys.exit('Missing required environment variable: %s' % name)
    return v


def _fedora_url():
    u = _require_env('FEDORA_URL')
    return u.rstrip('/') + '/'


def _fedora_user():
    return os.environ.get('FEDORA_USER', 'keep')


def _fedora_password():
    return _require_env('FEDORA_PASSWORD')


def _libsafe_api_url():
    return _require_env('LIBSAFE_GO_API_URL').rstrip('/')


def _libsafe_api_key():
    return _require_env('LIBSAFE_GO_API_KEY')


# Output files
MAIN_LOG = 'all_containers_transfer.csv'
PROGRESS_LOG = 'transfer_progress.log'

def setup_fedora_connection():
    """Set up authenticated connection to Fedora."""
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    auth = HTTPBasicAuthHandler()
    auth.add_password(
        'Fedora Repository Server',
        _fedora_url(),
        _fedora_user(),
        _fedora_password(),
    )
    opener = build_opener(auth, HTTPSHandler(context=ssl_ctx))
    
    return opener

def log_progress(message):
    """Log progress with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(PROGRESS_LOG, 'a') as f:
        f.write(log_line + '\n')
    sys.stdout.flush()

def get_collection_mapping(opener):
    """Get all collections and their container mappings."""
    log_progress("Loading collection to container mappings...")
    
    # Load container mapping from CSV
    containers = {}
    with open('created_containers.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            containers[row['Identifier']] = row['Container ID']
    
    # Get all unique collections with disk images
    log_progress("Querying for all unique collections...")
    sparql = '''
    select distinct ?coll where {
      ?pid <info:fedora/fedora-system:def/model#hasModel> <info:fedora/emory-control:DiskImage-1.0> .
      ?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> ?coll
    }
    '''
    
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'query': sparql,
    })
    
    resp = opener.open(Request(f'{_fedora_url()}risearch?{params}'))
    lines = resp.read().decode('utf-8').strip().split('\n')
    collections = [line.replace('info:fedora/', '') for line in lines[1:]]
    
    log_progress(f"Found {len(collections)} collections with disk images")
    
    # Map collections to containers
    collection_container_map = {}
    for coll_pid in collections:
        try:
            # Get source ID from MODS
            url = f'{_fedora_url()}objects/{coll_pid}/datastreams/MODS/content'
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            m = re.search(r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>', xml)
            
            if m:
                source_id = m.group(1)
                container_key = f'Manuscript Collection No. {source_id}'
                if container_key in containers:
                    collection_container_map[coll_pid] = {
                        'container_id': containers[container_key],
                        'source_id': source_id,
                        'name': container_key
                    }
        except Exception as e:
            log_progress(f"  Warning: Could not map {coll_pid}: {e}")
    
    log_progress(f"Successfully mapped {len(collection_container_map)} collections to containers")
    return collection_container_map

def get_collection_pids(coll_pid, opener):
    """Get all disk image PIDs for a specific collection."""
    sparql = f'''
    select ?pid where {{
      ?pid <info:fedora/fedora-system:def/model#hasModel> <info:fedora/emory-control:DiskImage-1.0> .
      ?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> <info:fedora/{coll_pid}>
    }}
    '''
    
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'query': sparql,
    })
    
    resp = opener.open(Request(f'{_fedora_url()}risearch?{params}'))
    lines = resp.read().decode('utf-8').strip().split('\n')
    return [line.replace('info:fedora/', '') for line in lines[1:]]

def list_datastreams(pid, opener):
    """List all datastreams for a PID."""
    url = f'{_fedora_url()}objects/{pid}/datastreams?format=xml'
    resp = opener.open(Request(url))
    xml = resp.read().decode('utf-8')
    # Parse datastream IDs
    dsids = re.findall(r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',xml)
    return dsids

def download_datastream(pid, dsid, opener):
    """Download a datastream's content."""
    url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}/content'
    resp = opener.open(Request(url))
    return resp.read()

def file_exists_in_container(container_id, filename, subfolder=None):
    """Check if a file already exists in LibSafe Go."""
    headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}

    if subfolder:
        full_path = f'{subfolder}/{filename}'
    else:
        full_path = filename

    url = f'{_libsafe_api_url()}/container/{container_id}/file/path/{full_path}'
    
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('success', False) and data.get('result', {}).get('size', 0) > 0
    except:
        pass
    return False

def upload_to_libsafe(container_id, content, filename, subfolder=None):
    """Upload content to LibSafe Go."""
    headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}
    url = f'{_libsafe_api_url()}/container/{container_id}/file/upload'
    
    data = {'fileName': filename, 'chunkIndex': 0}
    if subfolder:
        data['path'] = subfolder
    
    files = {'file': (filename, content, 'application/octet-stream')}
    
    try:
        resp = requests.post(url, headers=headers, data=data, files=files, verify=False, timeout=30)
        return resp.status_code in [200, 201]
    except Exception as e:
        log_progress(f"    Upload error: {e}")
        return False

def transfer_pid_metadata(pid, container_id, opener, skip_existing=True):
    """Transfer all metadata for a single PID."""
    folder_name = pid.replace(':', '_')
    results = []
    
    try:
        # Get all datastreams
        dsids = list_datastreams(pid, opener)
        
        # Filter to metadata only (skip 'content')
        metadata_ds = [ds for ds in dsids if ds.lower() != 'content']
        
        transferred = 0
        skipped = 0
        failed = 0
        
        for dsid in metadata_ds:
            # Determine filename
            ext_map = {
                'DC': '.xml', 'MODS': '.xml', 'RELS-EXT': '.rdf',
                'Rights': '.xml', 'provenanceMetadata': '.xml'
            }
            
            # Handle supplement files specially
            if 'supplement' in dsid.lower():
                # Try to get the label from Fedora
                try:
                    url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}?format=xml'
                    resp = opener.open(Request(url))
                    xml = resp.read().decode('utf-8')
                    label_m = re.search(r'<dsLabel>([^<]*)</dsLabel>', xml)
                    if label_m and label_m.group(1):
                        filename = f"{label_m.group(1)}.txt"
                    else:
                        filename = f"{dsid}.txt"
                except:
                    filename = f"{dsid}.txt"
            else:
                filename = f"{dsid}{ext_map.get(dsid, '')}"
            
            # Check if exists
            if skip_existing and file_exists_in_container(container_id, filename, folder_name):
                skipped += 1
                results.append((pid, dsid, 'skipped', 0))
                continue
            
            # Download and upload
            try:
                content = download_datastream(pid, dsid, opener)
                
                if upload_to_libsafe(container_id, content, filename, folder_name):
                    transferred += 1
                    results.append((pid, dsid, 'success', len(content)))
                else:
                    failed += 1
                    results.append((pid, dsid, 'failed', len(content)))
                    
            except Exception as e:
                failed += 1
                results.append((pid, dsid, f'error: {e}', 0))
        
        return {
            'transferred': transferred,
            'skipped': skipped,
            'failed': failed,
            'total': len(metadata_ds),
            'results': results
        }
        
    except Exception as e:
        return {
            'transferred': 0,
            'skipped': 0,
            'failed': 1,
            'total': 0,
            'results': [(pid, 'ALL', f'error: {e}', 0)]
        }

def process_container(coll_pid, container_info, opener, skip_existing=True):
    """Process all PIDs for a single container."""
    container_id = container_info['container_id']
    container_name = container_info['name']
    
    log_progress(f"\n{'='*70}")
    log_progress(f"Processing Container {container_id}: {container_name}")
    log_progress(f"Collection: {coll_pid}")
    
    # Get PIDs for this collection
    pids = get_collection_pids(coll_pid, opener)
    log_progress(f"Found {len(pids)} PIDs to process")
    
    if not pids:
        return {
            'container_id': container_id,
            'collection': coll_pid,
            'total_pids': 0,
            'transferred_files': 0,
            'skipped_files': 0,
            'failed_files': 0
        }
    
    # Process each PID
    container_stats = {
        'container_id': container_id,
        'collection': coll_pid,
        'total_pids': len(pids),
        'transferred_files': 0,
        'skipped_files': 0,
        'failed_files': 0
    }
    
    for i, pid in enumerate(pids, 1):
        print(f"  [{i}/{len(pids)}] {pid}: ", end='', flush=True)
        
        result = transfer_pid_metadata(pid, container_id, opener, skip_existing)
        
        container_stats['transferred_files'] += result['transferred']
        container_stats['skipped_files'] += result['skipped']
        container_stats['failed_files'] += result['failed']
        
        # Write individual results to detailed log
        with open(MAIN_LOG, 'a', newline='') as f:
            writer = csv.writer(f)
            for r in result['results']:
                writer.writerow([container_id, coll_pid, r[0], r[1], r[2], r[3]])
        
        # Print summary for this PID
        if result['transferred'] > 0:
            print(f"✓ {result['transferred']} transferred", end='')
        if result['skipped'] > 0:
            print(f", {result['skipped']} skipped", end='')
        if result['failed'] > 0:
            print(f", {result['failed']} failed", end='')
        print()
    
    log_progress(f"Container {container_id} complete: {container_stats['transferred_files']} transferred, "
                 f"{container_stats['skipped_files']} skipped, {container_stats['failed_files']} failed")
    
    return container_stats

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Transfer metadata to LibSafe Go by container')
    parser.add_argument('--start-container', type=int, help='Start from specific container ID')
    parser.add_argument('--single-container', type=int, help='Process only this container ID')
    parser.add_argument('--skip-existing', action='store_true', default=True,
                       help='Skip files that already exist (default: True)')
    parser.add_argument('--limit', type=int, help='Process only N containers')
    
    args = parser.parse_args()
    
    # Initialize logs
    if not args.start_container and not args.single_container:
        # Starting fresh - create new logs
        with open(MAIN_LOG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Container ID', 'Collection', 'PID', 'Datastream', 'Status', 'Size'])
        
        with open(PROGRESS_LOG, 'w') as f:
            f.write(f"Transfer started at {datetime.now()}\n")
    
    log_progress("="*70)
    log_progress("METADATA TRANSFER TO LIBSAFE GO - BY CONTAINER")
    log_progress("="*70)
    
    # Set up connection
    opener = setup_fedora_connection()
    
    # Get all collection->container mappings
    collection_map = get_collection_mapping(opener)
    
    # Sort by container ID for consistent processing
    sorted_collections = sorted(collection_map.items(), 
                               key=lambda x: int(x[1]['container_id']))
    
    # Filter based on arguments
    if args.single_container:
        sorted_collections = [(c, info) for c, info in sorted_collections 
                             if int(info['container_id']) == args.single_container]
        log_progress(f"Processing only container {args.single_container}")
    elif args.start_container:
        sorted_collections = [(c, info) for c, info in sorted_collections 
                             if int(info['container_id']) >= args.start_container]
        log_progress(f"Starting from container {args.start_container}")
    
    if args.limit:
        sorted_collections = sorted_collections[:args.limit]
        log_progress(f"Limiting to {args.limit} containers")
    
    log_progress(f"Will process {len(sorted_collections)} containers")
    
    # Track overall statistics
    overall_stats = {
        'containers_processed': 0,
        'total_pids': 0,
        'total_transferred': 0,
        'total_skipped': 0,
        'total_failed': 0
    }
    
    start_time = time.time()
    
    # Process each container
    for coll_pid, container_info in sorted_collections:
        try:
            stats = process_container(coll_pid, container_info, opener, args.skip_existing)
            
            overall_stats['containers_processed'] += 1
            overall_stats['total_pids'] += stats['total_pids']
            overall_stats['total_transferred'] += stats['transferred_files']
            overall_stats['total_skipped'] += stats['skipped_files']
            overall_stats['total_failed'] += stats['failed_files']
            
        except Exception as e:
            log_progress(f"ERROR processing container {container_info['container_id']}: {e}")
            continue
        
        # Show running totals
        elapsed = time.time() - start_time
        log_progress(f"Running totals: {overall_stats['containers_processed']} containers, "
                    f"{overall_stats['total_pids']} PIDs, "
                    f"{overall_stats['total_transferred']} files transferred "
                    f"(elapsed: {elapsed/60:.1f} minutes)")
    
    # Final summary
    elapsed = time.time() - start_time
    log_progress("\n" + "="*70)
    log_progress("TRANSFER COMPLETE")
    log_progress("="*70)
    log_progress(f"Containers processed: {overall_stats['containers_processed']}")
    log_progress(f"Total PIDs:          {overall_stats['total_pids']}")
    log_progress(f"Files transferred:   {overall_stats['total_transferred']}")
    log_progress(f"Files skipped:       {overall_stats['total_skipped']}")
    log_progress(f"Files failed:        {overall_stats['total_failed']}")
    log_progress(f"Total time:          {elapsed/60:.1f} minutes")
    log_progress(f"Details logged to:   {MAIN_LOG}")

if __name__ == '__main__':
    main()