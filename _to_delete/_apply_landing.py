#!/usr/bin/env python3
# Faithful port of the approved landing-video prototype into the live index.html
import io, sys, datetime

PATH = "index.html"
s = io.open(PATH, "r", encoding="utf-8").read()
orig = s

NEW_CSS = r'''
 #landing.vhero{position:fixed;inset:0;z-index:300;overflow:hidden;isolation:isolate;display:block;padding:0;background:var(--lpagebg);--livory:#F7F2E8;--lbody:#C3CBD5;--lmuted:#8A94A0;--lfaint:#7E8894;--lteal:#0FB3B3;--lteal4:#3AD0D0;--lamber:#F4A24C;--lcard:rgba(16,23,31,.66);--lcardbd:rgba(255,255,255,.10);--lpagebg:#080C11}
 :root[data-theme="light"] #landing.vhero{--lbody:#D7DCE2;--lmuted:#AEB6BF;--lfaint:#9AA2AB;--lteal4:#4FE0E0;--lcard:rgba(255,255,255,.90);--lcardbd:rgba(255,255,255,.7);--lpagebg:#FBF8F1}
 #landing .vhero-vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:64% 40%;z-index:0}
 #landing .vhero-scrim{position:absolute;inset:0;z-index:1;transition:opacity 1s ease;background:linear-gradient(90deg,rgba(6,9,13,.9) 0%,rgba(6,9,13,.74) 30%,rgba(6,9,13,.36) 52%,rgba(6,9,13,.05) 74%,transparent 88%),linear-gradient(0deg,rgba(6,9,13,.9) 1%,transparent 26%),linear-gradient(180deg,rgba(6,9,13,.6),transparent 16%)}
 :root[data-theme="light"] #landing .vhero-scrim{background:linear-gradient(90deg,rgba(6,9,13,.82) 0%,rgba(6,9,13,.62) 30%,rgba(6,9,13,.28) 52%,rgba(6,9,13,.04) 74%,transparent 88%),linear-gradient(0deg,rgba(6,9,13,.86) 1%,transparent 26%),linear-gradient(180deg,rgba(6,9,13,.5),transparent 16%)}
 #landing > canvas{display:none!important}
 #landing .bar{position:absolute;top:0;left:0;right:0;z-index:6;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:18px clamp(24px,4vw,56px);opacity:0;transform:translateY(-8px);transition:opacity .8s ease,transform .8s ease}
 #landing.playing .bar{opacity:1;transform:none}
 #landing .brand{display:inline-flex;align-items:center;gap:11px;font-family:var(--disp);font-weight:800;font-size:19px;letter-spacing:-.01em;color:var(--livory);text-decoration:none}
 #landing .brand img{width:32px;height:32px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:1px solid rgba(255,255,255,.25)}
 #landing .brand .dot{color:var(--lteal4)}
 #landing .navr{display:flex;align-items:center;gap:12px}
 #landing .tgl{width:38px;height:38px;border:1px solid rgba(255,255,255,.24);border-radius:9px;background:rgba(8,12,17,.35);color:var(--livory);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
 #landing .book{display:inline-flex;align-items:center;height:38px;padding:0 18px;background:var(--lteal);color:#042020;border-radius:9px;font-family:var(--disp);font-weight:700;font-size:14px;text-decoration:none}
 #landing .wrap{position:relative;z-index:5;height:100%;max-width:1300px;margin:0 auto;padding:84px clamp(24px,4vw,56px) 104px;display:flex;align-items:center}
 #landing .panel{width:min(56%,700px)}
 #landing .rv{opacity:0;transform:translateY(24px);transition:opacity .85s cubic-bezier(.16,1,.3,1),transform .85s cubic-bezier(.16,1,.3,1)}
 #landing.entered .rv{opacity:1;transform:none}
 #landing .eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--lteal4);display:inline-flex;align-items:center;gap:10px;margin-bottom:16px}
 #landing .eyebrow i{width:7px;height:7px;border-radius:50%;background:var(--lteal);box-shadow:0 0 12px var(--lteal)}
 #landing .vh1{font-family:var(--disp);font-weight:800;font-size:clamp(28px,3.6vw,46px);line-height:1;letter-spacing:-.03em;color:var(--livory);margin:0 0 11px;max-width:none}
 #landing .lead{font-family:var(--body);font-size:clamp(13px,1.25vw,14.5px);line-height:1.5;color:var(--lbody);max-width:50ch;margin:0 0 16px}
 #landing .acts{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:18px}
 #landing .btn2{display:inline-flex;align-items:center;gap:8px;height:46px;padding:0 22px;border-radius:10px;background:var(--lteal);color:#042020;font-family:var(--disp);font-weight:700;font-size:14px;white-space:nowrap;border:0;cursor:pointer;box-shadow:0 12px 30px -16px rgba(15,179,179,.6)}
 #landing .btn2 svg{width:14px;height:14px;stroke:#042020;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round}
 #landing .ghost{display:inline-flex;align-items:center;gap:8px;height:46px;padding:0 17px;border-radius:10px;background:rgba(8,12,17,.4);border:1px solid rgba(255,255,255,.22);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);color:var(--livory);font-family:var(--disp);font-weight:700;font-size:14px;cursor:pointer}
 #landing .ghost svg{width:13px;height:13px;fill:var(--lteal4)}
 #landing .scrollh{background:none;border:0;cursor:pointer;font-family:var(--body);font-size:13px;color:var(--lbody);border-bottom:1px solid rgba(255,255,255,.3);padding:3px 1px}
 #landing .fineln{margin-top:11px;font-family:var(--mono);font-size:11px;letter-spacing:.03em;color:var(--lfaint)}
 #landing .cards{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:12px;max-width:620px}
 #landing .lc{--ctitle:#F7F2E8;--cbody:#AAB4BE;--cind:#7E8894;position:relative;text-align:left;background:var(--lcard);border:1px solid var(--lcardbd);border-radius:14px;padding:14px 15px 12px;cursor:pointer;overflow:hidden;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);display:flex;flex-direction:column;transition:transform .24s cubic-bezier(.2,.7,.2,1),border-color .2s,box-shadow .24s;box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 2px 4px rgba(0,0,0,.25),0 20px 40px -26px rgba(0,0,0,.75)}
 :root[data-theme="light"] #landing .lc{--ctitle:#12171D;--cbody:#4B5560;--cind:#9AA2AB;box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 2px 4px rgba(60,50,30,.08),0 20px 40px -26px rgba(60,50,30,.4)}
 #landing .lc::before{content:"";position:absolute;top:0;left:16px;right:16px;height:2px;background:linear-gradient(90deg,transparent,var(--lens),transparent);opacity:0;transition:opacity .2s}
 #landing .lc:hover{transform:translateY(-5px);border-color:var(--lens);box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 4px 8px rgba(0,0,0,.28),0 30px 54px -24px rgba(0,0,0,.6),0 0 0 1px var(--lens)}
 :root[data-theme="light"] #landing .lc:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 6px 14px rgba(60,50,30,.12),0 30px 54px -24px rgba(60,50,30,.35),0 0 0 1px var(--lens)}
 #landing .lc:hover::before{opacity:1}
 #landing .crow{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
 #landing .chip{width:40px;height:40px;border-radius:11px;background:var(--lenssoft);border:1px solid var(--lcardbd);display:flex;align-items:center;justify-content:center;color:var(--lens);box-shadow:inset 0 1px 0 rgba(255,255,255,.12)}
 #landing .chip svg{width:22px;height:22px;color:var(--lens);overflow:visible}
 #landing .ind{width:24px;height:24px;border-radius:50%;border:1px solid var(--lcardbd);color:var(--cind);display:flex;align-items:center;justify-content:center;transition:transform .3s,color .2s,border-color .2s}
 #landing .ind svg{width:13px;height:13px;stroke:currentColor;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
 #landing .lc:hover .ind{transform:rotate(45deg);color:var(--lens);border-color:var(--lens)}
 #landing .lc:hover .chip{transform:translateY(-1px) scale(1.04);transition:transform .2s}
 #landing .ey{font-family:var(--mono);font-weight:500;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--lens);margin-bottom:5px;line-height:1.4;min-height:24px}
 :root[data-theme="light"] #landing .ey{color:var(--lensd)}
 #landing .tt{font-family:var(--disp);font-weight:700;font-size:15.5px;line-height:1.16;letter-spacing:-.01em;color:var(--ctitle);margin-bottom:5px}
 #landing .ds{font-family:var(--body);font-size:11.5px;line-height:1.42;color:var(--cbody);margin-bottom:11px}
 #landing .enter{margin-top:auto;font-family:var(--disp);font-weight:700;font-size:11.5px;color:var(--lens);display:inline-flex;align-items:center;gap:6px}
 :root[data-theme="light"] #landing .enter{color:var(--lensd)}
 #landing .enter svg{width:12px;height:12px;stroke:currentColor;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
 #landing .a-arrow{stroke-dasharray:44;stroke-dashoffset:0;animation:vdraw 2.4s ease-in-out infinite}
 @keyframes vdraw{0%,100%{stroke-dashoffset:0;opacity:.6}50%{stroke-dashoffset:0;opacity:1}}
 #landing .a-wave,#landing .a-wave2{opacity:0;transform-origin:16px 12px}
 #landing .a-wave{animation:vwv 1.6s ease-out infinite}
 #landing .a-wave2{animation:vwv 1.6s ease-out .6s infinite}
 @keyframes vwv{0%{opacity:.95;transform:scale(.55)}100%{opacity:0;transform:scale(1.7)}}
 #landing .a-orbit{animation:vorb 2s linear infinite;transform-origin:12px 12px}
 #landing .a-spin{animation:vorb 4.5s linear infinite;transform-origin:12px 12px}
 #landing .a-pip{animation:vpip 1.9s ease-in-out infinite}
 @keyframes vpip{0%,100%{opacity:.35}50%{opacity:1}}
 @keyframes vorb{to{transform:rotate(360deg)}}
 #landing .hbar{position:absolute;right:clamp(24px,4vw,56px);bottom:92px;z-index:5;width:min(39%,460px);background:rgba(10,14,19,.64);border:1px solid rgba(255,255,255,.13);border-radius:16px;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);padding:18px 18px 20px;box-shadow:inset 0 1px 0 rgba(255,255,255,.09),0 3px 8px rgba(0,0,0,.35),0 30px 60px -30px rgba(0,0,0,.8);opacity:0;transform:translateY(20px);transition:opacity .85s cubic-bezier(.16,1,.3,1) .2s,transform .85s cubic-bezier(.16,1,.3,1) .2s}
 #landing.entered .hbar{opacity:1;transform:none}
 #landing .hcap{font-family:var(--body);font-size:12.5px;line-height:1.45;color:var(--lbody);margin-top:12px}
 :root[data-theme="light"] #landing .hbar{background:#fff;border-color:#ECE5D6;box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 3px 8px rgba(60,50,30,.08),0 30px 60px -30px rgba(60,50,30,.5)}
 :root[data-theme="light"] #landing .hbar .hlabel{color:#0A7373}
 :root[data-theme="light"] #landing .hbar .hcap{color:#5E6772}
 :root[data-theme="light"] #landing .hbar .hstats{border-top-color:#ECE5D6}
 :root[data-theme="light"] #landing .hbar .hstats .n{color:#12171D}
 :root[data-theme="light"] #landing .hbar .hstats .l{color:#8A8578}
 #landing .hlabel{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--lteal4);margin-bottom:12px;transition:color .3s ease}
 #landing .hlabel svg{width:11px;height:11px;fill:currentColor}
 #landing .vbig{position:relative;width:100%;aspect-ratio:16/9;border-radius:11px;overflow:hidden;border:1px solid rgba(255,255,255,.15);cursor:pointer;background:#0a1620}
 #landing .vbig img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
 #landing .vbig:hover img{transform:scale(1.04)}
 #landing .vbig::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 46%,rgba(6,9,13,.72))}
 #landing .vbig .vcap2{position:absolute;left:14px;bottom:12px;z-index:2;max-width:72%}
 #landing .vbig .vcap2 b{display:block;font-family:var(--disp);font-weight:700;font-size:15px;color:#F7F2E8;line-height:1.15;letter-spacing:-.01em}
 #landing .vbig .vcap2 .s1{display:block;font-family:var(--body);font-size:10.5px;color:#D7DCE2;line-height:1.3;margin-top:3px}
 #landing .vbig .vcap2 .s2{display:block;font-family:var(--mono);font-size:8.5px;letter-spacing:.08em;color:#9AA2AB;line-height:1.3;margin-top:3px}
 #landing .vbig .vplay{position:absolute;right:14px;bottom:14px;z-index:2;width:50px;height:50px;border-radius:50%;background:var(--playtint,#0FB3B3);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px -6px rgba(0,0,0,.6);transition:background .3s ease;animation:lensPlayPulse 2.2s ease-in-out infinite}
 #landing .vbig .vplay::after,#landing .vbig .vplay::before{content:"";position:absolute;inset:0;border-radius:50%;border:2px solid var(--lensring,#0FB3B3);animation:lensPlayRing 2s ease-out infinite;pointer-events:none}
 #landing .vbig .vplay::before{animation-delay:1s}
 @keyframes lensPlayPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
 @keyframes lensPlayRing{0%{transform:scale(1);opacity:.7}100%{transform:scale(2.3);opacity:0}}
 #landing .vbig .vplay svg{width:22px;height:22px;fill:#042020;margin-left:2px}
 #landing .hstats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:15px;padding-top:14px;border-top:1px solid rgba(255,255,255,.13);text-align:center}
 #landing .hstats .n{font-family:var(--disp);font-weight:800;font-size:20px;color:var(--livory);line-height:1}
 #landing .hstats .n em{color:var(--lamber);font-style:normal}
 #landing .hstats .l{font-family:var(--mono);font-size:9px;letter-spacing:.05em;text-transform:uppercase;color:var(--lfaint);margin-top:5px;line-height:1.3}
 @media(prefers-reduced-motion:reduce){#landing .vhero-vid{display:none}#landing.vhero{background:url(assets/hero/hero-poster.jpg) 64% 40%/cover}#landing .a-arrow,#landing .a-wave,#landing .a-wave2,#landing .a-orbit,#landing .a-spin,#landing .a-pip,#landing .vbig .vplay,#landing .vbig .vplay::after,#landing .vbig .vplay::before{animation:none}}
 @media(max-width:820px){
  #landing.vhero{overflow-y:auto}
  #landing .vhero-vid{position:absolute;top:0;left:0;inset:auto;width:100%;height:66vh;object-fit:cover;object-position:58% 14%;z-index:0}
  #landing .vhero-scrim{position:absolute;top:0;left:0;width:100%;height:66vh;bottom:auto;z-index:1;background:linear-gradient(0deg,var(--lpagebg) 4%,rgba(6,9,13,.86) 20%,rgba(6,9,13,.42) 40%,transparent 66%),linear-gradient(180deg,rgba(6,9,13,.45),transparent 18%)}
  #landing .bar{background:linear-gradient(180deg,rgba(6,9,13,.5),transparent)}
  #landing .book{height:34px;padding:0 14px;font-size:13px}
  #landing .wrap{position:relative;z-index:5;height:auto;display:block;max-width:none;margin:0;padding:40vh 0 0;align-items:stretch}
  #landing .panel{width:100%}
  #landing .headblock{padding:0 20px}
  #landing .eyebrow{margin-bottom:10px}
  #landing .vh1{font-size:clamp(30px,8vw,40px);margin-bottom:10px}
  #landing .lead{font-size:14.5px;max-width:none}
  #landing .cardwrap{position:relative;background:var(--lpagebg);margin-top:26px;padding:2px 20px 34px}
  #landing .cardwrap::before{content:"";position:absolute;left:0;right:0;top:-64px;height:64px;background:linear-gradient(180deg,transparent,var(--lpagebg))}
  #landing .cards{grid-template-columns:1fr;max-width:none;margin-top:6px}
  #landing .lc{-webkit-backdrop-filter:none;backdrop-filter:none}
  #landing .acts{flex-direction:column;align-items:stretch;gap:10px;margin-top:20px}
  #landing .btn2,#landing .ghost{justify-content:center;width:100%;height:50px;font-size:15px}
  #landing .scrollh{align-self:center;margin-top:4px}
  #landing .fineln{text-align:center}
  #landing .hbar{position:relative;right:auto;bottom:auto;width:auto;max-width:none;margin:26px 20px 34px;opacity:1;transform:none;background:rgba(10,14,19,.92)}
  :root[data-theme="light"] #landing .fineln{color:#8A8578}
  :root[data-theme="light"] #landing .scrollh{color:#3D4651;border-bottom-color:rgba(0,0,0,.22)}
  :root[data-theme="light"] #landing .hbar{background:#fff;border-color:#ECE5D6;box-shadow:0 16px 40px -26px rgba(60,50,30,.4)}
 }
 @media(max-width:400px){#landing .vhero-vid{height:60vh}#landing .wrap{padding-top:36vh}}
'''

NEW_MARKUP = r'''<div id="landing" class="vhero">
 <video id="vhero-vid" class="vhero-vid" muted playsinline preload="none" poster="assets/hero/hero-poster.jpg" aria-label="Md Shafaat Ali Choyon walking into frame">
 <source src="assets/hero/hero-walkin.webm" type="video/webm">
 <source src="assets/hero/hero-walkin.mp4" type="video/mp4">
 </video>
 <div class="vhero-scrim"></div>
 <div class="bar">
 <span class="brand"><img src="assets/headshot-hero.jpg" alt="Md Shafaat Ali Choyon" width="32" height="32" /><span>Md Shafaat Ali Choyon<span class="dot">.</span></span></span>
 <div class="navr">
 <button id="landing-theme" type="button" class="tgl" aria-label="Toggle light/dark"><i id="landing-icon" data-lucide="moon" style="width:18px;height:18px;"></i></button>
 <a class="book" href="https://calendly.com/shafaat-alic/30min" target="_blank" rel="noopener" data-cta>Book a call</a>
 </div>
 </div>
 <div class="wrap"><div class="panel">
 <div class="headblock">
 <div class="eyebrow rv" style="transition-delay:0s"><i></i>One career, seen four ways</div>
 <h2 class="vh1 rv" style="transition-delay:.06s">Choose the lens<br>that fits you.</h2>
 <p class="lead rv" style="transition-delay:.14s">16+ years across growth, communication, product and public health. Every lens shows the complete portfolio, framed for what matters to you.</p>
 </div>
 <div class="cardwrap">
 <div id="landing-cards" class="cards"></div>
 <div class="acts rv" style="transition-delay:.46s">
 <button id="landing-all" type="button" class="btn2">See everything, the full portfolio <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
 <button id="landing-tour" type="button" class="ghost"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg> Take the 70-second tour</button>
 <button id="landing-scroll" type="button" class="scrollh">Scroll to explore &darr;</button>
 </div>
 <div class="fineln rv" style="transition-delay:.52s">Every lens shows the complete work &middot; switch any time from the top bar.</div>
 </div>
 </div></div>
 <div class="hbar">
 <span class="hlabel"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> A 45-SECOND HELLO</span>
 <div id="introvid" role="button" tabindex="0" aria-label="Play Md Shafaat Ali Choyon intro video" class="vbig">
 <img src="https://img.youtube.com/vi/FZLnsmMEXvo/maxresdefault.jpg" onerror="this.onerror=null;this.src='https://img.youtube.com/vi/FZLnsmMEXvo/hqdefault.jpg';" alt="Md Shafaat Ali Choyon: video intro" loading="lazy">
 <div class="vcap2"><b>Md Shafaat Ali Choyon</b><span class="s1">Growth &amp; health-systems strategist &middot; 16+ years</span><span class="s2">MBA &middot; MCIM &middot; MPH &middot; CHES&reg;</span></div>
 <span class="vplay" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
 </div>
 <p class="hcap">One career, seen four ways - the short version, in my own words.</p>
 <div class="hstats">
 <div><div class="n"><em>#1</em></div><div class="l">Global launch growth</div></div>
 <div><div class="n">10M</div><div class="l">G2P beneficiaries</div></div>
 <div><div class="n">~57%</div><div class="l">B2C CAGR 2021-23</div></div>
 </div>
 </div>
 <script>
 (function(){
  var L=document.getElementById('landing'); if(!L) return;
  var v=document.getElementById('vhero-vid');
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var started=false, entered=false;
  function enter(){ if(entered) return; entered=true; L.classList.add('playing','entered'); }
  if(reduce){ enter(); }
  setTimeout(function(){ L.classList.add('playing'); }, 900);
  if(v && !reduce){
   v.addEventListener('playing', function(){ started=true; L.classList.add('playing'); }, {once:true});
   v.addEventListener('timeupdate', function(){ if(v.duration && v.currentTime>=v.duration-0.35) enter(); });
   v.addEventListener('ended', function(){ try{v.pause();}catch(e){} enter(); });
   var isMobile=matchMedia('(max-width:820px)').matches;
   if(isMobile){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){ if(e.isIntersecting){ v.preload='auto'; v.play().catch(function(){}); io.disconnect(); } });},{threshold:.25});
    io.observe(v);
   } else { v.preload='auto'; v.play().catch(function(){}); }
  }
  setTimeout(function(){ if(!started){ L.classList.add('playing'); enter(); } }, 1600);
  setTimeout(function(){ enter(); }, 7000);
  L.addEventListener('mouseover', function(e){ var c=e.target.closest?e.target.closest('.lc'):null; if(!c)return; var ac=c.getAttribute('data-accent'); if(ac){ L.style.setProperty('--playtint',ac); L.style.setProperty('--lensring',ac); } });
  L.addEventListener('mousemove', function(e){ var c=e.target.closest?e.target.closest('.lc'):null; if(!c)return; c.style.transitionDelay='0s'; var b=c.getBoundingClientRect(); var x=(e.clientX-b.left)/b.width-.5, y=(e.clientY-b.top)/b.height-.5; c.style.transform='translateY(-5px) perspective(900px) rotateY('+(x*6)+'deg) rotateX('+(-y*6)+'deg)'; });
  L.addEventListener('mouseout', function(e){ var c=e.target.closest?e.target.closest('.lc'):null; if(!c)return; if(e.relatedTarget && c.contains(e.relatedTarget))return; c.style.transform=''; L.style.removeProperty('--playtint'); L.style.removeProperty('--lensring'); });
  L.addEventListener('click', function(e){ var g=e.target.closest?e.target.closest('#landing-tour'):null; if(!g)return; e.preventDefault(); var b=document.querySelector('.st-launch'); if(b) b.click(); });
 })();
 </script>
 </div>'''

old_lensin = " .lens-card{opacity:0;animation:lensIn .45s ease forwards;}\n"
if old_lensin in s:
    s = s.replace(old_lensin, "")
else:
    print("WARN: lensIn rule not found (may already be removed)")

a = s.index('<style id="vhero-css">')
b = s.index('</style>', a)
s = s[:a] + '<style id="vhero-css">\n' + NEW_CSS.strip('\n') + '\n </style>' + s[b+len('</style>'):]

start = s.index('<div id="landing" class="vhero">')
sc = s.index('</script>', start)
divc = s.index('</div>', sc)
end = divc + len('</div>')
s = s[:start] + NEW_MARKUP + s[end:]

OLD_TPL = (
 " if(lc){ lc.innerHTML = order.map((id,i)=>{ const L=this._lenses[id]; return `\n"
 " <button type=\"button\" class=\"lens-card\" data-lens-pick=\"${id}\" style=\"--lens:${L.accent};--lensd:${L.deep||L.accent};--lenssoft:${L.soft};animation-delay:${i*70}ms;\">\n"
 " <span class=\"chip\"><i data-lucide=\"${L.icon}\" style=\"width:23px;height:23px;\"></i></span>\n"
 " <div class=\"ey\">${L.forWho||''}</div>\n"
 " <div class=\"tt\">${L.label}</div>\n"
 " <div class=\"ds\">${L.blurb}</div>\n"
 " <div class=\"enter\">Enter this lens <span aria-hidden=\"true\">-&gt;</span></div>\n"
 " </button>`; }).join(''); }"
)
NEW_TPL = (
 " if(lc){\n"
 " const _ic={growth:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline class=\"a-arrow\" points=\"3 17 9 11 13 15 21 7\"/><polyline points=\"14 7 21 7 21 14\"/></svg>',healthcomm:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 11l11-6v14L3 13z\"/><path class=\"a-wave\" d=\"M17 8c2 1.5 2 6.5 0 8\"/><path class=\"a-wave2\" d=\"M19 6c3 2.2 3 9.8 0 12\"/></svg>',healthtech:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"7\" y=\"7\" width=\"10\" height=\"10\" rx=\"1.5\"/><circle class=\"a-orbit\" cx=\"12\" cy=\"7\" r=\"1.4\" fill=\"currentColor\" stroke=\"none\"/><path class=\"a-pip\" d=\"M4 10v4M20 10v4M10 4h4M10 20h4\"/></svg>',pophealth:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><g class=\"a-spin\"><path d=\"M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18\"/></g></svg>'};\n"
 " const _plus='<svg viewBox=\"0 0 24 24\"><path d=\"M12 5v14M5 12h14\"/></svg>';\n"
 " const _arr='<svg viewBox=\"0 0 24 24\"><path d=\"M5 12h14M13 6l6 6-6 6\"/></svg>';\n"
 " lc.innerHTML = order.map((id,i)=>{ const L=this._lenses[id]; return `\n"
 " <button type=\"button\" class=\"lc lens-card rv\" data-lens-pick=\"${id}\" data-accent=\"${L.accent}\" style=\"--lens:${L.accent};--lensd:${L.deep||L.accent};--lenssoft:${L.soft};transition-delay:${(0.2+i*0.07).toFixed(2)}s\">\n"
 " <div class=\"crow\"><span class=\"chip\">${_ic[id]||''}</span><div class=\"ind\">${_plus}</div></div>\n"
 " <div class=\"ey\">${L.forWho||''}</div>\n"
 " <div class=\"tt\">${L.label}</div>\n"
 " <div class=\"ds\">${L.blurb}</div>\n"
 " <div class=\"enter\">Enter this lens ${_arr}</div>\n"
 " </button>`; }).join(''); }"
)
if OLD_TPL in s:
    s = s.replace(OLD_TPL, NEW_TPL)
else:
    print("ERROR: card template not found -- aborting")
    sys.exit(2)

OLD_BH = "root.querySelectorAll('[data-lens-pick]').forEach(el=>{ if(el._hb) return; el._hb=1; el.addEventListener('mouseenter',()=>{ el.style.transform='translateY(-3px)';"
NEW_BH = "root.querySelectorAll('[data-lens-pick]:not(.lc)').forEach(el=>{ if(el._hb) return; el._hb=1; el.addEventListener('mouseenter',()=>{ el.style.transform='translateY(-3px)';"
if OLD_BH in s:
    s = s.replace(OLD_BH, NEW_BH)
else:
    print("WARN: _bindHovers lens-pick selector not found")

if s == orig:
    print("ERROR: no changes made")
    sys.exit(3)

ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
io.open(PATH.replace("index.html","index.backup-prototypeport-"+ts+".html"),"w",encoding="utf-8").write(orig)
io.open(PATH,"w",encoding="utf-8").write(s)
print("OK wrote index.html (%d -> %d chars)" % (len(orig), len(s)))
