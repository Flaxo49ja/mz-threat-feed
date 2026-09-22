import { numbers } from '../data/feedData';

export default function Header() {
  return (
    <header className="border-b border-ink bg-paper-raised no-print">
      <div className="mx-auto flex max-w-5xl flex-wrap items-baseline justify-between gap-x-6 gap-y-1 px-5 py-3 sm:px-8">
        <p className="num text-[12px] uppercase tracking-[0.14em] text-ink-soft">
          Issues daily, 04:00 UTC
        </p>
        <p className="num text-[12px] text-ink-faint">
          {numbers.storiesTriaged} headlines read so you don't have to
        </p>
      </div>
    </header>
  );
}
