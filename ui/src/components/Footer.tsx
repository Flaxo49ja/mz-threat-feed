import { lastRun } from '../data/feedData';

export default function Footer() {
  return (
    <footer className="mt-8 border-t border-ink bg-paper-raised">
      <div className="mx-auto max-w-5xl px-5 py-10 sm:px-8">
        <div className="grid gap-10 sm:grid-cols-3">
          <div>
            <h3 className="text-[13px] font-semibold uppercase tracking-[0.08em] text-ink">
              Where the data comes from
            </h3>
            <p className="mt-3 text-[14px] leading-relaxed text-ink-soft">
              Indicators from URLhaus and AbuseIPDB, both public. Prefixes from
              RIPEstat. Headlines from seven RSS feeds, including a standing search
              for African cybersecurity news. Every number on this page is traceable
              to a JSON file in the repository.
            </p>
          </div>

          <div>
            <h3 className="text-[13px] font-semibold uppercase tracking-[0.08em] text-ink">
              How to read it
            </h3>
            <p className="mt-3 text-[14px] leading-relaxed text-ink-soft">
              An overlap is a lead, not a verdict: hosting ranges get reused, and
              one bad customer can flag an innocent ISP. Check the indicator against
              your own logs before acting on anything here.
            </p>
          </div>

          <div>
            <h3 className="text-[13px] font-semibold uppercase tracking-[0.08em] text-ink">
              The machinery
            </h3>
            <p className="mt-3 text-[14px] leading-relaxed text-ink-soft">
              Plain Python, no framework, run daily by GitHub Actions and published
              through Pages. The triage verdicts come from an LLM when a key is
              configured, and from a keyword classifier when it isn't.
            </p>
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-2 border-t border-slate-line pt-5 sm:flex-row sm:items-baseline sm:justify-between">
          <p className="num text-[12px] text-ink-faint">
            Built as an open tool; copy it, fork it, run it for your own country.
          </p>
          <a
            href="https://github.com/Anayo-Anyafulu/mz-threat-feed"
            className="text-[14px] text-oxide underline decoration-slate-strong underline-offset-4 hover:decoration-oxide"
          >
            Source on GitHub
          </a>
        </div>
        <p className="num mt-4 text-[12px] text-ink-faint">Last run {lastRun}</p>
      </div>
    </footer>
  );
}
