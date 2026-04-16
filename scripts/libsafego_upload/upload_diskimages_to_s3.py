#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Disk Image *content* datastreams from Fedora to AWS S3.

- Uses the same collection → container ID mapping as download_diskimages.py
  (Fedora MODS local_source_id + created_containers.csv).
- Processes collections in **hardcoded survey order** (smallest total first),
  from `survey_diskimages.py` output (largest→smallest list reversed).
  Use ``--compute-collection-order`` to sort by live Fedora sizes instead.
- S3 layout (default --use-pid-folders):
    s3://BUCKET/{container_id}/{pid_with_underscores}/{filename}

Credentials: load aws_s3_credentials.env (gitignored) or set env vars.
  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION=us-east-1
  AWS_S3_BUCKET=your-bucket-name   (add this line to the env file)

Usage:
  python upload_diskimages_to_s3.py --fedora-password SECRET --no-ssl-verify --dry-run
  python upload_diskimages_to_s3.py --fedora-password SECRET --no-ssl-verify \\
      --limit-collections 1
  python upload_diskimages_to_s3.py --fedora-password SECRET --no-ssl-verify \\
      --collection emory:YOUR_COLLECTION_PID
"""

from __future__ import print_function

import argparse
import csv
import os
import re
import ssl
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from urllib.request import Request, urlopen, HTTPBasicAuthHandler, HTTPSHandler, build_opener
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import Request, urlopen, HTTPBasicAuthHandler, HTTPSHandler, build_opener
    from urllib import urlencode

import boto3
from botocore.exceptions import ClientError

SPARQL_DISK_IMAGES = (
    'select ?pid ?coll where { '
    '?pid <info:fedora/fedora-system:def/model#hasModel> '
    '<info:fedora/emory-control:DiskImage-1.0> . '
    '?pid <info:fedora/fedora-system:def/relations-external#isMemberOfCollection> '
    '?coll }'
)

# Survey order from survey_diskimages.py (largest total first in terminal).
# Smallest-first upload = reverse of that list.
DISKIMAGE_COLLECTION_UPLOAD_ORDER = (
    'emory:v944f',
    'emory:94jf1',
    'emory:rqdvw',
    'emory:tbmn0',
    'emory:sq7zt',
    'emory:gj0pb',
    'emory:94k3r',
    'emory:bt8pk',
    'emory:tbnn3',
    'emory:smxs0',
    'emory:rr344',
    'emory:gk5wr',
    'emory:tx74z',
    'emory:txbv5',
    'emory:cksdk',
    'emory:pqh47',
    'emory:smxqq',
    'emory:fhrph',
    'emory:bszb6',
    'emory:gj2c9',
    'emory:rxcm7',
    'emory:th3jc',
    'emory:bsq86',
    'emory:smxrv',
    'emory:f7gtp',
    'emory:sj9s0',
    'emory:st56s',
    'emory:rqtrq',
    'emory:f8kjz',
    'emory:t01dk',
    'emory:stgpn',
    'emory:v29k8',
    'emory:rpt0m',
    'emory:crnng',
    'emory:sq802',
    'emory:sq816',
    'emory:th4vq',
    'emory:mrc8c',
    'emory:t6jmc',
    'emory:st4k6',
    'emory:vp11g',
    'emory:s05q6',
    'emory:h790x',
    'emory:s7h6n',
    'emory:gk2t5',
    'emory:rmdh9',
    'emory:vx1xj',
    'emory:th6vx',
    'emory:pmsms',
    'emory:tnb19',
    'emory:thnxj',
    'emory:b73kg',
    'emory:rr7fs',
    'emory:tkzrx',
    'emory:tmhhp',
    'emory:tzs3j',
    'emory:94mcz',
    'emory:tdsft',
    'emory:sq9r6',
    'emory:s48rx',
    'emory:q4d3n',
    'emory:94jr8',
    'emory:q4d2h',
    'emory:gj0tw',
    'emory:t0qvf',
    'emory:tmzxp',
    'emory:t0m8s',
    'emory:rmv1q',
    'emory:vpng4',
    'emory:tnb2f',
    'emory:tbdb4',
    'emory:pqh5c',
    'emory:s48s2',
    'emory:tmw1w',
    'emory:sqcp4',
    'emory:pmgz7',
    'emory:t0g08',
    'emory:g1btw',
    'emory:tbh2b',
    'emory:tjwtx',
    'emory:tm9vf',
    'emory:94jbm',
    'emory:b73xv',
    'emory:s73pb',
    'emory:sdxhg',
    'emory:tgp8z',
    'emory:bsq6x',
    'emory:tnb3k',
    'emory:sqmzz',
    'emory:rmdf1',
    'emory:th1k9',
    'emory:tn9wn',
    'emory:94khd',
    'emory:94k2m',
    'emory:kzxww',
    'emory:rmkgp',
    'emory:ghsdj',
    'emory:tgbrv',
    'emory:v92rq',
    'emory:tnnj9',
    'emory:f3qwd',
    'emory:gk0st',
    'emory:94kf4',
    'emory:tgn0r',
    'emory:94k9k',
)


def load_s3_env_file(path):
    if not path or not os.path.isfile(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())


def fedora_opener(fedora_url, user, password, ssl_context):
    auth = HTTPBasicAuthHandler()
    auth.add_password('Fedora Repository Server', fedora_url, user, password)
    return build_opener(auth, HTTPSHandler(context=ssl_context))


def risearch(fedora_url, sparql, opener):
    params = urlencode({
        'type': 'tuples', 'lang': 'sparql', 'format': 'CSV',
        'limit': 100000, 'query': sparql,
    })
    url = '%srisearch?%s' % (fedora_url, params)
    resp = opener.open(Request(url))
    body = resp.read().decode('utf-8')
    lines = body.strip().split('\n')
    if len(lines) < 2:
        return []
    headers = [h.strip('"') for h in lines[0].split(',')]
    rows = []
    for line in lines[1:]:
        vals = line.split(',')
        rows.append(dict(zip(headers, vals)))
    return rows


def get_mods_title(fedora_url, pid, opener):
    url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<mods:title>([^<]+)</mods:title>', xml)
        return m.group(1).strip() if m else ''
    except Exception:
        return ''


def get_content_size(fedora_url, pid, opener):
    """Size of content datastream (profile, then HEAD)."""
    url = '%sobjects/%s/datastreams/content?format=xml' % (fedora_url, pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<dsSize>(\d+)</dsSize>', xml)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    try:
        content_url = '%sobjects/%s/datastreams/content/content' % (fedora_url, pid)
        req = Request(content_url)
        req.get_method = lambda: 'HEAD'
        resp = opener.open(req)
        cl = resp.headers.get('Content-Length')
        return int(cl) if cl else 0
    except Exception:
        return 0


def get_content_label(fedora_url, pid, opener):
    url = '%sobjects/%s/datastreams/content?format=xml' % (fedora_url, pid)
    try:
        resp = opener.open(Request(url))
        xml = resp.read().decode('utf-8')
        m = re.search(r'<dsLabel>([^<]*)</dsLabel>', xml)
        return m.group(1).strip() if m else ''
    except Exception:
        return ''


def build_content_filename(pid, label, title):
    disk_exts = ('.img', '.iso', '.dd', '.dmg', '.ima', '.image', '.bin')
    if label:
        fn = label
    else:
        safe = re.sub(r'[^\w\-.]', '_', title) if title else ''
        fn = '%s__%s' % (pid.replace(':', '_'), safe or 'content')
    low = fn.lower()
    if not any(low.endswith(ext) for ext in disk_exts):
        fn = '%s.img' % fn
    return fn


def build_collection_map(csv_path):
    mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            ident = row.get('Identifier', '').strip()
            cid = row.get('Container ID', '').strip()
            if ident and cid:
                mapping[ident] = cid
    return mapping


def map_collections_to_containers(fedora_url, coll_pids, id_to_container, opener):
    out = {}
    for coll_pid in sorted(coll_pids):
        url = '%sobjects/%s/datastreams/MODS/content' % (fedora_url, coll_pid)
        try:
            resp = opener.open(Request(url))
            xml = resp.read().decode('utf-8')
            m = re.search(
                r'<mods:identifier[^>]*type="local_source_id">(\d+)</mods:identifier>',
                xml
            )
            if m:
                formatted = 'Manuscript Collection No. %s' % m.group(1)
                out[coll_pid] = id_to_container.get(formatted, 'unmapped')
            else:
                out[coll_pid] = 'unmapped'
        except Exception:
            out[coll_pid] = 'unmapped'
    return out


def download_content_to_temp(fedora_url, pid, opener):
    """Stream content to a temp file; return (path, bytes_written)."""
    url = '%sobjects/%s/datastreams/content/content' % (fedora_url, pid)
    resp = opener.open(Request(url))
    fd, path = tempfile.mkstemp(prefix='fedora_content_', suffix='.bin')
    os.close(fd)
    n = 0
    try:
        with open(path, 'wb') as f:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                n += len(chunk)
        return path, n
    except Exception:
        if os.path.exists(path):
            os.unlink(path)
        raise


def format_size(nbytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(nbytes) < 1024.0:
            return '%.1f %s' % (nbytes, unit)
        nbytes /= 1024.0
    return '%.1f PB' % nbytes


def s3_head_ok(s3, bucket, key, expected_size):
    try:
        r = s3.head_object(Bucket=bucket, Key=key)
        if expected_size and r.get('ContentLength') != expected_size:
            return False
        return True
    except ClientError:
        return False


def _upload_from_csv(args, fedora_url, opener, s3, bucket):
    """Upload files listed in a CSV (from --list-remaining), in CSV order."""
    csv_path = args.from_csv
    items = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            items.append(row)

    print('Loaded %d items from %s (sorted by size in CSV order)' % (len(items), csv_path))
    if args.limit_objects:
        print('Will stop after %d successful uploads' % args.limit_objects)

    total_size = sum(int(r.get('Size (bytes)', 0)) for r in items)
    print('Total size in CSV: %s\n' % format_size(total_size))

    uploaded = 0
    skipped = 0
    errors = 0

    for i, row in enumerate(items):
        if args.limit_objects and uploaded >= args.limit_objects:
            print('Stopped: --limit-objects %d' % args.limit_objects)
            break

        pid = row['PID']
        s3_key = row['S3 Key']
        expected_size = int(row.get('Size (bytes)', 0))

        if args.skip_existing and expected_size and s3_head_ok(s3, bucket, s3_key, expected_size):
            print('  [%d/%d] SKIP (exists) %s -> s3://%s/%s'
                  % (i + 1, len(items), pid, bucket, s3_key))
            skipped += 1
            continue

        print('  [%d/%d] UPLOAD %s (%s) -> s3://%s/%s'
              % (i + 1, len(items), pid, format_size(expected_size), bucket, s3_key))

        if args.dry_run:
            continue

        tmp_path = None
        try:
            t0 = time.time()
            tmp_path, nbytes = download_content_to_temp(fedora_url, pid, opener)
            s3.upload_file(tmp_path, bucket, s3_key)
            elapsed = time.time() - t0
            print('    done %s in %.1fs (%s/s)'
                  % (format_size(nbytes), elapsed,
                     format_size(nbytes / elapsed) if elapsed else '?'))
            uploaded += 1
        except Exception as e:
            print('    ERROR: %s' % e, file=sys.stderr)
            errors += 1
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    print('\n' + '=' * 60)
    print('Uploaded: %d  Skipped: %d  Errors: %d' % (uploaded, skipped, errors))


def _check_one_pid(fedora_url, pid, coll, container_id, use_pid_folders,
                    s3, bucket, user, password, ssl_ctx):
    """Thread worker: get size + label from Fedora, check S3 existence."""
    opener = fedora_opener(fedora_url, user, password, ssl_ctx)
    size = get_content_size(fedora_url, pid, opener)
    label = get_content_label(fedora_url, pid, opener)
    title = get_mods_title(fedora_url, pid, opener)
    filename = build_content_filename(pid, label, title)
    pid_folder = pid.replace(':', '_')
    if use_pid_folders:
        key = '%s/%s/%s' % (container_id, pid_folder, filename)
    else:
        key = '%s/%s__%s' % (container_id, pid_folder, filename)
    exists = s3_head_ok(s3, bucket, key, size) if size else False
    return {
        'pid': pid, 'coll': coll, 'container_id': container_id,
        'filename': filename, 's3_key': key, 'size': size, 'exists': exists,
    }


def _list_remaining(args, fedora_url, opener, ssl_ctx,
                    ordered_colls, by_coll, coll_to_cid,
                    s3, bucket, use_pid_folders):
    """Write CSV of files not yet on S3, sorted by size ascending."""
    all_pids = []
    for coll in ordered_colls:
        container_id = coll_to_cid.get(coll, 'unmapped')
        if container_id == 'unmapped':
            continue
        for pid in by_coll.get(coll, []):
            all_pids.append((pid, coll, container_id))

    print('Checking %d objects (%d threads) ...' % (len(all_pids), args.workers))
    results = []
    done = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                _check_one_pid, fedora_url, pid, coll, cid, use_pid_folders,
                s3, bucket, args.fedora_user, args.fedora_password, ssl_ctx
            ): pid
            for pid, coll, cid in all_pids
        }
        for fut in as_completed(futures):
            done += 1
            row = fut.result()
            if not row['exists']:
                results.append(row)
            if done % 100 == 0 or done == len(all_pids):
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed else 0
                eta = (len(all_pids) - done) / rate if rate else 0
                sys.stdout.write(
                    '\r  %d / %d checked  |  %d remaining so far  |  ETA %.0fs   '
                    % (done, len(all_pids), len(results), eta))
                sys.stdout.flush()

    results.sort(key=lambda r: r['size'])
    print('\n\nRemaining (not on S3): %d objects' % len(results))

    total_bytes = sum(r['size'] for r in results)
    print('Total size remaining: %s' % format_size(total_bytes))

    csv_path = args.list_remaining
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['PID', 'Collection', 'Container ID', 'Filename', 'S3 Key',
                     'Size (bytes)', 'Size (human)'])
        for r in results:
            w.writerow([r['pid'], r['coll'], r['container_id'], r['filename'],
                        r['s3_key'], r['size'], format_size(r['size'])])

    print('Wrote %s (%d rows)' % (csv_path, len(results)))


def main():
    p = argparse.ArgumentParser(description='Upload disk images from Fedora to S3')
    p.add_argument('--fedora-url',
                   default=os.environ.get('FEDORA_URL', ''),
                   help='Fedora base URL (default: $FEDORA_URL)')
    p.add_argument('--fedora-user', default='keep')
    p.add_argument('--fedora-password', required=True)
    p.add_argument('--no-ssl-verify', action='store_true')
    p.add_argument('--containers-csv', default='created_containers.csv')
    p.add_argument('--s3-cred-env', default='aws_s3_credentials.env',
                   help='Env file with AWS keys and optional AWS_S3_BUCKET')
    p.add_argument('--bucket', default=None,
                   help='S3 bucket (overrides AWS_S3_BUCKET in env)')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--skip-existing', action='store_true', default=True,
                   help='Skip upload if object exists with same size (default: on)')
    p.add_argument('--no-skip-existing', action='store_true',
                   help='Always upload even if key exists')
    p.add_argument('--use-pid-folders', action='store_true', default=True,
                   help='Use s3://.../container/pid_folder/file (default)')
    p.add_argument('--no-use-pid-folders', action='store_true',
                   help='Flat: s3://.../container/file')
    p.add_argument('--limit-collections', type=int, default=0,
                   help='Only first N collections in order (0 = all)')
    p.add_argument('--limit-objects', type=int, default=0,
                   help='Stop after N successful uploads (0 = no limit)')
    p.add_argument('--collection', default=None,
                   help='Only this Fedora collection PID (e.g. emory:v944f)')
    p.add_argument('--compute-collection-order', action='store_true',
                   help='Sort collections by live Fedora content sizes (slow); '
                        'default uses hardcoded DISKIMAGE_COLLECTION_UPLOAD_ORDER')
    p.add_argument('--list-remaining', default=None, metavar='CSV_FILE',
                   help='Instead of uploading, write a CSV of files not yet on S3, '
                        'sorted by size (smallest first). Uses threaded checks.')
    p.add_argument('--from-csv', default=None, metavar='CSV_FILE',
                   help='Upload from a pre-sorted CSV (e.g. remaining_uploads.csv) '
                        'instead of querying Fedora for collection order.')
    p.add_argument('--workers', type=int, default=10,
                   help='Thread pool size for --list-remaining (default: 10)')
    args = p.parse_args()

    if not (args.fedora_url or '').strip():
        print('Set FEDORA_URL or pass --fedora-url', file=sys.stderr)
        sys.exit(1)

    load_s3_env_file(args.s3_cred_env)
    bucket = args.bucket or os.environ.get('AWS_S3_BUCKET')
    if not bucket:
        print('Set AWS_S3_BUCKET in %s or pass --bucket' % args.s3_cred_env, file=sys.stderr)
        sys.exit(1)

    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    ak = os.environ.get('AWS_ACCESS_KEY_ID')
    sk = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not ak or not sk:
        print('AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY required', file=sys.stderr)
        sys.exit(1)

    if args.no_skip_existing:
        args.skip_existing = False

    fedora_url = args.fedora_url.rstrip('/') + '/'
    ssl_ctx = ssl.create_default_context()
    if args.no_ssl_verify:
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    opener = fedora_opener(fedora_url, args.fedora_user, args.fedora_password, ssl_ctx)

    s3 = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
    )

    print('S3 bucket: %s  region: %s' % (bucket, region))

    # --from-csv: upload from a pre-sorted CSV (skips Fedora collection queries)
    if args.from_csv:
        _upload_from_csv(args, fedora_url, opener, s3, bucket)
        return

    print('Loading container mapping from %s ...' % args.containers_csv)
    id_to_container = build_collection_map(args.containers_csv)
    print('  %d identifiers' % len(id_to_container))

    print('Querying Fedora for disk images ...')
    rows = risearch(fedora_url, SPARQL_DISK_IMAGES, opener)
    print('  %d objects' % len(rows))

    coll_pids = set()
    for row in rows:
        coll_pids.add(row['coll'].replace('info:fedora/', ''))

    print('Mapping collections to container IDs ...')
    coll_to_cid = map_collections_to_containers(
        fedora_url, coll_pids, id_to_container, opener)

    if args.collection:
        if args.collection not in coll_pids:
            print('Collection %s not found among disk image collections.' % args.collection)
            sys.exit(1)
        coll_pids = {args.collection}

    # Group PIDs by collection
    by_coll = {}
    for row in rows:
        coll = row['coll'].replace('info:fedora/', '')
        if coll not in coll_pids:
            continue
        pid = row['pid'].replace('info:fedora/', '')
        by_coll.setdefault(coll, []).append(pid)

    coll_totals = {}

    if args.collection:
        ordered_colls = [args.collection]
        print('Single collection: %s' % args.collection)
    elif args.compute_collection_order:
        print('Computing content sizes per collection (for sort order) ...')
        for coll, pids in by_coll.items():
            total = 0
            for pid in pids:
                total += get_content_size(fedora_url, pid, opener)
            coll_totals[coll] = total
            print('  %s  %d files  %s' % (coll, len(pids), format_size(total)))
        ordered_colls = sorted(coll_totals.keys(), key=lambda c: (coll_totals[c], c))
        if args.limit_collections:
            ordered_colls = ordered_colls[:args.limit_collections]
            print('\nLimiting to %d smallest collection(s): %s'
                  % (args.limit_collections, ', '.join(ordered_colls)))
    else:
        print('Using hardcoded survey order (smallest total first, %d entries) ...'
              % len(DISKIMAGE_COLLECTION_UPLOAD_ORDER))
        ordered_colls = [c for c in DISKIMAGE_COLLECTION_UPLOAD_ORDER if c in by_coll]
        missing = sorted(set(by_coll.keys()) - set(ordered_colls))
        if missing:
            print('  WARNING: %d collection(s) not in hardcoded list (appended at end): %s'
                  % (len(missing), ', '.join(missing)))
            ordered_colls.extend(missing)
        if args.limit_collections:
            ordered_colls = ordered_colls[:args.limit_collections]
            print('\nLimiting to first %d collection(s) in that order: %s'
                  % (args.limit_collections, ', '.join(ordered_colls)))

    use_pid_folders = args.use_pid_folders and not args.no_use_pid_folders
    print('PID folders: %s\n' % ('yes' if use_pid_folders else 'no'))

    if args.list_remaining:
        _list_remaining(args, fedora_url, opener, ssl_ctx,
                        ordered_colls, by_coll, coll_to_cid,
                        s3, bucket, use_pid_folders)
        return

    uploaded = 0
    skipped = 0
    errors = 0
    done_objects = 0
    stop_uploads = False

    for coll in ordered_colls:
        if stop_uploads:
            break
        container_id = coll_to_cid.get(coll, 'unmapped')
        if container_id == 'unmapped':
            print('SKIP collection %s (unmapped container)' % coll)
            continue

        pids = by_coll[coll]
        total_note = (format_size(coll_totals[coll]) if coll in coll_totals
                      else 'hardcoded order')
        print('\n=== Collection %s -> container %s (%d PIDs, %s) ==='
              % (coll, container_id, len(pids), total_note))

        for pid in pids:
            if args.limit_objects and done_objects >= args.limit_objects:
                print('Stopped: --limit-objects %d' % args.limit_objects)
                stop_uploads = True
                break

            size = get_content_size(fedora_url, pid, opener)
            label = get_content_label(fedora_url, pid, opener)
            title = get_mods_title(fedora_url, pid, opener)
            filename = build_content_filename(pid, label, title)
            pid_folder = pid.replace(':', '_')

            if use_pid_folders:
                key = '%s/%s/%s' % (container_id, pid_folder, filename)
            else:
                key = '%s/%s__%s' % (container_id, pid_folder, filename)

            if args.skip_existing and size and s3_head_ok(s3, bucket, key, size):
                print('  SKIP (exists) %s -> s3://%s/%s' % (pid, bucket, key))
                skipped += 1
                continue

            print('  UPLOAD %s (%s) -> s3://%s/%s'
                  % (pid, format_size(size), bucket, key))

            if args.dry_run:
                continue

            tmp_path = None
            try:
                t0 = time.time()
                tmp_path, nbytes = download_content_to_temp(fedora_url, pid, opener)
                s3.upload_file(tmp_path, bucket, key)
                elapsed = time.time() - t0
                print('    done %s in %.1fs (%s/s)'
                      % (format_size(nbytes), elapsed,
                         format_size(nbytes / elapsed) if elapsed else '?'))
                uploaded += 1
                done_objects += 1
            except Exception as e:
                print('    ERROR: %s' % e, file=sys.stderr)
                errors += 1
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    print('\n' + '=' * 60)
    print('Uploaded: %d  Skipped: %d  Errors: %d' % (uploaded, skipped, errors))


if __name__ == '__main__':
    main()
