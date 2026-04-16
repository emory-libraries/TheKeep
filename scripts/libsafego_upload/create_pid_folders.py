#!/usr/bin/env python3
"""
Create PID-based folder structure in LibSafe Go containers for all disk images.

This script:
1. Queries Fedora for all disk images and their collection memberships
2. Maps collections to LibSafe Go containers
3. Creates PID-named folders in the appropriate containers

Usage:
    python create_pid_folders.py
    python create_pid_folders.py --limit 10  # Process only first 10 PIDs
    python create_pid_folders.py --container 194  # Process only specific container
    python create_pid_folders.py --dry-run  # Show what would be created without doing it
"""

import argparse
import csv
import os
import re
import ssl
import sys
from collections import defaultdict
from urllib.request import Request, urlopen, HTTPBasicAuthHandler, HTTPSHandler, build_opener
from urllib.parse import urlencode
import requests
import urllib3

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


def get_collection_source_id(coll_pid, opener):
    """Get the source ID for a collection from its MODS record."""
    try:
        url = f'{_fedora_url()}objects/{coll_pid}/datastreams/MODS/content'
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        
        # Extract source_id from MODS
        m = re.search(r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>', xml)
        if m:
            return m.group(1)
    except Exception as e:
        print(f'  Warning: Could not get source ID for {coll_pid}: {e}')
    return None

def load_container_mapping():
    """Load the collection->container mapping from CSV."""
    containers = {}
    try:
        with open('created_containers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Map "Manuscript Collection No. XXX" to container ID
                containers[row['Identifier']] = row['Container ID']
    except Exception as e:
        print(f'Error loading container mapping: {e}')
        sys.exit(1)
    
    return containers

def create_folder_in_container(api_url, api_key, container_id, folder_path, verify_ssl=True):
    """Create a folder in a LibSafe Go container."""
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{api_url}/container/{container_id}/folder'
    
    try:
        resp = requests.post(url, headers=headers, json={'path': folder_path}, 
                           verify=verify_ssl, timeout=30)
        if resp.status_code in [200, 201]:
            return True, 'created'
        elif resp.status_code == 409:
            return True, 'exists'
        else:
            return False, f'HTTP {resp.status_code}'
    except Exception as e:
        return False, str(e)

def folder_exists_in_container(api_url, api_key, container_id, folder_path, verify_ssl=True):
    """Check if a folder exists in a container."""
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{api_url}/container/{container_id}/file/path/{folder_path}'
    
    try:
        resp = requests.get(url, headers=headers, verify=verify_ssl, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('success', False)
    except:
        pass
    return False

def main():
    parser = argparse.ArgumentParser(description='Create PID folders in LibSafe Go containers')
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit number of PIDs to process')
    parser.add_argument('--container', type=int, default=None,
                        help='Process only this container ID')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be created without actually creating')
    parser.add_argument('--no-ssl-verify', action='store_true',
                        help='Disable SSL verification for LibSafe Go API')
    parser.add_argument('--output', default='pid_folders_created.csv',
                        help='Output CSV log file')
    
    args = parser.parse_args()
    
    verify_ssl = not args.no_ssl_verify
    
    # Set up Fedora connection
    print("Setting up Fedora connection...")
    opener = setup_fedora_connection()
    
    # Load container mapping
    print("Loading container mapping...")
    containers = load_container_mapping()
    print(f"  Loaded {len(containers)} container mappings")
    
    # Query for all disk images
    print("Querying Fedora for disk images...")
    sparql = '''
    select ?pid ?coll where {
      ?pid <info:fedora/fedora-system:def/model#hasModel> <info:fedora/emory-control:DiskImage-1.0> .
      ?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> ?coll
    }
    '''
    
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'limit': args.limit or 100000, 'query': sparql,
    })
    
    resp = opener.open(Request(f'{_fedora_url()}risearch?{params}'))
    lines = resp.read().decode('utf-8').strip().split('\n')
    headers = [h.strip('"') for h in lines[0].split(',')]
    rows = [dict(zip(headers, l.split(','))) for l in lines[1:]]
    
    print(f"  Found {len(rows)} disk images")
    
    # Group PIDs by collection
    collection_pids = defaultdict(list)
    for row in rows:
        pid = row['pid'].replace('info:fedora/', '')
        coll = row['coll'].replace('info:fedora/', '')
        collection_pids[coll].append(pid)
    
    print(f"  Organized into {len(collection_pids)} collections")
    
    # Map collections to containers
    print("\nMapping collections to containers...")
    collection_containers = {}
    unmapped = []
    
    for coll in collection_pids.keys():
        source_id = get_collection_source_id(coll, opener)
        if source_id:
            container_key = f'Manuscript Collection No. {source_id}'
            if container_key in containers:
                collection_containers[coll] = {
                    'container_id': containers[container_key],
                    'source_id': source_id,
                    'pids': collection_pids[coll]
                }
            else:
                unmapped.append(coll)
        else:
            unmapped.append(coll)
    
    print(f"  Mapped {len(collection_containers)} collections to containers")
    if unmapped:
        print(f"  Could not map {len(unmapped)} collections: {', '.join(unmapped[:5])}")
    
    # Process containers
    print("\n" + "=" * 70)
    print("Creating PID folders in containers...")
    print("=" * 70)
    
    with open(args.output, 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['Container ID', 'Collection', 'PID', 'Folder', 'Status', 'Message'])
        
        stats = {
            'containers_processed': 0,
            'folders_created': 0,
            'folders_existed': 0,
            'folders_failed': 0,
            'folders_skipped': 0
        }
        
        total_pids = sum(len(info['pids']) for info in collection_containers.values())
        processed_pids = 0
        
        for coll, info in sorted(collection_containers.items()):
            container_id = info['container_id']
            source_id = info['source_id']
            pids = info['pids']
            
            # Skip if specific container requested and this isn't it
            if args.container and int(container_id) != args.container:
                continue
            
            print(f"\nContainer {container_id} (Collection {coll}, {len(pids)} PIDs):")
            stats['containers_processed'] += 1
            
            for i, pid in enumerate(pids, 1):
                folder_name = pid.replace(':', '_')
                
                if args.dry_run:
                    # Check if exists but don't create
                    exists = folder_exists_in_container(
                        _libsafe_api_url(), _libsafe_api_key(), container_id, folder_name, verify_ssl
                    )
                    if exists:
                        status = 'exists'
                        print(f"  [{container_id}] {folder_name}: would skip (exists)")
                        stats['folders_existed'] += 1
                    else:
                        status = 'would_create'
                        print(f"  [{container_id}] {folder_name}: would create")
                        stats['folders_skipped'] += 1
                    writer.writerow([container_id, coll, pid, folder_name, status, 'dry run'])
                else:
                    # Actually create the folder
                    success, message = create_folder_in_container(
                        _libsafe_api_url(), _libsafe_api_key(), container_id, folder_name, verify_ssl
                    )
                    
                    if success:
                        if message == 'created':
                            print(f"  [{container_id}] ({i}/{len(pids)}) {folder_name}: ✓ created")
                            stats['folders_created'] += 1
                            status = 'created'
                        else:
                            print(f"  [{container_id}] ({i}/{len(pids)}) {folder_name}: - already exists")
                            stats['folders_existed'] += 1
                            status = 'exists'
                    else:
                        print(f"  [{container_id}] ({i}/{len(pids)}) {folder_name}: ✗ failed ({message})")
                        stats['folders_failed'] += 1
                        status = 'failed'
                    
                    writer.writerow([container_id, coll, pid, folder_name, status, message])
                    
                # Flush output for real-time monitoring
                sys.stdout.flush()
                csvf.flush()
            
            # Progress summary after each container
            processed_pids += len(pids)
            print(f"  Container {container_id} complete. Progress: {processed_pids}/{total_pids} PIDs processed")
            print(f"  Running totals - Created: {stats['folders_created']}, Existed: {stats['folders_existed']}, Failed: {stats['folders_failed']}")
            sys.stdout.flush()
    
    # Print summary
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print(f"Containers processed: {stats['containers_processed']}")
    print(f"Folders created:      {stats['folders_created']}")
    print(f"Folders existed:      {stats['folders_existed']}")
    print(f"Folders failed:       {stats['folders_failed']}")
    if args.dry_run:
        print(f"Folders skipped:      {stats['folders_skipped']} (dry run)")
    print(f"\nLog written to: {args.output}")

if __name__ == '__main__':
    main()