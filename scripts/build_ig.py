#!/usr/bin/env python3
"""Build /ig/index.html: the Instagram hub (link in bio).

Every published essay, numbered oldest to newest (#1 = first essay), so a post can
say "Link in bio, #13". Press mentions are read from the homepage press section.
The page also re-reads /essays.json in the browser, so scheduled essays appear on
their publish date without a rebuild, and keep their number.

Usage: python3 scripts/build_ig.py [site_root]
"""
import datetime, html, json, os, re, sys
from zoneinfo import ZoneInfo

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://shafaatalichoyon.com"
CALL = "https://calendly.com/shafaat-alic/30min"
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)


def numbered(essays):
    """Stable numbering: by date, then by position in essays.json."""
    order = sorted(range(len(essays)), key=lambda i: (essays[i]["date"], i))
    return [dict(essays[i], n=k + 1) for k, i in enumerate(order)]


def press_items(index_html):
    i = index_html.find('id="press"')
    seg = index_html[i:i + 40000]
    out = []
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', seg, re.S):
        parts = [html.unescape(" ".join(re.sub(r"<[^>]+>", "", x).split()))
                 for x in re.split(r"<(?:/?(?:div|span|p|b|strong|em|small|h\d|i)[^>]*)>", m.group(2))]
        parts = [p for p in parts if p]
        if len(parts) < 6 or not parts[0].isdigit():
            continue
        out.append({"url": m.group(1), "title": parts[1], "note": parts[2], "outlet": parts[4],
                    "when": parts[5].lstrip("· ").strip(), "tv": "youtube.com" in m.group(1)})
    return out


# Each card switches on when its Reel goes live: 7:30 PM Michigan time on its date (Business Suite posting time).
REEL_LIVE = datetime.time(19, 30)
REEL_TZ = ZoneInfo("America/Detroit")


def live_ms(d, at=None):
    t = datetime.datetime.combine(datetime.date.fromisoformat(d), at or REEL_LIVE, tzinfo=REEL_TZ)
    return int(t.timestamp() * 1000)


REEL_UTM = "utm_source=instagram&utm_medium=social&utm_campaign={d}-reel-{k}&utm_content={c}"
# (date, key, label, hook from the IG caption, destination label, url, utm_content, optional second link[, "HH:MM"])
# Second link: (label, url, utm_content) or None. Optional 9th item: go-live time in Michigan time ("18:00")
# when the Reel is not scheduled at the usual 7:30 PM. Never edit or remove past entries; append new ones in date order.
REELS = [
    ("2026-11-02", "start-here", "Start here", "Growth and public health aren't two careers. For me, they're one skill.",
     "My portfolio, with sources", SITE + "/", "home", None),
    ("2026-11-03", "ch1", "Chapter 1", "80,000 customer conversations taught me how people decide.",
     "The essay: when nobody trusts anybody, trust is the growth strategy", SITE + "/trust-is-the-growth-strategy.html", "essay", None),
    ("2026-11-04", "ch2", "Chapter 2", "Marketing gets attention. Growth gets people back.",
     "The SureCash case: a stipend to 10 million beneficiaries", SITE + "/case/surecash-g2p/", "case", None),
    ("2026-11-05", "ch3", "Chapter 3", "Run a global brand like a local business.",
     "The Galaxy Note9 launch case", SITE + "/case/note9/", "case", ("the ACCA member-growth case", SITE + "/case/acca-ecosystem/", "case2")),
    ("2026-11-06", "ch4", "Chapter 4", "I took growth into healthcare on purpose.",
     "The Praava case: door-to-door and 6-hour traveler testing", SITE + "/case/praava-travel/", "case", ("the corporate-sales engine case", SITE + "/case/praava-corp/", "case2")),
    ("2026-11-07", "ch5", "Chapter 5", "Growth without operations doesn't last.",
     "The Laser Treat case: digitizing a multi-entity clinical group", SITE + "/case/laser-treat/", "case", None),
    ("2026-11-08", "ch6", "Chapter 6", "Prevention only matters if people finish it.",
     "The HSREP initiative", "https://hsraep.org/initiative.html", "initiative", None),
    ("2026-11-09", "ch7", "Chapter 7", "New field. New tool. Same discipline.",
     "The Applied AI page", SITE + "/ai/", "ai", None),
]


def utm(url, d, k, c):
    return url + ("&" if "?" in url else "?") + REEL_UTM.format(d=d, k=k, c=c)


def reel_row(r):
    d, k, label, hook, dest, url, c, also = r[:8]
    at = datetime.time.fromisoformat(r[8]) if len(r) > 8 else None
    ext = not url.startswith(SITE)
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    when = datetime.date.fromisoformat(d).strftime("%b %-d")
    row = (f'<li class="reel" data-date="{d}" data-at="{live_ms(d, at)}" data-k="{k}"><a href="{E(utm(url, d, k, c))}"{tgt}>'
           f'<span class="rk">{E(label)}</span>'
           f'<span class="body"><span class="meta"><time datetime="{d}">{when}</time></span>'
           f'<span class="tt">{E(hook)}</span><span class="dest">{E(dest)}</span></span>'
           f'<span class="go" aria-hidden="true">{"&nearr;" if ext else "&rarr;"}</span></a>')
    if also:
        row += f'<p class="also">Also: <a href="{E(utm(also[1], d, k, also[2]))}" data-to="{E(also[2])}">{E(also[0])}</a></p>'
    return row + "</li>"


def essay_row(e):
    return (f'<li class="row" id="e{e["n"]}" data-n="{e["n"]}" data-lens="{E(e["lens"])}" data-q="{E((e["title"] + " " + e["dek"]).lower())}">'
            f'<a href="{E(e["url"])}" data-slug="{E(e["slug"])}">'
            f'<span class="num">#{e["n"]}</span>'
            f'<span class="body"><span class="meta"><span class="lens l-{E(e["lens"])}">{E(e["lensLabel"])}</span>'
            f'<time datetime="{e["date"]}">{datetime.date.fromisoformat(e["date"]).strftime("%b %-d, %Y")}</time></span>'
            f'<span class="tt">{E(e["title"])}</span><span class="dk">{E(e["dek"])}</span></span>'
            f'<span class="go" aria-hidden="true">&rarr;</span></a></li>')


def press_row(p):
    kind = "TV" if p["tv"] else "Article"
    return (f'<li class="prow"><a href="{E(p["url"])}" target="_blank" rel="noopener">'
            f'<span class="pk {"tv" if p["tv"] else ""}">{kind}</span>'
            f'<span class="body"><span class="meta"><b>{E(p["outlet"])}</b> &middot; {E(p["when"])}</span>'
            f'<span class="tt">{E(p["title"])}</span><span class="dk">{E(p["note"])}</span></span>'
            f'<span class="go" aria-hidden="true">&nearr;</span></a></li>')


def main():
    essays = json.load(open(os.path.join(ROOT, "essays.json")))
    allnum = numbered(essays)
    pub = [e for e in allnum if e["date"] <= TODAY]
    press = press_items(open(os.path.join(ROOT, "index.html"), encoding="utf-8").read())
    lenses = []
    for e in pub:
        if (e["lens"], e["lensLabel"]) not in lenses:
            lenses.append((e["lens"], e["lensLabel"]))
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ig_template.html"), encoding="utf-8").read()
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE + "/ig/#page", "url": SITE + "/ig/",
          "name": "Every post, one tap away | Shafaat Choyon",
          "about": {"@id": SITE + "/#person"},
          "mainEntity": {"@type": "ItemList", "numberOfItems": len(pub), "itemListOrder": "https://schema.org/ItemListOrderAscending",
                         "itemListElement": [{"@type": "ListItem", "position": e["n"], "url": SITE + e["url"], "name": e["title"]} for e in pub]}}
    out = (tpl.replace("{{ESSAY_ROWS}}", "\n".join(essay_row(e) for e in pub))
              .replace("{{PRESS_ROWS}}", "\n".join(press_row(p) for p in press))
              .replace("{{REEL_ROWS}}", "\n".join(reel_row(r) for r in REELS))
              .replace("{{N_ESSAYS}}", str(len(pub)))
              .replace("{{N_PRESS}}", str(len(press)))
              .replace("{{LENS_CHIPS}}", "".join(f'<button type="button" class="chip" data-lens="{E(k)}" aria-pressed="false">{E(v)}</button>' for k, v in lenses))
              .replace("{{LD}}", json.dumps(ld, ensure_ascii=False))
              .replace("{{CALL}}", CALL)
              .replace("{{BUILT}}", TODAY))
    os.makedirs(os.path.join(ROOT, "ig"), exist_ok=True)
    open(os.path.join(ROOT, "ig", "index.html"), "w", encoding="utf-8").write(out)
    print(f"ig/index.html: {len(pub)} essays (#{pub[0]['n']} to #{pub[-1]['n']}), {len(press)} press, {len(allnum) - len(pub)} scheduled")


if __name__ == "__main__":
    main()
