#!/usr/bin/env python3
import csv
import ipaddress
import os
import sys

HERE = os.path.dirname(__file__) or '.'
RESULTS = os.path.join(HERE, 'results.csv')
IPINFO = os.path.join(HERE, 'ipinfo_lite.csv')
OUT = os.path.join(HERE, 'results_enriched.csv')
UNMATCHED = os.path.join(HERE, 'results_unmatched.csv')
BACKUP = os.path.join(HERE, 'results.csv.bak')

info_fields = ['country','country_code','continent','continent_code','asn','as_name','as_domain']

def load_ipinfo(path):
    nets = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        r = csv.DictReader(f)
        for row in r:
            net = row.get('network')
            if not net:
                continue
            try:
                n = ipaddress.ip_network(net.strip())
            except Exception:
                continue
            nets.append((n, {k: row.get(k, '') for k in info_fields}))
    # sort by prefixlen desc so first match is most specific
    nets.sort(key=lambda x: x[0].prefixlen, reverse=True)
    return nets


def enrich():
    if not os.path.exists(RESULTS):
        print('results.csv not found', file=sys.stderr); sys.exit(1)
    if not os.path.exists(IPINFO):
        print('ipinfo_lite.csv not found', file=sys.stderr); sys.exit(1)

    networks = load_ipinfo(IPINFO)
    if not networks:
        print('No networks loaded from ipinfo_lite.csv', file=sys.stderr); sys.exit(1)

    matched = 0
    total = 0

    with open(RESULTS, newline='', encoding='utf-8-sig') as fin, \
         open(OUT, 'w', newline='', encoding='utf-8') as fout, \
         open(UNMATCHED, 'w', newline='', encoding='utf-8') as funm:

        r = csv.DictReader(fin)
        fieldnames = r.fieldnames[:] if r.fieldnames else ['ip']
        # add info fields (avoid duplicates)
        for f in info_fields:
            if f not in fieldnames:
                fieldnames.append(f)

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        um_writer = csv.DictWriter(funm, fieldnames=r.fieldnames or ['ip','status'])
        um_writer.writeheader()

        for row in r:
            total += 1
            ip = row.get('ip') or row.get('IP')
            if not ip:
                # write row with empty info
                for f in info_fields:
                    row[f] = ''
                writer.writerow(row)
                continue
            try:
                ip_obj = ipaddress.ip_address(ip.strip())
            except Exception:
                for f in info_fields:
                    row[f] = ''
                writer.writerow(row)
                continue

            found = None
            for net, data in networks:
                if ip_obj in net:
                    found = data
                    break
            if found:
                for k, v in found.items():
                    row[k] = v
                matched += 1
                writer.writerow(row)
            else:
                for f in info_fields:
                    row[f] = ''
                writer.writerow(row)
                um_writer.writerow(row)

    # backup original and replace
    try:
        if os.path.exists(BACKUP):
            os.remove(BACKUP)
        os.replace(RESULTS, BACKUP)
        os.replace(OUT, RESULTS)
    except Exception as e:
        print('Error replacing files:', e, file=sys.stderr)
        sys.exit(1)

    print(f'Total rows processed: {total}')
    print(f'Matched rows: {matched}')
    print(f'Unmatched rows: {total - matched} (see {os.path.basename(UNMATCHED)})')
    print(f'Original results backed up as {os.path.basename(BACKUP)}')
    print(f'Updated {os.path.basename(RESULTS)} written')


if __name__ == '__main__':
    enrich()
