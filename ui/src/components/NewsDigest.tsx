import { useMemo, useState } from 'react';
import { stories, filteredOut, categoryLabels } from '../data/feedData';

const categoryOrder = [
  'vulnerability',
  'breach',
  'ransomware',
  'phishing',
  'policy_regulation',
  'infrastructure',
  'other',
];

export default function NewsDigest() {
  const [showFiltered, setShowFiltered] = useState(false);

  const counts = useMemo(() => {
    const m = new Map<string, number>();
    for (const s of stories) m.set(s.category, (m.get(s.category) ?? 0) + 1);
    return m;
  }, []);

  const present = categoryOrder.filter((c) => counts.has(c));

  return (
    <section id="digest" className="settle py-14">
      <div className="rule-double pt-1">
        <h2 className="display pt-5 text-3xl">Worth your time</h2>
        <p className="mt-3 max-w-2xl leading-relaxed text-ink-soft">
          {stories.length} of {stories.length + filteredOut.length} headlines survived
          the filter. The test is blunt on purpose: does this change what a small team
          in Maputo or Nairobi should do this week? Vendor announcements, market news
          and geopolitical roundups fail it.
        </p>
      </div>

      {/* Category index, newspaper-classifieds style */}
      <nav
        aria-label="Story categories"
        className="mt-6 flex flex-wrap items-baseline gap-x-5 gap-y-1 border-y border-slate-line py-3"
      >
        {present.map((cat) => (
          <span key={cat} className="text-[14px] text-ink-soft">
            <span className="font-semibold text-ink">{categoryLabels[cat] ?? cat}</span>{' '}
            <span className="num text-oxide">{counts.get(cat)}</span>
          </span>
        ))}
      </nav>

      <div className="mt-2 divide-y divide-slate-line">
        {stories.map((story) => {
          const external = /^https?:/.test(story.link);
          return (
            <article key={story.title} className="grid gap-x-8 gap-y-2 py-7 sm:grid-cols-[13rem_1fr]">
              <div className="text-[13px] leading-relaxed text-ink-faint">
                <p className="font-semibold uppercase tracking-[0.07em] text-ink-soft">
                  {categoryLabels[story.category] ?? story.category}
                </p>
                <p className="mt-1">
                  {story.source} · {story.published}
                </p>
                <p className="num mt-1 text-ink-faint">
                  {story.tags.slice(0, 3).map((t) => `#${t}`).join(' ')}
                </p>
              </div>

              <div>
                <h3 className="display text-[1.35rem] leading-snug">
                  {external ? (
                    <a
                      href={story.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline decoration-slate-strong decoration-1 underline-offset-4 hover:decoration-oxide"
                    >
                      {story.title}
                    </a>
                  ) : (
                    story.title
                  )}
                </h3>
                <p className="mt-2.5 text-[15px] leading-relaxed text-ink-soft">
                  {story.whyItMatters}
                </p>
              </div>
            </article>
          );
        })}
      </div>

      {/* The discard pile, honest and inspectable */}
      <div className="mt-10 border-t border-ink pt-6">
        <button
          onClick={() => setShowFiltered(!showFiltered)}
          aria-expanded={showFiltered}
          className="num text-[13px] uppercase tracking-[0.1em] text-ink-soft underline decoration-slate-strong underline-offset-4 hover:text-oxide hover:decoration-oxide"
        >
          {showFiltered ? 'Hide' : 'Show'} the {filteredOut.length} headlines that
          didn't make it
        </button>

        {showFiltered && (
          <ul className="mt-5 space-y-3">
            {filteredOut.map((item) => (
              <li key={item.title} className="grid gap-x-8 gap-y-1 sm:grid-cols-[13rem_1fr]">
                <span className="text-[13px] text-ink-faint">{item.source}</span>
                <span className="text-[14px]">
                  <span className="text-ink-soft">{item.title}</span>
                  <span className="block text-[13px] italic text-ink-faint">
                    {item.reason}
                  </span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
