import { useState } from "react";
import { evidence } from "./data.js";
import "./atlas.css";

/* Coordinate space: 1000 x 640. HTML nodes are positioned by percentage of the
   stage (locked to a 1000/640 aspect ratio), so they align 1:1 with the SVG
   paths drawn in the same coordinate space. */

const ENGINE = [
  { n: 1, key: "listen", title: "Listen", sub: "Customer insight", y: 205 },
  { n: 2, key: "position", title: "Position", sub: "Brand + strategy", y: 273 },
  { n: 3, key: "activate", title: "Activate", sub: "Digital + GTM", y: 341 },
  { n: 4, key: "scale", title: "Scale", sub: "Revenue + reach", y: 409 },
  { n: 5, key: "systemize", title: "Systemize", sub: "Operations + AI", y: 477 },
];
const ENGINE_X = 415;

const BREADTH = [
  "Customer behavior", "Brand", "Digital", "Operations", "AI systems", "Health communication", "Population health",
];

const SOURCES = [
  { org: "Asiatic", sector: "Brand & advertising", metric: "~$1M/mo in 7 months", y: 150 },
  { org: "Samsung", sector: "Consumer tech", metric: "#1 globally for growth", y: 248 },
  { org: "SureCash", sector: "Fintech", metric: "~10M reached", y: 346 },
  { org: "Ekhanei", sector: "E-commerce", metric: "#1 in 2.5 months", y: 444 },
  { org: "ACCA", sector: "Education", metric: "100% of targets", y: 542 },
];
const SOURCE_X = 150;

const APPS = [
  { org: "Praava", sector: "Primary healthcare", metric: "~57% B2C growth", y: 210 },
  { org: "Laser Treat", sector: "Specialized healthcare", metric: "+16% revenue", y: 350 },
  { org: "HSREP", sector: "Public & population health", metric: "57,274 at $0", y: 490 },
];
const APP_X = 852;

const pct = (x, y) => ({ left: (x / 1000) * 100 + "%", top: (y / 640) * 100 + "%" });

function hpath(x1, y1, x2, y2) {
  const mx = (x1 + x2) / 2;
  return `M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`;
}
function vpath(x1, y1, x2, y2) {
  const my = (y1 + y2) / 2;
  return `M ${x1} ${y1} C ${x1} ${my}, ${x2} ${my}, ${x2} ${y2}`;
}

const ORG_META = {
  Asiatic: { label: "Asiatic", sector: "Brand & advertising" },
  Samsung: { label: "Samsung", sector: "Consumer tech" },
  SureCash: { label: "SureCash", sector: "Fintech + government" },
  Ekhanei: { label: "Ekhanei", sector: "E-commerce" },
  ACCA: { label: "ACCA", sector: "Professional education" },
  Praava: { label: "Praava", sector: "Primary healthcare" },
  "Laser Treat": { label: "Laser Treat", sector: "Specialized healthcare" },
  HSREP: { label: "HSREP", sector: "Public & population health" },
};

export default function AtlasView({ selectedOrganization, setSelectedOrganization, setActiveEvidenceId, openLedger, onStartTour }) {
  const [hover, setHover] = useState(null);
  const active = selectedOrganization;

  const pick = (org) => {
    setSelectedOrganization(org);
    const first = evidence.find((e) => e.organization === org);
    if (first && setActiveEvidenceId) setActiveEvidenceId(first.id);
  };

  const orgEvidence = evidence.filter((e) => e.organization === active);
  const lead = orgEvidence[0];
  const meta = ORG_META[active] || { label: active, sector: "" };
  const lenses = Array.from(new Set(orgEvidence.map((e) => e.lens))).join(" · ");
  const isHealth = ["Praava", "Laser Treat", "HSREP", "EMU"].includes(active);
  const traceOn = (org) => hover === org || active === org;

  return (
    <div className="atlas-layout" id="impact-map">
      <div className="atlas-panel">
        <div className="atlas-helper">
          <span className="atlas-helper-dot" />
          <span>One deep engine, applied everywhere. <b>Hover a node to trace it; click to inspect the evidence.</b></span>
          <button type="button" className="atlas-tour-btn" onClick={onStartTour}>&#9658; Play the story</button>
        </div>

        <div className="atlas-stage-outer">
          <div className="atlas-stage">
            <svg className="atlas-svg" viewBox="0 0 1000 640" preserveAspectRatio="none" aria-hidden="true">
              <g className="atlas-rings">
                {[150, 250, 350].map((r) => (<circle key={r} cx={ENGINE_X} cy={341} r={r} />))}
              </g>
              <g className="atlas-links breadth">
                {BREADTH.map((b, i) => {
                  const bx = 150 + i * ((858 - 150) / (BREADTH.length - 1));
                  return <path key={b} d={vpath(bx, 108, ENGINE_X, 178)} className="atlas-link cap" style={{ animationDelay: `${0.1 + i * 0.05}s` }} />;
                })}
              </g>
              <g className="atlas-links src">
                {SOURCES.map((s, i) => (
                  <path key={s.org} d={hpath(SOURCE_X + 34, s.y, ENGINE_X - 46, ENGINE[Math.min(i, 4)].y)}
                    className={`atlas-link grow ${traceOn(s.org) ? "lit" : ""}`} style={{ animationDelay: `${0.5 + i * 0.12}s` }} />
                ))}
              </g>
              <g className="atlas-links app">
                {APPS.map((a, i) => (
                  <path key={a.org} d={hpath(ENGINE_X + 46, ENGINE[[0, 2, 4][i]].y, APP_X - 34, a.y)}
                    className={`atlas-link grow ${traceOn(a.org) ? "lit" : ""}`} style={{ animationDelay: `${1.05 + i * 0.12}s` }} />
                ))}
              </g>
              <path d="M 800 490 C 620 430, 540 250, 470 205" className="atlas-link loop" style={{ animationDelay: "1.5s" }} />
            </svg>

            <div className="atlas-badge" style={pct(560, 292)}>
              <span className="atlas-badge-k">MPH &middot; CHES&reg;</span>
              <span className="atlas-badge-s">behavior science &rarr; growth insight</span>
            </div>

            <div className="atlas-region-label breadth" style={pct(504, 66)}>APPLIED BREADTH</div>

            {BREADTH.map((b, i) => {
              const bx = 150 + i * ((858 - 150) / (BREADTH.length - 1));
              return (
                <div key={b} className="atlas-node breadth" style={pct(bx, 108)}>
                  <span className="atlas-dot cap" />
                  <span className="atlas-node-label">{b}</span>
                </div>
              );
            })}

            <div className="atlas-engine" style={{ left: (ENGINE_X / 1000) * 100 + "%", top: `${(178 / 640) * 100}%`, height: `${((504 - 178) / 640) * 100}%` }}>
              <span className="atlas-engine-cap">THE GROWTH ENGINE</span>
            </div>
            {ENGINE.map((s) => (
              <div key={s.key} className="atlas-step" style={pct(ENGINE_X, s.y)}>
                <span className="atlas-step-num">{s.n}</span>
                <span className="atlas-step-copy"><b>{s.title}</b><i>{s.sub}</i></span>
              </div>
            ))}

            {SOURCES.map((s) => (
              <button key={s.org} type="button"
                className={`atlas-node src ${active === s.org ? "active" : ""}`}
                style={pct(SOURCE_X, s.y)}
                onMouseEnter={() => setHover(s.org)} onMouseLeave={() => setHover(null)}
                onClick={() => pick(s.org)} aria-label={`${s.sector}: ${s.metric}`}>
                <span className="atlas-dot grow" />
                <span className="atlas-node-label">{s.org}</span>
                <span className="atlas-metric grow">{s.metric}</span>
              </button>
            ))}

            {APPS.map((a) => (
              <button key={a.org} type="button"
                className={`atlas-node app ${active === a.org ? "active" : ""}`}
                style={pct(APP_X, a.y)}
                onMouseEnter={() => setHover(a.org)} onMouseLeave={() => setHover(null)}
                onClick={() => pick(a.org)} aria-label={`${a.sector}: ${a.metric}`}>
                <span className="atlas-dot health" />
                <span className="atlas-node-label">{a.org}</span>
                <span className="atlas-metric health">{a.metric}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      <aside className="atlas-inspector">
        <div className="ai-eyebrow">{(meta.label || "").toUpperCase()} &middot; {(meta.sector || "").toUpperCase()}</div>
        <h3 className="ai-title">{isHealth ? "Growth directed toward health" : "Growth, forged in market"}</h3>
        <div className="ai-sep" />
        <div className="ai-block">
          <span className="ai-k">Key result</span>
          <div className="ai-metric">{lead ? lead.metric : ""}</div>
          <div className="ai-metric-t">{lead ? lead.title : ""}</div>
        </div>
        <div className="ai-block">
          <span className="ai-k">Lenses</span>
          <div className="ai-lenses">{lenses}</div>
        </div>
        <div className="ai-block">
          <span className="ai-k">Outcome</span>
          <div className="ai-out">{isHealth ? "Human outcomes + durable growth" : "Growth compounded into the core capability"}</div>
        </div>
        <button type="button" className="ai-cta" onClick={openLedger}>Open case evidence <span aria-hidden="true">&rarr;</span></button>
        <div className="ai-count">{orgEvidence.length} result{orgEvidence.length === 1 ? "" : "s"} at {meta.label}</div>
      </aside>
    </div>
  );
}
