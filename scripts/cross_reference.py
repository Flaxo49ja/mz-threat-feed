#!/usr/bin/env python3
"""Cross-reference IOCs against tracked SADC IP ranges.
Output: data/matches.json -> IOCs whose IP falls inside a tracked prefix,
with matched_asn, matched_org and matched_country attached.
"""
import ipaddress
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IOCS = ROOT / "data" / "iocs.json"
PREFIXES = ROOT / "data" / "prefixes.json"
LEGACY_PREFIXES = ROOT / "data" / "mz_prefixes.json"
OUT = ROOT / "data" / "matches.json"

DNS_TIMEOUT = 3.0   # seconds per resolution
MAX_WORKERS = 20


def load_networks():
    """Load (network, asn, org, country_code) tuples from the multi-country
    prefix file, with a legacy fallback to the MZ-only file."""
    path = PREFIXES if PREFIXES.exists() else LEGACY_PREFIXES
    entries = json.loads(path.read_text())
    networks = []
    for e in entries:
        code = e.get("code", "MZ")
        for cidr in e["prefixes"]:
            try:
                networks.append((ipaddress.ip_network(cidr), e["asn"], e["name"], code))
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
    countries = sorted({c for *_, c in networks})
    print(f"Checking {len(iocs)} IOCs against {len(networks)} prefixes in {len(countries)} countries ({', '.join(countries)})...")

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
        for network, asn, name, code in networks:
            if ip_obj in network:
                matches.append({**ioc_entry, "resolved_ip": ip_str, "matched_asn": asn,
                                "matched_org": name, "matched_country": code})
                break

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(matches, indent=2))
    by_cc = {}
    for m in matches:
        by_cc[m["matched_country"]] = by_cc.get(m["matched_country"], 0) + 1
    breakdown = ", ".join(f"{cc}: {n}" for cc, n in sorted(by_cc.items())) or "none"
    print(f"Wrote {OUT} ({len(matches)} matches — by country: {breakdown})")


if __name__ == "__main__":
    main()
