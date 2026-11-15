#!/usr/bin/env python3
"""Check that every scheduled Reel's essay is findable on /ig and /fb when the Reel goes live.

For each row in _local_archive/instagram/scheduled.json with an "essay" number:
  /ig: essay #N is in the generated ig/index.html (id="eN") or becomes visible from essays.json
       on or before the Reel's date (the page re-reads essays.json in the browser).
  /fb: fb/index.html has a card with data-n="N" whose data-at is at or before the Reel's time.
Exit code 1 if anything is missing, so it can gate scheduling.

Usage: python3 scripts/check_reel_links.py [--all]   (default: Reels from today on)
"""
import datetime, json, os, re, sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_ig  # noqa: E402  (numbering lives there)

TZ = ZoneInfo("America/Detroit")
today = datetime.date.today().isoformat()
essays = json.load(open(os.path.join(ROOT, "essays.json")))
num = {}
for e in build_ig.numbered(essays):
    num[e["n"]] = e
fb = open(os.path.join(ROOT, "fb", "index.html"), encoding="utf-8").read()
fb_at = {}
for n, at in re.findall(r'data-n="(\d+)" data-at="(\d+)"', fb):
    n, at = int(n), int(at)
    fb_at[n] = min(at, fb_at.get(n, at))

rows = json.load(open(os.path.join(ROOT, "_local_archive", "instagram", "scheduled.json")))
bad, ok = [], 0
for r in rows:
    n = r.get("essay")
    if not isinstance(n, int) or not r.get("date"):
        continue
    if "--all" not in sys.argv and r["date"] < today:
        continue
    hh, mm = (r.get("time") or "00:00").split(":")
    live = datetime.datetime.fromisoformat(f"{r['date']}T{int(hh):02d}:{int(mm):02d}").replace(tzinfo=TZ)
    live_ms = int(live.timestamp() * 1000)
    where = f"{r['date']} {r.get('time')} {r.get('account','')} essay #{n}"
    e = num.get(n)
    if not e:
        bad.append(f"{where}: /ig has no essay #{n}")
    elif e["date"] > r["date"]:
        bad.append(f"{where}: /ig shows #{n} only from {e['date']}")
    targets_fb = r.get("facebook_page") or "facebook" in str(r.get("account", "")).lower() or "Shafaat Ali Choyon MCIM" in str(r.get("account", ""))
    if n not in fb_at:
        bad.append(f"{where}: /fb has no card #{n}" + ("" if targets_fb else " (IG only; /fb points readers to /ig)"))
    elif fb_at[n] > live_ms:
        when = datetime.datetime.fromtimestamp(fb_at[n] / 1000, TZ).strftime("%b %d %I:%M %p")
        bad.append(f"{where}: /fb shows #{n} only from {when}" + ("" if targets_fb else " (IG only)"))
    else:
        ok += 1
print(f"{ok} Reels OK on /ig and /fb")
for b in bad:
    print("MISSING:", b)
sys.exit(1 if any("IG only" not in b for b in bad) else 0)
