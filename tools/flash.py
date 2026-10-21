#!/usr/bin/env python3
"""Daily flash deals: 3 a day, R2,000 off one machine per slot, claimed on WhatsApp.
Slots (South African time): 08:00-12:00, 12:00-17:00, 17:00-22:00. 22:00-08:00 shows the next morning's deal as "starts at 08:00".
The machine for each slot is picked from the catalog by date + slot, so everyone sees the same deal and it changes on its own,
no daily work needed. Deals are for machines from R25,000 (not consumables).
- Banner at the top of the home page.
- /flash/ : a page to share on WhatsApp status, Facebook and Instagram ("today's flash deal").
Runs in rebuild.sh after subscribe.py and before meta_pixel.py."""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "public")
OFF = 2000
MIN_PRICE = 25000
MARK = "<!--ta-flash-->"

P = json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))
pool = []
for p in P:
    v = int(re.sub(r"\D", "", p.get("price") or "") or 0)
    if p.get("sid") == "supplies" or v < MIN_PRICE:
        continue
    pool.append({"k": p["k"], "n": p["name"], "m": p["model"], "p": v, "i": p["img"]})
pool.sort(key=lambda x: x["k"])
DATA = json.dumps(pool, ensure_ascii=False, separators=(",", ":"))

CSS = """<style>
.tafl{--fl1:#ff3b30;--fl2:#ff9500;max-width:1100px;margin:12px auto;padding:0 12px}
.tafl-c{display:flex;gap:12px;align-items:center;background:linear-gradient(135deg,#1a0a00,#3a1300);color:#fff;border-radius:16px;padding:12px;
  box-shadow:0 0 0 2px var(--fl2),0 6px 22px rgba(255,90,0,.25);text-decoration:none}
.tafl-i{flex:0 0 92px;height:92px;border-radius:12px;background:#fff;display:grid;place-items:center;overflow:hidden}
.tafl-i img{width:100%;height:100%;object-fit:contain}
.tafl-t{flex:1;min-width:0}
.tafl-e{display:inline-block;font:800 11px/1 system-ui,sans-serif;letter-spacing:.08em;background:var(--fl1);color:#fff;border-radius:99px;padding:5px 8px;margin-bottom:6px}
.tafl-n{font:700 15px/1.25 system-ui,sans-serif;margin:0 0 4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.tafl-p{margin:0;font:600 14px/1.3 system-ui,sans-serif}
.tafl-p s{opacity:.6;font-weight:400;margin-right:6px}
.tafl-p b{color:#ffd23f;font-size:18px}
.tafl-cd{margin:4px 0 0;font:600 12px/1.3 system-ui,sans-serif;color:#ffb27a}
.tafl-b{display:block;margin-top:8px;text-align:center;background:#25d366;color:#05301a;font:800 14px/1 system-ui,sans-serif;border-radius:10px;padding:11px 8px;text-decoration:none}
@media (prefers-reduced-motion:no-preference){.tafl-e{animation:taflp 1.4s ease-in-out infinite}}
@keyframes taflp{50%{opacity:.6}}
</style>"""

# One script drives both the banner and the /flash/ page. Times are worked out in South African time (UTC+2, no DST).
JS = """<script>(function(){
var POOL=%s,OFF=%d,WA='27644548506',S=[[8,12],[12,17],[17,22]];
function sast(){return new Date(Date.now()+2*3600e3)}
function h(s){var x=2166136261;for(var i=0;i<s.length;i++){x^=s.charCodeAt(i);x=Math.imul(x,16777619)}return x>>>0}
function slot(){var d=sast(),hr=d.getUTCHours()+d.getUTCMinutes()/60,day=new Date(Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate())),i=-1,live=true;
  for(var j=0;j<3;j++)if(hr>=S[j][0]&&hr<S[j][1])i=j;
  if(i<0){live=false;if(hr>=22)day=new Date(day.getTime()+864e5);i=0}
  var key=day.toISOString().slice(0,10)+'#'+i,end=new Date(day.getTime()+(live?S[i][1]:S[i][0])*3600e3-2*3600e3);
  return{key:key,i:i,live:live,end:end,p:POOL[h(key)%%POOL.length]}}
function R(v){return'R'+String(v).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',')}
function msg(s){return'https://wa.me/'+WA+'?text='+encodeURIComponent('Hi Trimion, I want the FLASH DEAL: '+s.p.n+' ('+s.p.m+') for '+R(s.p.p-OFF)+' ('+R(OFF)+' off). Is it still available?\\n\\nMachine: https://trimionafrica.co.za/p/m'+s.p.k)}
function two(n){return(n<10?'0':'')+n}
function render(){var s=slot();
  document.querySelectorAll('[data-tafl]').forEach(function(el){
    var q=function(n){return el.querySelector('[data-f='+n+']')};
    if(el.dataset.key!==s.key){el.dataset.key=s.key;
      q('img').src=s.p.i;q('img').alt=s.p.n;q('n').textContent=s.p.n;
      q('was').textContent=R(s.p.p);q('now').textContent=R(s.p.p-OFF);
      q('e').textContent=s.live?'⚡ FLASH DEAL '+(s.i+1)+' OF 3 TODAY':'⏰ NEXT FLASH DEAL';
      q('b').href=s.live?msg(s):'https://wa.me/'+WA+'?text='+encodeURIComponent('Hi Trimion, please remind me about the 08:00 flash deal: '+s.p.n);
      q('b').textContent=s.live?'Claim R2,000 off on WhatsApp':'Remind me on WhatsApp';
      var l=q('link');if(l)l.href='/p/m'+s.p.k}
    var t=Math.max(0,Math.floor((s.end-Date.now())/1000));
    q('cd').textContent=(s.live?'Ends in ':'Starts in ')+two(Math.floor(t/3600))+':'+two(Math.floor(t%%3600/60))+':'+two(t%%60)+(s.live?' · first 3 orders only':' (08:00)');
  });}
render();setInterval(render,1000);
})();</script>""" % (DATA, OFF)

CARD = """<div class="tafl-c" data-tafl>
  <a class="tafl-i" data-f="link" href="/"><img data-f="img" alt="" width="92" height="92"></a>
  <div class="tafl-t">
    <span class="tafl-e" data-f="e">⚡ FLASH DEAL</span>
    <p class="tafl-n" data-f="n"></p>
    <p class="tafl-p"><s data-f="was"></s><b data-f="now"></b></p>
    <p class="tafl-cd" data-f="cd"></p>
    <a class="tafl-b" data-f="b" href="https://wa.me/27644548506" target="_blank" rel="noopener">Claim R2,000 off on WhatsApp</a>
  </div>
</div>"""

BANNER = f'{MARK}{CSS}<section class="tafl" aria-label="Flash deal">{CARD}<p style="margin:6px 2px 0;font-size:12px;opacity:.75">3 new flash deals every day at 08:00, 12:00 and 17:00 · <a href="/flash/">Share this deal</a> · <a href="/subscribe/">Get deals by email</a></p></section>{JS}{MARK}'

PAGE = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Flash Deal Today</title>
<meta name="description" content="Today's Trimion Africa flash deal: R2,000 off a salon machine. 3 new deals every day at 08:00, 12:00 and 17:00.">
<meta property="og:title" content="⚡ Flash deal: R2,000 off a salon machine today">
<meta property="og:description" content="3 new deals a day at 08:00, 12:00 and 17:00. Claim on WhatsApp before the timer runs out.">
<meta property="og:image" content="https://trimionafrica.co.za/og.jpg">
<meta property="og:url" content="https://trimionafrica.co.za/flash/">
<link rel="canonical" href="https://trimionafrica.co.za/flash/">
<link rel="icon" href="/icon-192.png"><meta name="theme-color" content="#1a0a00">
<style>body{{margin:0;background:#0f0600;color:#fff;font:16px/1.5 system-ui,sans-serif}}
.w{{max-width:520px;margin:0 auto;padding:24px 4px 40px}}h1{{font-size:1.7rem;line-height:1.2;margin:0 12px 6px}}.sub{{margin:0 12px 6px;opacity:.8}}
.tafl-c{{flex-direction:column;text-align:center}}.tafl-i{{flex-basis:auto;width:100%;height:240px}}.tafl-n{{font-size:18px}}.tafl-b{{font-size:16px;padding:14px}}
.more{{display:flex;flex-direction:column;gap:10px;margin:18px 12px 0}}.more a{{display:block;text-align:center;color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:12px;padding:12px;text-decoration:none;font-weight:600}}
.fine{{margin:18px 12px 0;font-size:12px;opacity:.65}}</style>
{CSS}
</head><body><div class="w">
<h1>⚡ Today's flash deal</h1>
<p class="sub">R2,000 off one machine. New deal at 08:00, 12:00 and 17:00 every day.</p>
<section class="tafl">{CARD}</section>
<div class="more"><a href="/subscribe/">📧 Get every flash deal by email</a><a href="/offers/">🎁 See all offers</a><a href="/">Browse all 167 machines</a></div>
<p class="fine">R2,000 off the listed price of the machine shown, while the timer runs, for the first 3 orders. Works with lay-by. Cannot be combined with other codes. Trimion Africa Precision (Pty) Ltd.</p>
</div>{JS}</body></html>"""

os.makedirs(os.path.join(PUB, "flash"), exist_ok=True)
open(os.path.join(PUB, "flash", "index.html"), "w", encoding="utf-8").write(PAGE)

p = os.path.join(PUB, "index.html")
s = open(p, encoding="utf-8").read()
s = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK), "", s, flags=re.S)
anchor = '<section class="hs" aria-label="Featured">'
if anchor in s:
    s = s.replace(anchor, BANNER + anchor, 1)
    print("flash deal banner on home page;", len(pool), "machines in the rotation")
else:
    print("  ! home page anchor not found; banner not added")
open(p, "w", encoding="utf-8").write(s)
print("flash page: /flash/")
