#!/usr/bin/env python3
"""Render the triaged news digest as a static HTML page (docs/digest.html),
styled to match the IOC dashboard."""
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "docs" / "digest.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Africa/SADC Threat Intel Digest</title>
<style>
  :root {{ --bg:#0b0f14; --panel:#121822; --border:#232c3a; --text:#e6edf3; --muted:#8b96a5; --accent:#4fc3f7; --danger:#f47174; --ok:#4caf50; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text); font-family:-apple-system,Segoe UI,Roboto,sans-serif; padding:32px 16px; }}
  .wrap {{ max-width:900px; margin:0 auto; }}
  h1 {{ font-size:1.6rem; margin:0 0 4px; }}
  h2 {{ font-size:1.1rem; margin:32px 0 12px; }}
  .sub {{ color:var(--muted); font-size:0.9rem; margin-bottom:28px; }}
  .card {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:16px; margin-bottom:14px; }}
  .card h3 {{ margin:0 0 6px; font-size:1rem; line-height:1.4; }}
  .card h3 a {{ color:var(--text); text-decoration:none; }}
  .card h3 a:hover {{ color:var(--accent); }}
  .meta {{ color:var(--muted); font-size:0.78rem; margin-bottom:8px; }}
  .meta .src {{ color:var(--accent); }}
  .why {{ border-left:3px solid var(--ok); padding:6px 10px; margin:10px 0 0; color:var(--text); font-size:0.88rem; background:#10171f; border-radius:0 6px 6px 0; }}
  .why b {{ color:var(--ok); font-size:0.75rem; text-transform:uppercase; letter-spacing:.05em; }}
  .tag {{ display:inline-block; background:#1a2230; color:var(--muted); border-radius:4px; padding:2px 8px; font-size:0.72rem; margin-right:6px; margin-top:8px; }}
  .badge {{ display:inline-block; border-radius:4px; padding:2px 8px; font-size:0.72rem; font-weight:600; margin-left:8px; vertical-align:middle; }}
  .badge.vulnerability {{ background:#3a2b12; color:#f5b04c; }}
  .badge.breach {{ background:#3a1216; color:var(--danger); }}
  .badge.ransomware {{ background:#3a1216; color:var(--danger); }}
  .badge.phishing {{ background:#3a2b12; color:#f5b04c; }}
  .badge.policy_regulation {{ background:#12283a; color:var(--accent); }}
  .badge.infrastructure {{ background:#12283a; color:var(--accent); }}
  .badge.tooling {{ background:#152b1c; color:var(--ok); }}
  .badge.other {{ background:#1a2230; color:var(--muted); }}
  .count {{ color:var(--muted); font-size:0.85rem; }}
  footer {{ margin-top:32px; color:var(--muted); font-size:0.78rem; }}
  a {{ color:var(--accent); }}
  code {{ background:#1a2230; padding:2px 6px; border-radius:4px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🛰️ Africa/SADC Threat Intel Digest</h1>
  <div class="sub">Weekly triage of cybersecurity news for IT/security staff at African organizations. Updated {generated_at} UTC &middot; {counts}</div>

  <h2>Relevant this week</h2>
  {relevant_cards}

  <h2>Not relevant (filtered out)</h2>
  {other_cards}

  <footer>
    Triage via {backend_note} &middot; Sources: public RSS feeds &middot;
    Data: <code>data/triaged_news.json</code> &middot;
    <a href="index.html">IOC dashboard</a> &middot;
    <a href="https://github.com/Anayo-Anyafulu/mz-threat-feed">Source on GitHub</a>
  </footer>
</div>
</body>
</html>
"""

CARD = """<div class="card">
  <h3><a href="{link}">{title}</a><span class="badge {category}">{category}</span></h3>
  <div class="meta"><span class="src">{source}</span> &middot; {date}{countries} &middot; relevance: {relevance_reason}</div>
  <div>{summary}</div>
  {why_block}
  <div>{tags}</div>
</div>"""


def _esc(v) -> str:
    return html.escape(str(v or ""), quote=True)


def render_card(item: dict) -> str:
    t = item["triage"]
    why = t.get("why_it_matters_africa", "")
    why_block = (
        f'<div class="why"><b>Why it matters here</b><br>{_esc(why)}</div>'
        if why else ""
    )
    countries = t.get("countries") or []
    country_bit = f' &middot; {" ".join(_esc(c) for c in countries)}' if countries else ""
    tags = " ".join(f'<span class="tag">{_esc(tag)}</span>' for tag in t.get("suggested_tags", []))
    return CARD.format(
        link=_esc(item.get("link", "#")),
        title=_esc(item.get("title", "")),
        category=_esc(t.get("category", "other")),
        source=_esc(item.get("source", "")),
        date=_esc(item.get("date", "")),
        countries=country_bit,
        relevance_reason=_esc(t.get("relevance_reason", "")),
        summary=_esc(t.get("summary", "")),
        why_block=why_block,
        tags=tags,
    )


def main():
    items = json.loads((DATA / "triaged_news.json").read_text()) if (DATA / "triaged_news.json").exists() else []
    relevant = [i for i in items if i["triage"]["relevant"]]
    others = [i for i in items if not i["triage"]["relevant"]]

    backends = {i.get("backend", "heuristic") for i in items}
    backend_note = " + ".join(sorted(backends)) if backends else "no data"

    html_out = TEMPLATE.format(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        counts=f"{len(relevant)} relevant of {len(items)} triaged",
        relevant_cards="\n".join(render_card(i) for i in relevant)
            or '<div class="card">No relevant stories this week.</div>',
        other_cards="\n".join(render_card(i) for i in others)
            or '<div class="card">Nothing was filtered out.</div>',
        backend_note=backend_note,
    )

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html_out)
    print(f"Wrote {OUT} ({len(relevant)} relevant / {len(items)} total)")


if __name__ == "__main__":
    main()
