#!/usr/bin/env python3
"""Test the improved resume logic."""

from collections import defaultdict
import csv
import os

# Copy the functions from the main script
def analyze_transfer_log(log_path):
    """Analyze the transfer log to provide detailed status information."""
    stats = {
        'total_pids': set(),
        'pids_with_content': set(),
        'pids_with_metadata': set(),
        'total_files': 0,
        'successful_files': 0,
        'failed_files': 0,
        'datastream_counts': defaultdict(int)
    }
    
    if not os.path.exists(log_path):
        return stats
    
    with open(log_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get('PID', '')
            ds = row.get('Datastream', '')
            status = row.get('Status', '')
            
            if pid and ds and ds != 'SURVEY':
                stats['total_pids'].add(pid)
                stats['total_files'] += 1
                
                if status in ('OK', 'EXISTS'):
                    stats['successful_files'] += 1
                    stats['datastream_counts'][ds] += 1
                    
                    if ds.lower() == 'content':
                        stats['pids_with_content'].add(pid)
                    elif ds.lower() in ('dc', 'mods', 'rels-ext', 'rights', 'provenancemetadata'):
                        stats['pids_with_metadata'].add(pid)
                elif status.startswith('ERROR'):
                    stats['failed_files'] += 1
    
    return stats


def load_completed_pids(log_path, transfer_mode='both'):
    """Load PIDs already completed from a previous transfer log."""
    # Track what datastreams were successfully transferred for each PID
    pid_datastreams = defaultdict(set)
    
    if os.path.exists(log_path):
        with open(log_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Status') in ('OK', 'EXISTS'):
                    pid = row.get('PID', '')
                    ds = row.get('Datastream', row.get('Filename', ''))
                    if pid and ds and ds != 'SURVEY':
                        pid_datastreams[pid].add(ds.lower())
    
    # Determine which PIDs are complete based on transfer mode
    done = set()
    
    # Common metadata datastreams to check
    core_metadata = {'dc', 'mods', 'rels-ext', 'rights', 'provenancemetadata'}
    
    for pid, datastreams in pid_datastreams.items():
        if transfer_mode == 'content':
            # Content-only: PID is done if content was transferred
            if 'content' in datastreams:
                done.add(pid)
                
        elif transfer_mode == 'metadata':
            # Metadata-only: PID is done if core metadata was transferred
            # Consider done if at least DC, MODS, and RELS-EXT are present
            required_metadata = {'dc', 'mods', 'rels-ext'}
            if required_metadata.issubset(datastreams):
                done.add(pid)
                
        else:  # 'both'
            # Both: PID is done if content AND core metadata were transferred
            required_metadata = {'dc', 'mods', 'rels-ext'}
            if 'content' in datastreams and required_metadata.issubset(datastreams):
                done.add(pid)
    
    return done


# Create test log
test_log = '''PID,Datastream,Container ID,Size,Status
emory:1d182,DC,176,425,OK
emory:1d182,MODS,176,395,OK
emory:1d182,RELS-EXT,176,725,OK
emory:1d182,Rights,176,142,OK
emory:1d182,provenanceMetadata,176,21427,OK
emory:1d182,content,176,60011642880,OK
emory:1d17x,DC,176,433,OK
emory:1d17x,MODS,176,403,OK
emory:1d17x,RELS-EXT,176,725,OK
emory:1d196,DC,176,435,ERROR: Connection timeout
emory:1d196,MODS,176,405,OK
'''

with open('test_resume_log.csv', 'w') as f:
    f.write(test_log)

# Test analyze function
print('Testing analyze_transfer_log():')
print('=' * 50)
stats = analyze_transfer_log('test_resume_log.csv')
print('Total PIDs attempted:', len(stats['total_pids']))
print('PIDs with content:', stats['pids_with_content'])
print('PIDs with metadata:', stats['pids_with_metadata'])
print('Successful files:', stats['successful_files'])
print('Failed files:', stats['failed_files'])

print('\nTesting load_completed_pids() with different modes:')
print('=' * 50)

# Test different modes
for mode in ['content', 'metadata', 'both']:
    done = load_completed_pids('test_resume_log.csv', mode)
    print(f'{mode:10} mode: {done}')

# Check actual transfer log
if os.path.exists('transfer_log.csv'):
    print('\n\nAnalyzing actual transfer_log.csv:')
    print('=' * 50)
    stats = analyze_transfer_log('transfer_log.csv')
    print('Total PIDs attempted:', len(stats['total_pids']))
    print('PIDs with content:', stats['pids_with_content'])
    print('PIDs with metadata:', stats['pids_with_metadata'])
    
    for mode in ['content', 'metadata', 'both']:
        done = load_completed_pids('transfer_log.csv', mode)
        print(f'\n{mode:10} mode would skip: {len(done)} PIDs')

# Clean up
os.unlink('test_resume_log.csv')

print('\n\nExplanation of test cases:')
print('=' * 50)
print('- emory:1d182 has both content and all core metadata → complete for all modes')
print('- emory:1d17x has only metadata (DC, MODS, RELS-EXT) → complete for metadata mode only')
print('- emory:1d196 has incomplete metadata (DC failed) → not complete for any mode')
