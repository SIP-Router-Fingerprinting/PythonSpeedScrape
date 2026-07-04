#!/usr/bin/env python3
import csv
import ipaddress
import os
import sys

HERE = os.path.dirname(__file__) or '.'
RESULTS_PATH = os.path.join(HERE, 'results.csv')
IPINFO_PATH = os.path.join(HERE, 'ipinfo_lite.csv')
ENRICHED_PATH = os.path.join(HERE, 'results_enriched.csv')
TEMP_PATH = os.path.join(HERE, 'results_enriched.csv.tmp')
BACKUP_PATH = os.path.join(HERE, 'results_enriched.csv.bak')

INFO_FIELDS = ['country', 'country_code', 'continent', 'continent_code', 'asn', 'as_name', 'as_domain']
FIELDNAMES = ['ip', 'status'] + INFO_FIELDS


def load_existing_enriched(path):
    existing = {}
    if not os.path.exists(path):
        return existing
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ip = (row.get('ip') or row.get('IP') or '').strip()
            if not ip:
                continue
            existing[ip] = {
                'status': (row.get('status') or row.get('Status') or '').strip(),
                **{field: (row.get(field) or '').strip() for field in INFO_FIELDS}
            }
    return existing


def build_network_map(path):
    nets = {}
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            network = (row.get('network') or '').strip()
            if not network:
                continue
            try:
                net = ipaddress.ip_network(network, strict=False)
            except Exception:
                continue
            if net.version != 4:
                continue
            prefix = net.prefixlen
            network_int = int(net.network_address)
            data = {field: (row.get(field) or '').strip() for field in INFO_FIELDS}
            nets.setdefault(prefix, {})[network_int] = data
    if not nets:
        raise RuntimeError('No valid IPv4 networks loaded from ipinfo_lite.csv')
    return nets


def build_masks(prefixes):
    masks = {}
    for prefix in prefixes:
        if prefix == 0:
            masks[prefix] = 0
        else:
            masks[prefix] = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return masks


def lookup_ip(ip_text, nets, masks, sorted_prefixes):
    try:
        ip_obj = ipaddress.ip_address(ip_text.strip())
    except Exception:
        return None
    if ip_obj.version != 4:
        return None
    ip_int = int(ip_obj)
    for prefix in sorted_prefixes:
        key = ip_int & masks[prefix]
        data = nets[prefix].get(key)
        if data is not None:
            return data
    return None


def main():
    if not os.path.exists(RESULTS_PATH):
        print('Error: results.csv not found.', file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(IPINFO_PATH):
        print('Error: ipinfo_lite.csv not found.', file=sys.stderr)
        sys.exit(1)

    print('Loading existing enriched rows...')
    existing_enriched = load_existing_enriched(ENRICHED_PATH)
    print(f'Existing enriched IPs: {len(existing_enriched)}')

    print('Loading IP network map...')
    nets = build_network_map(IPINFO_PATH)
    sorted_prefixes = sorted(nets.keys(), reverse=True)
    masks = build_masks(sorted_prefixes)
    print(f'Loaded {sum(len(v) for v in nets.values())} IPv4 prefix entries')

    total = 0
    appended = 0
    matched_existing = 0
    unmatched = 0

    with open(RESULTS_PATH, newline='', encoding='utf-8-sig') as results_file, \
         open(TEMP_PATH, 'w', newline='', encoding='utf-8') as temp_file:

        results_reader = csv.DictReader(results_file)
        writer = csv.DictWriter(temp_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in results_reader:
            total += 1
            ip = (row.get('ip') or row.get('IP') or '').strip()
            status = (row.get('status') or row.get('Status') or '').strip()
            if not ip:
                continue

            if ip in existing_enriched:
                record = existing_enriched[ip]
                # preserve existing status unless original row is blank
                status = status or record.get('status', '')
                writer.writerow({
                    'ip': ip,
                    'status': status,
                    **record
                })
                matched_existing += 1
                continue

            enrich_data = lookup_ip(ip, nets, masks, sorted_prefixes)
            if enrich_data is None:
                enrich_data = {field: '' for field in INFO_FIELDS}
                unmatched += 1
            writer.writerow({
                'ip': ip,
                'status': status,
                **enrich_data
            })
            appended += 1

    print(f'Total results rows processed: {total}')
    print(f'Existing enriched rows reused: {matched_existing}')
    print(f'New rows added: {appended}')
    print(f'Unmatched rows: {unmatched}')

    if os.path.exists(BACKUP_PATH):
        os.remove(BACKUP_PATH)
    if os.path.exists(ENRICHED_PATH):
        os.replace(ENRICHED_PATH, BACKUP_PATH)
    os.replace(TEMP_PATH, ENRICHED_PATH)

    print(f'Updated enriched file written to {ENRICHED_PATH}')
    print(f'Backup of previous enriched file written to {BACKUP_PATH}')


if __name__ == '__main__':
    main()
