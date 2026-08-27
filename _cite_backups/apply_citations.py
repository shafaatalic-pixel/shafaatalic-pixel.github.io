import json, re, os, sys, glob

CIT=json.load(open("_cite_backups/citations.json"))
ONLY=os.environ.get("CIT_ONLY","").strip()
only=set(s for s in ONLY.split(",") if s) if ONLY else None

CSS='''
.cref{font-size:.6em;font-weight:700;vertical-align:super;line-height:0;margin-left:1px;white-space:nowrap}
.cref a{color:var(--teal);text-decoration:none}
.cref a:hover{text-decoration:underline}
.sources{margin:40px 0 0;padding:22px 0 0;border-top:1px solid var(--line)}
.sources h2{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);margin:0 0 14px}
.sources ol{margin:0;padding:0 0 0 22px}
.sources li{font-size:13.5px;line-height:1.55;color:var(--muted);margin:0 0 10px;padding-left:5px}
.sources li a{color:var(--teal);text-decoration:none;word-break:break-word}
.sources li a:hover{text-decoration:underline}
.sources li:target{background:rgba(51,196,196,.10);border-radius:6px;box-shadow:0 0 0 6px rgba(51,196,196,.10)}
:target{scroll-margin-top:90px}
'''
def domain(u):
    m=re.search(r'https?://([^/]+)', u); d=m.group(1) if m else u
    return d[4:] if d.startswith('www.') else d
def esc(s): return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def inside_tag(s,pos):
    return s.rfind('<',0,pos) > s.rfind('>',0,pos)

done=[]; logs=[]
for slug,d in CIT.items():
    if only and slug not in only: continue
    if d.get('correction'): continue
    fn=slug+".html"
    if not os.path.exists(fn): logs.append((slug,"FILE MISSING")); continue
    s=open(fn,encoding='utf-8').read()
    if '<section class="sources"' in s: logs.append((slug,"already processed - skip")); continue
    astart=s.find('<article')
    bio=s.find('<p class="bio"')
    if astart<0 or bio<0: logs.append((slug,"no article/bio anchor")); continue
    # collect insertions within (astart,bio)
    inserts=[]; used=[]; covered=set()
    def overlaps(a,b):
        return any(not(b<=x or a>=y) for x,y in used)
    for p in d['points']:
        placed=False
        for anc in p['anchors']:
            start=astart
            while True:
                pos=s.find(anc, start, bio)
                if pos<0: break
                end=pos+len(anc)
                if inside_tag(s,pos) or overlaps(pos,end):
                    start=pos+1; continue
                # advance past trailing </b> or </strong>
                ins=end
                for tag in ('</b>','</strong>'):
                    if s[ins:ins+len(tag)]==tag: ins+=len(tag); break
                inserts.append((ins,p['src'])); used.append((pos,end)); covered.add(p['src']); placed=True
                break
            if placed: break
    # apply superscripts in reverse
    for pos,n in sorted(inserts, key=lambda x:-x[0]):
        s=s[:pos]+('<sup class="cref"><a href="#src-%d">%d</a></sup>'%(n,n))+s[pos:]
    # build + insert sources before bio (re-find)
    lis=[]
    for src in d['sources']:
        pub=esc(src['publisher'] or src['url'])
        lis.append('<li id="src-%d">%s. <a href="%s" target="_blank" rel="noopener">%s &#8599;</a></li>'%(src['n'],pub,src['url'],domain(src['url'])))
    sec='<section class="sources" aria-label="Sources">\n<h2>Sources</h2>\n<ol>\n'+'\n'.join(lis)+'\n</ol>\n</section>\n'
    bio2=s.find('<p class="bio"')
    s=s[:bio2]+sec+s[bio2:]
    # insert CSS
    if '.cref{' not in s:
        st=s.find('</style>'); s=s[:st]+CSS+s[st:]
    open(fn,'w',encoding='utf-8').write(s)
    zero=[src['n'] for src in d['sources'] if src['n'] not in covered]
    done.append(slug)
    if zero: logs.append((slug,"sources with 0 placements: "+",".join(map(str,zero))))
print("PROCESSED:",len(done))
print("--- logs ---")
for a,b in logs: print(" ",a,"::",b)
