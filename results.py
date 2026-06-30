#!/usr/bin/env python3
"""Merge country data from an enriched CSV into the original results CSV.

Usage:
  python results.py [results.csv] [results_enriched.csv]

If arguments are omitted the script uses `results.csv` and `results_enriched.csv` in the
script directory. The script writes `results_updated.csv` and leaves a backup of the
original `results.csv` as `results.csv.bak`.
"""
import csv
import os
import sys


def load_enriched(path):
    mapping = {}
    if not os.path.exists(path):
        return mapping
    with open(path, newline='', encoding='utf-8-sig') as f:
        r = csv.DictReader(f)
        for row in r:
            ip = row.get('ip') or row.get('IP')
            if not ip:
                continue
            country = row.get('country') or row.get('Country') or ''
            mapping[ip.strip()] = country.strip()
    return mapping


def merge(results_path, enriched_path):
    if not os.path.exists(results_path):
        print(f'Results file not found: {results_path}', file=sys.stderr)
        sys.exit(1)

    enriched = load_enriched(enriched_path)

    out_path = os.path.splitext(results_path)[0] + '_updated.csv'

    with open(results_path, newline='', encoding='utf-8-sig') as fin, \
         open(out_path, 'w', newline='', encoding='utf-8') as fout:

        r = csv.DictReader(fin)
        fieldnames = r.fieldnames[:] if r.fieldnames else ['ip']
        if 'country' not in [f.lower() for f in fieldnames]:
            fieldnames.append('country')

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in r:
            ip = (row.get('ip') or row.get('IP') or '').strip()
            # preserve existing country if present (case-insensitive)
            existing = ''
            for k in row:
                if k.lower() == 'country':
                    existing = row.get(k, '').strip()
                    break

            if existing:
                row['country'] = existing
            else:
                country = enriched.get(ip, '')
                row['country'] = country

            writer.writerow(row)

    # backup original and replace
    bak = results_path + '.bak'
    try:
        if os.path.exists(bak):
            os.remove(bak)
        os.replace(results_path, bak)
        os.replace(out_path, results_path)
    except Exception as e:
        print('Error replacing files:', e, file=sys.stderr)
        print(f'Updated file left at {out_path}')
        sys.exit(1)

    print(f'Updated {results_path} (backup at {bak})')


def main():
    here = os.path.dirname(__file__) or '.'
    results = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'results.csv')
    enriched = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, 'results_enriched.csv')
    merge(results, enriched)


if __name__ == '__main__':
    main()
