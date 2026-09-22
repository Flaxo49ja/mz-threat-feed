import { numbers } from '../data/feedData';

export default function StatsGrid() {
  const rows: Array<[string, string, string]> = [
    [
      numbers.iocsChecked.toLocaleString('en-US'),
      'indicators checked',
      'malicious IPs and domains pulled from URLhaus and AbuseIPDB, deduplicated',
    ],
    [
      numbers.sadcPrefixes.toLocaleString('en-US'),
      'prefixes watched',
      `the ${numbers.sadcAsns} networks below announce these ranges across ${numbers.countriesTracked} countries, per RIPEstat`,
    ],
    [
      String(numbers.overlaps),
      'overlaps found',
      numbers.overlaps === 0
        ? 'no IOC landed inside tracked space this run. The empty result is the result.'
        : 'indicators that resolve into tracked SADC space',
    ],
    [
      `${numbers.storiesKept} of ${numbers.storiesTriaged}`,
      'news items kept',
      `the rest failed the Africa-SADC relevance test across ${numbers.newsFeeds} feeds`,
    ],
  ];

  return (
    <section className="settle border-y border-ink bg-paper-raised" aria-label="Run totals">
      <dl className="mx-auto grid max-w-5xl grid-cols-2 gap-px bg-slate-line sm:grid-cols-4">
        {rows.map(([value, label, note]) => (
          <div key={label} className="bg-paper-raised px-5 py-6 sm:px-6">
            <dd className="num text-3xl leading-none text-ink">{value}</dd>
            <dt className="mt-2 text-[13px] font-semibold uppercase tracking-[0.08em] text-oxide">
              {label}
            </dt>
            <p className="mt-2 text-[13px] leading-snug text-ink-soft">{note}</p>
          </div>
        ))}
      </dl>
    </section>
  );
}
