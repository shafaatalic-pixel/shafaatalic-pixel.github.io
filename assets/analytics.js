/* Shared GA4 + consent for shafaatalichoyon.com standalone pages (essays, writing, research).
   Mirrors the homepage: geo-gated consent — GA loads immediately outside the EU/UK,
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
    window.__gaOn = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
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
