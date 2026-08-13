#!/usr/bin/env python3
"""Regenerate sitemap.xml from essays.json.

Only essays whose publish date is on or before today are included, so the
sitemap matches the set the site actually shows as published (no future
lastmod dates, no advertising of not-yet-live essays). Core/section URLs
(homepage, writing, essays, impact, brand, residence-life) are preserved
verbatim from the existing sitemap.

Re-run whenever essays publish (or on a schedule) to keep the sitemap in
sync with the publish calendar:  python3 build-sitemap.py
"""
import json, re, datetime, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
ESSAYS = os.path.join(ROOT, "essays.json")
BASE = "https://shafaatalichoyon.com"

today = datetime.date.today().isoformat()

essays = json.load(open(ESSAYS))
essay_urls = {BASE + e["url"] for e in essays}

sm = open(SITEMAP).read()
blocks = re.findall(r"<url>.*?</url>", sm, re.S)
loc_of = lambda b: re.search(r"<loc>(.*?)</loc>", b).group(1)

# Preserve non-essay (core/section) blocks verbatim, in original order.
non_essay_blocks = [b for b in blocks if loc_of(b) not in essay_urls]

# Live essays only (date <= today), newest first.
live = sorted(
    (e for e in essays if str(e.get("date", ""))[:10] <= today),
    key=lambda e: e["date"], reverse=True,
)

def essay_block(e):
    return (
        "  <url>\n"
        f"    <loc>{BASE}{e['url']}</loc>\n"
        f"    <lastmod>{e['date']}</lastmod>\n"
        "    <changefreq>yearly</changefreq>\n"
        "    <priority>0.7</priority>\n"
        "  </url>"
    )

out = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
out += ["  " + b for b in non_essay_blocks]
out += [essay_block(e) for e in live]
out.append("</urlset>")
open(SITEMAP, "w").write("\n".join(out) + "\n")

print(f"today={today} core={len(non_essay_blocks)} live_essays={len(live)} "
      f"total={len(non_essay_blocks) + len(live)} (was {len(blocks)})")
