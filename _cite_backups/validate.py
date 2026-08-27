import re, glob, os, json
CIT=json.load(open("_cite_backups/citations.json"))
bad=[]
for slug in list(CIT.keys())+['the-verification-gap-in-ai-code','aging-happens-fast']:
    fn=slug+".html"
    if not os.path.exists(fn): continue
    s=open(fn,encoding='utf-8').read()
    refs=set(int(x) for x in re.findall(r'href="#src-(\d+)"', s))
    ids=set(int(x) for x in re.findall(r'id="src-(\d+)"', s))
    hascss = '.cref{' in s
    hassec = '<section class="sources"' in s
    if not refs and not ids: 
        bad.append((slug,"NO CITATIONS AT ALL")); continue
    if refs!=ids:
        bad.append((slug,f"MISMATCH refs={sorted(refs)} ids={sorted(ids)}"))
    if refs and not hascss:
        bad.append((slug,"has sups but NO .cref CSS"))
    if ids and not hassec:
        bad.append((slug,"has src ids but no <section sources>"))
print("Validated",len([f for f in CIT])+2,"essays.")
if not bad: print("ALL CONSISTENT ✓")
for a,b in bad: print("  ✗",a,"::",b)
