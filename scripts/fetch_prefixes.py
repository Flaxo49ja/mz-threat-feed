#!/usr/bin/env python3
"""Resolve tracked SADC ASNs to their currently announced IPv4 prefixes via RIPEstat.

Reads config/sadc_asns.json (multi-country). Output: data/prefixes.json ->
[{country, code, asn, name, prefixes: [cidr,...]}]

Kept compatible with the old single-country flow: if config/sadc_asns.json is
missing, falls back to config/mz_asns.json tagged as MZ.
"""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SADC_CONFIG = ROOT / "config" / "sadc_asns.json"
MZ_CONFIG = ROOT / "config" / "mz_asns.json"
OUT = ROOT / "data" / "prefixes.json"
LEGACY_OUT = ROOT / "data" / "mz_prefixes.json"
CACHE = ROOT / "data" / "prefix_cache.json"  # resume support for long runs

RIPESTAT_URL = "https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"


def fetch_prefixes(asn: str, retries: int = 3) -> list[str]:
    """Fetch announced IPv4 prefixes for one ASN, retrying transient failures.
    RIPEstat regularly hiccups (SSL handshakes, 5xx) and a failed fetch would
    silently zero out an entire network on the public ledger."""
    url = RIPESTAT_URL.format(asn=asn)
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mz-threat-feed/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
            prefixes = data.get("data", {}).get("prefixes", [])
            return [p["prefix"] for p in prefixes if ":" not in p["prefix"]]  # IPv4 only for MVP
        except Exception as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"gave up after {retries} attempts: {last_err}")


def load_entries():
    """Yield (code, country_name, asn, org) tuples from whichever config exists."""
    if SADC_CONFIG.exists():
        cfg = json.loads(SADC_CONFIG.read_text())
        for country in cfg["countries"]:
            for e in country["asns"]:
                yield country["code"], country["name"], e["asn"], e["name"]
    elif MZ_CONFIG.exists():
        for e in json.loads(MZ_CONFIG.read_text()):
            yield "MZ", "Mozambique", e["asn"], e["name"]


def main():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    results = []
    failed = []
    total_prefixes = 0
    for code, country, asn, name in load_entries():
        key = f"{code}/{asn}"
        if key in cache:
            prefixes = cache[key]
            print(f"[{code}] {asn} ({name}): {len(prefixes)} prefixes (cached)", flush=True)
        else:
            try:
                prefixes = fetch_prefixes(asn)
                print(f"[{code}] {asn} ({name}): {len(prefixes)} prefixes", flush=True)
                cache[key] = prefixes
                CACHE.write_text(json.dumps(cache))  # persist after each ASN, so a timeout costs nothing
            except Exception as e:
                print(f"[{code}] {asn} ({name}): FAILED - {e}", flush=True)
                prefixes = []
                failed.append(key)  # failures are NOT cached - a re-run must retry them
        total_prefixes += len(prefixes)
        results.append({
            "country": country,
            "code": code,
            "asn": asn,
            "name": name,
            "prefixes": prefixes,
        })
        time.sleep(1)  # be polite to RIPEstat

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))

    # Keep the legacy file in sync (MZ only) so older dashboards keep working.
    mz = [r for r in results if r["code"] == "MZ"]
    LEGACY_OUT.write_text(json.dumps(mz, indent=2))

    n_countries = len({r["code"] for r in results})
    print(f"\nWrote {OUT}: {total_prefixes} prefixes across "
          f"{len(results)} ASNs in {n_countries} countries")
    print(f"Synced {LEGACY_OUT} ({sum(len(r['prefixes']) for r in mz)} MZ prefixes)")
    if failed:
        print(f"WARNING: {len(failed)} ASNs failed all retries: {', '.join(failed)}")
        print("Their rows are empty this run - re-run before trusting the totals.")
    else:
        # Clean run: drop the cache so tomorrow's cron fetches fresh prefixes.
        CACHE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
