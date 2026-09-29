/* Shared GA4 + consent for shafaatalichoyon.com standalone pages (essays, writing, research).
   Mirrors the homepage: geo-gated consent, GA loads immediately outside the EU/UK,
   and is gated behind a consent banner inside. Consent is remembered in the same
   localStorage key ('analytics-consent') the homepage uses, so a visitor's choice
   carries across every page. Measurement ID G-RN7EPJQQPC. */
(function () {
  var GA_ID = 'G-RN7EPJQQPC';
  var KEY = 'analytics-consent';

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  window.__gaOn = false;
  window.loadGA = function () {
    if (window.__gaOn) return;
    /* Never track local builds or headless tooling. Until 2026-09-09 the
       prerender/build scripts fired real GA events from localhost:
       298 users at 0.38s average, ~52% of all reported traffic. */
    var _h = location.hostname;
    if (_h === 'localhost' || _h === '127.0.0.1' || _h === '::1' || _h === ''
        || navigator.webdriver === true) return;
    window.__gaOn = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
  };

  /* Lightweight event helper for standalone pages (impact map, essays, etc.).
     Consent-gated: only sends once GA is actually on. The homepage defines its
     own richer window.track first, so guard against clobbering it. */
  window.track = window.track || function (name, params) {
    try { if (!window.__gaOn) return; gtag('event', name, params || {}); } catch (e) {}
  };

  function grant() { try { localStorage.setItem(KEY, 'granted'); } catch (e) {} window.loadGA(); }
  function deny()  { try { localStorage.setItem(KEY, 'denied'); } catch (e) {} }

  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (e) {}

  if (choice === 'granted') { window.loadGA(); return; }
  if (choice === 'denied') { return; }

  /* Undecided: EU/UK visitors see a banner; everyone else loads immediately.
     Timezone is a lightweight, no-network proxy for EU/UK (Europe/* covers UK). */
  var tz = '';
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
  if (!/^Europe\//.test(tz)) { grant(); return; }

  function showBanner() {
    if (document.getElementById('sac-consent')) return;
    var b = document.createElement('div');
    b.id = 'sac-consent';
    b.style.cssText = 'position:fixed;left:16px;right:16px;bottom:16px;max-width:660px;margin:0 auto;' +
      'background:#11161D;color:#C7CDD6;border:1px solid rgba(255,255,255,.12);border-radius:12px;' +
      'padding:14px 16px;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;' +
      'box-shadow:0 12px 40px rgba(0,0,0,.4);z-index:99999;display:flex;gap:12px;align-items:center;' +
      'flex-wrap:wrap;justify-content:space-between;';
    var txt = document.createElement('span');
    txt.style.cssText = 'flex:1;min-width:220px;';
    txt.textContent = 'This site uses cookies for anonymous analytics.';
    var grp = document.createElement('span');
    grp.style.cssText = 'display:flex;gap:8px;';
    var dec = document.createElement('button');
    dec.type = 'button'; dec.textContent = 'Decline';
    dec.style.cssText = 'font:600 13px sans-serif;border:1px solid rgba(255,255,255,.22);border-radius:8px;' +
      'padding:8px 14px;background:transparent;color:#C7CDD6;cursor:pointer;';
    var acc = document.createElement('button');
    acc.type = 'button'; acc.textContent = 'Accept';
    acc.style.cssText = 'font:600 13px sans-serif;border:0;border-radius:8px;padding:8px 16px;' +
      'background:#0FB3B3;color:#04222A;cursor:pointer;';
    dec.onclick = function () { deny(); b.remove(); };
    acc.onclick = function () { grant(); b.remove(); };
    grp.appendChild(dec); grp.appendChild(acc);
    b.appendChild(txt); b.appendChild(grp);
    document.body.appendChild(b);
  }

  if (document.body) showBanner();
  else document.addEventListener('DOMContentLoaded', showBanner);
})();


/* Scroll-depth + engaged-time milestones (added 2026-09-15) — mirrors the HSREP
   site so the portfolio dashboard's per-page completion funnel and depth ladder
   fill in on standalone essay/section pages too. Fires scroll_depth{percent} at
   25/50/75/100 and engaged_time{seconds} at 30/60/120/240. Idempotent via window
   flag; consent-gated through window.track. NOTE: querying these needs GA4
   event-scoped custom dimensions `percent` and `seconds` registered on the
   portfolio property. */
(function () {
  if (window.__depthTrackOn) return; window.__depthTrackOn = true;
  function T(n, p) { try { if (window.track) window.track(n, p); } catch (e) {} }
  var SP = [25, 50, 75, 100], sf = {};
  function frac() {
    var de = document.documentElement, b = document.body;
    var h = Math.max(de.scrollHeight, b ? b.scrollHeight : 0) - window.innerHeight;
    if (h <= 0) return 100;
    return Math.min(100, Math.round((window.pageYOffset || de.scrollTop || 0) / h * 100));
  }
  function onScroll() {
    var f = frac();
    for (var i = 0; i < SP.length; i++) { var m = SP[i]; if (f >= m && !sf[m]) { sf[m] = 1; T('scroll_depth', { percent: m }); } }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  window.addEventListener('load', onScroll); onScroll();
  var TM = [30, 60, 120, 240], tf = {}, secs = 0, timer = null;
  function tick() { secs++; for (var i = 0; i < TM.length; i++) { var m = TM[i]; if (secs >= m && !tf[m]) { tf[m] = 1; T('engaged_time', { seconds: m }); } } }
  function start() { if (!timer) timer = setInterval(tick, 1000); }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function vis() { (document.visibilityState === 'visible') ? start() : stop(); }
  document.addEventListener('visibilitychange', vis); vis();
})();
