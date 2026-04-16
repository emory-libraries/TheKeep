#!/usr/bin/env python3
"""
Direct transfer of Container 194 metadata only.
This script queries ONLY the PIDs for collection emory:94kf4 to avoid hanging.
"""

import os
import sys
import subprocess

print("=" * 70)
print("TRANSFERRING METADATA FOR CONTAINER 194 ONLY")
print("Collection: emory:94kf4 (Manuscript Collection No. 1054)")
print("=" * 70)
print()

# First, let's get just the PIDs for this collection using a targeted query
import ssl
from urllib.request import Request, urlopen, HTTPBasicAuthHandler, HTTPSHandler, build_opener
from urllib.parse import urlencode

def _require_env(name):
    v = (os.environ.get(name) or '').strip()
    if not v:
        sys.exit('Missing required environment variable: %s' % name)
    return v


def _fedora_url():
    u = _require_env('FEDORA_URL')
    return u.rstrip('/') + '/'


def _libsafe_api_url():
    return _require_env('LIBSAFE_GO_API_URL').rstrip('/')


def _libsafe_api_key():
    return _require_env('LIBSAFE_GO_API_KEY')


fedora_url = _fedora_url()
fedora_user = os.environ.get('FEDORA_USER', 'keep')
fedora_password = _require_env('FEDORA_PASSWORD')

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

auth = HTTPBasicAuthHandler()
auth.add_password('Fedora Repository Server', fedora_url, fedora_user, fedora_password)
opener = build_opener(auth, HTTPSHandler(context=ssl_ctx))

print("Step 1: Getting PIDs for collection emory:94kf4...")
sparql = '''
select ?pid where {
  ?pid <info:fedora/fedora-system:def/model#hasModel> <info:fedora/emory-control:DiskImage-1.0> .
  ?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> <info:fedora/emory:94kf4>
}
'''

params = urlencode({
    'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
    'query': sparql,
})

try:
    resp = opener.open(Request(f'{fedora_url}risearch?{params}'))
    lines = resp.read().decode('utf-8').strip().split('\n')
    pids = [line.replace('info:fedora/', '') for line in lines[1:]]
    print(f"  Found {len(pids)} PIDs: {', '.join(pids[:5])}...")
except Exception as e:
    print(f"ERROR: Failed to query PIDs: {e}")
    sys.exit(1)

# Now write a temporary file with just these PIDs
print("\nStep 2: Creating temporary PID list file...")
with open('temp_container_194_pids.txt', 'w') as f:
    for pid in pids:
        f.write(f"info:fedora/{pid}\n")

print(f"  Wrote {len(pids)} PIDs to temp_container_194_pids.txt")

# Now we'll modify the approach - directly transfer each PID
print("\nStep 3: Transferring metadata for each PID...")
print("-" * 70)

import csv
import re
import tempfile
import time
import requests
import urllib3

urllib3.disable_warnings()

# Get container mapping for this collection
container_id = 194  # We know this from earlier

def download_datastream(fedora_url, pid, dsid, opener):
    """Download a datastream content."""
    url = f'{fedora_url}objects/{pid}/datastreams/{dsid}/content'
    resp = opener.open(Request(url))
    return resp.read()

def upload_to_libsafe(api_url, api_key, container_id, content, filename, subfolder=None):
    """Upload content to LibSafe Go."""
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{api_url}/container/{container_id}/file/upload'
    
    data = {'fileName': filename, 'chunkIndex': 0}
    if subfolder:
        data['path'] = subfolder
    
    files = {'file': (filename, content, 'application/octet-stream')}
    resp = requests.post(url, headers=headers, data=data, files=files, verify=False)
    return resp.status_code in [200, 201]

results = []
for i, pid in enumerate(pids, 1):
    print(f"[{i}/{len(pids)}] Processing {pid}:")
    
    # Create folder name
    folder_name = pid.replace(':', '_')
    
    # Get list of datastreams
    try:
        url = f'{fedora_url}objects/{pid}/datastreams?format=xml'
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        
        # Parse datastream IDs
        dsids = re.findall(r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',xml)
        
        # Filter to metadata only
        metadata_ds = [ds for ds in dsids if ds.lower() != 'content']
        print(f"  Found {len(metadata_ds)} metadata datastreams")
        
        transferred = 0
        for dsid in metadata_ds[:5]:  # Limit to core metadata for this test
            if dsid not in ['DC', 'MODS', 'RELS-EXT', 'Rights', 'provenanceMetadata']:
                continue
                
            try:
                # Download
                content = download_datastream(fedora_url, pid, dsid, opener)
                
                # Create filename
                ext = '.xml' if dsid in ['DC', 'MODS', 'Rights', 'provenanceMetadata'] else '.rdf'
                filename = f"{dsid}{ext}"
                
                # Upload
                success = upload_to_libsafe(
                    _libsafe_api_url(), _libsafe_api_key(), container_id,
                    content, filename, folder_name
                )
                
                if success:
                    print(f"    ✓ {folder_name}/{filename} ({len(content)} bytes)")
                    transferred += 1
                else:
                    print(f"    ✗ Failed: {folder_name}/{filename}")
                    
            except Exception as e:
                print(f"    ✗ Error on {dsid}: {e}")
        
        if transferred > 0:
            print(f"  Summary: {transferred} files transferred for {pid}")
            results.append((pid, container_id, transferred, 'SUCCESS'))
        else:
            results.append((pid, container_id, 0, 'FAILED'))
            
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append((pid, container_id, 0, f'ERROR: {e}'))
    
    print()

# Write results
print("=" * 70)
print("SUMMARY")
print("=" * 70)

with open('container_194_direct_results.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['PID', 'Container', 'Files', 'Status'])
    for r in results:
        w.writerow(r)

successful = len([r for r in results if r[3] == 'SUCCESS'])
print(f"Successfully processed: {successful}/{len(pids)} PIDs")
print(f"Results written to: container_194_direct_results.csv")

# Clean up
if os.path.exists('temp_container_194_pids.txt'):
    os.unlink('temp_container_194_pids.txt')