import re, glob, os, json
from PIL import Image
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pages=['index.html','essays.html','writing.html']+[f for f in glob.glob('*.html') if 'backup' not in f and 'newlanding' not in f and 'HSREP' not in f and 'Homepage' not in f]+glob.glob('case/*/index.html')
pages=list(dict.fromkeys(pages))
pat=re.compile(r'((?:src|data-src|data-zoom|poster)=")(/?)(assets/[^"]+\.(?:png|jpe?g))(")',re.I)
refs=set()
for p in pages:
    s=open(p,encoding='utf-8',errors='ignore').read()
    for m in pat.finditer(s): refs.add(m.group(3))
adopted={}; before=0; after=0; fails=[]
for i,f in enumerate(sorted(refs)):
    if not os.path.exists(f): continue
    src_sz=os.path.getsize(f)
    w=os.path.splitext(f)[0]+'.webp'
    try:
        if os.path.exists(w) and os.path.getmtime(w)>os.path.getmtime(f):
            wsz=os.path.getsize(w)
        else:
            im=Image.open(f); ext=f.lower().rsplit('.',1)[1]
            if ext=='png':
                im2=im.convert('RGBA') if im.mode not in('RGB','RGBA') else im
                im2.save('_cite_backups/_t1.webp','WEBP',lossless=True,method=4)
                s1=os.path.getsize('_cite_backups/_t1.webp')
                im2.save('_cite_backups/_t2.webp','WEBP',quality=90,method=4)
                s2=os.path.getsize('_cite_backups/_t2.webp')
                pick='_cite_backups/_t1.webp' if s1<=s2 else '_cite_backups/_t2.webp'
            else:
                im.convert('RGB').save('_cite_backups/_t2.webp','WEBP',quality=82,method=4); pick='_cite_backups/_t2.webp'
            os.replace(pick,w); wsz=os.path.getsize(w)
        if wsz <= src_sz*0.85:
            adopted[f]=1; before+=src_sz; after+=wsz
        else:
            os.remove(w)
    except Exception as e:
        fails.append((f,str(e)[:60]))
    if i%25==0: print(f"...{i}/{len(refs)}",flush=True)
print(f"ADOPTED {len(adopted)}/{len(refs)} | {before/1e6:.1f}MB -> {after/1e6:.1f}MB")
if fails: print("FAILS:",fails[:6])
changed=0
for p in pages:
    s=open(p,encoding='utf-8',errors='ignore').read()
    def sub(m):
        f=m.group(3)
        if f in adopted: return m.group(1)+m.group(2)+os.path.splitext(f)[0]+'.webp'+m.group(4)
        return m.group(0)
    s2=pat.sub(sub,s)
    if s2!=s: open(p,'w',encoding='utf-8').write(s2); changed+=1
print("PAGES REWRITTEN:",changed)
print("DONE")
