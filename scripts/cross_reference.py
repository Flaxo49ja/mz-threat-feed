#!/usr/bin/env python3
"""Cross-reference IOCs against Mozambican ASN IP ranges.
Output: data/matches.json -> IOCs whose IP falls inside a MZ-registered prefix.
"""
import ipaddress
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IOCS = ROOT / "data" / "iocs.json"
PREFIXES = ROOT / "data" / "mz_prefixes.json"
OUT = ROOT / "data" / "matches.json"

DNS_TIMEOUT = 3.0   # seconds per resolution
MAX_WORKERS = 20


def load_networks():
    entries = json.loads(PREFIXES.read_text())
    networks = []
    for e in entries:
        for cidr in e["prefixes"]:
            try:
                networks.append((ipaddress.ip_network(cidr), e["asn"], e["name"]))
            except ValueError:
                continue
    return networks


def resolve_to_ip(ioc: str) -> str | None:
    try:
        ipaddress.ip_address(ioc)
        return ioc  # already an IP, no DNS needed
    except ValueError:
        pass
    try:
        return socket.gethostbyname(ioc)
    except OSError:
        return None


def main():
    networks = load_networks()
    iocs = json.loads(IOCS.read_text())
    print(f"Checking {len(iocs)} IOCs against {len(networks)} MZ prefixes...")

    # gethostbyname is a blocking libc call with no timeout parameter, so run
    # resolutions in a bounded pool: 20 workers x 3s socket timeout keeps a
    # dead resolver from stalling the daily cron.
    socket.setdefaulttimeout(DNS_TIMEOUT)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        resolved = list(pool.map(resolve_to_ip, (e["ioc"] for e in iocs)))

    matches = []
    for ioc_entry, ip_str in zip(iocs, resolved):
        if not ip_str:
            continue
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        for network, asn, name in networks:
            if ip_obj in network:
                matches.append({**ioc_entry, "resolved_ip": ip_str, "matched_asn": asn, "matched_org": name})
                break

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(matches, indent=2))
    print(f"Wrote {OUT} ({len(matches)} matches found in Mozambican IP space)")


if __name__ == "__main__":
    main()
