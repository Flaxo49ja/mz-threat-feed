# mz-threat-feed

Open, reproducible threat-intel feed for Mozambique. Pulls IOCs (malicious
IPs/domains) from free threat-intel sources, cross-references them against
IP space registered to Mozambican ISPs/networks, and publishes a daily
auto-updating dashboard via GitHub Pages.

Extends the regional-security-gap angle from the HTTP security header study:
same "underrepresented region, open reproducible tooling" approach, applied
to threat intel instead of header scanning.

## How it works

1. `scripts/fetch_prefixes.py` — resolves a list of Mozambican ASNs
   (Movitel, Vodacom Mocambique, TVCABO, Teledata, MoRENet, banks, etc.) into
   their currently announced IPv4 prefixes via [RIPEstat](https://stat.ripe.net)
   (free, no API key).
2. `scripts/fetch_iocs.py` — pulls recent malicious IOCs from
   [URLhaus](https://urlhaus.abuse.ch) (no key) and optionally
   [AbuseIPDB](https://www.abuseipdb.com) (free tier, needs API key).
3. `scripts/cross_reference.py` — resolves each IOC to an IP and checks
   whether it falls inside a tracked Mozambican prefix.
4. `scripts/generate_dashboard.py` — renders `docs/index.html`, a static
   dashboard showing totals and any matches.
5. `scripts/fetch_news.py` — pulls recent cybersecurity headlines from
   public RSS feeds (The Hacker News, BleepingComputer, SecurityWeek,
   Google News Africa-cyber search, The Africa Report, etc.) into
   `data/news.json`.
6. `scripts/triage_news.py` — triages each headline for relevance to
   IT/security staff at African organizations (governments, banks,
   universities, SMEs, ISPs), producing verdict JSON per article. Uses an
   OpenAI-compatible LLM if `DIGEST_LLM_API_KEY` is set (optionally with
   `DIGEST_LLM_BASE_URL` and `DIGEST_LLM_MODEL`); otherwise falls back to a
   conservative heuristic keyword classifier. Already-seen links
   (`data/seen_links.json`) are skipped across runs.
7. `scripts/generate_digest.py` — renders `docs/digest.html`, the weekly
   news digest page, linked from the dashboard.
8. `.github/workflows/update.yml` — runs the whole pipeline daily via
   GitHub Actions and publishes `docs/` to GitHub Pages.

## Local run

```bash
pip install -r requirements.txt   # stdlib only for now, kept for future deps
python scripts/fetch_prefixes.py
export ABUSEIPDB_API_KEY=your_key_here   # optional
python scripts/fetch_iocs.py
python scripts/cross_reference.py
python scripts/generate_dashboard.py
python scripts/fetch_news.py          # RSS headlines
python scripts/triage_news.py         # optional: export DIGEST_LLM_API_KEY first
python scripts/generate_digest.py
open docs/index.html docs/digest.html   # or: python -m http.server -d docs
```

## Deploy on GitHub

1. Push this repo to GitHub.
2. Settings → Pages → Build and deployment → Source: **GitHub Actions**.
3. (Optional) Settings → Secrets and variables → Actions → add
   `ABUSEIPDB_API_KEY` if you want AbuseIPDB coverage
   ([free signup](https://www.abuseipdb.com/register)).
4. Run the workflow once manually (Actions tab → Update Mozambique Threat
   Feed → Run workflow) or wait for the daily cron.

## Extending

- Add more ASNs to `config/mz_asns.json` as you find them (bgp.he.net,
  ip2location.com, ipinfo.io are good sources).
- Add AlienVault OTX as a third IOC source (needs free API key + pulse
  subscription) — same shape as `fetch_abuseipdb()` in `scripts/fetch_iocs.py`.
- News digest: for LLM-quality triage, add `DIGEST_LLM_API_KEY` (Actions
  secret) and optionally `DIGEST_LLM_BASE_URL` / `DIGEST_LLM_MODEL`
  (Actions variables) pointing at any OpenAI-compatible endpoint; without
  them the heuristic classifier runs, which is free but cruder.
- IPv6 prefix support is stubbed out (`fetch_prefixes.py` currently filters
  to IPv4 only).
- Cross-reference against your `header-study` site sample instead of/along
  with ASN ranges, to flag which scanned .mz sites' hosting IPs show up in
  threat feeds.
