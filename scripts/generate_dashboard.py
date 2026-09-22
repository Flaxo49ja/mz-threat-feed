#!/usr/bin/env python3
"""Renders a self-contained static HTML dashboard from data/*.json."""
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PREFIXES_FILE = DATA / "prefixes.json"
LEGACY_PREFIXES = DATA / "mz_prefixes.json"
OUT = ROOT / "docs" / "index.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mozambique Threat Intel Feed</title>
<style>
  :root {{ --bg:#0b0f14; --panel:#121822; --border:#232c3a; --text:#e6edf3; --muted:#8b96a5; --accent:#4fc3f7; --danger:#f47174; --ok:#4caf50; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text); font-family:-apple-system,Segoe UI,Roboto,sans-serif; padding:32px 16px; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  h1 {{ font-size:1.6rem; margin:0 0 4px; }}
  .sub {{ color:var(--muted); font-size:0.9rem; margin-bottom:28px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-bottom:28px; }}
  .stat {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:16px; }}
  .stat .n {{ font-size:1.8rem; font-weight:700; }}
  .stat .l {{ color:var(--muted); font-size:0.8rem; text-transform:uppercase; letter-spacing:.04em; }}
  .match .n {{ color:var(--danger); }}
  table {{ width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--border); border-radius:10px; overflow:hidden; }}
  th, td {{ padding:10px 12px; text-align:left; font-size:0.85rem; border-bottom:1px solid var(--border); }}
  th {{ color:var(--muted); text-transform:uppercase; font-size:0.72rem; letter-spacing:.04em; }}
  tr:last-child td {{ border-bottom:none; }}
  .empty {{ padding:24px; text-align:center; color:var(--muted); }}
  footer {{ margin-top:28px; color:var(--muted); font-size:0.78rem; }}
  code {{ background:#1a2230; padding:2px 6px; border-radius:4px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🇲🇿 Mozambique Threat Intel Feed</h1>
  <div class="sub">Open, reproducible IOC feed cross-referenced against Mozambican ISP/network IP space. Updated {generated_at} UTC.</div>

  <div class="stats">
    <div class="stat"><div class="n">{total_iocs}</div><div class="l">IOCs pulled</div></div>
    <div class="stat"><div class="n">{total_prefixes}</div><div class="l">prefixes tracked ({n_countries} countries)</div></div>
    <div class="stat match"><div class="n">{total_matches}</div><div class="l">Matches in MZ space</div></div>
  </div>

  <h2>Matches</h2>
  {matches_table}

  <footer>
    Sources: URLhaus, AbuseIPDB (free tiers) &middot; MZ prefixes via RIPEstat &middot;
    Data: <code>data/iocs.json</code>, <code>data/matches.json</code> &middot;
    <a href="https://github.com/Anayo-Anyafulu/mz-threat-feed" style="color:var(--accent)">Source on GitHub</a>
  </footer>
</div>
</body>
</html>
"""

ROW = """<tr><td>{ioc}</td><td>{resolved_ip}</td><td>{matched_org}</td><td>{matched_country}</td><td>{source}</td><td>{first_seen}</td></tr>"""


def _esc(value) -> str:
    """Escape a feed-sourced value before it hits the HTML template.
    IOC hosts/tags come straight from external feeds, so treat as untrusted."""
    if value is None:
        return "-"
    return html.escape(str(value), quote=True)


def main():
    iocs = json.loads((DATA / "iocs.json").read_text()) if (DATA / "iocs.json").exists() else []
    pfile = PREFIXES_FILE if PREFIXES_FILE.exists() else LEGACY_PREFIXES
    prefixes = json.loads(pfile.read_text()) if pfile.exists() else []
    matches = json.loads((DATA / "matches.json").read_text()) if (DATA / "matches.json").exists() else []

    total_prefixes = sum(len(p["prefixes"]) for p in prefixes)
    n_countries = len({p.get("code", "MZ") for p in prefixes})

    if matches:
        rows = "\n".join(
            ROW.format(
                ioc=_esc(m.get("ioc")),
                resolved_ip=_esc(m.get("resolved_ip")),
                matched_org=_esc(m.get("matched_org")),
                matched_country=_esc(m.get("matched_country", "MZ")),
                source=_esc(m.get("source")),
                first_seen=_esc(m.get("first_seen")),
            )
            for m in matches
        )
        matches_table = f"<table><tr><th>IOC</th><th>Resolved IP</th><th>Network</th><th>Country</th><th>Source</th><th>First Seen</th></tr>{rows}</table>"
    else:
        matches_table = '<div class="empty">No IOCs currently overlap tracked SADC IP space.</div>'

    html = TEMPLATE.format(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        total_iocs=len(iocs),
        total_prefixes=total_prefixes,
        total_matches=len(matches),
        n_countries=n_countries,
        matches_table=matches_table,
    )

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
