import re, os
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
def dom(u):
    m=re.search(r'https?://([^/]+)',u); d=m.group(1) if m else u
    return d[4:] if d.startswith('www.') else d
def sup(n): return '<sup class="cref"><a href="#src-%d">%d</a></sup>'%(n,n)

# per-essay: corrections=[(old,new)...] replace_all ; sources=[(n,publisher,url)] ; place=[(anchor, n)] in body
CFG={
 'healthtech-leapfrog':{
   'corr':[('6 doctors per 100,000 people','6 doctors per 10,000 people'),
           ('6 doctors per 100k','6 doctors per 10k'),
           ('and about 73% of urban patients already booking care on an app','and telehealth adoption still early but climbing'),
           ('73% book care by app','telehealth still emerging')],
   'sources':[(1,'World Bank (physicians per 1,000, Bangladesh)','https://data.worldbank.org/indicator/SH.MED.PHYS.ZS?locations=BD'),
              (2,'World Bank','https://www.worldbank.org/en/news/press-release/2023/08/30/world-bank-helps-bangladesh-improve-primary-healthcare-in-cities'),
              (3,'BMC Digital Health (Bangladesh telehealth survey)','https://link.springer.com/article/10.1186/s44247-024-00106-8')],
   'place':[('6 doctors per 10,000 people',1),('telehealth adoption still early but climbing',3),('$200M',2)],
 },
 'the-first-1000-days':{
   'corr':[('30% of births still at home','35% of births still at home')],
   'sources':[(1,'UNFPA Bangladesh','https://bangladesh.unfpa.org/en/news/uncertainty-aid-commitments'),
              (2,'Commonwealth Fund','https://www.commonwealthfund.org/publications/issue-briefs/2024/jun/insights-us-maternal-mortality-crisis'),
              (3,'UNICEF','https://www.unicef.org/bangladesh/en/press-releases/bangladesh-has-highest-stillbirth-rate-south-asia'),
              (4,'DHS Program / NIPORT (Bangladesh DHS 2022)','https://www.dhsprogram.com/pubs/pdf/PR148/PR148.pdf'),
              (5,'World Health Organization','https://www.who.int/bangladesh/activities/strengthening-vaccination-coverage/strengthening-vaccination-coverage')],
   'place':[('roughly 79%',1),('63,000 stillbirths',3),('35% of births still at home',4),('above 90%',5)],  # src2 already placed by pass2
 },
 'brand-vs-performance':{
   'corr':[('global digital ad spend has crossed $1 trillion','global ad spend has crossed $1 trillion')],
   'sources':[(1,'Taboola','https://investors.taboola.com/news-releases/news-release-details/taboola-reports-record-results'),
              (2,'WARC','https://www.warc.com/content/feed/global-advertising-spend-to-pass-1-trillion-for-the-first-time-this-year/en-GB/10119')],
   'place':[('diminishing returns',1),('global ad spend has crossed $1 trillion',2)],
 },
 'health-ai-2027-bet':{
   'corr':[("Google's own research pins roughly 70%","BCG's research pins roughly 70%")],
   'sources':[(1,'MIT (NANDA initiative)','https://www.legal.io/blog/5719519/MIT-Report-Finds-95-of-AI-Pilots-Fail'),
              (2,'Boston Consulting Group (BCG) — the 10-20-70 rule','https://www.bcg.com/publications/2024/the-leaders-guide-to-transforming-with-ai')],
   'place':[('95% of enterprise AI pilots',1),("BCG's research pins roughly 70%",2)],
 },
 'social-commerce-growth':{
   'corr':[('crossed $3 billion in 2025','crossed $6 billion in 2025')],
   'sources':[(1,'Ashraful Islam (LinkedIn), citing F-commerce data','https://www.linkedin.com/posts/ashraful-islam-659295169_digitalmarketing-fcommerce-ecommerce-activity-7348365897658417155-sPv6'),
              (2,'ResearchAndMarkets — Bangladesh B2C e-commerce, 2025','https://www.researchandmarkets.com/reports/6191236/bangladesh-b2c-ecommerce-market-size-and-forecast')],
   'place':[('300,000+ sellers',1),('crossed $6 billion in 2025',2)],
 },
 'grad-jobs-disappearing':{
   'corr':[('37.3% of UK workers','38% of UK workers')],
   'sources':[(1,'The Guardian','https://www.theguardian.com/business/2025/jun/30/uk-entry-level-jobs-chatgpt-launch-adzuna'),
              (2,'Institute of Student Employers','https://ise.org.uk/knowledge/insights/410/record_graduate_job_applications/'),
              (3,'BSS (citing UNFPA / census)','https://www.bssnews.net/news-flash/289857'),
              (4,'New Possible, What Workers Want 2026','https://newpossible.io/resources/what-workers-want-2026-findings')],
   'place':[('fell 33% year-on-year',1),('17,000',2),('170 million people',3),('38% of UK workers',4)],
 },
 'gen-z-pay-cut-for-ethics':{
   'corr':[('70% would take a lower salary','roughly two-thirds would take a lower salary')],
   'sources':[(1,'Deloitte Global Gen Z & Millennial Survey','https://www.deloitte.com/us/en/insights/topics/talent/2025-gen-z-millennial-survey.html'),
              (2,'Bupa Wellbeing Index (via The HR Director)','https://www.thehrdirector.com/features/the-workplace/nearly-half-gen-z-workers-take-pay-cut-move-sustainable-role/')],
   'place':[('86%',1),('roughly two-thirds would take a lower salary',2)],
 },
 'nutrition-transition':{
   'corr':[('weight gain independent of calorie count','weight gain, because people freely ate about 500 more calories a day on it')],
   'sources':[(1,'International Diabetes Federation','https://diabetesatlas.org/data-by-location/country/bangladesh/'),
              (2,'NIH Clinical Center (Hall et al., Cell Metabolism 2019)','https://www.cc.nih.gov/news/2019/summer/story-01'),
              (3,'NIH / published research (ultra-processed food intake)','https://pmc.ncbi.nlm.nih.gov/articles/PMC8532572/')],
   'place':[('more than 13 million adults',1)],  # src2,3 placed by pass2
 },
}
def inside_tag(s,pos): return s.rfind('<',0,pos)>s.rfind('>',0,pos)
for slug,c in CFG.items():
    fn=slug+".html"; s=open(fn,encoding='utf-8').read()
    for old,new in c['corr']:
        assert old in s, "%s: correction anchor missing: %s"%(slug,old)
        s=s.replace(old,new)
    # place sups in body region
    astart=s.find('<article'); bend=s.find('<p class="bio"')
    ins=[]
    for anc,n in c['place']:
        pos=s.find(anc,astart,bend)
        if pos<0: print("  !! %s place miss: %s"%(slug,anc)); continue
        end=pos+len(anc)
        for tag in ('</b>','</strong>'):
            if s[end:end+len(tag)]==tag: end+=len(tag); break
        ins.append((end,n))
    for pos,n in sorted(ins,key=lambda x:-x[0]):
        s=s[:pos]+sup(n)+s[pos:]
    # sources section before bio
    lis=['<li id="src-%d">%s. <a href="%s" target="_blank" rel="noopener">%s &#8599;</a></li>'%(n,pub,url,dom(url)) for n,pub,url in c['sources']]
    sec='<section class="sources" aria-label="Sources">\n<h2>Sources</h2>\n<ol>\n'+'\n'.join(lis)+'\n</ol>\n</section>\n'
    b=s.find('<p class="bio"'); s=s[:b]+sec+s[b:]
    if '.cref{' not in s:
        st=s.find('</style>'); s=s[:st]+CSS+s[st:]
    open(fn,'w',encoding='utf-8').write(s); print("done",slug)
print("CORRECTIONS COMPLETE")
