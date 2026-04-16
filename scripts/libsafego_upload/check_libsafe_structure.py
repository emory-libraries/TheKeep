#!/usr/bin/env python3
"""Check the structure of files in a LibSafe Go container via API."""

import json
import os
import sys

import requests


def _require_env(name):
    v = (os.environ.get(name) or '').strip()
    if not v:
        sys.exit('Missing required environment variable: %s' % name)
    return v


def _libsafe_api_url():
    return _require_env('LIBSAFE_GO_API_URL').rstrip('/')


def _libsafe_api_key():
    return _require_env('LIBSAFE_GO_API_KEY')


def list_container_files(container_id):
    """List all files in a container."""
    url = f'{_libsafe_api_url()}/container/{container_id}/file/list'
    headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}
    
    try:
        resp = requests.get(url, headers=headers, verify=False)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching container files: {e}")
        return None

def get_file_info(container_id, file_path):
    """Get info for a specific file."""
    url = f'{_libsafe_api_url()}/container/{container_id}/file/path/{file_path}'
    headers = {'Authorization': 'Bearer %s' % _libsafe_api_key()}
    
    try:
        resp = requests.get(url, headers=headers, verify=False)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def display_tree(files, indent=0):
    """Display files in a tree structure."""
    # Group files by directory
    dirs = {}
    root_files = []
    
    for file_info in files:
        path = file_info.get('path', file_info.get('name', ''))
        if '/' in path:
            dir_name = path.split('/')[0]
            if dir_name not in dirs:
                dirs[dir_name] = []
            dirs[dir_name].append(path)
        else:
            root_files.append(path)
    
    # Display directories first
    for dir_name in sorted(dirs.keys()):
        print('  ' * indent + f'📁 {dir_name}/')
        for file_path in sorted(dirs[dir_name]):
            file_name = file_path.split('/')[-1]
            if file_name:  # Skip if it's just the directory
                print('  ' * (indent + 1) + f'📄 {file_name}')
    
    # Display root files
    for file_name in sorted(root_files):
        print('  ' * indent + f'📄 {file_name}')

def main():
    container_id = int(os.environ.get('LIBSAFE_CONTAINER_ID', '176'))
    
    print(f"Checking structure in LibSafe Go container {container_id}...")
    print("=" * 60)
    
    # Get list of files
    result = list_container_files(container_id)
    
    if result and result.get('success'):
        files = result.get('result', [])
        print(f"Found {len(files)} files in container:\n")
        
        if files:
            # Display tree structure
            display_tree(files)
            
            # Show details for emory_1d182 folder
            print("\n" + "=" * 60)
            print("Details for emory_1d182 folder:")
            print("-" * 60)
            
            emory_files = [f for f in files if f.get('path', '').startswith('emory_1d182/')]
            for file_info in sorted(emory_files, key=lambda x: x.get('path', '')):
                path = file_info.get('path', '')
                size = file_info.get('size', 0)
                print(f"  {path:40} {size:>10} bytes")
        else:
            print("No files found in container")
    else:
        print(f"Failed to get container files: {result}")

if __name__ == '__main__':
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()