import Header from './components/Header';
import Ledger from './components/StatsGrid';
import Overlaps from './components/IOCDashboard';
import Digest from './components/NewsDigest';
import Footer from './components/Footer';
import { lastRun } from './data/feedData';

export default function App() {
  return (
    <div className="min-h-screen">
      <a
        href="#overlaps"
        className="no-print sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-paper-raised focus:px-3 focus:py-2 focus:text-sm focus:border focus:border-ink"
      >
        Skip to the ledger
      </a>

      <Header />

      <main className="mx-auto max-w-5xl px-5 sm:px-8">
        {/* Masthead */}
        <section className="settle pt-14 pb-10 sm:pt-20">
          <p className="num text-[13px] uppercase tracking-[0.14em] text-oxide">
            MZ Threat Feed
          </p>
          <h1 className="display mt-4 max-w-3xl text-4xl leading-[1.12] sm:text-[3.4rem]">
            What the internet's underworld is doing this week, and how much of it
            touches home.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-soft">
            Every day a script pulls indicators of compromise from public abuse feeds
            and checks them against the IP ranges that networks across Mozambique and
            eight neighbouring SADC countries announce. Alongside that, security news
            gets triaged for the people who actually have to act on it: admins of
            banks, universities, ISPs and ministries who run old software with small
            teams.
          </p>
          <p className="mt-5 text-sm text-ink-faint">
            Last pipeline run {lastRun}. Data comes straight from{' '}
            <code className="num text-[13px] text-ink-soft">data/*.json</code> in the
            repo; nothing on this page is hand-written.
          </p>
        </section>

        <Ledger />
        <Overlaps />
        <Digest />
      </main>

      <Footer />
    </div>
  );
}
