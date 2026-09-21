#!/usr/bin/env python3
"""Pull malicious IP/domain IOCs from free threat-intel feeds.
- URLhaus: no API key needed, pulls recent malicious URLs -> extracts host/IP.
- AbuseIPDB: needs ABUSEIPDB_API_KEY env var (free tier: 1000 checks/day, blacklist endpoint).
Output: data/iocs.json -> [{ioc, type, source, first_seen, tags}]
"""
import csv
import io
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "iocs.json"

URLHAUS_CSV = "https://urlhaus.abuse.ch/downloads/csv_recent/"
ABUSEIPDB_BLACKLIST = "https://api.abuseipdb.com/api/v2/blacklist"


def _parse_urlhaus(raw: str) -> list[dict]:
    """Parse the URLhaus CSV dump.

    The dump starts with '#' comment lines, one of which is a column header
    (e.g. '# id,dateadded,url,url_status,last_online,threat,tags,...'). The
    column set has changed over time (last_online/link/reporter added), so we
    map fields by header name instead of fixed positions. If the header is
    missing we fall back to picking the URL field by its 'http' prefix.
    """
    header = None
    for line in raw.splitlines():
        if line.startswith("#"):
            stripped = line.lstrip("# ").strip()
            if stripped.startswith("id,"):
                header = [c.strip() for c in stripped.split(",")]
            continue
        if line.strip():
            break  # header comments come before data rows

    iocs = []
    for row in csv.reader(l for l in raw.splitlines() if l and not l.startswith("#")):
        if header and len(row) == len(header):
            rec = dict(zip(header, row))
            dateadded = rec.get("dateadded", "")
            url = rec.get("url", "")
            tags = rec.get("tags", "")
        else:
            if len(row) < 3:
                continue
            dateadded = row[1] if len(row) > 1 else ""
            url = next((f for f in row if f.startswith("http")), "")
            tags = ""  # tags column position unknown without header; not displayed anyway
        if not url or "://" not in url:
            continue
        host = url.split("/")[2]
        host = host.split(":")[0]  # strip port
        iocs.append({
            "ioc": host,
            "type": "domain_or_ip",
            "source": "urlhaus",
            "first_seen": dateadded,
            "tags": tags,
        })
    return iocs


def fetch_urlhaus() -> list[dict]:
    req = urllib.request.Request(URLHAUS_CSV, headers={"User-Agent": "mz-threat-feed/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    return _parse_urlhaus(raw)


def fetch_abuseipdb() -> list[dict]:
    key = os.environ.get("ABUSEIPDB_API_KEY")
    if not key:
        print("ABUSEIPDB_API_KEY not set, skipping AbuseIPDB")
        return []
    req = urllib.request.Request(
        ABUSEIPDB_BLACKLIST + "?confidenceMinimum=90",
        headers={"Key": key, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    iocs = []
    for entry in data.get("data", []):
        iocs.append({
            "ioc": entry["ipAddress"],
            "type": "ip",
            "source": "abuseipdb",
            "first_seen": None,
            "tags": f"score={entry.get('abuseConfidenceScore')}",
        })
    return iocs


def main():
    all_iocs = []
    try:
        urlhaus_iocs = fetch_urlhaus()
        print(f"URLhaus: {len(urlhaus_iocs)} IOCs")
        all_iocs.extend(urlhaus_iocs)
    except Exception as e:
        print(f"URLhaus fetch failed: {e}")

    try:
        abuse_iocs = fetch_abuseipdb()
        print(f"AbuseIPDB: {len(abuse_iocs)} IOCs")
        all_iocs.extend(abuse_iocs)
    except Exception as e:
        print(f"AbuseIPDB fetch failed: {e}")

    # Dedupe on (ioc, source): the same host appears in many URLs/entries,
    # and duplicates would inflate counts and DNS work downstream.
    seen = set()
    deduped = []
    for ioc in all_iocs:
        key = (ioc["ioc"], ioc["source"])
        if key not in seen:
            seen.add(key)
            deduped.append(ioc)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(deduped, indent=2))
    print(f"\nWrote {OUT} ({len(deduped)} unique IOCs, {len(all_iocs) - len(deduped)} duplicates dropped)")


if __name__ == "__main__":
    main()
