#!/usr/bin/env python3
"""Shop-style home page layer (runs after build.py and visual_search.py).
Keeps every feature of the main page (cart, lay-by, account, compare, search by photo, details pop-ups)
and adds: underline category tabs, big round category pictures, deal tiles, a code banner,
a 'Trending now' swipe row, badge ribbons on machine photos, red prices and a compact card."""
import json, os, re, html

T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
f = os.path.join(PUB, 'index.html'); s = open(f, encoding='utf-8').read()
assert 'id="shx-cats"' not in s, 'already applied'
P = json.load(open(os.path.join(T, 'products.json')))
E = lambda t: html.escape(t, quote=True)
def num(p):
    m = re.search(r'R([\d,]+)', p or ''); return int(m.group(1).replace(',', '')) if m else 0

SECS = [('ems', 'EMS & electromagnetic'), ('cryo', 'Cryo'), ('rf', 'RF & cavitation'), ('hifu', 'HIFU'),
        ('face', 'Facial & skin'), ('massage', 'Body massage'), ('salon', 'Wellness & salon'), ('supplies', 'Consumables')]
ICON = {'ems': 'c021091d6e', 'cryo': 'e4305724de', 'face': '8821169da8', 'hifu': '5a31655f10', 'rf': 'c6e678ad75'}
icons = {}
for sid, _ in SECS:
    c = sorted([x for x in P if x['sid'] == sid], key=lambda x: -num(x['price']))
    icons[sid] = f'/img/{ICON[sid]}.webp' if sid in ICON else (c[0]['img'] if c else '')

circ = ''.join(f'<a class="shc" href="#{sid}"><span><img src="{icons[sid]}" alt="" loading="lazy" decoding="async" width="110" height="110"></span>{E(lab)}</a>' for sid, lab in SECS)
circ += ('<a class="shc" href="/offers/"><span class="shi">🎁</span>Offers</a>'
         '<a class="shc" href="#plan"><span class="shi">💳</span>Lay-by plans</a>'
         '<a class="shc" href="#earn"><span class="shi">📈</span>Earnings calculator</a>'
         '<a class="shc" href="/guide/"><span class="shi">📘</span>Buyer\'s guide</a>')

priced = [x for x in P if num(x['price']) and x['sid'] != 'supplies']
under = sorted([x for x in priced if num(x['price']) <= 25000], key=lambda x: -num(x['price']))[:2]
newest = sorted(P, key=lambda x: -x['k'])[:2]
def tile(title, sub, link, two, tag):
    cells = ''.join(f'<a href="/p/m{x["k"]}"><img src="{x["img"]}" alt="{E(x["name"])}" loading="lazy" width="200" height="200"><b>{E(x["price"])}</b><small>{tag}</small></a>' for x in two)
    return f'<div class="sht"><a class="shth" href="{link}"><span>{title}</span><i>›</i></a><p>{sub}</p><div class="shtg">{cells}</div></div>'
tiles = tile('Under R25k', 'Start earning sooner', '#plan', under, 'Lay-by') + tile('<em>New</em> in', 'Just added', '/p/m' + str(newest[0]['k']), newest, 'New')

# trending: the best-priced pick from each section, then fill with high-value machines
seen, trend = set(), []
for sid, _ in SECS[:6]:
    c = sorted([x for x in priced if x['sid'] == sid], key=lambda x: -num(x['price']))
    if c: trend.append(c[min(1, len(c) - 1)]); seen.add(c[min(1, len(c) - 1)]['k'])
for x in sorted(priced, key=lambda x: -num(x['price'])):
    if len(trend) >= 10: break
    if x['k'] not in seen: trend.append(x); seen.add(x['k'])
trow = ''.join(f'<a class="txr" href="/p/m{x["k"]}"><span><img src="{x["img"]}" alt="" loading="lazy" decoding="async" width="200" height="200">'
               f'<em>#{i+1}</em></span><b>{E(x["name"])}</b><i>{E(x["price"])}</i></a>' for i, x in enumerate(trend))

block = f'''<div class="shx" id="shx-cats">
<section class="shs" aria-label="Shop by category"><div class="shcg">{circ}</div></section>
<div class="shts">{tiles}</div>
<a class="shcode" href="/promo/"><b>🎁 10% OFF</b><span>Any machine, with code</span><em id="shcp">TRIMION10</em></a>
<section class="shs" aria-label="Trending now"><div class="txh"><h2>🔥 Trending now</h2><a href="#ems">See all ›</a></div><div class="txrw">{trow}</div></section>
</div>
'''
# put the slider first, then the new shop blocks, then the existing intro
hs = re.search(r'<section class="hs" aria-label="Featured">.*?</section>', s, re.S); assert hs
lead = s.find('<section class="lead"'); assert lead > 0 and lead < hs.start()
hs_html = hs.group(0)
s = s[:hs.start()] + s[hs.end():]
s = s[:lead] + hs_html + '\n' + block + s[lead:]

CSS = '''<style id="shx-css">
/* shop-style layer */
:root{--shred:#e2231a;--shink:#111827}
nav:not(.bnav):not([role]){gap:22px!important;padding:2px 14px 0!important;background:#fff}
nav:not(.bnav):not([role]) a{background:none!important;border:0!important;border-radius:0!important;padding:9px 0 8px!important;font-size:.92rem!important;color:#4b5563!important;border-bottom:3px solid transparent!important}
nav:not(.bnav):not([role]) a.on,nav:not(.bnav):not([role]) a:hover{color:var(--shink)!important;font-weight:700!important;border-bottom-color:var(--shink)!important}
.shx{display:flex;flex-direction:column;gap:8px;margin:8px 0 4px}
.shs{background:#fff;border-radius:10px;padding:12px 4px 6px}
.shcg{display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,auto);grid-auto-columns:23%;gap:12px 2.5%;overflow-x:auto;scrollbar-width:none;padding:0 8px 6px}
.shcg::-webkit-scrollbar,.txrw::-webkit-scrollbar{display:none}
.shc{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:.74rem;text-align:center;line-height:1.2;color:var(--shink);text-decoration:none;font-weight:500}
.shc span{width:100%;aspect-ratio:1/1;border-radius:50%;background:#f1f3f6;overflow:hidden;display:grid;place-items:center;transition:transform .2s}
.shc:active span{transform:scale(.94)}
.shc img{width:84%;height:84%;object-fit:contain}.shi{font-size:1.9rem}
.shts{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sht{background:#fff;border-radius:10px;padding:10px 8px 9px;min-width:0}
.shth{display:flex;justify-content:space-between;align-items:center;font:italic 800 1rem/1.2 Arial,sans-serif;color:var(--shink);text-decoration:none;letter-spacing:-.2px}
.shth em{color:var(--shred)}.shth i{font-style:normal;font-weight:400;font-size:1.3rem;line-height:1}
.sht p{margin:1px 0 6px;font-size:.72rem;color:#6b7280}
.shtg{display:grid;grid-template-columns:1fr 1fr;gap:6px}.shtg a{min-width:0;text-decoration:none}
.shtg img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;background:#f6f7f9;border-radius:4px}
.shtg b{display:block;color:var(--shred);font-size:.92rem;margin-top:4px}.shtg small{color:var(--shred);font-size:.7rem}
.shcode{display:flex;align-items:center;gap:10px;background:linear-gradient(90deg,#0b1f4d,#1d4fa8);color:#fff;border-radius:10px;padding:11px 12px;text-decoration:none}
.shcode b{font-size:.98rem}.shcode span{flex:1;font-size:.78rem;opacity:.9}
.shcode em{background:#ffd34d;color:#111;font-weight:800;font-style:normal;border-radius:16px;padding:7px 12px;font-size:.82rem;letter-spacing:.5px}
.txh{display:flex;justify-content:space-between;align-items:baseline;padding:0 10px 8px}
.txh h2{margin:0;font-size:1.05rem;color:var(--shink)}.txh a{font-size:.8rem;color:#4b5563;text-decoration:none}
.txrw{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x proximity;padding:0 10px 6px}
.txr{flex:0 0 38%;scroll-snap-align:start;text-decoration:none;color:var(--shink);min-width:0}
.txr span{display:block;position:relative;background:#f6f7f9;border-radius:6px}
.txr img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;display:block}
.txr em{position:absolute;left:0;top:0;background:var(--shink);color:#fff;font:800 .72rem/1 Arial;padding:5px 7px;border-radius:6px 0 6px 0;font-style:normal}
.txr b{display:block;font-size:.76rem;font-weight:500;line-height:1.25;margin-top:5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.txr i{display:block;font-style:normal;color:var(--shred);font-weight:800;font-size:.95rem;margin-top:2px}
@media(min-width:760px){.shcg{grid-auto-columns:10%;grid-template-rows:auto}.shts{grid-template-columns:repeat(4,1fr)}.txr{flex-basis:16%}}
/* machine cards */
.card .price{color:var(--shred)!important;font-weight:800!important;font-size:1.15rem!important;letter-spacing:-.3px}
.card .model{font-size:.7rem!important}
.card h3{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card .lb{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .act{display:none!important}
.card .more{font-size:.74rem!important}
.card .btn{padding-top:8px!important;padding-bottom:8px!important}
.txrb{position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;height:24px;font:800 italic .72rem Arial,sans-serif;color:#fff;background:linear-gradient(90deg,#f97316 0 36%,var(--shred) 36%);pointer-events:none}
.txrb i{padding:0 7px;font-style:italic;white-space:nowrap}.txrb em{flex:1;text-align:center;font-style:normal;font-weight:700;white-space:nowrap;overflow:hidden}
.txrb.g{background:linear-gradient(90deg,#0f766e 0 36%,#0b1f4d 36%)}
.txnb{position:absolute;left:6px;top:6px;background:var(--shink);color:#fff;font:700 .62rem/1 Arial;padding:4px 6px;border-radius:2px;letter-spacing:.5px;pointer-events:none}
@media (prefers-reduced-motion:reduce){.shc span{transition:none}}
</style>
'''
s = s.replace('</head>', CSS + '</head>', 1)
JS = r'''<script>
(function(){
function R(n){return n.toLocaleString('en-ZA').replace(/\s/g,',')}
[].forEach.call(document.querySelectorAll('.card'),function(c){
 var ph=c.querySelector('.photo');if(!ph||ph.querySelector('.txrb'))return;
 var t=(c.querySelector('.price')||{}).textContent||'',m=t.replace(/,/g,'').match(/R(\d+)/),p=m?+m[1]:0,k=+c.dataset.k;
 var lb=(c.querySelector('.lb')||{}).textContent||'',d=lb.match(/R[\d,]+/);
 var b=document.createElement('div');
 if(p>=50000){b.className='txrb';b.innerHTML='<i>FREE KIT</i><em>+ SAVE R'+R(Math.round(p*.1))+'</em>'}
 else if(p&&d){b.className='txrb g';b.innerHTML='<i>LAY-BY</i><em>'+d[0]+' now</em>'}
 else b=null;
 if(b)ph.appendChild(b);
 if(k>=160){var n=document.createElement('span');n.className='txnb';n.textContent='NEW';ph.appendChild(n)}
});
// underline the tab of the section in view
var tabs=[].slice.call(document.querySelectorAll('nav:not(.bnav):not([role]) a[href^="#"]'));
var secs=tabs.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}).filter(Boolean);
if('IntersectionObserver' in window&&secs.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){tabs.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)});var on=tabs.filter(function(a){return a.classList.contains('on')})[0];if(on&&on.scrollIntoView)on.parentNode.scrollTo({left:on.offsetLeft-20,behavior:'smooth'})}})},{rootMargin:'-45% 0px -50% 0px'});secs.forEach(function(x){io.observe(x)})}
})();
</script>
'''
assert s.count('</body>') == 1
s = s.replace('</body>', JS + '</body>')

GIFT_CSS = """<style id="tx-gift-css">
.txtop{position:fixed;right:max(14px,env(safe-area-inset-right,0px));bottom:calc(78px + env(safe-area-inset-bottom,0px));z-index:43;width:46px;height:46px;border-radius:50%;border:0;background:#0b1f4d;color:#fff;box-shadow:0 4px 14px rgba(8,26,61,.35);display:grid;place-items:center;cursor:pointer;opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .25s,transform .25s}
.txtop.on{opacity:1;transform:none;pointer-events:auto}.txtop svg{width:22px;height:22px}
@media(min-width:900px){.txtop{bottom:calc(24px + env(safe-area-inset-bottom,0px))}}
.txg{position:fixed;inset:0;z-index:60;background:rgba(5,12,30,.62);display:flex;align-items:center;justify-content:center;padding:16px max(16px,env(safe-area-inset-right,0px)) 16px max(16px,env(safe-area-inset-left,0px))}
.txg[hidden]{display:none}
.txgc{width:100%;max-width:380px;border-radius:20px;overflow:hidden;background:radial-gradient(circle at 80% 0%,#2a5bd7 0,#0b1f4d 55%,#081536 100%);color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.45);position:relative;animation:txin .35s ease-out}
@keyframes txin{from{transform:scale(.9);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.txgc{animation:none}.txtop{transition:none}}
.txgx{position:absolute;right:10px;top:10px;width:34px;height:34px;border-radius:50%;border:0;background:rgba(255,255,255,.15);color:#fff;font-size:20px;cursor:pointer}
.txgh{padding:22px 20px 6px;text-align:center}
.txgh img{width:54px;height:54px;border-radius:50%;box-shadow:0 0 0 3px rgba(255,210,63,.6)}
.txgh small{display:block;letter-spacing:.18em;font-size:.68rem;color:#ffd23f;font-weight:800;margin-top:10px}
.txgh h3{margin:4px 0 0!important;font-size:1.45rem!important;line-height:1.15;color:#fff!important;font-weight:800!important;display:block!important;min-height:0!important;overflow:visible!important;-webkit-line-clamp:unset!important}
.txgl{list-style:none;margin:12px 14px 0;padding:0;display:grid;gap:8px}
.txgl li{display:flex;gap:12px;align-items:center;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:10px 12px}
.txgl i{font-style:normal;font-size:1.5rem;width:30px;text-align:center}
.txgl b{display:block;font-size:.95rem}.txgl span{display:block;font-size:.76rem;opacity:.8}
.txgl em{font-style:normal;color:#ffd23f;font-weight:800}
.txgb{display:grid;gap:8px;padding:14px}
.txgb a,.txgb button{display:block;text-align:center;border-radius:24px;padding:12px;font:700 .95rem system-ui,sans-serif;text-decoration:none;border:0;cursor:pointer}
.txgb .w{background:#1fa855;color:#fff}.txgb .y{background:#ffd23f;color:#2a1d00}
.txgf{text-align:center;font-size:.7rem;opacity:.65;padding:0 14px 14px}
.txgx.zap{position:absolute!important}.txtop.zap{position:fixed!important}.txgb a.zap{position:static!important}
.txgx:focus-visible,.txgb a:focus-visible,.txgb button:focus-visible,.txtop:focus-visible{outline:2px solid #ffd23f;outline-offset:2px}
</style>
"""
GIFT = """<button type="button" class="txtop" id="txtop" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<div class="txg" id="txg" hidden role="dialog" aria-modal="true" aria-labelledby="txgt"><div class="txgc">
<button type="button" class="txgx" id="txgx" aria-label="Close">×</button>
<div class="txgh"><img src="/img/4880f983c6.png" alt="" width="54" height="54"><small>TRIMION AFRICA · GIFTS FOR SALONS</small><h3 id="txgt">Your salon deals this week</h3></div>
<ul class="txgl">
<li id="txgd"><i>🪔</i><div><b>Diwali Special</b><span>FREE Starter Kit from R30,000 · until 15 Nov</span></div></li>
<li><i>🚚</i><div><b id="txgdl">R150 delivery, anywhere in SA</b><span id="txgds">Door to door, 9–12 business days</span></div></li>
<li><i>🏷️</i><div><b>10% off with <em>TRIMION10</em></b><span>On any machine, on WhatsApp</span></div></li>
<li><i>💰</i><div><b>Refer a salon, earn <em>R2,000</em></b><span>When they buy a machine from R25,000</span></div></li>
</ul>
<div class="txgb"><a class="w" id="txgs" href="#" target="_blank" rel="noopener">📲 Send to a friend on WhatsApp</a><a class="y" href="/offers/">See all offers</a></div>
<div class="txgf">Screenshot this and share it with a salon owner 📸</div>
</div></div>
"""
GIFT_JS = r"""<script>
(function(){
var t=document.getElementById('txtop');
addEventListener('scroll',function(){t.classList.toggle('on',scrollY>900)},{passive:true});
t.onclick=function(){scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})};
var g=document.getElementById('txg');
if(new Date()>=new Date('2026-11-16T00:00:00+02:00')){var d=document.getElementById('txgd');if(d)d.remove()}
if(window.TA_PROMO){document.getElementById('txgdl').textContent='FREE delivery (save R150)';document.getElementById('txgds').textContent='Flash deal · first 5 orders only'}
var msg='Hi! Have a look at Trimion Africa, salon machines with lay-by, free training and delivery anywhere in SA. Right now: '+(document.getElementById('txgd')?'Diwali Special with a FREE Starter Kit, ':'')+'10% off with code TRIMION10. https://trimionafrica.co.za/offers/';
document.getElementById('txgs').href='https://wa.me/?text='+encodeURIComponent(msg);
function close(){g.hidden=true}
document.getElementById('txgx').onclick=close;g.addEventListener('click',function(e){if(e.target===g)close()});
addEventListener('keydown',function(e){if(e.key==='Escape'&&!g.hidden)close()});
var K='ta_gift',last=0;try{last=+localStorage.getItem(K)||0}catch(e){}
if(Date.now()-last<2*864e5)return;
var shown=false;
function busy(){var w=document.getElementById('wag');if(w&&!w.hidden&&getComputedStyle(w).display!=='none'&&w.offsetParent!==null)return true;
 return [].some.call(document.querySelectorAll('[role=dialog]'),function(x){return x!==g&&!x.hidden&&getComputedStyle(x).display!=='none'&&x.offsetParent!==null})}
function open(){if(shown)return;if(busy()){setTimeout(open,4000);return}shown=true;try{localStorage.setItem(K,Date.now())}catch(e){}g.hidden=false;document.getElementById('txgx').focus()}
setTimeout(open,5000);
addEventListener('scroll',function f(){if(scrollY>document.body.scrollHeight*0.35){removeEventListener('scroll',f);open()}},{passive:true});
})();
</script>
"""

NAV_CSS = """<style id="tx-nav-css">
/* keep the bottom menu on top of My account and the cart, with a big back button above it */
@media(max-width:899px){
body.txpan .bnav{z-index:58!important}
body.txpan #acct,body.txpan #cart{padding-bottom:calc(132px + env(safe-area-inset-bottom,0px))!important}
}
#acx,#crx{width:52px!important;height:52px!important;font-size:26px!important}
.txback{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(70px + env(safe-area-inset-bottom,0px));z-index:59;display:none;align-items:center;gap:10px;background:#0b1f4d;color:#fff;border:2px solid #ffd23f;border-radius:30px;padding:12px 26px;font:800 1rem system-ui,sans-serif;box-shadow:0 8px 24px rgba(8,26,61,.4);cursor:pointer;white-space:nowrap}
.txback.zap{position:fixed!important}
body.txpan .txback{display:flex}
@media(min-width:900px){.txback{bottom:calc(24px + env(safe-area-inset-bottom,0px))}}
.txback:focus-visible{outline:3px solid #ffd23f;outline-offset:3px}
</style>
"""
NAV_HTML = '<button type="button" class="txback" id="txback">← Back to shop</button>\n'
NAV_JS = r"""<script>
(function(){
var A=document.getElementById('acct'),C=document.getElementById('cart'),b=document.getElementById('txback');
function open_(x){return x&&x.classList.contains('open')}
function sync(){var a=open_(A),c=open_(C);document.body.classList.toggle('txpan',a||c);
 var ids={bnh:!a&&!c&&!document.querySelector('.cats.open'),bna:a&&!c,bnk:c};
 if(a||c||sync.was){Object.keys(ids).forEach(function(i){var e=document.getElementById(i);if(!e)return;if(ids[i])e.setAttribute('aria-current','page');else if(i!=='bnh'||a||c)e.removeAttribute('aria-current')});var cc=document.getElementById('bnc');if(cc&&(a||c))cc.removeAttribute('aria-current')}
 sync.was=a||c}
[A,C].forEach(function(x){if(x)new MutationObserver(sync).observe(x,{attributes:true,attributeFilter:['class']})});
function back(){if(open_(C)){var c=document.getElementById('crx');if(c)c.click()}if(open_(A)){var a=document.getElementById('acx');if(a)a.click()}sync()}
b.addEventListener('click',back);
var h=document.getElementById('bnh'),g=document.getElementById('bnc'),k=document.getElementById('bnk'),m=document.getElementById('bna');
if(h)h.addEventListener('click',back,true);
if(g)g.addEventListener('click',back,true);
if(k)k.addEventListener('click',function(){if(open_(A)){var a=document.getElementById('acx');if(a)a.click()}},true);
if(m)m.addEventListener('click',function(){if(open_(C)){var c=document.getElementById('crx');if(c)c.click()}},true);
sync();
})();
</script>
"""
s = s.replace('</head>', NAV_CSS + '</head>', 1)
s = s.replace('</body>', NAV_HTML + NAV_JS + '</body>', 1)

ATC_CSS = """<style id="tx-atc-css">
/* Add to cart: bright, glowing, easy to spot */
.card .atc{background:linear-gradient(135deg,#1d6fe0,#0a4dff)!important;color:#fff!important;border:0!important;box-shadow:0 0 0 2px rgba(80,160,255,.35),0 0 14px rgba(40,130,255,.55)!important;font-weight:800!important;padding:10px 4px!important;animation:txglow 2.4s ease-in-out infinite}
.card .atc svg{stroke:#fff!important}
.card .atc[aria-pressed=true]{background:linear-gradient(135deg,#17a34a,#0f8a3c)!important;box-shadow:0 0 0 2px rgba(60,200,120,.35),0 0 12px rgba(30,180,90,.5)!important;animation:none}
@keyframes txglow{0%,100%{box-shadow:0 0 0 2px rgba(80,160,255,.35),0 0 10px rgba(40,130,255,.45)}50%{box-shadow:0 0 0 3px rgba(80,160,255,.55),0 0 22px rgba(40,130,255,.85)}}
.txpc{position:absolute;right:8px;bottom:32px;z-index:3;width:44px;height:44px;border-radius:50%;border:0;background:#0a4dff;color:#fff;display:grid;place-items:center;cursor:pointer;box-shadow:0 0 0 3px rgba(255,255,255,.95),0 0 16px rgba(10,77,255,.75);animation:txglow2 2.4s ease-in-out infinite}
.txpc.zap{position:absolute!important}
.txpc svg{width:22px;height:22px;stroke:#fff;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.txpc b{position:absolute;top:-4px;right:-4px;width:18px;height:18px;border-radius:50%;background:#ffd23f;color:#111;font:900 13px/18px Arial;text-align:center}
.txpc.in{background:#17a34a;box-shadow:0 0 0 3px #fff,0 0 12px rgba(23,163,74,.7);animation:none}
.txpc.in b{background:#fff;color:#17a34a}
@keyframes txglow2{0%,100%{box-shadow:0 0 0 3px rgba(255,255,255,.95),0 0 8px rgba(10,77,255,.5)}50%{box-shadow:0 0 0 3px rgba(255,255,255,.95),0 0 22px rgba(10,77,255,.95)}}
@media (prefers-reduced-motion:reduce){.card .atc,.txpc{animation:none}}
.txpc:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}
/* Buy now in navy so it doesn't blend with Add to cart */
.card .btn{background:#0b1f4d!important;color:#fff!important;border-color:#0b1f4d!important}
body.trayon .txtop{bottom:calc(150px + env(safe-area-inset-bottom,0px))}
/* expired flash-deal bar must stay hidden */
.promo[hidden]{display:none!important}
/* the trust chips above already say this */
@media(max-width:899px){.perks{display:none!important}}
/* chat bubble: remove the little white tail */
.wag:after{display:none!important}
/* Home tab shows the Trimion logo */
#bnh img.txlg{width:26px;height:26px;border-radius:50%;display:block;margin:0 auto;box-shadow:0 0 0 2px rgba(10,77,255,.25)}
#bnh[aria-current] img.txlg{box-shadow:0 0 0 2px #0a4dff,0 0 8px rgba(10,77,255,.6)}
</style>
"""
ATC_JS = r"""<script>
(function(){
var CART='<svg viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h2.6l2.4 11.2h11.3l2-8H6.3"/></svg>';
[].forEach.call(document.querySelectorAll('.card'),function(c){var ph=c.querySelector('.photo'),a=c.querySelector('.atc');if(!ph||!a||ph.querySelector('.txpc'))return;
 var b=document.createElement('button');b.type='button';b.className='txpc';b.setAttribute('aria-label','Add '+(c.dataset.n||'machine')+' to cart');
 function paint(){var on=a.getAttribute('aria-pressed')==='true';b.classList.toggle('in',on);b.innerHTML=CART+'<b>'+(on?'✓':'+')+'</b>';b.setAttribute('aria-pressed',on?'true':'false')}
 b.addEventListener('click',function(e){e.stopPropagation();e.preventDefault();a.click();setTimeout(paint,30)});
 new MutationObserver(paint).observe(a,{attributes:true,attributeFilter:['aria-pressed']});paint();ph.appendChild(b)});
var h=document.getElementById('bnh');if(h){var sv=h.querySelector('svg');if(sv){var im=document.createElement('img');im.src='/img/4880f983c6.png';im.alt='';im.className='txlg';im.width=26;im.height=26;sv.replaceWith(im)}}
})();
</script>
"""
s = s.replace('</head>', ATC_CSS + '</head>', 1)
s = s.replace('</body>', ATC_JS + '</body>', 1)

recs = sorted([x for x in priced if 15000 <= num(x['price']) <= 70000], key=lambda x: -num(x['price']))
seen2, rec = set(), []
for sid, _ in SECS[:6]:
    for x in recs:
        if x['sid'] == sid and x['k'] not in seen2:
            rec.append(x); seen2.add(x['k']); break
rec_html = ''.join(f'<div class="txrc"><a href="/p/m{x["k"]}"><img src="{x["img"]}" alt="" loading="lazy" width="200" height="200"></a><a class="txrn" href="/p/m{x["k"]}">{E(x["name"])}</a><div class="txrp"><b>{E(x["price"])}</b><button type="button" class="txra" data-id="m{x["k"]}" aria-label="Add {E(x["name"])} to cart">+</button></div></div>' for x in rec)
CART_CSS = """<style id="tx-cart-css">
.txcx{padding:0 12px calc(20px + env(safe-area-inset-bottom,0px));max-width:760px;margin:0 auto}
.txtr{background:#fff;border-radius:14px;padding:14px 12px;margin-top:12px;box-shadow:0 1px 3px rgba(8,26,61,.08)}
.txtr h4{margin:0 0 4px;font-size:1rem;color:#0b1f4d}.txtr p{margin:0 0 10px;font-size:.8rem;color:#5b6780}
.txtg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.txtg div{background:#f3f6fb;border-radius:10px;padding:10px 6px;text-align:center;font-size:.74rem;line-height:1.25;color:#0b1f4d;font-weight:600}
.txtg i{display:block;font-style:normal;font-size:1.35rem;margin-bottom:4px}
.txpay{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:12px;font-size:.76rem;color:#5b6780}
.txpay span{border:1px solid #d9dfeb;border-radius:6px;padding:3px 7px;font-weight:700;color:#0b1f4d;background:#fff}
.txrh{margin:18px 2px 8px;font-size:1.05rem;color:#0b1f4d}
.txrg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
@media(min-width:700px){.txrg{grid-template-columns:repeat(3,1fr)}}
.txrc{background:#fff;border-radius:12px;padding:8px;min-width:0;box-shadow:0 1px 3px rgba(8,26,61,.08)}
.txrc img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;display:block}
.txrn{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:.8rem;line-height:1.3;color:#14213d;text-decoration:none;margin-top:6px;min-height:2.6em}
.txrp{display:flex;align-items:center;justify-content:space-between;margin-top:4px}
.txrp b{color:#e2231a;font-size:1rem}
.txra{width:34px;height:34px;border-radius:50%;border:0;background:#0a4dff;color:#fff;font:800 20px/1 Arial;cursor:pointer;box-shadow:0 0 10px rgba(10,77,255,.55)}
.txra.zap{position:relative}
.txra.in{background:#17a34a;box-shadow:0 0 8px rgba(23,163,74,.5)}
.txra:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}
</style>
"""
CART_HTML = ('<div class="txcx" id="txcx"><div class="txtr"><h4>Order with confidence</h4><p>Every order is confirmed in writing on WhatsApp before you pay.</p>'
 '<div class="txtg"><div><i>🧾</i>Invoice before you pay</div><div><i>🔒</i>Secure card link or EFT</div><div><i>🚚</i>R150 delivery anywhere in SA</div>'
 '<div><i>🛡️</i>Warranty on every machine</div><div><i>🎓</i>Free online training</div><div><i>💬</i>WhatsApp support</div></div>'
 '<div class="txpay">Pay with: <span>EFT</span><span>VISA</span><span>Mastercard</span><span>Lay-by</span></div></div>'
 '<h4 class="txrh">Recommended for your salon</h4><div class="txrg">' + rec_html + '</div></div>')
CART_JS = r"""<script>
(function(){
var C=document.getElementById('cart'),X=document.getElementById('txcx');if(!C||!X)return;C.appendChild(X);
function ids(){return window.TA_CART?window.TA_CART.ids():[]}
function paint(){var a=ids();[].forEach.call(X.querySelectorAll('.txra'),function(b){var on=a.indexOf(b.dataset.id)>-1;b.classList.toggle('in',on);b.textContent=on?'✓':'+'})}
X.addEventListener('click',function(e){var b=e.target.closest('.txra');if(!b||!window.TA_CART)return;var a=ids(),i=a.indexOf(b.dataset.id);if(i>-1)a.splice(i,1);else a.push(b.dataset.id);window.TA_CART.set(a);paint()});
new MutationObserver(paint).observe(C,{attributes:true,attributeFilter:['class']});paint();
})();
</script>
"""
s = s.replace('</head>', CART_CSS + '</head>', 1)
s = s.replace('</body>', CART_HTML + CART_JS + '</body>', 1)

import re as _re2
_m = _re2.search(r'(<header class="top"><div class="bar">.*?<a class="wa" [^>]*>WhatsApp</a>)', s, _re2.S); assert _m
s = s.replace(_m.group(1), _m.group(1) + '<a class="txcall" href="tel:+27644548506" aria-label="Call Trimion Africa on 064 454 8506"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg></a>', 1)
CALL_CSS = """<style id="tx-call-css">
.txcall{flex:none;width:44px;height:44px;margin-left:8px;border-radius:50%;background:#1fa855;color:#fff;display:grid;place-items:center;box-shadow:0 0 0 3px rgba(31,168,85,.3),0 0 14px rgba(31,168,85,.6);animation:txring 2.6s ease-in-out infinite;text-decoration:none}
.txcall svg{width:21px;height:21px}
.txcall.zap{position:relative}
@keyframes txring{0%,82%,100%{transform:none}86%{transform:rotate(-14deg)}90%{transform:rotate(12deg)}94%{transform:rotate(-8deg)}}
@media (prefers-reduced-motion:reduce){.txcall{animation:none}}
.txcall:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}
header.top .bar .wa{display:none!important}
header.top .bar .bt{min-width:0;flex:1}
.txcall{margin-left:auto}

</style>
"""
s = s.replace('</head>', CALL_CSS + '</head>', 1)

TILES = json.load(open(os.path.join(T, 'treatment_tiles.json')))
TR = [
 ('ems', 'Body toning', 'Relaxing body sessions', 'Electromagnetic stimulation sessions for the abs, buttocks, arms and thighs while the client lies back.',
  ['Abs and core', 'Glutes', 'Arms and thighs'], '30 min', '4–6 sessions'),
 ('cryo', 'Cryo body care', 'Cooling treatments', 'Controlled cooling cups for body care sessions on the tummy, sides, thighs and chin area.',
  ['Tummy and sides', 'Thighs', 'Chin area'], '40–60 min per area', '1–3 sessions'),
 ('hifu', 'HIFU skin care', 'Refreshed-looking skin', 'Focused ultrasound sessions for the face, jawline, neck and body, with no downtime.',
  ['Face and jawline', 'Neck', 'Body'], '30–60 min', '1 session, top-up yearly'),
 ('rf', 'Body smoothing', 'Smooth & relax', 'Radio-frequency warmth, cavitation and vacuum for smooth-looking skin on the body and a refreshed face.',
  ['Smooth-looking skin', 'Body RF', 'Face and eye RF'], '30–45 min', '6–10 sessions'),
 ('face', 'Facials', 'Glow treatments', 'Water dermabrasion, oxygen and bubble facials for deep-cleansed, hydrated, glowing skin.',
  ['Deep cleansing', 'Hydration and glow', 'Pore refining'], '45–60 min', 'Monthly'),
 ('massage', 'Massage & relax', 'Relax & unwind', 'Vacuum roller, 360° roller and pressotherapy for relaxing body massage.',
  ['Pressotherapy massage', 'Roller massage', 'Leg and body relaxation'], '30–45 min', 'Weekly'),
]
cnt = {sid: sum(1 for x in P if x['sid'] == sid) for sid, *_ in TR}
trm = {}
for sid, *_ in TR:
    c = sorted([x for x in P if x['sid'] == sid and num(x['price'])], key=lambda x: -num(x['price']))
    pick = c[::max(1, len(c)//6)][:6] if c else []
    trm[sid] = [dict(k=x['k'], n=x['name'], p=x['price'], i=x['img']) for x in pick]
lo = {sid: min([num(x['price']) for x in P if x['sid'] == sid and num(x['price'])] or [0]) for sid, *_ in TR}
fr = lambda v: ('From R' + f'{int(v):,}') if v else ''
tiles_html = ''.join(f'<button type="button" class="trt" data-t="{i}"><img src="{TILES[sid]}" alt="" loading="lazy" decoding="async" width="600" height="750"><span class="trg"></span>' + (f'<span class="trp0">{fr(lo[sid])}</span>' if lo[sid] else '') + f'<span class="trl"><small>{E(sub)}</small><b>{E(name)}</b><i>{cnt[sid]} machines</i></span><span class="trgo" aria-hidden="true">›</span></button>' for i, (sid, name, sub, *_ ) in enumerate(TR))
TRDATA = json.dumps([dict(sid=sid, name=name, sub=sub, d=d, b=b, t=t, n=n, img=TILES[sid], c=cnt[sid], m=trm[sid]) for sid, name, sub, d, b, t, n in TR], ensure_ascii=False).replace('</', '<\\/')
TR_BLOCK = f'<section class="shs trs" aria-label="Shop by treatment"><div class="txh"><h2>✨ Shop by treatment</h2><span class="trhint">Tap to explore</span></div><div class="trgrid">{tiles_html}</div></section>'
block_tr = TR_BLOCK
assert '<section class="shs" aria-label="Trending now">' in s
s = s.replace('<section class="shs" aria-label="Trending now">', block_tr + '\n<section class="shs" aria-label="Trending now">', 1)
TR_CSS = """<style id="tx-tr-css">
.trs{padding-bottom:10px}.trhint{font-size:.78rem;color:#6b7280}
.trgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 8px}
@media(min-width:760px){.trgrid{grid-template-columns:repeat(3,1fr)}}
.trt{position:relative;display:block;border:0;padding:0;border-radius:14px;overflow:hidden;cursor:pointer;aspect-ratio:4/5;background:#0b1f4d;text-align:left;box-shadow:0 2px 8px rgba(8,26,61,.18);transition:transform .25s}
.trt.zap{position:relative!important}
.trt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.trt:active img,.trt:hover img{transform:scale(1.06)}
.trg{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,12,30,.25) 0%,rgba(5,12,30,0) 22%,rgba(5,12,30,0) 42%,rgba(5,12,30,.92) 100%)}
.trt::after{content:"";position:absolute;inset:0;border-radius:14px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.14);pointer-events:none}
.trp0{position:absolute;top:10px;left:10px;background:#ffd23f;color:#1a1300;font:800 .7rem/1 system-ui,sans-serif;padding:6px 9px;border-radius:99px;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.trgo{position:absolute;right:10px;top:8px;width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);color:#fff;display:flex;align-items:center;justify-content:center;font:700 1.2rem/1 system-ui,sans-serif;backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);transition:transform .25s,background .25s}
.trt:hover .trgo,.trt:active .trgo{background:#ffd23f;color:#0b1f4d;transform:translateX(2px)}
.trt:active{transform:scale(.98)}
.trl{position:absolute;left:12px;right:12px;bottom:11px;color:#fff;display:flex;flex-direction:column;gap:1px}
.trl small{font-size:.64rem;letter-spacing:.1em;text-transform:uppercase;color:#ffd23f;font-weight:800}
.trl b{font-size:1.12rem;line-height:1.15;font-weight:800}
.trl i{font-style:normal;font-size:.74rem;opacity:.85;margin-top:2px}
.trp{position:fixed;inset:0;z-index:61;background:rgba(5,12,30,.6);display:flex;align-items:flex-end;justify-content:center}
.trp[hidden]{display:none}
.trc{width:100%;max-width:560px;max-height:92vh;overflow-y:auto;background:#f4f6fa;border-radius:20px 20px 0 0;animation:trup .3s ease-out;padding-bottom:env(safe-area-inset-bottom,0px)}
@keyframes trup{from{transform:translateY(100%)}to{transform:none}}
@media (prefers-reduced-motion:reduce){.trc{animation:none}.trt img{transition:none}}
.trhero{position:relative;height:230px;overflow:hidden}
.trhero img{width:100%;height:100%;object-fit:cover}
.trhero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,12,30,.1),rgba(5,12,30,.85))}
.trht{position:absolute;left:16px;right:60px;bottom:14px;color:#fff;z-index:1}
.trht small{color:#ffd23f;font-weight:800;letter-spacing:.12em;font-size:.7rem;text-transform:uppercase}
.trht h3{margin:2px 0 0!important;font-size:1.6rem!important;line-height:1.1;color:#fff!important;display:block!important;min-height:0!important;overflow:visible!important;-webkit-line-clamp:unset!important;font-weight:800!important}
.trx{position:absolute;top:12px;right:12px;z-index:2;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.9);color:#0b1f4d;font-size:22px;cursor:pointer}
.trx.zap{position:absolute!important}
.trtabs{display:flex;gap:6px;padding:12px 14px 0;overflow-x:auto;scrollbar-width:none}
.trtabs button{flex:none;border:1px solid #d9dfeb;background:#fff;color:#0b1f4d;border-radius:18px;padding:7px 13px;font:700 .8rem system-ui,sans-serif;cursor:pointer}
.trtabs button[aria-selected=true]{background:#0b1f4d;color:#fff;border-color:#0b1f4d}
.trb{padding:12px 14px 16px;display:grid;grid-template-columns:minmax(0,1fr);gap:12px}.trb>*{min-width:0}.trc{overflow-x:hidden}.trtabs{max-width:100%}
.trbox{background:#fff;border-radius:14px;padding:14px;box-shadow:0 1px 3px rgba(8,26,61,.08)}
.trbox p{margin:0;color:#334155;line-height:1.5}
.trbl{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.trbl li{background:#eef4ff;color:#0b1f4d;border-radius:16px;padding:5px 11px;font-size:.8rem;font-weight:700}
.trst{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.trst div{background:#fff;border-radius:12px;padding:10px 12px;box-shadow:0 1px 3px rgba(8,26,61,.08)}
.trst small{display:block;font-size:.68rem;color:#6b7280;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.trst b{color:#0b1f4d;font-size:.95rem}
.trmh{display:flex;justify-content:space-between;align-items:baseline}.trmh h4{margin:0;font-size:1rem;color:#0b1f4d}.trmh a{font-size:.8rem;color:#1d6fe0;font-weight:700;text-decoration:none}
.trm{display:flex;gap:8px;overflow-x:auto;padding:8px 0 4px;scroll-snap-type:x proximity}
.trmi{flex:0 0 44%;scroll-snap-align:start;background:#fff;border-radius:12px;padding:8px;box-shadow:0 1px 3px rgba(8,26,61,.08);position:relative;min-width:0}
.trmi a{text-decoration:none;color:#14213d}
.trmi img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;display:block}
.trmi span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:.76rem;line-height:1.3;margin-top:4px;min-height:2.6em}
.trmi b{display:block;color:#e2231a;font-size:.95rem;margin-top:2px}
.trmi button{position:absolute;right:8px;top:8px;width:34px;height:34px;border-radius:50%;border:0;background:#0a4dff;color:#fff;font:800 20px/1 Arial;cursor:pointer;box-shadow:0 0 10px rgba(10,77,255,.55)}
.trmi button.zap{position:absolute!important}
.trmi button.in{background:#17a34a}
.trcta{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.trcta a{display:block;text-align:center;border-radius:24px;padding:12px;font:800 .9rem system-ui,sans-serif;text-decoration:none}
.trcta .w{background:#1fa855;color:#fff}.trcta .s{background:#0b1f4d;color:#fff}
.trt:focus-visible,.trx:focus-visible,.trtabs button:focus-visible,.trmi button:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}
</style>
"""
TR_HTML = '<div class="trp" id="trp" hidden role="dialog" aria-modal="true" aria-labelledby="trh"><div class="trc" id="trc"></div></div>\n'
TR_JS = r"""<script>
(function(){
var D=__TRDATA__,P=document.getElementById('trp'),C=document.getElementById('trc'),cur=0;
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function ids(){return window.TA_CART?window.TA_CART.ids():[]}
function wa(t){return 'https://wa.me/27644548506?text='+encodeURIComponent('Hi Trimion Africa, I want to offer '+t.name.toLowerCase()+' in my salon. Which machine do you recommend?\n\nhttps://trimionafrica.co.za/#'+t.sid)}
function draw(i){cur=i;var t=D[i],inC=ids();
 C.innerHTML='<div class="trhero"><img src="'+t.img+'" alt=""><button type="button" class="trx" id="trx" aria-label="Close">×</button><div class="trht"><small>'+esc(t.sub)+'</small><h3 id="trh">'+esc(t.name)+'</h3></div></div>'+
 '<div class="trtabs" role="tablist">'+D.map(function(x,j){return '<button type="button" role="tab" data-j="'+j+'" aria-selected="'+(j===i)+'">'+esc(x.name)+'</button>'}).join('')+'</div>'+
 '<div class="trb"><div class="trbox"><p>'+esc(t.d)+'</p><ul class="trbl">'+t.b.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul></div>'+
 '<div class="trst"><div><small>Session</small><b>'+esc(t.t)+'</b></div><div><small>Course</small><b>'+esc(t.n)+'</b></div></div>'+
 '<div class="trbox"><div class="trmh"><h4>Machines for '+esc(t.name.toLowerCase())+'</h4><a href="#'+t.sid+'" data-go="'+t.sid+'">All '+t.c+' ›</a></div><div class="trm">'+
 t.m.map(function(m){var on=inC.indexOf('m'+m.k)>-1;return '<div class="trmi"><a href="/p/m'+m.k+'"><img src="'+m.i+'" alt="" loading="lazy" width="200" height="200"><span>'+esc(m.n)+'</span><b>'+esc(m.p)+'</b></a><button type="button" data-id="m'+m.k+'" class="'+(on?'in':'')+'" aria-label="Add '+esc(m.n)+' to cart">'+(on?'✓':'+')+'</button></div>'}).join('')+
 '</div></div><div class="trcta"><a class="w" href="'+wa(t)+'" target="_blank" rel="noopener">Ask which one</a><a class="s" href="#earn" data-go="earn">Earnings calculator</a></div></div>';
 var tb=C.querySelector('[aria-selected=true]');if(tb&&tb.scrollIntoView)tb.parentNode.scrollLeft=tb.offsetLeft-20;C.scrollTop=0}
function open(i){draw(i);P.hidden=false;document.body.style.overflow='hidden';var x=document.getElementById('trx');if(x)x.focus()}
function close(){P.hidden=true;document.body.style.overflow=''}
document.addEventListener('click',function(e){var t=e.target.closest('.trt');if(t){open(+t.dataset.t);return}
 if(!P.contains(e.target))return;
 if(e.target===P||e.target.closest('#trx')){close();return}
 var tab=e.target.closest('[data-j]');if(tab){draw(+tab.dataset.j);return}
 var a=e.target.closest('.trmi button');if(a&&window.TA_CART){var L=ids(),k=L.indexOf(a.dataset.id);if(k>-1)L.splice(k,1);else L.push(a.dataset.id);window.TA_CART.set(L);var on=k<0;a.classList.toggle('in',on);a.textContent=on?'✓':'+';return}
 var g=e.target.closest('[data-go]');if(g){e.preventDefault();close();var el=document.getElementById(g.dataset.go);if(el)el.scrollIntoView({behavior:'smooth'})}});
addEventListener('keydown',function(e){if(e.key==='Escape'&&!P.hidden)close()});
var sx=0;C.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
C.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>70&&!e.target.closest('.trm,.trtabs'))draw((cur+(dx<0?1:D.length-1))%D.length)},{passive:true});
})();
</script>
""".replace('__TRDATA__', TRDATA)
s = s.replace('</head>', TR_CSS + '</head>', 1)
s = s.replace('</body>', TR_HTML + TR_JS + '</body>', 1)
s = s.replace('</head>', GIFT_CSS + '</head>', 1)
s = s.replace('</body>', GIFT + GIFT_JS + '</body>', 1)

TINT_CSS = """<style id="tx-tint-css">
/* Colour behind every machine photo. multiply makes the photo's white
   background take this colour everywhere, including the gaps between
   handles and cables, so no white boxes or white pockets show. */
:root{--phbg:#eaf0fb}
.card .photo,.shc>span,.sht,.txr>span,.txrc>a:first-child,.trmi{background:var(--phbg)!important;isolation:isolate}
.card .photo img,.shc img,.shtg img,.txr img,.txrc img,.trmi img{mix-blend-mode:multiply;background:transparent!important}
.shtg b,.shtg small{mix-blend-mode:normal}
.txrc>a:first-child{display:block;border-radius:10px;overflow:hidden}
</style>
"""
s = s.replace('</head>', TINT_CSS + '</head>', 1)

open(f, 'w', encoding='utf-8').write(s)
print('shop layer applied:', len(trend), 'trending')
