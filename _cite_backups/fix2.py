import re
def load(f): return open(f,encoding='utf-8').read()
def save(f,s): open(f,'w',encoding='utf-8').write(s)
def sup(n): return '<sup class="cref"><a href="#src-%d">%d</a></sup>'%(n,n)

# healthtech: reword remaining body 73% clause + place src3
f='healthtech-leapfrog.html'; s=load(f)
old='where about <b>73%</b> of urban patients already book care on an app,'
new='where telehealth is still an early but rising habit'+sup(3)+',' 
assert old in s, "ht 73% body missing"
s=s.replace(old,new)
# ensure no stray 73% remains that means the app claim
save(f,s)

# brand: capital-G variant
f='brand-vs-performance.html'; s=load(f)
s=s.replace('Global digital ad spend has crossed','Global ad spend has crossed')
save(f,s)

# health-ai: apostrophe-tolerant Google->BCG
f='health-ai-2027-bet.html'; s=load(f)
s=re.sub(r"Google[’']s own research","BCG's research",s)
save(f,s)

# grad-jobs: any 37.3% -> 38%
f='grad-jobs-disappearing.html'; s=load(f)
s=s.replace('37.3%','38%')
save(f,s)

# gen-z: all 70% -> two-thirds (86% untouched)
f='gen-z-pay-cut-for-ethics.html'; s=load(f)
s=re.sub(r'70%','two-thirds',s)
save(f,s)

# social-commerce: body $3B/$4B + place src1
f='social-commerce-growth.html'; s=load(f)
old='<b>$3 billion</b> in 2025 and is climbing toward $4 billion'
new='<b>$6 billion</b> in 2025 and is climbing toward $10 billion by 2029'
assert old in s, "social body missing"
s=s.replace(old,new)
# place src1 after body "more than 300,000 sellers</b>" (first in article body)
a=s.find('<article'); b=s.find('<section class="sources"')
anc='<b>more than 300,000 sellers</b>'
pos=s.find(anc,a,b)
assert pos>0,"social sellers anchor missing"
ins=pos+len(anc)
s=s[:ins]+sup(1)+s[ins:]
save(f,s)
print("FIX2 DONE")
