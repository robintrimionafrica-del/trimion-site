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

SECS = [('ems', 'EMS & electromagnetic'), ('cryo', 'Cryo contouring'), ('rf', 'RF & cavitation'), ('hifu', 'HIFU tightening'),
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
setTimeout(open,14000);
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
s = s.replace('</head>', GIFT_CSS + '</head>', 1)
s = s.replace('</body>', GIFT + GIFT_JS + '</body>', 1)

open(f, 'w', encoding='utf-8').write(s)
print('shop layer applied:', len(trend), 'trending')
