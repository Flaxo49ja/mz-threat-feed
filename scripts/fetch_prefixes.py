#!/usr/bin/env python3
"""Resolve Mozambican ASNs to their currently announced IPv4 prefixes via RIPEstat.
No API key needed. Output: data/mz_prefixes.json -> [{asn, name, prefixes: [cidr,...]}]
"""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "mz_asns.json"
OUT = ROOT / "data" / "mz_prefixes.json"

RIPESTAT_URL = "https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"


def fetch_prefixes(asn: str) -> list[str]:
    url = RIPESTAT_URL.format(asn=asn)
    req = urllib.request.Request(url, headers={"User-Agent": "mz-threat-feed/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    prefixes = data.get("data", {}).get("prefixes", [])
    return [p["prefix"] for p in prefixes if ":" not in p["prefix"]]  # IPv4 only for MVP


def main():
    asns = json.loads(CONFIG.read_text())
    results = []
    for entry in asns:
        asn, name = entry["asn"], entry["name"]
        try:
            prefixes = fetch_prefixes(asn)
            print(f"{asn} ({name}): {len(prefixes)} prefixes")
        except Exception as e:
            print(f"{asn} ({name}): FAILED - {e}")
            prefixes = []
        results.append({"asn": asn, "name": name, "prefixes": prefixes})
        time.sleep(1)  # be polite to RIPEstat

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    total = sum(len(r["prefixes"]) for r in results)
    print(f"\nWrote {OUT} ({total} total prefixes across {len(results)} ASNs)")


if __name__ == "__main__":
    main()
