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
open(f, 'w', encoding='utf-8').write(s)
print('shop layer applied:', len(trend), 'trending')
