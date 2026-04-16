#!/usr/bin/env python3
"""
Transfer metadata for Container 194 (Collection emory:94kf4) specifically
"""

import ssl
import csv
import os
import sys
import tempfile
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


# Set up Fedora connection
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

def list_datastreams(fedora_url, pid, opener):
    """List all datastreams for an object."""
    url = f'{fedora_url}objects/{pid}/datastreams?format=xml'
    resp = opener.open(Request(url))
    xml = resp.read().decode('utf-8')
    # Parse datastream IDs from self-closing XML tags
    import re
    dsids = re.findall(r'<datastream[^>]*dsid="([^"]+)"[^>]*/?>',xml)
    return dsids

def download_datastream(fedora_url, pid, dsid, opener, dest_path):
    """Download a datastream content."""
    url = f'{fedora_url}objects/{pid}/datastreams/{dsid}/content'
    resp = opener.open(Request(url))
    content = resp.read()
    
    with open(dest_path, 'wb') as f:
        f.write(content)
    
    return len(content)

def create_folder_in_container(api_url, api_key, container_id, folder_path):
    """Create a folder in a container."""
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{api_url}/container/{container_id}/folder'
    resp = requests.post(url, headers=headers, json={'path': folder_path}, verify=False)
    return resp.status_code in [200, 201, 409]  # 409 = already exists

def upload_to_libsafe(api_url, api_key, container_id, filepath, filename, subfolder=None):
    """Upload a file to LibSafe Go."""
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{api_url}/container/{container_id}/file/upload'
    
    data = {'fileName': filename, 'chunkIndex': 0}
    if subfolder:
        data['path'] = subfolder
    
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'application/octet-stream')}
        resp = requests.post(url, headers=headers, data=data, files=files, verify=False)
    
    return resp.status_code in [200, 201]

def file_exists_in_container(api_url, api_key, container_id, filename, subfolder=None):
    """Check if a file exists in a container."""
    headers = {'Authorization': f'Bearer {api_key}'}
    
    if subfolder:
        full_path = f'{subfolder}/{filename}'
    else:
        full_path = filename
    
    url = f'{api_url}/container/{container_id}/file/path/{full_path}'
    resp = requests.get(url, headers=headers, verify=False, timeout=10)
    
    if resp.status_code == 200:
        data = resp.json()
        return data.get('success', False)
    return False

print("Transferring metadata for Container 194 (Collection emory:94kf4)")
print("=" * 70)

# Get PIDs from this collection
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
resp = opener.open(Request(f'{_fedora_url()}risearch?{params}'))
lines = resp.read().decode('utf-8').strip().split('\n')
pids = [line.replace('info:fedora/', '') for line in lines[1:]]

print(f"Found {len(pids)} disk images in collection emory:94kf4")
print("Target container: 194")
print()

# Transfer metadata for each PID
container_id = 194
transferred = 0
skipped = 0
failed = 0

with open('container_194_specific.csv', 'w') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['PID', 'Datastream', 'Container ID', 'Size', 'Status'])
    
    for pid in pids[:3]:  # Just do first 3 for test
        print(f"Processing {pid}...")
        
        # Create PID folder
        subfolder = pid.replace(':', '_')
        folder_created = create_folder_in_container(
            _libsafe_api_url(), _libsafe_api_key(), container_id, subfolder
        )
        if not folder_created:
            print(f'  Warning: Could not create folder {subfolder}')
        
        # Get all datastreams
        try:
            dsids = list_datastreams(_fedora_url(), pid, opener)
            # Filter to metadata only
            metadata_ds = [ds for ds in dsids if ds not in ['content']]
            
            for dsid in metadata_ds:
                # Determine filename
                ext_map = {
                    'DC': '.xml', 'MODS': '.xml', 'RELS-EXT': '.rdf',
                    'Rights': '.xml', 'provenanceMetadata': '.xml'
                }
                if dsid.startswith('supplement'):
                    filename = dsid.replace('supplement', 'SUPPLEMENT') + '.txt'
                else:
                    filename = dsid + ext_map.get(dsid, '')
                
                # Check if exists
                if file_exists_in_container(_libsafe_api_url(), _libsafe_api_key(), container_id, filename, subfolder):
                    print(f'  SKIP (exists): {subfolder}/{filename}')
                    writer.writerow([pid, dsid, container_id, 0, 'skipped'])
                    skipped += 1
                    continue
                
                # Download and upload
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    size = download_datastream(_fedora_url(), pid, dsid, opener, tmp.name)
                    print(f'  Downloaded {dsid}: {size} bytes')
                    
                    if upload_to_libsafe(_libsafe_api_url(), _libsafe_api_key(), container_id, tmp.name, filename, subfolder):
                        print(f'    ✓ Uploaded to {subfolder}/{filename}')
                        writer.writerow([pid, dsid, container_id, size, 'success'])
                        transferred += 1
                    else:
                        print(f'    ✗ Failed to upload')
                        writer.writerow([pid, dsid, container_id, size, 'failed'])
                        failed += 1
                    
                    os.unlink(tmp.name)
                    
        except Exception as e:
            print(f'  ERROR: {e}')
            writer.writerow([pid, 'ERROR', container_id, 0, str(e)])
            failed += 1

print()
print("=" * 70)
print(f"Transferred: {transferred}")
print(f"Skipped:     {skipped}")
print(f"Failed:      {failed}")
print("Log written to: container_194_specific.csv")
