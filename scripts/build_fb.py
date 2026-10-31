#!/usr/bin/env python3
"""Build /fb/index.html: the Facebook hub (link in the Page intro).

Facebook does not make links in this Page's comments clickable (checked 31 Oct 2026), so each
Facebook first comment points here instead. Every Facebook post gets one card with all of its
links (essay, case, tool, Ask Shafaat), newest first, under its essay number: "#125" in the
comment, shafaatalichoyon.com/fb#125 as the address.

Sources (the approved first comments, nothing typed by hand):
  LinkedIn_FourLink_Pack.md, LinkedIn_FourLink_Pack_PartC.md  daily 9:00 PM posts (LinkedIn + Facebook)
  Facebook_Archive_Pack.md                                     Wed/Sat 9:00 AM archive posts
  scripts/build_ig.py REELS                                    Reels (Instagram + Facebook, 7:30 PM)
Each card switches on at its post time (Michigan), same moment for every visitor.

Usage: python3 scripts/build_fb.py [site_root]
"""
import datetime, html, json, os, re, sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ig as ig  # numbering (FIXED_N) and the Reel list stay in one place

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
SITE = ig.SITE
TZ = ZoneInfo("America/Detroit")
E = lambda s: html.escape(str(s), quote=True)
MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
START = datetime.date(2026, 10, 20)  # first Facebook post with four links

KIND = {"essay": ("Read the essay", "e"), "case": ("See the receipt", "c"), "case2": ("See the receipt", "c"),
        "tool": ("Run the tool", "t"), "ask": ("Ask Shafaat", "a"), "hsrep": ("Ask HSREP", "h"),
        "home": ("Start here", "c"), "initiative": ("The initiative", "c"), "ai": ("Applied AI", "c")}


def at_ms(d, hh, mm):
    return int(datetime.datetime.combine(d, datetime.time(hh, mm), tzinfo=TZ).timestamp() * 1000)


def fb_url(u):
    u = u.replace("utm_source=linkedin", "utm_source=facebook").replace("utm_source=instagram", "utm_source=facebook")
    base, _, frag = u.partition("#")
    return base + "&utm_term=fb-hub" + ("#" + frag if frag else "")


def cap1(t):
    t = t.strip().lstrip(",;: ").strip()
    return t[:1].upper() + t[1:] if t else t


def sub_label(text, kind):
    m = re.search(r"\(([^)]*)\)", text)
    if m:
        return cap1(m.group(1))
    if kind == "hsrep":
        return cap1(re.sub(r"^Ask HSREP\s*", "", text)) or "On hsraep.org"
    if kind == "ask":
        return cap1(re.sub(r"^Ask the AI version of me\s*", "", text)) or "The AI version of me"
    return ""


def parse_comment(block):
    links = []
    for line in block.strip().splitlines():
        m = re.match(r"\s*(.*?):\s*(https://\S+)\s*$", line)
        if not m:
            continue
        text, url = m.groups()
        c = (re.search(r"utm_content=([a-z0-9]+)", url) or [None, "essay"])[1]
        if c not in KIND:
            continue
        links.append({"kind": c, "url": fb_url(url), "sub": sub_label(text, c), "text": text})
    return links


def date_from(dd, mon, yy):
    y = int(yy) if yy else (2027 if MON[mon] < 7 else 2026)
    return datetime.date(y, MON[mon], int(dd))


def daily_posts(path):
    t = open(path, encoding="utf-8").read()
    out = []
    for sec in re.split(r"^### ", t, flags=re.M)[1:]:
        m = re.match(r"Day \d+ · \w+ (\d+) (\w{3})(?: (\d{4}))? · ([^·]+) · (.+)", sec.splitlines()[0])
        cm = re.search(r"FIRST COMMENT.*?```text\n(.*?)```", sec, re.S)
        if not m or not cm:
            continue
        d = date_from(m.group(1), m.group(2), m.group(3))
        if d < START:
            continue
        out.append({"d": d, "at": at_ms(d, 21, 0), "kind": "post", "title": m.group(5).strip(), "links": parse_comment(cm.group(1))})
    return out


def archive_posts(path):
    t = open(path, encoding="utf-8").read()
    out = []
    for sec in re.split(r"^### ", t, flags=re.M)[1:]:
        m = re.match(r"FB \d+ · \w+ (\d+) (\w{3}) (\d{4}) · (.+)", sec.splitlines()[0])
        cm = re.search(r"FIRST COMMENT:?\s*```text\n(.*?)```", sec, re.S)
        if not m or not cm:
            continue
        d = date_from(m.group(1), m.group(2), m.group(3))
        out.append({"d": d, "at": at_ms(d, 9, 0), "kind": "archive", "title": m.group(4).strip(), "links": parse_comment(cm.group(1))})
    return out


def reel_posts():
    """Facebook Reels: links from the Facebook first comment (reels_posts.json) when the Reel has one,
    otherwise the caption link from build_ig.REELS (the same page Instagram's card points to)."""
    fbc = {}
    try:
        for r in json.load(open(os.path.join(ROOT, "_local_archive", "reels-video", "reels_posts.json"))):
            fbc[r["key"]] = r.get("fb_comment_links") or r.get("fb_comment", "")
    except FileNotFoundError:
        pass
    out = []
    for r in ig.REELS:
        d0, k, label, hook, dest, url, c, also = r[:8]
        d = datetime.date.fromisoformat(d0)
        hh, mm = (int(x) for x in (r[8] if len(r) > 8 else "19:30").split(":"))
        if fbc.get(k):
            links = parse_comment(fbc[k])
            for l in links:
                if l["kind"] != "ask" and not l["sub"]:
                    l["sub"] = l["text"]
        else:
            q = ig.REEL_UTM.format(d=d0, k=k, c=c).replace("instagram", "facebook")
            links = [{"kind": c if c in KIND else "essay", "url": url + "?" + q + "&utm_term=fb-hub", "sub": dest}]
        out.append({"d": d, "at": at_ms(d, hh, mm), "kind": "reel", "key": k, "title": hook, "rlabel": label, "links": links})
    return out


LAUNCH_LAB = {  # (button, line under it) for the launch posts' non-essay links
    "intro": ("My work, in one place", "Essays, case studies, tools and Ask Shafaat"),
    "start": ("Start at the home page", "Essays, case studies, tools and Ask Shafaat"),
    "home": ("Start at the home page", "Essays, case studies, tools and Ask Shafaat"),
    "impact": ("All 22 case studies", "Every role, with the numbers, mapped as one system"),
    "essays": ("All essays", "120+ essays on growth, AI, health tech and public health"),
    "tools": ("All 48 free tools", "Run them with your own numbers, no sign-up"),
    "advisor": ("Not sure which tool fits?", "Answer a few questions"),
    "identity": ("The mark and the theme", "Chapter by chapter, on hsraep.org"),
    "hsrep": ("HSREP", "The policy-research and advocacy platform I founded"),
}


def launch_posts(path):
    """The 11 posts that opened the Facebook Page (20 Oct 2026). Their first comments now point here."""
    out = []
    for r in json.load(open(path, encoding="utf-8")):
        d = datetime.date(2026, 10, 20)
        hh, mm = (int(x) for x in r["time"].split(":"))
        links = []
        for line in r["comment"].splitlines():
            m = re.match(r"\s*(.*?):\s*(https://\S+)\s*$", line)
            if not m:
                continue
            text, url = m.groups()
            c = re.search(r"utm_content=([a-z0-9]+)", url).group(1)
            essay_post = re.search(r"utm_content=essay(?![a-z])", r["comment"]) is not None
            if essay_post and c in KIND:
                links.append({"kind": c, "url": fb_url(url), "sub": sub_label(text, c), "text": text})
            else:
                lab, sub = LAUNCH_LAB.get(c, ("Open", text)) if c != "ask" else ("Ask Shafaat", "The AI version of me, from my published work")
                if c == "case":
                    lab, sub = "How it was built", "The HSREP case, with the numbers"
                links.append({"kind": "ask" if c == "ask" else ("essay" if c in ("intro", "start", "home") else "case"),
                              "url": fb_url(url), "sub": sub, "text": text, "label": lab})
        out.append({"d": d, "at": at_ms(d, hh, mm), "kind": "launch", "key": r["key"], "title": r["title"],
                    "order": r["order"], "links": links})
    return out


def card(p, emap):
    ess = next((l for l in p["links"] if l["kind"] == "essay"), None)
    e = None
    if ess:
        slug = re.search(r"/([a-z0-9-]+)\.html", ess["url"])
        e = emap.get(slug.group(1)) if slug else None
    n = e["n"] if e else None
    title = e["title"] if e else p["title"]
    lens = (f'<span class="lens l-{E(e["lens"])}">{E(e["lensLabel"])}</span>' if e else "")
    tag = {"post": "Post", "archive": "From the archive", "reel": "Reel", "launch": "Launch post"}[p["kind"]]
    when = p["d"].strftime("%b %-d")
    btns = []
    for l in p["links"]:
        lab, cls = KIND.get(l["kind"], ("Open", "e"))
        if p["kind"] == "reel" and l["kind"] not in ("ask", "hsrep"):
            lab = {"essay": "Read the essay", "case": "See the case", "case2": "See the case", "home": "Start here",
                   "initiative": "The initiative", "ai": "Applied AI"}.get(l["kind"], "Open")
        if l.get("label"):
            lab = l["label"]
        if l["kind"] == "essay" and not l["sub"] and e:
            l = dict(l, sub=f"Essay #{e['n']}, with its sources")
        btns.append(f'<a class="b b-{cls}" href="{E(l["url"])}" data-to="{E(l["kind"])}"><b>{E(lab)}</b>'
                    + (f'<span>{E(l["sub"])}</span>' if l["sub"] else "") + "</a>")
    num = f'<span class="num">#{n}</span>' if n else '<span class="num nn">&middot;</span>'
    kid = f' data-k="{E(p["key"])}"' if p.get("key") else ""
    hid = "" if p["kind"] == "launch" else " hidden"
    return (f'<li class="post"{kid} data-n="{n or ""}" data-at="{p["at"]}" data-date="{p["d"].isoformat()}" data-q="{E((title + " " + p["title"]).lower())}"{hid}>'
            f'<div class="ph">{num}<div class="body"><span class="meta"><span class="pk">{tag}</span>{lens}<time datetime="{p["d"].isoformat()}">{when}</time></span>'
            f'<span class="tt">{E(title)}</span></div></div>'
            f'<div class="btns n{len(btns)}">{"".join(btns)}</div></li>')


EXTRA_CSS = """
.post{background:var(--card);border:1px solid var(--ln);border-radius:18px;padding:14px 14px 12px}
.post.hit{border-color:var(--amb);box-shadow:0 0 0 4px var(--amb-soft)}
.ph{display:flex;gap:12px;align-items:flex-start}
.num.nn{color:var(--tx-4)}
#slist .num.nn{display:none}
#slist .post{scroll-margin-top:80px}
.pk{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--tx-4)}
.btns{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.btns.n1{grid-template-columns:1fr}
.btns .b:last-child:nth-child(odd){grid-column:1/-1}
.b-h b::before{content:"\\2726  ";color:var(--amb)}
.b{display:flex;flex-direction:column;gap:2px;min-width:0;border:1px solid var(--ln);border-radius:13px;padding:10px 12px;background:var(--card-2);transition:border-color .2s}
.b:hover{border-color:var(--acc-line)}
.b b{font-family:var(--disp);font-weight:800;color:var(--tx-1);font-size:14.5px;line-height:1.2}
.b span{font-size:12px;color:var(--tx-3);line-height:1.35;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.b-e{border-color:var(--acc-line);background:linear-gradient(120deg,var(--acc-soft),transparent 70%),var(--card-2)}
.b-e b{color:var(--acc-hi)}
.b-a b::before{content:"\\2726  ";color:var(--acc-hi)}
.howto{margin:14px auto 0;max-width:34em;font-size:13px;color:var(--tx-4)}
@media (max-width:360px){.btns{grid-template-columns:1fr}}
"""

BODY = """<body>
<header class="hd"><div class="wrap hd-in">
  <a class="brand" href="/"><img src="/assets/logos/sc-mark.png" alt="" width="26" height="26">Shafaat Choyon</a>
  <div class="hd-r"><a href="/">Portfolio</a></div>
</div></header>

<main id="main" class="wrap">
  <section class="hero">
    <img class="av" src="/assets/headshot-square.jpg" alt="Md Shafaat Ali Choyon" width="92" height="92">
    <p class="kick">From Facebook</p>
    <h1>Every link from every post.</h1>
    <p class="lede">Type the number from the post. You get the essay, the case behind it, the free tool and the AI version of me, one tap each.</p>
    <form class="jump" id="jump" autocomplete="off">
      <label for="jn">#<input id="jn" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" placeholder="Post number, e.g. 125"></label>
      <button type="submit">Open</button>
    </form>
    <p class="jmsg" id="jmsg" aria-live="polite"></p>
  </section>

  <section class="sec" id="posts" style="padding-top:14px" aria-labelledby="ph">
    <div class="sh"><h2 id="ph">Latest posts</h2><span class="cnt" id="pcnt"></span></div>
    <div class="tools"><input class="srch" id="q" type="search" placeholder="Search posts" aria-label="Search posts"></div>
    <ol class="list" id="plist">
{{CARDS}}
    </ol>
    <p class="empty" id="none" hidden>No post matches that. Try another word, or <a href="/?ask=1&amp;utm_source=facebook&amp;utm_medium=social&amp;utm_term=fb-hub&amp;utm_content=ask">ask the AI version of me</a>.</p>
  </section>

  <section class="sec" id="start" style="padding-top:26px" aria-labelledby="sh2">
    <div class="sh"><h2 id="sh2">Start here</h2><span class="cnt">The 11 posts that opened this Page, 20 Oct 2026</span></div>
    <ol class="list" id="slist">
{{LAUNCH}}
    </ol>
  </section>

  <nav class="qa" aria-label="Quick links" style="margin-top:26px">
    <a class="ask" href="/?ask=1&amp;utm_source=facebook&amp;utm_medium=social&amp;utm_term=fb-hub&amp;utm_content=ask" data-k="ask"><img src="/assets/advisor-avatar.webp" alt="" width="46" height="46"><span style="display:flex;flex-direction:column;gap:3px"><i>Live &middot; AI</i><b>Ask the AI version of me</b><span>Answers only from my published work, with sources.</span></span></a>
    <a href="/tools.html?utm_source=facebook&amp;utm_medium=social&amp;utm_term=fb-hub" data-k="tools"><i>Free</i><b>48 free tools</b><span>Calculators and checkers for growth and health teams.</span></a>
    <a class="call" href="{{CALL}}" data-k="call"><i>30 minutes</i><b>Book a free call</b><span>Bring a problem with a number attached.</span></a>
  </nav>

  <footer class="ft">
    <p><a href="/">Portfolio</a> &middot; <a href="/essays.html">All essays</a> &middot; <a href="/ig/">Instagram links</a> &middot; <a href="/privacy.html">Privacy</a></p>
    <p>&copy; 2026 Md Shafaat Ali Choyon</p>
  </footer>
</main>

<script>
(function(){
  var $=function(s){return document.querySelector(s)}, $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};
  function t(e,a,n){n=n||0;try{if(window.__gaOn&&window.track){window.track(e,a||{});}else if(n<40){setTimeout(function(){t(e,a,n+1);},250);}}catch(_){}}
  var now=Date.now(), list=$('#plist'), q='';
  /* A card appears at its post time (Michigan), newest first. */
  var cards=$$('#plist .post').filter(function(c){return now>=+c.dataset.at});
  cards.sort(function(a,b){return b.dataset.at-a.dataset.at}).forEach(function(c){c.hidden=false;list.appendChild(c)});
  $('#pcnt').textContent=cards.length+' posts, newest first';
  /* "#125" opens the newest card for essay 125 */
  var seen={};cards.concat($$('#slist .post')).forEach(function(c){var n=c.dataset.n;if(n&&!seen[n]){seen[n]=1;c.id='p'+n;}});
  function apply(){var shown=0;cards.forEach(function(c){var ok=!q||c.dataset.q.indexOf(q)>-1;c.hidden=!ok;if(ok)shown++;});$('#none').hidden=shown>0;}
  var qi=$('#q'),qt;qi.addEventListener('input',function(){q=qi.value.trim().toLowerCase();apply();clearTimeout(qt);qt=setTimeout(function(){if(q)t('fb_search',{len:q.length})},900);});
  function go(n,src){var c=document.getElementById('p'+n),m=$('#jmsg');
    if(!c){m.innerHTML='#'+n+' has no Facebook post yet. <a href="/ig/#'+n+'">Find essay #'+n+' here</a>.';t('fb_jump_miss',{n:n});return;}
    q='';qi.value='';apply();m.textContent='';$$('.post.hit').forEach(function(x){x.classList.remove('hit')});c.classList.add('hit');c.scrollIntoView({block:'center'});t('fb_jump',{n:n,from:src});}
  $('#jump').addEventListener('submit',function(e){e.preventDefault();var n=parseInt(($('#jn').value||'').replace(/\\D/g,''),10);if(n)go(n,'box');});
  function fromHash(){var raw=(location.hash||'').slice(1),h=raw.replace(/^[ep]?/,'');if(/^\\d+$/.test(h)){go(parseInt(h,10),'link');return;}
    var c=raw&&document.querySelector('.post[data-k="'+raw.replace(/[^a-z0-9-]/gi,'')+'"]');if(c&&!c.hidden){q='';qi.value='';apply();$$('.post.hit').forEach(function(x){x.classList.remove('hit')});c.classList.add('hit');c.scrollIntoView({block:'center'});t('fb_jump',{k:raw,from:'link'});}}
  fromHash();window.addEventListener('hashchange',fromHash);
  [list,$('#slist')].forEach(function(L){L.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;var c=a.closest('.post');t('fb_open',{n:+c.dataset.n||0,to:a.dataset.to,date:c.dataset.date,k:c.dataset.k||''});});});
  $$('.qa a').forEach(function(a){a.addEventListener('click',function(){t('fb_quick',{k:a.dataset.k})})});
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a||a.closest('#plist,#slist,.qa'))return;var to='';try{var u=new URL(a.href,location.href);to=u.host===location.host?u.pathname:u.host;}catch(_){}t('fb_link',{area:a.closest('.hd')?'header':a.closest('.ft')?'footer':'body',to:to});});
})();
</script>
<script src="/assets/ask-launch.js?v=20261023a" defer></script>
</body>
</html>
"""


def main():
    essays = json.load(open(os.path.join(ROOT, "essays.json")))
    emap = {e["slug"]: e for e in ig.numbered(essays)}
    posts = (daily_posts(os.path.join(ROOT, "LinkedIn_FourLink_Pack.md")) + daily_posts(os.path.join(ROOT, "LinkedIn_FourLink_Pack_PartC.md"))
             + archive_posts(os.path.join(ROOT, "Facebook_Archive_Pack.md")) + reel_posts())
    posts.sort(key=lambda p: -p["at"])
    tpl = open(os.path.join(HERE, "ig_template.html"), encoding="utf-8").read()
    head = tpl[:tpl.index("</style>")] + EXTRA_CSS + "</style>\n</head>\n"
    head = (head.replace("Every post, one tap away | Shafaat Choyon", "Every link from every Facebook post | Shafaat Choyon")
                .replace("The link in bio for Shafaat Choyon's Instagram: every essay numbered oldest to newest, the AI version of him, free tools and press coverage, one tap each.",
                         "The link in the Facebook Page intro: every post's essay, case, free tool and Ask Shafaat link, under the number in the post.")
                .replace("https://shafaatalichoyon.com/ig/", "https://shafaatalichoyon.com/fb/")
                .replace('content="Every post, one tap away"', 'content="Every link from every post"')
                .replace("Every essay from Instagram, numbered. Type the number from the post, or browse them all.", "Type the number from the Facebook post: essay, case, tool and Ask Shafaat, one tap each.")
                .replace('<script type="application/ld+json">{{LD}}</script>\n', ""))
    launch = sorted(launch_posts(os.path.join(ROOT, "_local_archive", "fb", "launch", "launch_comments.json")),
                    key=lambda p: (p["order"] != 11, p["order"]))  # "Start here" first, then posting order
    out = (head + BODY.replace("{{CARDS}}", "\n".join(card(p, emap) for p in posts))
           .replace("{{LAUNCH}}", "\n".join(card(p, emap) for p in launch)).replace("{{CALL}}", ig.CALL))
    os.makedirs(os.path.join(ROOT, "fb"), exist_ok=True)
    open(os.path.join(ROOT, "fb", "index.html"), "w", encoding="utf-8").write(out)
    nolink = [p["d"].isoformat() for p in posts if len(p["links"]) < (1 if p["kind"] == "reel" else 4)]
    print(f"fb/index.html: {len(launch)} launch cards + {len(posts)} cards ({sum(p['kind']=='post' for p in posts)} posts, {sum(p['kind']=='archive' for p in posts)} archive, {sum(p['kind']=='reel' for p in posts)} reels); under 4 links: {nolink}")


if __name__ == "__main__":
    main()
