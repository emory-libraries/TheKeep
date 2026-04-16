#!/usr/bin/env python3
"""
Efficient metadata transfer to LibSafe Go by container.
Only queries what's needed for each container.
"""

import os
import sys
import csv
import re
import ssl
import time
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
MAIN_LOG = 'metadata_transfer.csv'

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

def load_container_info():
    """Load container information from CSV."""
    containers = {}
    collections_to_containers = {}
    
    with open('created_containers.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            container_id = row['Container ID']
            identifier = row['Identifier']
            containers[container_id] = identifier
            
            # Extract source ID from identifier (e.g., "Manuscript Collection No. 1054")
            match = re.search(r'No\. (\d+)', identifier)
            if match:
                source_id = match.group(1)
                # We'll map this source_id to collection later
                collections_to_containers[source_id] = container_id
    
    return containers, collections_to_containers

def get_collection_for_container(container_id, containers, opener):
    """Find the collection PID for a given container."""
    identifier = containers.get(str(container_id))
    if not identifier:
        return None
    
    # Extract source ID
    match = re.search(r'No\. (\d+)', identifier)
    if not match:
        return None
    
    source_id = match.group(1)
    
    # Query for collection with this source ID
    # First get all collections with disk images (limited query)
    sparql = '''
    select distinct ?coll where {
      ?pid <info:fedora/fedora-system:def/model#hasModel> <info:fedora/emory-control:DiskImage-1.0> .
      ?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> ?coll
    } LIMIT 200
    '''
    
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'query': sparql,
    })
    
    resp = opener.open(Request(f'{_fedora_url()}risearch?{params}'))
    lines = resp.read().decode('utf-8').strip().split('\n')
    collections = [line.replace('info:fedora/', '') for line in lines[1:]]
    
    # Check each collection for matching source ID
    for coll_pid in collections:
        try:
            url = f'{_fedora_url()}objects/{coll_pid}/datastreams/MODS/content'
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            m = re.search(r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>', xml)
            
            if m and m.group(1) == source_id:
                return coll_pid
        except:
            continue
    
    return None

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

def transfer_pid_metadata(pid, container_id, opener):
    """Transfer metadata for a single PID."""
    folder_name = pid.replace(':', '_')
    transferred = 0
    skipped = 0
    failed = 0
    
    try:
        # Get all datastreams
        url = f'{_fedora_url()}objects/{pid}/datastreams?format=xml'
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        dsids = re.findall(r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',xml)
        
        # Filter to metadata only
        metadata_ds = [ds for ds in dsids if ds.lower() != 'content']
        
        for dsid in metadata_ds:
            # Determine filename
            ext_map = {
                'DC': '.xml', 'MODS': '.xml', 'RELS-EXT': '.rdf',
                'Rights': '.xml', 'provenanceMetadata': '.xml'
            }
            
            if 'supplement' in dsid.lower():
                # Get label for supplement files
                try:
                    ds_url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}?format=xml'
                    ds_resp = opener.open(Request(ds_url))
                    ds_xml = ds_resp.read().decode('utf-8')
                    label_m = re.search(r'<dsLabel>([^<]*)</dsLabel>', ds_xml)
                    if label_m and label_m.group(1):
                        filename = f"{label_m.group(1)}.txt"
                    else:
                        filename = f"{dsid}.txt"
                except:
                    filename = f"{dsid}.txt"
            else:
                filename = f"{dsid}{ext_map.get(dsid, '')}"
            
            # Check if exists
            headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}
            check_url = f'{_libsafe_api_url()}/container/{container_id}/file/path/{folder_name}/{filename}'
            
            try:
                check_resp = requests.get(check_url, headers=headers, verify=False, timeout=5)
                if check_resp.status_code == 200:
                    data = check_resp.json()
                    if data.get('success') and data.get('result', {}).get('size', 0) > 0:
                        skipped += 1
                        continue
            except:
                pass
            
            # Download and upload
            try:
                # Download
                content_url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}/content'
                content_resp = opener.open(Request(content_url))
                content = content_resp.read()
                
                # Upload
                upload_url = f'{_libsafe_api_url()}/container/{container_id}/file/upload'
                data = {'fileName': filename, 'chunkIndex': 0, 'path': folder_name}
                files = {'file': (filename, content, 'application/octet-stream')}
                
                upload_resp = requests.post(upload_url, headers=headers, data=data, 
                                          files=files, verify=False, timeout=30)
                
                if upload_resp.status_code in [200, 201]:
                    transferred += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
    
    except Exception as e:
        failed = 1
    
    return transferred, skipped, failed

def process_container(container_id, opener):
    """Process a single container."""
    print(f"\n{'='*70}")
    print(f"Processing Container {container_id}")
    print(f"{'='*70}")
    
    # Load container info
    containers, _ = load_container_info()
    
    # Find collection for this container
    print("Finding collection for this container...")
    coll_pid = get_collection_for_container(container_id, containers, opener)
    
    if not coll_pid:
        print(f"ERROR: Could not find collection for container {container_id}")
        return False
    
    print(f"Collection: {coll_pid}")
    print(f"Container name: {containers.get(str(container_id))}")
    
    # Get PIDs for this collection
    print("Getting PIDs...")
    pids = get_collection_pids(coll_pid, opener)
    print(f"Found {len(pids)} PIDs")
    
    if not pids:
        print("No PIDs to process")
        return True
    
    # Process each PID
    total_transferred = 0
    total_skipped = 0
    total_failed = 0
    
    for i, pid in enumerate(pids, 1):
        print(f"  [{i}/{len(pids)}] {pid}: ", end='', flush=True)
        
        transferred, skipped, failed = transfer_pid_metadata(pid, container_id, opener)
        
        total_transferred += transferred
        total_skipped += skipped
        total_failed += failed
        
        # Print summary
        parts = []
        if transferred > 0:
            parts.append(f"✓ {transferred} transferred")
        if skipped > 0:
            parts.append(f"{skipped} skipped")
        if failed > 0:
            parts.append(f"✗ {failed} failed")
        
        print(", ".join(parts) if parts else "no metadata")
        
        # Log to CSV
        with open(MAIN_LOG, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([container_id, coll_pid, pid, transferred, skipped, failed])
    
    print(f"\nContainer {container_id} complete:")
    print(f"  Files transferred: {total_transferred}")
    print(f"  Files skipped: {total_skipped}")
    print(f"  Files failed: {total_failed}")
    
    return True

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Efficient metadata transfer to LibSafe Go')
    parser.add_argument('container_ids', nargs='+', type=int,
                       help='Container IDs to process')
    parser.add_argument('--all', action='store_true',
                       help='Process all containers')
    
    args = parser.parse_args()
    
    print("EFFICIENT METADATA TRANSFER TO LIBSAFE GO")
    print("="*70)
    
    # Set up connection
    opener = setup_fedora_connection()
    
    # Initialize log
    if not os.path.exists(MAIN_LOG):
        with open(MAIN_LOG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Container ID', 'Collection', 'PID', 'Transferred', 'Skipped', 'Failed'])
    
    # Process containers
    if args.all:
        containers, _ = load_container_info()
        container_ids = sorted([int(cid) for cid in containers.keys()])
    else:
        container_ids = args.container_ids
    
    print(f"Will process {len(container_ids)} container(s)")
    
    start_time = time.time()
    
    for container_id in container_ids:
        try:
            success = process_container(container_id, opener)
            if not success:
                print(f"Warning: Container {container_id} had issues")
        except Exception as e:
            print(f"ERROR processing container {container_id}: {e}")
    
    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"TRANSFER COMPLETE")
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Log file: {MAIN_LOG}")

if __name__ == '__main__':
    main()