#!/usr/bin/env python3
"""Fetch recent cybersecurity headlines from RSS/Atom feeds.

Output: data/news.json -> [{title, link, source, date, excerpt}]
Stdlib only. Tolerates broken XML with per-feed try/except.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "news_feeds.json"
OUT = ROOT / "data" / "news.json"

MAX_PER_FEED = 15
MAX_AGE_DAYS = 7
MAX_EXCERPT = 600

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean_html(text: str) -> str:
    """Strip tags/entities crudely and collapse whitespace."""
    text = TAG_RE.sub(" ", text or "")
    for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        text = text.replace(ent, ch)
    return WS_RE.sub(" ", text).strip()


def parse_date(raw: str) -> str:
    try:
        return parsedate_to_datetime(raw).astimezone(timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return (datetime.now(timezone.utc).strftime("%Y-%m-%d"))


def entry_text(node, path: str) -> str:
    el = node.find(path)
    return el.text if el is not None and el.text else ""


def parse_feed(xml_bytes: bytes, source: str) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    items = []
    for e in entries[:MAX_PER_FEED]:
        # RSS vs Atom field names differ; check both.
        title = entry_text(e, "title") or entry_text(e, "{http://www.w3.org/2005/Atom}title")
        link = entry_text(e, "link") or next(
            (l.get("href") for l in e.findall("{http://www.w3.org/2005/Atom}link") if l.get("href")), "")
        desc = (entry_text(e, "description")
                or entry_text(e, "{http://www.w3.org/2005/Atom}summary")
                or entry_text(e, "{http://www.w3.org/2005/Atom}content"))
        date_raw = (entry_text(e, "pubDate") or entry_text(e, "{http://www.w3.org/2005/Atom}updated")
                    or entry_text(e, "{http://www.w3.org/2005/Atom}published"))
        if not title:
            continue
        items.append({
            "title": title.strip(),
            "link": link.strip(),
            "source": source,
            "date": parse_date(date_raw),
            "excerpt": clean_html(desc)[:MAX_EXCERPT],
        })
    return items


def fetch_feed(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "mz-threat-feed/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read()
    except Exception as e:
        print(f"  fetch failed: {e}")
        return None


def main():
    feeds = json.loads(CONFIG.read_text())["feeds"]
    all_items = []
    for f in feeds:
        print(f"Fetching {f['name']}...")
        body = fetch_feed(f["url"])
        if body is None:
            continue
        try:
            items = parse_feed(body, f["name"])
        except ET.ParseError as e:
            print(f"  parse failed: {e}")
            continue
        print(f"  {len(items)} items")
        all_items.extend(items)

    # Filter stale items and dedupe by normalized title.
    cutoff = datetime.now(timezone.utc).timestamp() - MAX_AGE_DAYS * 86400
    seen_titles = set()
    fresh = []
    for it in all_items:
        try:
            ts = datetime.strptime(it["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
            if ts < cutoff:
                continue
        except ValueError:
            pass
        key = re.sub(r"[^a-z0-9]+", "", it["title"].lower())
        if key in seen_titles:
            continue
        seen_titles.add(key)
        fresh.append(it)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(fresh, indent=2))
    print(f"\nWrote {OUT} ({len(fresh)} items from {len(feeds)} feeds, {MAX_AGE_DAYS}-day window)")


if __name__ == "__main__":
    main()
