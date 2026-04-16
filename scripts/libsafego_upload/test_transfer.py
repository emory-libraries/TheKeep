#!/usr/bin/env python3
"""Test transfer for emory:1d17x to verify folder structure works."""

import os
import subprocess
import sys

fedora_password = (os.environ.get('FEDORA_PASSWORD') or '').strip()
if not fedora_password:
    print('Set FEDORA_PASSWORD in the environment before running this script.', file=sys.stderr)
    sys.exit(1)

# Run the transfer for the second disk image
cmd = [
    'python', 'transfer_to_libsafego.py',
    '--fedora-password', fedora_password,
    '--no-ssl-verify',
    '--use-pid-folders',
    '--metadata-only',
    '--limit', '1'
]

# Add filter to get second object (skip emory:1d182 which we already did)
print("Note: This will process emory:1d182 again since we don't have a skip option")
print("In production, you would use resume capability or add a skip option\n")

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors/Warnings:", result.stderr)

sys.exit(result.returncode)
