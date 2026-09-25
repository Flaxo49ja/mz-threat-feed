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
<title>MZ Threat Feed — a security bulletin for the SADC region</title>
<meta name="description" content="Daily threat-intel bulletin for the SADC region: IOCs checked against local IP space, security news triaged for small IT teams.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..600&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{ --paper:#faf7f0; --paper-raised:#fffdf8; --paper-sunk:#f1ece0; --ink:#1f2a24; --ink-soft:#4c594f; --ink-faint:#7d877e; --oxide:#b3402a; --slate-line:#d8d2c2; --slate-strong:#a9a28e; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--paper); color:var(--ink); font-family:'Public Sans',-apple-system,'Segoe UI',sans-serif; padding:32px 16px; -webkit-font-smoothing:antialiased; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  h1 {{ font-family:'Newsreader',Georgia,serif; font-weight:500; letter-spacing:-0.02em; font-size:1.9rem; margin:0 0 4px; }}
  .kicker {{ font-family:'IBM Plex Mono',monospace; font-size:0.78rem; text-transform:uppercase; letter-spacing:.14em; color:var(--oxide); margin:0 0 10px; }}
  .sub {{ color:var(--ink-soft); font-size:0.95rem; margin-bottom:28px; max-width:44rem; line-height:1.55; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1px; background:var(--slate-line); border:1px solid var(--slate-line); margin-bottom:28px; }}
  .stat {{ background:var(--paper-raised); padding:18px; }}
  .stat .n {{ font-family:'IBM Plex Mono',monospace; font-variant-numeric:tabular-nums; font-size:1.9rem; font-weight:500; line-height:1.1; }}
  .stat .l {{ color:var(--oxide); font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-top:8px; }}
  .stat .note {{ color:var(--ink-soft); font-size:0.8rem; margin-top:4px; }}
  .match .n {{ color:var(--oxide); }}
  h2 {{ font-family:'Newsreader',Georgia,serif; font-weight:500; letter-spacing:-0.02em; font-size:1.35rem; margin:0 0 12px; }}
  table {{ width:100%; border-collapse:collapse; background:var(--paper-raised); border:1px solid var(--ink); }}
  th, td {{ padding:9px 12px; text-align:left; font-size:0.83rem; border-bottom:1px solid var(--slate-line); }}
  th {{ background:var(--paper-sunk); color:var(--ink-soft); text-transform:uppercase; font-size:0.7rem; font-weight:600; letter-spacing:.1em; border-bottom:1px solid var(--ink); }}
  tbody tr:nth-child(even) {{ background:var(--paper-raised); }}
  tbody tr:nth-child(odd) {{ background:var(--paper); }}
  tbody tr:last-child td {{ border-bottom:none; }}
  td.num, th.num {{ font-family:'IBM Plex Mono',monospace; font-variant-numeric:tabular-nums; }}
  .empty {{ padding:24px; text-align:center; color:var(--ink-faint); background:var(--paper-raised); border:1px solid var(--slate-line); }}
  footer {{ margin-top:28px; padding-top:14px; border-top:1px solid var(--slate-line); color:var(--ink-faint); font-size:0.78rem; }}
  code {{ font-family:'IBM Plex Mono',monospace; font-size:0.9em; background:var(--paper-sunk); padding:2px 6px; }}
  a {{ color:var(--oxide); }}
</style>
</head>
<body>
<div class="wrap">
  <p class="kicker">MZ Threat Feed</p>
  <h1>MZ Threat Feed — SADC regional security bulletin</h1>
  <div class="sub">Open, reproducible IOC feed cross-referenced against IP space announced across the SADC region — {n_countries} countries, updated daily. Alongside it, a weekly digest triages security news for small IT teams across the region. <a href="ui/">Open the full dashboard &rarr;</a></div>

  <div class="stats">
    <div class="stat"><div class="n">{total_iocs}</div><div class="l">IOCs pulled</div><div class="note">URLhaus and AbuseIPDB, deduplicated</div></div>
    <div class="stat"><div class="n">{total_prefixes}</div><div class="l">prefixes tracked</div><div class="note">{n_countries} SADC countries, per RIPEstat</div></div>
    <div class="stat match"><div class="n">{total_matches}</div><div class="l">Matches in SADC space</div><div class="note">leads, not verdicts — check your logs</div></div>
  </div>

  <h2>Matches</h2>
  {matches_table}

  <footer>
    Updated {generated_at} UTC &middot; Sources: URLhaus, AbuseIPDB (free tiers) &middot; SADC prefixes via RIPEstat &middot;
    Data: <code>data/iocs.json</code>, <code>data/matches.json</code> &middot;
    <a href="https://github.com/Anayo-Anyafulu/mz-threat-feed">Source on GitHub</a>
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
        matches_table = f"<table><thead><tr><th>IOC</th><th>Resolved IP</th><th>Network</th><th>Country</th><th>Source</th><th>First Seen</th></tr></thead><tbody>{rows}</tbody></table>"
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
