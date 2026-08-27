import json, re, os
CIT=json.load(open("_cite_backups/citations.json"))
MAT={e['slug']:e for e in json.load(open("_cite_backups/matrix.json"))} if os.path.exists("_cite_backups/matrix.json") else None

def inside_tag(s,pos): return s.rfind('<',0,pos) > s.rfind('>',0,pos)

STOP=set("the a an of to in on for and or is are was were be been being with as by at from that this it its their his her our your not now new more most than then into over under across per about roughly around already still only just even also".split())

def cand_phrases(dp):
    c=[]
    # quoted
    for m in re.finditer(r"'([^']{4,45})'", dp): c.append(m.group(1))
    for m in re.finditer(r'"([^"]{4,45})"', dp): c.append(m.group(1))
    # capitalized multiword sequences
    for m in re.finditer(r'([A-Z][a-zA-Z0-9.&-]+(?:\s+[A-Z][a-zA-Z0-9.&-]+){0,4})', dp):
        if len(m.group(1))>4: c.append(m.group(1))
    # distinctive lowercase 3-6 word shingles
    words=re.findall(r"[A-Za-z0-9%$.,-]+", dp)
    for n in (6,5,4,3):
        for i in range(len(words)-n+1):
            seg=words[i:i+n]
            if sum(1 for w in seg if w.lower() in STOP)>n//2: continue
            phrase=' '.join(seg).strip('.,')
            if len(phrase)>=12: c.append(phrase)
    # dedupe, longest first
    seen=[]
    for x in c:
        x=x.strip()
        if x and x not in seen: seen.append(x)
    seen.sort(key=len, reverse=True)
    return seen

fixed=[]; still=[]
for slug,d in CIT.items():
    zc=d.get('sources_without_anchor') or []
    # recompute zero-cov from current file (some may have been placed)
    fn=slug+".html"
    if not os.path.exists(fn): continue
    if not zc: continue
    s=open(fn,encoding='utf-8').read()
    astart=s.find('<article'); bio=s.find('<section class="sources"')
    if bio<0: bio=s.find('<p class="bio"')
    if astart<0 or bio<0: continue
    # map src->points
    from collections import defaultdict
    byp=defaultdict(list)
    for p in d['points']: byp[p['src']].append(p['dp'])
    inserts=[]
    for n in zc:
        placed=False
        for dp in byp.get(n,[]):
            for ph in cand_phrases(dp):
                pos=s.find(ph, astart, bio)
                if pos<0: continue
                # ensure unique-ish (first occurrence) and not inside tag
                if inside_tag(s,pos): continue
                end=pos+len(ph)
                ins=end
                for tag in ('</b>','</strong>','</a>'):
                    if s[ins:ins+len(tag)]==tag: ins+=len(tag); break
                inserts.append((ins,n)); placed=True; break
            if placed: break
        if not placed: still.append((slug,n,byp.get(n,[''])[0][:70]))
    for pos,n in sorted(inserts,key=lambda x:-x[0]):
        s=s[:pos]+('<sup class="cref"><a href="#src-%d">%d</a></sup>'%(n,n))+s[pos:]
    if inserts:
        open(fn,'w',encoding='utf-8').write(s); fixed.append((slug,[n for _,n in inserts]))
print("essays fixed:",len(fixed))
for a,b in fixed: print("  +",a,b)
print("--- STILL MISSING (hand-place) ---")
for a,b,c in still: print("  ",a,"src",b,"::",c)
