// Generated from the live pipeline run on 2026-09-22 09:10 UTC by scripts in ../scripts.
// Regenerate with: python3 scripts/export_ui_data.py (or ask Buffy to).
// Numbers here are real: prefix counts come from RIPEstat, IOC totals from
// the URLhaus/AbuseIPDB fetch, news verdicts from triage_news.py.

export interface AsnEntry {
  asn: string;
  org: string;
  prefixCount: number;
}

export interface Story {
  title: string;
  link: string;
  source: string;
  published: string;
  category: string;
  relevanceReason: string;
  whyItMatters: string;
  tags: string[];
}

export interface FilteredStory {
  title: string;
  source: string;
  reason: string;
}

export const lastRun = "2026-09-22 09:10 UTC";

export const numbers = {
  iocsChecked: 5400,
  mzPrefixes: 810,
  mzAsns: 14,
  overlaps: 0,
  storiesKept: 18,
  storiesTriaged: 75,
  newsFeeds: 7,
};

export const asnLedger: AsnEntry[] = [
  { asn: "AS37342", org: "Movitel SA", prefixCount: 541 },
  { asn: "AS37223", org: "Vodacom Mocambique S.A", prefixCount: 65 },
  { asn: "AS37110", org: "Moztel Lda", prefixCount: 48 },
  { asn: "AS25139", org: "TVCABO - Comunicacoes Multimedia Lda", prefixCount: 34 },
  { asn: "AS30619", org: "TMCEL - Mocambique Telecom SA", prefixCount: 33 },
  { asn: "AS36865", org: "Teledata Mozambique", prefixCount: 28 },
  { asn: "AS37697", org: "Webmasters Lda", prefixCount: 21 },
  { asn: "AS327700", org: "MoRENet - Mozambique Research & Education Network", prefixCount: 15 },
  { asn: "AS31960", org: "Eduardo Mondlane University", prefixCount: 9 },
  { asn: "AS36945", org: "Mocambique Celular SARL", prefixCount: 5 },
  { asn: "AS42235", org: "Intra Data Communication", prefixCount: 4 },
  { asn: "AS328274", org: "BIM - Banco Internacional de Mocambique", prefixCount: 3 },
  { asn: "AS328187", org: "EDM - Electricidade de Mocambique", prefixCount: 3 },
  { asn: "AS37477", org: "Mozabanco", prefixCount: 1 },
];

export const stories: Story[] = [
  {
    title: "WordPress Comment2Shell Flaw Can Turn Anonymous Comment XSS Into RCE via Admin Session",
    link: "https://thehackernews.com/2026/09/wordpress-comment2shell-flaw-can-turn.html",
    source: "The Hacker News",
    published: "2026-09-22",
    category: "vulnerability",
    relevanceReason: "Affects wordpress \u2014 widely deployed in under-resourced organizations \u2014 via xss, rce.",
    whyItMatters: "If you run wordpress, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["wordpress", "xss", "rce"],
  },
  {
    title: "Zyxel and Veeam Flaws Under Active Exploitation With Command and SYSTEM Access",
    link: "https://thehackernews.com/2026/09/zyxel-and-veeam-flaws-under-active.html",
    source: "The Hacker News",
    published: "2026-09-22",
    category: "vulnerability",
    relevanceReason: "Affects zyxel, veeam \u2014 widely deployed in under-resourced organizations \u2014 via active exploitation, exploited.",
    whyItMatters: "If you run zyxel, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["zyxel", "active-exploitation", "exploited"],
  },
  {
    title: "\u26a1 Weekly Recap: Cisco 0-Day, AI Agent RCE, ClickFix Attacks, ClickFix Surge, and Browser Hijacks",
    link: "https://thehackernews.com/2026/09/weekly-recap-cisco-0-day-ai-agent-rce.html",
    source: "The Hacker News",
    published: "2026-09-21",
    category: "vulnerability",
    relevanceReason: "Affects cisco \u2014 widely deployed in under-resourced organizations \u2014 via rce, exposed.",
    whyItMatters: "If you run cisco, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["cisco", "rce", "exposed"],
  },
  {
    title: "TASK#STOMP PowerShell Backdoor Steals Documents, Wi-Fi Passwords, and Clipboard Data",
    link: "https://thehackernews.com/2026/09/taskstomp-powershell-backdoor-steals.html",
    source: "The Hacker News",
    published: "2026-09-21",
    category: "other",
    relevanceReason: "Affects powershell \u2014 widely deployed in under-resourced organizations \u2014 via backdoor.",
    whyItMatters: "If you run powershell, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["powershell", "backdoor"],
  },
  {
    title: "SolarWinds Patches ARM Hard-Coded Key Flaw Enabling Unauthenticated RCE",
    link: "https://thehackernews.com/2026/09/solarwinds-patches-arm-hard-coded-key.html",
    source: "The Hacker News",
    published: "2026-09-19",
    category: "vulnerability",
    relevanceReason: "Affects solarwinds \u2014 widely deployed in under-resourced organizations \u2014 via rce, remote code.",
    whyItMatters: "If you run solarwinds, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["solarwinds", "rce", "remote-code"],
  },
  {
    title: "Critical Pre-Auth RCE in Orkes Conductor Workflow Platform Exploited in the Wild",
    link: "https://thehackernews.com/2026/09/critical-pre-auth-rce-in-orkes.html",
    source: "The Hacker News",
    published: "2026-09-19",
    category: "vulnerability",
    relevanceReason: "Affects fortinet \u2014 widely deployed in under-resourced organizations \u2014 via rce, remote code.",
    whyItMatters: "If you run fortinet, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["fortinet", "rce", "remote-code"],
  },
  {
    title: "BigCommerce alerts merchants of data breach linked to Ribon apps",
    link: "https://www.bleepingcomputer.com/news/security/bigcommerce-alerts-merchants-of-data-breach-linked-to-ribon-apps/",
    source: "BleepingComputer",
    published: "2026-09-21",
    category: "breach",
    relevanceReason: "Affects bigcommerce \u2014 widely deployed in under-resourced organizations \u2014 via credential, data breach.",
    whyItMatters: "If you run bigcommerce, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["bigcommerce", "credential", "data-breach"],
  },
  {
    title: "CISA alerts of active exploitation of three Linux kernel flaws",
    link: "https://www.bleepingcomputer.com/news/security/cisa-alerts-of-active-exploitation-of-three-linux-kernel-flaws/",
    source: "BleepingComputer",
    published: "2026-09-21",
    category: "vulnerability",
    relevanceReason: "Affects linux \u2014 widely deployed in under-resourced organizations \u2014 via active exploitation, exploitation.",
    whyItMatters: "If you run linux, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["linux", "active-exploitation", "exploitation"],
  },
  {
    title: "WordPress Click2Shell flaw lets hackers execute PHP on the server",
    link: "https://www.bleepingcomputer.com/news/security/wordpress-click2shell-flaw-lets-hackers-execute-php-on-the-server/",
    source: "BleepingComputer",
    published: "2026-09-21",
    category: "other",
    relevanceReason: "Affects wordpress, php \u2014 widely deployed in under-resourced organizations \u2014 via cross-site.",
    whyItMatters: "If you run wordpress, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["wordpress", "cross-site"],
  },
  {
    title: "Microsoft reminds admins to migrate Entra ID users to passkeys",
    link: "https://www.bleepingcomputer.com/news/microsoft/microsoft-reminds-admins-to-migrate-entra-id-users-to-passkeys/",
    source: "BleepingComputer",
    published: "2026-09-21",
    category: "phishing",
    relevanceReason: "Affects entra \u2014 widely deployed in under-resourced organizations \u2014 via phishing.",
    whyItMatters: "If you run entra, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["entra", "phishing"],
  },
  {
    title: "Malicious npm packages evade install-script defenses at runtime",
    link: "https://www.bleepingcomputer.com/news/security/malicious-npm-packages-evade-install-script-defenses-at-runtime/",
    source: "BleepingComputer",
    published: "2026-09-20",
    category: "policy_regulation",
    relevanceReason: "Affects npm \u2014 widely deployed in under-resourced organizations \u2014 via malware, threat actors.",
    whyItMatters: "If you run npm, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["npm", "malware", "threat-actors"],
  },
  {
    title: "RatHat Android Trojan Uses AI for Automation",
    link: "https://www.securityweek.com/rathat-android-trojan-uses-ai-for-automation/",
    source: "SecurityWeek",
    published: "2026-09-21",
    category: "other",
    relevanceReason: "Affects android \u2014 widely deployed in under-resourced organizations \u2014 via malware.",
    whyItMatters: "If you run android, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["android", "malware"],
  },
  {
    title: "Rust Team Members and Popular Crate Owners Targeted via Video Calls",
    link: "https://www.securityweek.com/rust-team-members-and-popular-crate-owners-targeted-via-video-calls/",
    source: "SecurityWeek",
    published: "2026-09-21",
    category: "other",
    relevanceReason: "Affects rust \u2014 widely deployed in under-resourced organizations \u2014 via attackers.",
    whyItMatters: "If you run rust, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["rust", "attackers"],
  },
  {
    title: "Organizations Warned of 3 Exploited Linux Kernel Vulnerabilities",
    link: "https://www.securityweek.com/organizations-warned-of-3-exploited-linux-kernel-vulnerabilities/",
    source: "SecurityWeek",
    published: "2026-09-21",
    category: "vulnerability",
    relevanceReason: "Affects linux \u2014 widely deployed in under-resourced organizations \u2014 via exploited, attackers.",
    whyItMatters: "If you run linux, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["linux", "exploited", "attackers"],
  },
  {
    title: "ShinyHunters cybercrime gang takes over Cl0p ransomware site, demands extortion payment",
    link: "https://therecord.media/shinyhunters-clop-cyberattack-website",
    source: "The Record",
    published: "2026-09-21",
    category: "ransomware",
    relevanceReason: "Attack activity against payment-sector organizations, the same targets common across SADC.",
    whyItMatters: "If you run affected software, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["ransomware"],
  },
  {
    title: "Attackers Abuse npm Trusted Publishing in GHAPPIER Campaign",
    link: "https://www.infosecurity-magazine.com/news/attackers-abuse-npm-trusted/",
    source: "Infosecurity Magazine",
    published: "2026-09-21",
    category: "other",
    relevanceReason: "Affects npm \u2014 widely deployed in under-resourced organizations \u2014 via attackers.",
    whyItMatters: "If you run npm, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["npm", "attackers"],
  },
  {
    title: "New Chinese-Made \u2018RatHat\u2019 Android Malware Leverages AI to Steal Financial Data",
    link: "https://www.infosecurity-magazine.com/news/rathat-android-malware-ai-steal/",
    source: "Infosecurity Magazine",
    published: "2026-09-17",
    category: "other",
    relevanceReason: "Affects android \u2014 widely deployed in under-resourced organizations \u2014 via malware, backdoor.",
    whyItMatters: "If you run android, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["android", "malware", "backdoor"],
  },
  {
    title: "Cisco Warns of Active Exploitation of Critical ISE Flaw",
    link: "https://www.infosecurity-magazine.com/news/cisco-active-exploitation-critical/",
    source: "Infosecurity Magazine",
    published: "2026-09-17",
    category: "vulnerability",
    relevanceReason: "Affects cisco \u2014 widely deployed in under-resourced organizations \u2014 via active exploitation, exploitation.",
    whyItMatters: "If you run cisco, verify you are on a patched version; unpatched instances are the most common entry point for small teams without dedicated security staff.",
    tags: ["cisco", "active-exploitation", "exploitation"],
  },
];

export const filteredOut: FilteredStory[] = [
  {
    title: "One Hidden Meta Muse Setting Could Let Attackers Turn the AI Assistant Into a Backdoor",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Fake LastPass Authenticator Installer Abuses Microsoft-Signed Driver to Kill Antivirus and EDR",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Contagious Interview Campaign Compromises 30,000 Devices, Steals $10.71M in Crypto",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Google Fined \u20ac403 Million Over GDPR Violations Tied to Location Data",
    source: "The Hacker News",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "ClickFix Lures Deploy ChainScript RAT Using Polygon to Rotate C2 Infrastructure",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Jade Sleet Linked to Indian IT Provider Breach With FLATROOF and ROOFDECK Backdoors",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Claude Opus 5 Helped Researchers Take Over OpenAI Staff Accounts via Chained Flaws",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Can You Prove a New CVE Is Exploitable Before Attackers Do? Learn How in This Webinar",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Identity Visibility in 2026: The Foundation of Identity Security",
    source: "The Hacker News",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Microsoft to retire Microsoft 365 Companion apps in December",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Google fined \u20ac403 million over location data privacy violations",
    source: "BleepingComputer",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Microsoft fixes broken Excel copy and paste for all Office users",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "FBI's CJIS v6.1: What Security Teams Need to Know.",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Microsoft: September updates break File History backup feature",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Researchers escape OpenAI Codex sandbox to run commands on host",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "BragJack attacks hijack AI browser agents through malicious extensions",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "North Korean WaterPlum hackers infected 30,000 devices worldwide",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "ShinyHunters hacks Clop leak site, threatens to extort ransomware gang",
    source: "BleepingComputer",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Viral AI actress' hotline face-scans every caller, watches their mood",
    source: "BleepingComputer",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "US Proposes AI Incident Alert System in Talks With China, Bessent Says",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Google Hit With $463 Million Fine for EU Location Data Rule Breach",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Fake LastPass Installers Push Kernel-Level EDR Killer, \u2018Rapuncel\u2019 Stealer",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "CISO Conversations: Noopur Davis \u2013 The Accidental Global CISO at Comcast",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Dragos Completes NetRise and runZero Acquisitions Following Accenture Deal",
    source: "SecurityWeek",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "CrowdSec Confirms Source Code Stolen in Supply Chain Attack",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Colorado Water Utilities Hit by Cyberattacks Targeting OT Systems",
    source: "SecurityWeek",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "EU data regulator fines Google more than $460 million for location data violations",
    source: "The Record",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Belgian table tennis, gymnastics federations hit by cyberattacks",
    source: "The Record",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Cyberattack hits University of Munich, potentially exposing student financial data",
    source: "The Record",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "LinkedIn wins court order blocking mass scraping of user data",
    source: "The Record",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Huntress expands cybersecurity platform to Africa through QBS Software partnership - MSSP Alert",
    source: "Google News: Africa cybersecurity",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Terra Industries leads strategic investment in Nigerian cybersecurity startup Aeon - Portal ERP",
    source: "Google News: Africa cybersecurity",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Zuo Bruno Builds Zuoix Into a Preventive Cybersecurity Firm Across Africa - We are Tech",
    source: "Google News: Africa cybersecurity",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Terra Industries puts $1M into Aeon, a Nigerian cybersecurity startup - Resilience Media",
    source: "Google News: Africa cybersecurity",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Africa\u2019s AI Governance, Data & Cybersecurity to Take Center Stage at 4th TICON Confab in Zambia - CediRates",
    source: "Google News: Africa cybersecurity",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "Burkina Faso\u2019s Great\u00a0Green\u00a0Wall\u00a0is being stalled by more than war",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "5 questions to understand Somaliland President Irro\u2019s Washington debut",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "US plays catch-up with China in race for Nigeria\u2019s critical minerals",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "US-Africa Week Ahead: Washington retreats from African priorities at the UN",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Tinubu\u2019s poll rebound reveals Nigeria\u2019s town-country divide",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "How al-Amoudi broke Morocco\u2019s only refinery",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Meet UN Secretary-General Guterres\u2019 Africa team",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Algeria accuses UAE of trying to sway two presidential elections",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Mali: Kyiv\u2019s support for Sahel insurgents clashes with US goals",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "After Niger\u2019s coup attempt, Tiani is running out of people to trust",
    source: "The Africa Report",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Google Hit with \u20ac403m GDPR Fine Over Location Data Practices",
    source: "Infosecurity Magazine",
    reason: "Industry, business, or political news with no vulnerability, incident, or technique defenders can act on.",
  },
  {
    title: "New Exvicy ClickFix Framework Built on Rival ErrTraffic's Code",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "ShinyHunters Claim Hack of Rival Ransomware Gang Clop",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Experts Alarmed Over Gyazo\u2019s Breach of 490 Million Metadata Records",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Revolut Customers Targeted with New Wave of Phishing Attacks",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "New Settra Ransomware Variant Deployed in Attacks on Retail and Manufacturing",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "CISA Upgrades Vulnerability Reporting Platform with More Automation",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Manufacturing Accounts for 22% of all Ransomware Victims",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "FamousSparrow Swaps SparrowDoor For New SparroWocky Backdoor",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "CISA Urges Critical Infrastructure to Plant Decoys Inside Networks",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "Cyber Essentials Has Record Year but Takeup Remains Low",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
  {
    title: "AI Agent Carries Out Multi-Stage Data Theft Attack",
    source: "Infosecurity Magazine",
    reason: "No African angle, and no widely-deployed-platform issue with a transferable lesson for low-resource defenders.",
  },
];

export const categoryLabels: Record<string, string> = {
  vulnerability: 'Vulnerability',
  breach: 'Breach',
  ransomware: 'Ransomware',
  phishing: 'Phishing',
  policy_regulation: 'Policy',
  infrastructure: 'Infrastructure',
  tooling: 'Tooling',
  other: 'Note',
};
