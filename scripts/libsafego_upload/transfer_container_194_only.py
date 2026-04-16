#!/usr/bin/env python3
"""
Transfer metadata for only Container 194 PIDs
"""

import os
import subprocess
import sys

# The 12 PIDs that belong to Container 194
container_194_pids = [
    'emory:fkcdd', 'emory:rg99w', 'emory:ghzrf', 'emory:ghzq9',
    'emory:ghzp5', 'emory:ghzsk', 'emory:ghztq', 'emory:rg2md',
    'emory:rg2pp', 'emory:rg2qt', 'emory:rg2rz', 'emory:rg2zs'
]

print("=" * 70)
print("TRANSFERRING METADATA FOR CONTAINER 194")
print("Collection: emory:94kf4 (Manuscript Collection No. 1054)")
print("PIDs:", len(container_194_pids))
print("=" * 70)
print()

fedora_password = (os.environ.get('FEDORA_PASSWORD') or '').strip()
if not fedora_password:
    print('Set FEDORA_PASSWORD in the environment before running this script.', file=sys.stderr)
    sys.exit(1)

# Build command - we'll process all PIDs and filter output
cmd = [
    'python3', 'transfer_to_libsafego.py',
    '--fedora-password', fedora_password,
    '--no-ssl-verify',
    '--metadata-only',
    '--use-pid-folders',
    '--output', 'container_194_metadata.csv'
]

# Run the command and filter output
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                        universal_newlines=True, bufsize=1)

found_any = False
skip_warnings = True
for line in proc.stdout:
    # Skip SSL warnings
    if 'InsecureRequestWarning' in line or 'urllib3' in line:
        if skip_warnings:
            continue
    else:
        skip_warnings = False
    
    # Always show these lines
    if any(x in line for x in ['Loading', 'Querying', 'Mapping', 'Found', 'Across']):
        print(line.rstrip())
    
    # Show lines for our specific PIDs
    elif any(pid in line for pid in container_194_pids):
        print(line.rstrip())
        found_any = True
    
    # Show Container 194 related lines
    elif 'Container 194' in line or 'container 194' in line or '/194/' in line:
        print(line.rstrip())
        found_any = True
    
    # Show summary lines
    elif any(x in line for x in ['Total', 'Transferred', 'Skipped', 'Error', '====']):
        if found_any:  # Only show summary if we found our PIDs
            print(line.rstrip())

proc.wait()
print()
print("=" * 70)
print("Container 194 transfer complete!")
print("Check container_194_metadata.csv for full details")
