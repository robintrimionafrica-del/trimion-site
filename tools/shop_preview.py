"""Preview of a shop-style home page (big category circles, deal tiles, 2-column product feed) at /new/.
Not linked from the live home page and marked noindex, so it can be reviewed before replacing anything.
Uses the same cart as the main site (localStorage 'ta_quote', ids 'm<k>'). Runs after build.py."""
import json, os, re, html
T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
P = json.load(open(os.path.join(T, 'products.json')))
D = {d['k']: d for d in json.load(open(os.path.join(T, 'details.json')))}
home = open(os.path.join(PUB, 'index.html'), encoding='utf-8').read()
slides = re.findall(r'class="hs-s"><img src="([^"]+)" alt="([^"]*)"', home)

def num(p):
    m = re.search(r'R([\d,]+)', p or ''); return int(m.group(1).replace(',', '')) if m else 0

SECS = [('ems', 'EMS', 'EMS & electromagnetic'), ('cryo', 'Cryo', 'Cryo contouring'), ('rf', 'RF', 'RF & cavitation'),
        ('hifu', 'HIFU', 'HIFU tightening'), ('face', 'Facial', 'Facial & skin'), ('massage', 'Massage', 'Body massage'),
        ('salon', 'Salon', 'Wellness & salon'), ('supplies', 'Supplies', 'Consumables')]
items = []
for x in P:
    d = D.get(x['k'], {}); sp = [s for s in d.get('specs', []) if ':' in s][:2]
    def kv(t):
        k, v = t.split(':', 1); k = re.sub(r'\s*\(.*?\)', '', k).strip(); v = re.sub(r'\s*\(.*?\)', '', v).strip().split(',')[0]
        return (k + ' ' + v) if len(v) < 6 else v[:30]
    short = ' · '.join(kv(t) for t in sp)
    items.append(dict(k=x['k'], s=x['sid'], n=x['name'], m=x['model'], i=x['img'], p=num(x['price']),
                      l=(re.search(r'R[\d,]+', x.get('lb') or '') or [''])[0], t=short))
# section icons: the most expensive priced machine in each section has the most recognisable photo
icon = {}
for sid, _, _ in SECS:
    c = sorted([i for i in items if i['s'] == sid], key=lambda i: -i['p'])
    icon[sid] = c[0]['i'] if c else ''
newest = sorted(items, key=lambda i: -i['k'])[:2]
under = sorted([i for i in items if 0 < i['p'] <= 25000 and i['s'] != 'supplies'], key=lambda i: -i['p'])[:2]
data = json.dumps(items, ensure_ascii=False, separators=(',', ':'))

circles = ''.join(f'<button type="button" class="cc" data-s="{sid}"><span><img src="{icon[sid]}" alt="" loading="lazy" decoding="async" width="120" height="120"></span>{html.escape(lab)}</button>' for sid, _, lab in SECS)
circles += '<a class="cc" href="/#plan"><span class="ci">💳</span>Lay-by plans</a><a class="cc" href="/promo/"><span class="ci">🎁</span>10% off code</a>'
tabs = '<button type="button" class="on" data-s="">All</button>' + ''.join(f'<button type="button" data-s="{sid}">{lab}</button>' for sid, lab, _ in SECS)
def tile(title, sub, link, two, tag):
    cells = ''.join(f'<a href="/p/m{i["k"]}.html"><img src="{i["i"]}" alt="{html.escape(i["n"])}" loading="lazy" width="200" height="200"><b>R{i["p"]:,}</b><small>{tag}</small></a>' for i in two)
    return f'<div class="tile"><a class="th" href="{link}"><span>{title}</span><i>›</i></a><p>{sub}</p><div class="tg">{cells}</div></div>'
tiles = tile('Under R25k', 'Start earning sooner', '#feed" data-f="u25', under, 'Lay-by') + tile('<em>New</em> in', 'Just added', '#feed" data-f="new', newest, 'New')
slides_html = ''.join(f'<li><img src="{s}" alt="{html.escape(a)}" width="960" height="960" {"fetchpriority=high" if n == 0 else "loading=lazy"} decoding="async"></li>' for n, (s, a) in enumerate(slides))
hints = ['EMS body sculpting', 'Cryo fat freezing', 'HIFU face lifting', 'Hydra facial machine', 'Vacuum roller', 'Lay-by under R25k']

page = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Trimion Africa Shop (preview)</title>
<link rel="icon" href="/favicon.ico"><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#ffffff"><link rel="apple-touch-icon" href="/icon-192.png">
<style>
:root{--ink:#111827;--muted:#6b7280;--line:#eceef2;--bg:#f4f5f7;--navy:#0b1f4d;--blue:#1d6fe0;--red:#e2231a;--org:#f97316;--wa:#1fa855}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.35 Roboto,-apple-system,"Segoe UI",Arial,sans-serif;padding-bottom:calc(64px + env(safe-area-inset-bottom,0px))}
a{color:inherit;text-decoration:none}button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
img{max-width:100%;display:block}
.hd{position:sticky;top:0;z-index:20;background:#fff;padding-top:env(safe-area-inset-top,0px);box-shadow:0 1px 0 var(--line)}
.hr{display:flex;align-items:center;gap:10px;padding:8px max(12px,env(safe-area-inset-right,0px)) 6px max(12px,env(safe-area-inset-left,0px))}
.ib{width:34px;height:34px;display:grid;place-items:center;flex:none;position:relative}
.ib svg{width:24px;height:24px;stroke:var(--ink);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.lg{width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#2f7fe8,#0b1f4d 70%);color:#fff;font:800 13px/34px Arial;text-align:center;flex:none;letter-spacing:-.5px}
.sb{flex:1;min-width:0;display:flex;align-items:center;border:1.5px solid var(--ink);border-radius:4px;height:38px;padding-left:10px;background:#fff}
.sb input{flex:1;min-width:0;border:0;outline:0;font:15px Roboto,Arial,sans-serif;background:none;color:var(--ink)}
.sb input::placeholder{color:#374151}
.sb .go{width:44px;height:30px;margin-right:3px;border-radius:3px;background:var(--ink);display:grid;place-items:center}
.sb .go svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:2.4}
.bd{position:absolute;top:0;right:-2px;min-width:17px;height:17px;border-radius:9px;background:var(--red);color:#fff;font:700 10px/17px Arial;text-align:center;padding:0 4px}
.bd:empty{display:none}
.tb{display:flex;gap:22px;overflow-x:auto;scrollbar-width:none;padding:2px max(14px,env(safe-area-inset-right,0px)) 0 max(14px,env(safe-area-inset-left,0px))}
.tb::-webkit-scrollbar{display:none}
.tb button{flex:none;padding:6px 0 9px;font-size:15px;color:#4b5563;border-bottom:3px solid transparent}
.tb button.on{color:var(--ink);font-weight:700;border-color:var(--ink)}
.strip{display:flex;background:#fdf6e9;font-size:12px;padding:8px max(12px,env(safe-area-inset-left,0px));gap:0}
.strip div{flex:1;display:flex;flex-direction:column;padding:0 8px;min-width:0}.strip div+div{border-left:1px solid #e9dcc2}
.strip b{font-weight:600}.strip span{color:var(--muted)}
.hero{position:relative;background:var(--navy);overflow:hidden}
.hero ul{display:flex;margin:0;padding:0;list-style:none;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.hero ul::-webkit-scrollbar{display:none}
.hero li{flex:0 0 100%;scroll-snap-align:center}.hero img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover}
.dots{position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;gap:5px}
.dots i{width:6px;height:6px;border-radius:3px;background:rgba(255,255,255,.55);transition:width .2s}.dots i.on{width:18px;background:#fff}
.ai{position:absolute;right:8px;bottom:8px;font-size:10px;color:#fff;opacity:.8}
.sec{background:#fff;margin:8px 6px 0;border-radius:6px;padding:12px 4px 6px}
.cg{display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,auto);grid-auto-columns:23%;gap:10px 2%;overflow-x:auto;scrollbar-width:none;padding:0 8px 6px}
.cg::-webkit-scrollbar{display:none}
.cc{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12px;text-align:center;line-height:1.2}
.cc span{width:100%;aspect-ratio:1/1;border-radius:50%;background:#f2f3f5;overflow:hidden;display:grid;place-items:center}
.cc img{width:86%;height:86%;object-fit:contain}.ci{font-size:30px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 6px 0}
.tile{background:#fff;border-radius:6px;padding:9px 7px 8px;min-width:0}
.th{display:flex;justify-content:space-between;align-items:center;font:italic 800 15px Arial,sans-serif;letter-spacing:-.2px}
.th em{color:var(--red);font-style:italic}.th i{font-style:normal;font-weight:400;font-size:20px;line-height:1}
.tile p{margin:1px 0 6px;font-size:11px;color:var(--muted)}
.tg{display:grid;grid-template-columns:1fr 1fr;gap:5px}.tg a{min-width:0}
.tg img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;background:#f6f7f9;border-radius:3px}
.tg b{display:block;color:var(--red);font-size:15px;margin-top:4px}.tg small{color:var(--red);font-size:11px}
.code{display:flex;align-items:center;gap:10px;margin:8px 6px 0;background:linear-gradient(90deg,#0b1f4d,#1d4fa8);color:#fff;border-radius:6px;padding:11px 12px}
.code b{font-size:15px}.code span{flex:1;font-size:12px;opacity:.9}
.code button{background:#ffd34d;color:#111;font-weight:800;border-radius:16px;padding:7px 12px;font-size:13px;letter-spacing:.5px}
.fh{display:flex;align-items:center;justify-content:space-between;margin:14px 10px 6px}
.fh h2{margin:0;font-size:17px}.fh span{color:var(--muted);font-size:12px}
.feed{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:0 6px}
@media(min-width:760px){.feed{grid-template-columns:repeat(4,1fr)}.cg{grid-auto-columns:11%}.tiles{grid-template-columns:repeat(4,1fr)}}
.pc{background:#fff;border-radius:6px;overflow:hidden;display:flex;flex-direction:column;min-width:0;position:relative}
.ph{position:relative;background:#fff}.ph img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;padding:6px}
.rb{position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;height:26px;font:800 italic 13px Arial;color:#fff;background:linear-gradient(90deg,var(--org) 0 34%,var(--red) 34%)}
.rb i{padding:0 8px;font-style:italic}.rb em{flex:1;text-align:center;font-style:normal;font-weight:700}
.nb{position:absolute;left:6px;top:6px;background:var(--ink);color:#fff;font:700 10px/1 Arial;padding:4px 6px;border-radius:2px;letter-spacing:.5px}
.pb{padding:7px 9px 9px;display:flex;flex-direction:column;gap:3px;flex:1}
.pn{font-size:13.5px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.ps{font-size:11.5px;color:#c2410c;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pm{font-size:11px;color:var(--muted)}
.pr{display:flex;align-items:flex-end;justify-content:space-between;margin-top:auto;padding-top:3px}
.pv{color:var(--red);font-weight:800;font-size:19px;letter-spacing:-.3px}.pv small{font-size:12px;margin-right:1px}
.pl{display:inline-block;font-size:10.5px;color:var(--red);border:1px solid #fbc4c0;background:#fff4f3;padding:1px 4px;border-radius:2px;margin-top:2px}
.ad{width:32px;height:32px;border-radius:50%;border:1.5px solid var(--ink);display:grid;place-items:center;flex:none}
.ad svg{width:17px;height:17px;stroke:var(--ink);fill:none;stroke-width:2}
.ad.in{background:var(--ink)}.ad.in svg{stroke:#fff}
.more{height:60px}
.wa{position:fixed;left:0;right:0;bottom:calc(56px + env(safe-area-inset-bottom,0px));background:rgba(17,24,39,.92);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:9px max(12px,env(safe-area-inset-right,0px)) 9px max(12px,env(safe-area-inset-left,0px));z-index:15;font-size:14px}
.wa a{background:#fff;color:var(--ink);padding:6px 12px;border-radius:2px;font-weight:600}
.wa button{color:#fff;opacity:.7;font-size:18px;margin-left:10px}
.bn{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);display:flex;z-index:16;padding-bottom:env(safe-area-inset-bottom,0px)}
.bn a,.bn button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:7px 0 6px;font-size:11.5px;color:#4b5563;position:relative}
.bn svg{width:23px;height:23px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.bn .on{color:var(--ink);font-weight:600}.bn .bd{right:calc(50% - 20px);top:3px}
.sh{position:fixed;inset:0;z-index:30;background:rgba(0,0,0,.45);display:none}.sh.open{display:block}
.sp{position:absolute;left:0;top:0;bottom:0;width:min(86vw,360px);background:#fff;overflow-y:auto;padding:calc(14px + env(safe-area-inset-top,0px)) 0 20px}
.sp h3{margin:0 16px 8px;font-size:17px}.sp button,.sp a{display:flex;align-items:center;gap:12px;width:100%;padding:10px 16px;font-size:15px;text-align:left}
.sp img{width:44px;height:44px;border-radius:50%;background:#f2f3f5;object-fit:contain}
.toast{position:fixed;left:50%;bottom:calc(120px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:#fff;padding:9px 16px;border-radius:20px;font-size:13px;z-index:40;display:none}
.empty{grid-column:1/-1;text-align:center;color:var(--muted);padding:30px 10px}
.ip{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.5);display:flex;align-items:flex-end;justify-content:center}
.ip[hidden]{display:none}
.ib2{width:100%;max-width:480px;background:#fff;border-radius:14px 14px 0 0;padding:18px max(18px,env(safe-area-inset-right,0px)) calc(18px + env(safe-area-inset-bottom,0px)) max(18px,env(safe-area-inset-left,0px));animation:up .25s ease-out}
@keyframes up{from{transform:translateY(100%)}to{transform:none}}
@media (prefers-reduced-motion:reduce){.ib2{animation:none}}
.it{display:flex;gap:14px;align-items:center}.it img{width:60px;height:60px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.it b{display:block;font-size:17px}.it span{color:var(--muted);font-size:13px}
.iu{margin:14px 0 6px;padding:0;list-style:none;display:grid;gap:7px;font-size:14px}
.iu li::before{content:"✓";color:var(--wa);font-weight:800;margin-right:8px}
.is{margin:8px 0 0;padding-left:20px;font-size:14px;line-height:1.5}.is[hidden]{display:none}
.ia{display:flex;gap:10px;margin-top:14px}.ia button{flex:1;height:44px;border-radius:22px;font-weight:700;font-size:15px}
.ia .y{background:var(--ink);color:#fff}.ia .n{border:1.5px solid #d1d5db}
:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
</style></head><body>
<header class="hd"><div class="hr">
<button class="ib" type="button" id="mn" aria-label="Categories"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<a class="lg" href="/" aria-label="Trimion Africa home">TA</a>
<form class="sb" id="sf" role="search"><input id="q" type="search" autocomplete="off" aria-label="Search machines" placeholder="EMS body sculpting 🔥"><button class="go" aria-label="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></button></form>
<a class="ib" href="/#cart" aria-label="Cart"><svg viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h2.6l2.4 11.2h11.3l2-8H6.3"/></svg><span class="bd" id="cn"></span></a>
</div><nav class="tb" id="tb">__TABS__</nav></header>
<div class="strip"><div><b>🚚 R150 delivery</b><span>Anywhere in South Africa</span></div><div><b>💳 Lay-by</b><span>Pay over 2 or 3 months</span></div></div>
<section class="hero" aria-label="Featured"><ul id="hs">__SLIDES__</ul><div class="dots" id="hd"></div><span class="ai">AI-generated model</span></section>
<section class="sec" aria-label="Shop by category"><div class="cg">__CIRCLES__</div></section>
<div class="tiles">__TILES__</div>
<div class="code"><b>🎁 10% OFF</b><span>Any machine, with code</span><button type="button" id="cp">TRIMION10</button></div>
<div class="fh" id="feed"><h2 id="ft">Recommended for your salon</h2><span id="fc"></span></div>
<main class="feed" id="fd"></main><div class="more" id="mo"></div>
<div class="wa" id="wa"><span>Not sure which machine? We'll help.</span><span><a href="https://wa.me/27644548506?text=Hi%20Trimion%20Africa%2C%20please%20help%20me%20choose%20a%20machine." target="_blank" rel="noopener">WhatsApp</a><button type="button" id="wx" aria-label="Hide">×</button></span></div>
<nav class="bn" aria-label="Main"><a class="on" href="#top"><svg viewBox="0 0 24 24"><path d="M4 10.5 12 4l8 6.5V20h-5v-6H9v6H4z"/></svg>Shop</a>
<button type="button" id="bc"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="6" height="6" rx="1.5"/><rect x="14" y="4" width="6" height="6" rx="1.5"/><rect x="4" y="14" width="6" height="6" rx="1.5"/><circle cx="17" cy="17" r="3"/><path d="m21 21-1.8-1.8"/></svg>Category</button>
<a href="https://wa.me/27644548506" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 1-.5 1.7c-3.5 0-7.7-4.2-7.7-7.7L10.2 7l1 2z"/></svg>WhatsApp</a>
<a href="/#cart"><svg viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h2.6l2.4 11.2h11.3l2-8H6.3"/></svg>Cart<span class="bd" id="cn2"></span></a>
<a href="/#account"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>Me</a></nav>
<div class="sh" id="sh"><div class="sp"><h3>Shop by category</h3>__SHEET__<a href="/guide/">📘 Buyer's guide</a><a href="/#faq">❓ Questions</a></div></div>
<div class="ip" id="ip" hidden role="dialog" aria-modal="true" aria-labelledby="ipt"><div class="ib2">
<div class="it"><img src="/icon-192.png" alt=""><div><b id="ipt">Get the Trimion app</b><span>Free · no Play Store · tiny download</span></div></div>
<ul class="iu"><li>Open the shop in one tap from your home screen</li><li>Your cart and lay-by saved for next time</li><li>See new machines and deals first</li></ul>
<ol class="is" id="isteps" hidden></ol>
<div class="ia"><button type="button" class="n" id="ino">Not now</button><button type="button" class="y" id="iyes">Install</button></div></div></div>
<div class="toast" id="to"></div>
<script>
var A=__DATA__,HINTS=__HINTS__;
function g(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function p(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function cart(){return g('ta_quote',[])}
function paint(){var n=cart().length;document.getElementById('cn').textContent=n||'';document.getElementById('cn2').textContent=n||''}
function toast(t){var e=document.getElementById('to');e.textContent=t;e.style.display='block';clearTimeout(toast.t);toast.t=setTimeout(function(){e.style.display='none'},1700)}
function R(n){return n.toLocaleString('en-ZA').replace(/\\s/g,',')}
var fd=document.getElementById('fd'),shown=0,list=[],PAGE=20;
var plus='<svg viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h2.6l2.4 11.2h11.3l2-8H6.3"/></svg>';
function card(x){var inC=cart().indexOf('m'+x.k)>-1,save=x.p?Math.round(x.p*.1):0;
 var rb=x.p>=40000?'<div class="rb"><i>TOP PICK</i><em>SAVE R'+R(save)+'</em></div>':(x.p&&x.l?'<div class="rb"><i>LAY-BY</i><em>'+x.l+' now</em></div>':'');
 return '<article class="pc"><a href="/p/m'+x.k+'.html"><div class="ph"><img src="'+x.i+'" alt="" loading="lazy" decoding="async" width="300" height="300">'+(x.k>=165?'<span class="nb">NEW</span>':'')+rb+'</div></a>'+
 '<div class="pb"><a class="pn" href="/p/m'+x.k+'.html">'+x.n+'</a>'+(x.t?'<div class="ps">'+x.t+'</div>':'')+'<div class="pm">Model '+x.m+' · 1-year warranty</div>'+
 '<div class="pr"><div>'+(x.p?'<div class="pv"><small>R</small>'+R(x.p)+'</div><span class="pl">-10% with TRIMION10</span>':'<div class="pv" style="font-size:15px">Price on request</div>')+'</div>'+
 '<button type="button" class="ad'+(inC?' in':'')+'" data-k="'+x.k+'" aria-label="Add to cart">'+plus+'</button></div></div></article>'}
function more(){var s=list.slice(shown,shown+PAGE);fd.insertAdjacentHTML('beforeend',s.map(card).join(''));shown+=s.length}
function show(f,title){var q=(document.getElementById('q').value||'').trim().toLowerCase();
 list=A.filter(function(x){if(f==='u25')return x.p&&x.p<=25000&&x.s!=='supplies';if(f==='new')return x.k>=160;return !f||x.s===f});
 if(q)list=list.filter(function(x){return (x.n+' '+x.m+' '+x.t+' '+x.s).toLowerCase().indexOf(q)>-1});
 if(!f&&!q)list=list.slice().sort(function(a,b){return (b.p>0)-(a.p>0)||((a.k*7919)%167)-((b.k*7919)%167)});
 fd.innerHTML='';shown=0;more();if(!list.length)fd.innerHTML='<p class="empty">No machines match that. Try "EMS", "cryo" or "facial", or WhatsApp us.</p>';
 document.getElementById('ft').textContent=title||(q?'Results for "'+q+'"':'Recommended for your salon');document.getElementById('fc').textContent=list.length+' machines'}
function tab(s,title){[].forEach.call(document.querySelectorAll('#tb button'),function(b){b.classList.toggle('on',b.dataset.s===s)});show(s,title)}
new IntersectionObserver(function(e){if(e[0].isIntersecting&&shown<list.length)more()},{rootMargin:'600px'}).observe(document.getElementById('mo'));
document.getElementById('tb').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;document.getElementById('q').value='';tab(b.dataset.s,b.dataset.s?b.textContent+' machines':'');if(b.dataset.s)document.getElementById('feed').scrollIntoView({behavior:'smooth'})});
function jump(s,t){document.getElementById('q').value='';tab(s,t);document.getElementById('sh').classList.remove('open');document.getElementById('feed').scrollIntoView({behavior:'smooth'})}
document.addEventListener('click',function(e){var c=e.target.closest('.cc[data-s],.sp [data-s]');if(c){jump(c.dataset.s,c.textContent.trim()+' machines');return}
 var t=e.target.closest('[data-f]');if(t){e.preventDefault();jump(t.dataset.f,t.dataset.f==='u25'?'Under R25,000':'New in');return}
 var a=e.target.closest('.ad');if(a){var id='m'+a.dataset.k,Q=cart(),i=Q.indexOf(id);if(i>-1){Q.splice(i,1);a.classList.remove('in');toast('Removed from cart')}else{Q.push(id);a.classList.add('in');toast('Added to cart')}p('ta_quote',Q);paint()}});
document.getElementById('sf').addEventListener('submit',function(e){e.preventDefault();document.getElementById('q').blur();tab('');document.getElementById('feed').scrollIntoView({behavior:'smooth'})});
document.getElementById('q').addEventListener('input',function(){if(!this.value)tab('')});
var hi=0;setInterval(function(){var q=document.getElementById('q');if(document.activeElement===q)return;hi=(hi+1)%HINTS.length;q.placeholder=HINTS[hi]+' 🔥'},3000);
document.getElementById('cp').addEventListener('click',function(){var t='TRIMION10';(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){toast('Code TRIMION10 copied')},function(){toast('Use code TRIMION10 on WhatsApp')})});
document.getElementById('mn').onclick=document.getElementById('bc').onclick=function(){document.getElementById('sh').classList.add('open')};
document.getElementById('sh').addEventListener('click',function(e){if(e.target===this)this.classList.remove('open')});
document.getElementById('wx').onclick=function(){document.getElementById('wa').style.display='none';document.body.style.paddingBottom=''};
var hs=document.getElementById('hs'),hd=document.getElementById('hd'),n=hs.children.length;hd.innerHTML=new Array(n+1).join('<i></i>');
function dot(){var i=Math.round(hs.scrollLeft/hs.clientWidth);[].forEach.call(hd.children,function(d,j){d.classList.toggle('on',j===i)})}
hs.addEventListener('scroll',dot,{passive:true});dot();
setInterval(function(){if(document.hidden)return;var i=Math.round(hs.scrollLeft/hs.clientWidth);hs.scrollTo({left:((i+1)%n)*hs.clientWidth,behavior:'smooth'})},4500);
window.addEventListener('storage',paint);window.addEventListener('pageshow',paint);paint();show('');

// install pop-up: once every 3 days, after a little browsing, never inside the installed app
(function(){var dp=null,ip=document.getElementById('ip'),u=navigator.userAgent,ios=/iPhone|iPad|iPod/.test(u),inapp=/FBAN|FBAV|FB_IAB|Instagram|WhatsApp|; wv\\)/.test(u);
if(window.matchMedia('(display-mode: standalone)').matches||navigator.standalone)return;
if('serviceWorker' in navigator&&location.protocol==='https:')navigator.serviceWorker.register('/sw.js').catch(function(){});
window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();dp=e});
window.addEventListener('appinstalled',function(){ip.hidden=true;toast('Installed. Find Trimion Shop on your home screen 👍')});
var last=g('ta_ipop',0);if(Date.now()-last<3*864e5)return;
var armed=false;function open(){if(armed)return;armed=true;p('ta_ipop',Date.now());ip.hidden=false;document.getElementById('iyes').focus()}
setTimeout(function(){if(scrollY>300)open();else window.addEventListener('scroll',function f(){if(scrollY>300){removeEventListener('scroll',f);open()}},{passive:true})},6000);
function close(){ip.hidden=true}
document.getElementById('ino').onclick=close;ip.addEventListener('click',function(e){if(e.target===ip)close()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
document.getElementById('iyes').onclick=function(){
 if(dp){dp.prompt();dp.userChoice.then(function(r){if(r.outcome==='accepted')close();dp=null});return}
 var st=ios?(inapp?'<li>Tap <b>⋯</b> and choose <b>Open in Safari</b>.</li><li>Tap <b>Share</b>, then <b>Add to Home Screen</b>.</li>':'<li>Tap the <b>Share</b> button at the bottom.</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>')
  :(inapp?'<li>Tap <b>⋮</b> at the top right.</li><li>Tap <b>Open in Chrome</b>, then tap Install again.</li>':'<li>Tap <b>⋮</b> (browser menu).</li><li>Tap <b>Install app</b> or <b>Add to Home screen</b>.</li>');
 var o=document.getElementById('isteps');o.innerHTML=st;o.hidden=false;this.textContent='Got it';this.onclick=close};
})();
</script></body></html>'''
sheet = ''.join(f'<button type="button" data-s="{sid}"><img src="{icon[sid]}" alt="" loading="lazy">{html.escape(lab)}</button>' for sid, _, lab in SECS)
page = (page.replace('__TABS__', tabs).replace('__SLIDES__', slides_html).replace('__CIRCLES__', circles)
        .replace('__TILES__', tiles).replace('__SHEET__', sheet).replace('__DATA__', data.replace('</', '<\\/'))
        .replace('__HINTS__', json.dumps(hints)))
os.makedirs(os.path.join(PUB, 'new'), exist_ok=True)
open(os.path.join(PUB, 'new', 'index.html'), 'w', encoding='utf-8').write(page)
print('shop preview: /new/ with', len(items), 'items')
