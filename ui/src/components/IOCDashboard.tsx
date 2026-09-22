import { numbers, asnLedger } from '../data/feedData';

export default function IOCDashboard() {
  return (
    <section id="overlaps" className="settle py-14">
      <h2 className="display text-3xl">The SADC ledger</h2>
      <p className="mt-3 max-w-2xl leading-relaxed text-ink-soft">
        {numbers.sadcAsns} networks across {numbers.countriesTracked} SADC countries
        carry the region's traffic: the carriers, the banks, the power company, the
        university, two governments. Their announced ranges are what "IP space in
        the region" concretely means, so that is the yardstick every indicator gets
        measured against. Mozambique gets the deepest coverage; the rest grows as
        each network mapping gets verified against the registry.
      </p>

      {/* Overlap status: the line that matters most, stated plainly */}
      {numbers.overlaps === 0 ? (
        <div className="mt-8 border border-slate-strong bg-paper-sunk px-5 py-4">
          <p className="text-[15px] leading-relaxed text-ink">
            <span className="num font-medium text-oxide">0 overlaps</span> this run:
            none of the {numbers.iocsChecked.toLocaleString('en-US')} indicators
            checked resolved into any of the {numbers.sadcPrefixes.toLocaleString('en-US')}{' '}
            tracked prefixes. Quiet is normal here; the check runs daily and this
            page is where a nonzero day gets announced.
          </p>
        </div>
      ) : (
        <div className="mt-8 border-2 border-oxide bg-paper-raised px-5 py-4">
          <p className="text-[15px] leading-relaxed text-ink">
            <span className="num font-semibold text-oxide">
              {numbers.overlaps} overlap{numbers.overlaps === 1 ? '' : 's'}
            </span>{' '}
            this run. Indicators below resolved into tracked SADC space; treat them
            as starts of an investigation, not proof on their own.
          </p>
        </div>
      )}

      <div className="mt-8 overflow-hidden border border-ink">
        <table className="w-full text-left text-[14px]">
          <caption className="sr-only">
            Tracked SADC autonomous systems by country and announced prefix counts
          </caption>
          <thead>
            <tr className="border-b border-ink bg-paper-sunk">
              <th scope="col" className="px-4 py-2.5 text-[12px] font-medium uppercase tracking-[0.1em] text-ink-soft">
                Country
              </th>
              <th scope="col" className="num px-4 py-2.5 text-[12px] font-medium uppercase tracking-[0.1em] text-ink-soft">
                ASN
              </th>
              <th scope="col" className="px-4 py-2.5 text-[12px] font-medium uppercase tracking-[0.1em] text-ink-soft">
                Operating organisation
              </th>
              <th scope="col" className="num px-4 py-2.5 text-right text-[12px] font-medium uppercase tracking-[0.1em] text-ink-soft">
                Prefixes
              </th>
            </tr>
          </thead>
          <tbody>
            {asnLedger.map((entry, i) => (
              <tr
                key={entry.asn}
                className={i % 2 === 1 ? 'bg-paper-raised' : 'bg-paper'}
              >
                <td className="num whitespace-nowrap px-4 py-2.5 text-ink-soft">{entry.code}</td>
                <td className="num whitespace-nowrap px-4 py-2.5 text-oxide">{entry.asn}</td>
                <td className="px-4 py-2.5">{entry.org}</td>
                <td className="num px-4 py-2.5 text-right">{entry.prefixCount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-[13px] text-ink-faint">
        Counts from RIPEstat's announced-prefixes dataset at last run. Every
        ASN-to-organisation mapping was checked against the registry before it
        entered this table; anything unverified stays out.
      </p>
    </section>
  );
}
