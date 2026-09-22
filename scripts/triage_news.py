#!/usr/bin/env python3
"""Triage news headlines for the Africa/SADC threat-intel digest.

Two backends:
1. LLM (if DIGEST_LLM_API_KEY is set): calls an OpenAI-compatible API using
   the triage prompt below verbatim as the system message.
2. Heuristic fallback (no keys needed): deterministic keyword rules encoding
   the same criteria, tuned conservative (uncertain -> not relevant).

Output: data/triaged_news.json, one record per article with the exact JSON
schema from the triage prompt.
"""
import json
import os
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN = ROOT / "data" / "news.json"
SEEN = ROOT / "data" / "seen_links.json"
OUT = ROOT / "data" / "triaged_news.json"

MAX_LLM_ARTICLES = 40
LLM_DELAY_S = 0.5

SYSTEM_PROMPT = """You are a cybersecurity news triage assistant for a threat-intel digest \
focused on Africa, with emphasis on Mozambique and the SADC region.

You will be given one news article (title, source, date, excerpt). Decide \
whether it is relevant to this audience: IT/security staff at African \
organizations — governments, banks, universities, SMEs, ISPs — who \
typically run legacy systems, have small or no dedicated security teams, \
and face resource constraints.

Relevance criteria (mark relevant if ANY apply):
- Directly mentions Africa, an African country, or an African \
organization/company as a victim, target, or subject
- Describes a vulnerability, misconfiguration, or attack technique common \
in under-resourced environments (legacy CMS, unpatched software, weak \
TLS/header config, exposed admin panels, default credentials, phishing \
targeting financial/government sectors)
- Covers a widely-used product/platform likely deployed in the region \
(WordPress, cPanel, common banking software, telecom infrastructure, \
widely used open-source tools)
- Is a major global incident with lessons directly transferable to \
low-resource defenders (e.g. a technique cheap to defend against)

Mark NOT relevant if the article is: a vendor product announcement with no \
broader lesson, a purely US/EU-enterprise story with no transferable \
takeaway (e.g. a Fortune 500-specific compliance fine), stock/financial \
market news, or a duplicate of a story already covered.

For each article, respond with ONLY this JSON, no other text:
{
  "relevant": true | false,
  "relevance_reason": "one sentence: why this matters (or doesn't) for the target audience",
  "category": "one of: vulnerability | breach | ransomware | phishing | policy_regulation | infrastructure | tooling | other",
  "summary": "2-3 sentence neutral summary of what happened, in plain language, no jargon left unexplained",
  "why_it_matters_africa": "1-2 sentences, ONLY if relevant=true: concrete action or risk relevant to a small/under-resourced org. Leave empty string if relevant=false.",
  "suggested_tags": ["short", "keyword", "tags"]
}

Be conservative: when uncertain, mark relevant=false rather than padding the \
digest with generic global news that has no clear African-context angle. \
Never fabricate an Africa-specific angle that isn't supported by the article \
content — if you can't honestly justify why_it_matters_africa, mark it \
relevant=false instead of inventing a connection."""

# ---------------------------------------------------------------------------
# Heuristic fallback
# ---------------------------------------------------------------------------

AFRICA_TERMS = [
    "africa", "african", "sadc", "mozambique", "mozambican", "south africa",
    "kenya", "nigeria", "egypt", "ghana", "angola", "tanzania", "uganda",
    "zambia", "zimbabwe", "botswana", "namibia", "lesotho", "eswatini",
    "malawi", "rwanda", "ethiopia", "senegal", "ivory coast", "morocco",
    "algeria", "tunisia", "libya", "sudan", "somalia", "johannesburg",
    "nairobi", "lagos", "cairo", "cape town", "pretoria", "maputo",
    "joburg", "joburgb", "gaborone", "lusaka", "harare",
]

PLATFORM_TERMS = [
    "wordpress", "cpanel", "joomla", "drupal", "moodle", "exchange server",
    "microsoft exchange", "fortinet", "fortigate", "sophos", "mikrotik",
    "cisco", "pfsense", "citrix", "vpn", "apache", "nginx", "tomcat",
    "vmware", "vcenter", "esxi", "coldfusion", "sharepoint", "oracle", "mysql",
    "postgres", "zimbra", "roundcube", "atlassian", "confluence",
    "jira", "gitlab", "jenkins", "craft cms", "linux", "windows", "android",
    "ios", "macos", "chrome", "firefox", "safari", "outlook", "microsoft 365",
    "office 365", "entra", "azure", "aws", "google workspace", "zyxel",
    "veeam", "solarwinds", "qnap", "d-link", "tp-link", "netgear", "draytek",
    "ivanti", "npm", "pypi", "docker", "kubernetes", "openssh", "openvpn",
    "nextcloud", "bigcommerce", "shopify", "magento", "powershell", "php",
    "python", "java", "rust", "struts", "log4j", "smb", "samba",
]

TECHNIQUE_TERMS = [
    "sql injection", "xss", "cross-site", "rce", "remote code",
    "zero-day", "zero day", "actively exploited", "active exploitation",
    "exploited", "exploitation", "in the wild", "cve-",
    "ransomware", "phishing", "business email compromise", "bec ", "botnet",
    "ddos", "malware", "backdoor", "credential", "password spray",
    "default credentials", "brute force", "data breach", "breach", "hacked",
    "defaced", "defacement", "unpatched", "misconfigur", "exposed",
    "apocalypse", "patch now", "update now", "attackers", "threat actors",
]

# General cybersecurity vocabulary: an article must show SOME security signal
# to be eligible, even if it names an African country (generic Africa news
# feeds publish politics/business stories that name countries constantly).
CYBER_TERMS = [
    "cyber", "cybersecurity", "infosec", "hacker", "hackers", "malware",
    "ransomware", "phishing", "data protection", "data breach", "vulnerability",
    "encryption", "spyware", "stolen data", "personal data", "gdpr", "ndpc",
    "computer emergency", "cert ", "csirt", "zero-day", "patch",
]

BUSINESS_TERMS = [
    "stock", "share price", "ipo", "earnings", "quarterly profit",
    "acquisition", "merger", "funding round", "valuation", "investment",
    "invests", "invested", "startup", "venture capital", "series a",
    "raises $", "raised $", "puts $", "fine", "fined", "sets sights",
    "builds", "expands cybersecurity", "partnership", "unveils", "launches",
    "confab", "conference", "summit", "webinar", "roundtable", "awards",
]

SECTOR_TERMS = [
    "bank", "banks", "financial", "fintech", "payment", "government",
    "ministry", "parliament", "municipal", "hospital", "healthcare",
    "school", "university", "telecom", "isp", "utility", "utilities",
]

CATEGORIES = (
    "vulnerability", "breach", "ransomware", "phishing",
    "policy_regulation", "infrastructure", "tooling", "other",
)


def _has_term(text: str, terms: list[str]) -> list[str]:
    found = []
    for t in terms:
        if re.search(r"\b" + re.escape(t.strip()), text):
            found.append(t.strip())
    return found


def heuristic_triage(article: dict) -> dict:
    title = article.get("title", "")
    excerpt = article.get("excerpt", "")
    text = f"{title} {excerpt}".lower()

    africa = _has_term(text, AFRICA_TERMS)
    platforms = _has_term(text, PLATFORM_TERMS)
    techniques = _has_term(text, TECHNIQUE_TERMS)
    cyber = _has_term(text, CYBER_TERMS)
    business = _has_term(text, BUSINESS_TERMS)

    # A concrete technique/CVE mention counts as substance; a bare "cybersecurity"
    # mention does not when the story is really industry/business news.
    has_security_signal = bool(techniques) or (bool(cyber) and not business)

    if business and not techniques:
        # Industry/funding/politics story. An African country name or the word
        # "cybersecurity" alone is not enough — general Africa feeds name
        # countries and companies in every other headline.
        relevant = False
        reason = ("Industry, business, or political news with no vulnerability, "
                  "incident, or technique defenders can act on.")
    elif africa and has_security_signal:
        relevant = True
        reason = ("Security story involving " + ", ".join(africa[:2]) +
                  ", directly relevant to the region.")
    elif techniques and platforms:
        relevant = True
        reason = ("Affects " + ", ".join(platforms[:2]) + " — widely deployed "
                  "in under-resourced organizations — via " +
                  (", ".join(techniques[:2]) or "a known attack technique") + ".")
    elif techniques and _has_term(text, SECTOR_TERMS):
        relevant = True
        reason = ("Attack activity against " +
                  ", ".join(_has_term(text, SECTOR_TERMS)[:2]) +
                  "-sector organizations, the same targets common across SADC.")
    else:
        relevant = False
        reason = ("No African angle, and no widely-deployed-platform issue "
                  "with a transferable lesson for low-resource defenders.")

    # Category from strongest signal (word-bounded matching; substring checks
    # misfired, e.g. 'exact ' matching the pattern 'act ').
    if relevant:
        joined = " ".join(techniques)
        if "ransomware" in joined:
            cat = "ransomware"
        elif "phish" in joined or "business email compromise" in joined:
            cat = "phishing"
        elif any(k in joined for k in ("cve-", "zero-day", "zero day", "sql injection", "rce", "remote code", "xss", "unpatched", "exploited", "exploitation")):
            cat = "vulnerability"
        elif "breach" in joined or "hacked" in joined or "leak" in joined:
            cat = "breach"
        elif _has_term(text, ["regulat", "law", "act", "policy", "compliance", "gdpr", "data protection"]):
            cat = "policy_regulation"
        elif _has_term(text, ["isp", "undersea cable", "dns", "bgp", "telecom", "internet shutdown", "power grid"]):
            cat = "infrastructure"
        else:
            cat = "other"
    else:
        cat = "other"

    # Summary: reuse the excerpt's first sentences (heuristic can't paraphrase).
    summary = excerpt or title
    sentences = re.split(r"(?<=[.!?])\s+", summary)
    summary = " ".join(sentences[:2])[:400].strip()

    if relevant:
        if africa:
            why = ("Regional story: organizations in " + (africa[0].title() if africa[0] not in ("africa", "african", "sadc") else "the region") +
                   " should check whether the described exposure or technique applies to their own systems.")
        else:
            why = ("If you run " + (platforms[0] if platforms else "affected software") +
                   ", verify you are on a patched version; unpatched instances are the "
                   "most common entry point for small teams without dedicated security staff.")
    else:
        why = ""

    tags = []
    if africa:
        tags.extend(africa[:2])
    tags.extend(platforms[:1])
    tags.extend(t.replace(" ", "-") for t in techniques[:2])
    tags = [t for t in tags if t and len(t) > 2][:5] or ["news"]

    return {
        "relevant": relevant,
        "relevance_reason": reason,
        "category": cat if cat in CATEGORIES else "other",
        "summary": summary,
        "why_it_matters_africa": why,
        "suggested_tags": tags,
    }


# ---------------------------------------------------------------------------
# LLM backend
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> dict | None:
    text = text.strip()
    # Strip markdown code fences if the model adds them.
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict) or "relevant" not in obj:
        return None
    return obj


def llm_triage(article: dict, base_url: str, key: str, model: str) -> dict | None:
    user_msg = (f"Title: {article.get('title','')}\n"
                f"Source: {article.get('source','')}\n"
                f"Date: {article.get('date','')}\n"
                f"Excerpt: {article.get('excerpt','')}")
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    }).encode()

    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        content = data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  LLM call failed: {e}")
        return None

    parsed = _extract_json(content)
    if parsed is None:
        print("  LLM returned unparseable JSON")
        return None
    # Normalize fields the schema requires.
    parsed["relevant"] = bool(parsed.get("relevant"))
    if parsed.get("category") not in CATEGORIES:
        parsed["category"] = "other"
    if not parsed.get("relevant"):
        parsed["why_it_matters_africa"] = ""
    parsed.setdefault("relevance_reason", "")
    parsed.setdefault("summary", "")
    parsed.setdefault("suggested_tags", [])
    return parsed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    articles = json.loads(IN.read_text()) if IN.exists() else []
    seen_links = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()

    api_key = os.environ.get("DIGEST_LLM_API_KEY", "")
    base_url = os.environ.get("DIGEST_LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("DIGEST_LLM_MODEL", "gpt-4o-mini")

    results = []
    new_links = []
    llm_used = 0
    for a in articles:
        link = a.get("link", "")
        if link and link in seen_links:
            continue  # already in a previous digest
        if link:
            new_links.append(link)

        verdict = None
        backend = "heuristic"
        if api_key and llm_used < MAX_LLM_ARTICLES:
            verdict = llm_triage(a, base_url, api_key, model)
            if verdict is not None:
                backend = "llm"
                llm_used += 1
                time.sleep(LLM_DELAY_S)
        if verdict is None:
            verdict = heuristic_triage(a)

        results.append({**a, "triage": verdict, "backend": backend})
        flag = "+" if verdict["relevant"] else "-"
        print(f"[{flag}] ({backend}) {a['title'][:70]}")

    SEEN.parent.mkdir(exist_ok=True)
    SEEN.write_text(json.dumps(sorted(set(new_links) | seen_links), indent=2))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    n_rel = sum(1 for r in results if r["triage"]["relevant"])
    print(f"\nWrote {OUT}: {len(results)} triaged ({n_rel} relevant, "
          f"{llm_used} via LLM, {len(results) - llm_used} heuristic)")


if __name__ == "__main__":
    main()
