#!/usr/bin/env python3
"""
Transfer metadata for all containers to LibSafe Go.
Processes each container individually to avoid hanging issues.
"""

import os
import sys
import csv
import re
import ssl
import time
import json
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


# Files for tracking progress
PROGRESS_FILE = 'container_transfer_progress.json'
LOG_FILE = 'container_transfer.log'
DETAIL_LOG = 'container_transfer_details.csv'

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

def log(message, level='INFO'):
    """Log message to console and file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')
    sys.stdout.flush()

def load_progress():
    """Load progress from file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'completed_containers': [], 'failed_containers': {}, 'stats': {}}

def save_progress(progress):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_all_container_mappings():
    """Get all container to collection mappings."""
    log("Loading container mappings...")
    
    # First, load all containers from CSV
    containers = {}
    with open('created_containers.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            container_id = row['Container ID']
            identifier = row['Identifier']
            containers[container_id] = identifier
    
    log(f"Loaded {len(containers)} containers from CSV")
    
    # Now we need to map each container to its collection
    # We'll do this by getting all collections and matching source IDs
    opener = setup_fedora_connection()
    
    # Get all collections with disk images
    log("Getting all collections with disk images...")
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
    
    log(f"Found {len(collections)} collections with disk images")
    
    # Map collections to containers
    container_mappings = {}
    
    for coll_pid in collections:
        try:
            # Get source ID from MODS
            url = f'{_fedora_url()}objects/{coll_pid}/datastreams/MODS/content'
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            m = re.search(r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>', xml)
            
            if m:
                source_id = m.group(1)
                # Find matching container
                for container_id, identifier in containers.items():
                    if f'No. {source_id}' in identifier:
                        container_mappings[container_id] = {
                            'collection': coll_pid,
                            'name': identifier,
                            'source_id': source_id
                        }
                        break
        except Exception as e:
            log(f"Warning: Could not get source ID for {coll_pid}: {e}", 'WARN')
    
    log(f"Successfully mapped {len(container_mappings)} containers to collections")
    return container_mappings

def get_pids_for_collection(coll_pid, opener):
    """Get all PIDs for a collection."""
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
    transferred = []
    skipped = []
    failed = []
    
    try:
        # Get all datastreams
        url = f'{_fedora_url()}objects/{pid}/datastreams?format=xml'
        resp = opener.open(Request(url), timeout=10)
        xml = resp.read().decode('utf-8')
        dsids = re.findall(r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',xml)
        
        # Filter to metadata only
        metadata_ds = [ds for ds in dsids if ds.lower() != 'content']
        
        headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}
        
        for dsid in metadata_ds:
            # Determine filename
            ext_map = {
                'DC': '.xml', 'MODS': '.xml', 'RELS-EXT': '.rdf',
                'Rights': '.xml', 'provenanceMetadata': '.xml'
            }
            
            if 'supplement' in dsid.lower():
                try:
                    ds_url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}?format=xml'
                    ds_resp = opener.open(Request(ds_url), timeout=5)
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
            check_url = f'{_libsafe_api_url()}/container/{container_id}/file/path/{folder_name}/{filename}'
            
            try:
                check_resp = requests.get(check_url, headers=headers, verify=False, timeout=5)
                if check_resp.status_code == 200:
                    data = check_resp.json()
                    if data.get('success') and data.get('result', {}).get('size', 0) > 0:
                        skipped.append(dsid)
                        continue
            except:
                pass
            
            # Download and upload
            try:
                # Download with timeout
                content_url = f'{_fedora_url()}objects/{pid}/datastreams/{dsid}/content'
                content_resp = opener.open(Request(content_url), timeout=30)
                content = content_resp.read()
                
                # Upload with timeout
                upload_url = f'{_libsafe_api_url()}/container/{container_id}/file/upload'
                data = {'fileName': filename, 'chunkIndex': 0, 'path': folder_name}
                files = {'file': (filename, content, 'application/octet-stream')}
                
                upload_resp = requests.post(upload_url, headers=headers, data=data, 
                                          files=files, verify=False, timeout=30)
                
                if upload_resp.status_code in [200, 201]:
                    transferred.append(dsid)
                else:
                    failed.append(dsid)
                    
            except Exception as e:
                failed.append(f"{dsid}:{str(e)[:50]}")
    
    except Exception as e:
        failed.append(f"ERROR:{str(e)[:50]}")
    
    return len(transferred), len(skipped), len(failed)

def process_container(container_id, container_info, opener, progress):
    """Process a single container."""
    collection = container_info['collection']
    name = container_info['name']
    
    log(f"\nProcessing Container {container_id}: {name}")
    log(f"  Collection: {collection}")
    
    # Get PIDs for this collection
    try:
        pids = get_pids_for_collection(collection, opener)
        log(f"  Found {len(pids)} PIDs")
        
        if not pids:
            log(f"  No PIDs to process", 'WARN')
            return True
        
        # Process each PID
        container_stats = {
            'total_pids': len(pids),
            'transferred_files': 0,
            'skipped_files': 0,
            'failed_files': 0
        }
        
        for i, pid in enumerate(pids, 1):
            # Always show progress for better visibility
            print(f"    [{i}/{len(pids)}] {pid}: ", end='', flush=True)
            
            transferred, skipped, failed = transfer_pid_metadata(pid, container_id, opener)
            
            container_stats['transferred_files'] += transferred
            container_stats['skipped_files'] += skipped
            container_stats['failed_files'] += failed
            
            # Log to CSV
            with open(DETAIL_LOG, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([container_id, collection, pid, transferred, skipped, failed])
            
            # Show inline progress
            parts = []
            if transferred > 0:
                parts.append(f"✓ {transferred}")
            if skipped > 0:
                parts.append(f"↷ {skipped}")
            if failed > 0:
                parts.append(f"✗ {failed}")
            print(" ".join(parts) if parts else "no metadata")
        
        log(f"  Container {container_id} complete: "
            f"{container_stats['transferred_files']} transferred, "
            f"{container_stats['skipped_files']} skipped, "
            f"{container_stats['failed_files']} failed")
        
        # Update progress
        progress['stats'][container_id] = container_stats
        
        return True
        
    except Exception as e:
        log(f"  ERROR processing container {container_id}: {e}", 'ERROR')
        return False

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Transfer metadata for all containers')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from last successful container')
    parser.add_argument('--start-from', type=int,
                       help='Start from specific container ID')
    parser.add_argument('--limit', type=int,
                       help='Process only N containers')
    parser.add_argument('--skip-194', action='store_true',
                       help='Skip container 194 (already done)')
    
    args = parser.parse_args()
    
    log("="*70)
    log("METADATA TRANSFER FOR ALL CONTAINERS")
    log("="*70)
    
    # Load progress
    progress = load_progress() if args.resume else {
        'completed_containers': [],
        'failed_containers': {},
        'stats': {}
    }
    
    # Initialize detail log
    if not args.resume and not os.path.exists(DETAIL_LOG):
        with open(DETAIL_LOG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Container ID', 'Collection', 'PID', 'Transferred', 'Skipped', 'Failed'])
    
    # Get all container mappings
    container_mappings = get_all_container_mappings()
    
    # Sort by container ID
    sorted_containers = sorted(container_mappings.items(), key=lambda x: int(x[0]))
    
    # Filter based on arguments
    if args.skip_194 or 194 in progress.get('completed_containers', []):
        sorted_containers = [(cid, info) for cid, info in sorted_containers if cid != '194']
        log("Skipping container 194 (already completed)")
    
    if args.resume:
        completed = set(map(str, progress.get('completed_containers', [])))
        sorted_containers = [(cid, info) for cid, info in sorted_containers if cid not in completed]
        log(f"Resuming: {len(completed)} containers already completed")
    
    if args.start_from:
        sorted_containers = [(cid, info) for cid, info in sorted_containers 
                           if int(cid) >= args.start_from]
        log(f"Starting from container {args.start_from}")
    
    if args.limit:
        sorted_containers = sorted_containers[:args.limit]
        log(f"Limiting to {args.limit} containers")
    
    log(f"Will process {len(sorted_containers)} containers")
    
    # Set up Fedora connection
    opener = setup_fedora_connection()
    
    # Process each container
    start_time = time.time()
    successful = 0
    failed = 0
    
    for container_id, container_info in sorted_containers:
        try:
            success = process_container(container_id, container_info, opener, progress)
            
            if success:
                successful += 1
                progress['completed_containers'].append(int(container_id))
            else:
                failed += 1
                progress['failed_containers'][container_id] = "Processing failed"
            
            # Save progress after each container
            save_progress(progress)
            
            # Show overall progress
            elapsed = time.time() - start_time
            rate = successful / (elapsed / 60) if elapsed > 0 else 0
            remaining = len(sorted_containers) - (successful + failed)
            eta = remaining / rate if rate > 0 else 0
            
            log(f"Progress: {successful} successful, {failed} failed, {remaining} remaining "
                f"(Rate: {rate:.1f} containers/min, ETA: {eta:.1f} min)")
            
        except KeyboardInterrupt:
            log("\nTransfer interrupted by user", 'WARN')
            save_progress(progress)
            break
        except Exception as e:
            log(f"Unexpected error with container {container_id}: {e}", 'ERROR')
            failed += 1
            progress['failed_containers'][container_id] = str(e)
            save_progress(progress)
    
    # Final summary
    elapsed = time.time() - start_time
    log("\n" + "="*70)
    log("TRANSFER SUMMARY")
    log("="*70)
    log(f"Containers successful: {successful}")
    log(f"Containers failed:     {failed}")
    log(f"Total time:           {elapsed/60:.1f} minutes")
    log(f"Progress saved to:    {PROGRESS_FILE}")
    log(f"Details saved to:     {DETAIL_LOG}")
    
    if progress.get('failed_containers'):
        log("\nFailed containers:")
        for cid, reason in progress['failed_containers'].items():
            log(f"  Container {cid}: {reason}")

if __name__ == '__main__':
    main()