#!/usr/bin/env python3
"""
Monitor the progress of the metadata transfer.
"""

import os
import json
import csv
import time
from datetime import datetime

PROGRESS_FILE = 'container_transfer_progress.json'
DETAIL_LOG = 'container_transfer_details.csv'
LOG_FILE = 'container_transfer.log'

def main():
    print("=" * 70)
    print("METADATA TRANSFER MONITOR")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if transfer is running
    stream = os.popen('ps aux | grep "transfer_all_containers.py" | grep -v grep')
    processes = stream.read()
    if processes:
        print("✓ Transfer process is RUNNING")
        for line in processes.strip().split('\n'):
            parts = line.split()
            if parts:
                pid = parts[1]
                cpu = parts[2]
                print(f"  PID: {pid}, CPU: {cpu}%")
    else:
        print("✗ Transfer process is NOT running")
    
    print()
    
    # Load progress file
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
        
        completed = len(progress.get('completed_containers', []))
        failed_count = len(progress.get('failed_containers', {}))
        
        print(f"Completed containers: {completed}")
        print(f"Failed containers:    {failed_count}")
        
        if progress.get('stats'):
            # Calculate totals
            total_transferred = 0
            total_skipped = 0
            total_failed = 0
            total_pids = 0
            
            for container_id, stats in progress['stats'].items():
                total_pids += stats.get('total_pids', 0)
                total_transferred += stats.get('transferred_files', 0)
                total_skipped += stats.get('skipped_files', 0)
                total_failed += stats.get('failed_files', 0)
            
            print(f"\nTotal PIDs processed:  {total_pids}")
            print(f"Files transferred:     {total_transferred}")
            print(f"Files skipped:         {total_skipped}")
            print(f"Files failed:          {total_failed}")
    else:
        print("Progress file not found yet")
    
    print()
    
    # Check detail log
    if os.path.exists(DETAIL_LOG):
        with open(DETAIL_LOG, 'r') as f:
            lines = sum(1 for line in f) - 1  # Subtract header
        
        print(f"Detail log entries: {lines}")
        
        # Show last few entries
        print("\nLast 5 transfers:")
        stream = os.popen(f'tail -6 {DETAIL_LOG} | tail -5')
        for line in stream:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                container, collection, pid, transferred, skipped, failed = parts
                print(f"  Container {container}: {pid} - "
                      f"✓ {transferred}, ↷ {skipped}, ✗ {failed}")
    
    print()
    
    # Check last log entries
    if os.path.exists(LOG_FILE):
        print("Recent log entries:")
        stream = os.popen(f'tail -5 {LOG_FILE}')
        for line in stream:
            print(f"  {line.strip()}")
    
    print()
    print("=" * 70)
    print("To see live progress: tail -f transfer_all.out")
    print("To see detailed transfers: tail -f container_transfer_details.csv")

if __name__ == '__main__':
    main()