"""Build Trimion catalog v16 from the v15 source.
Change the warranty wording here (one place) and re-run."""
import re, json, html, os, shutil

SRC = '/home/claude/trimion-site/tools/src'
OUT = '/home/claude/trimion-site/public'
SITE = 'https://trimionafrica.co.za'

# ---- warranty wording (edit here) ----
W_MAIN = '1-year warranty'                       # headline
W_HP = '6 months on handpieces'                   # handpieces / handles
W_FULL = '1-year warranty on the machine, ' + W_HP
HP_SECTIONS = {'ems', 'cryo', 'rf', 'hifu', 'massage', 'face'}   # machines that have handpieces
SPECIAL = {1: ('2-year warranty', '2-year warranty on the machine, 1 year on handles and power module')}

s = open(f'{SRC}/index.html', encoding='utf-8').read()
import sys as _s; _s.path.insert(0, '/home/claude/trimion-site/tools'); import apply_prices; s = apply_prices.apply(s)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:80])
    s = s.replace(old, new)

# ---------- 1. head: share preview tags ----------
rep('<meta name="description" content="Trimion Africa Shop: 162 professional salon and spa machines. R150 nationwide delivery, online training included. Order on WhatsApp 064 454 8506.">',
    '<meta name="description" content="Trimion Africa Shop: 162 professional salon and spa machines. 1-year warranty, R150 nationwide delivery, free online training and lay-by. Order on WhatsApp 064 454 8506.">')
rep('<meta property="og:type" content="website">',
    '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Trimion Africa Shop">\n<meta property="og:locale" content="en_ZA">')
rep('<meta property="og:description" content="Shop 162 salon machines online. R150 nationwide delivery, online training included. Order on WhatsApp 064 454 8506.">',
    '<meta property="og:description" content="Shop 162 salon machines online. 1-year warranty, R150 delivery anywhere in SA, free online training, lay-by over 2 or 3 months. Order on WhatsApp 064 454 8506.">')
rep('<meta property="og:image" content="https://trimionafrica.co.za/og.jpg?v=19">',
    '<meta property="og:image" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta property="og:image:secure_url" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta property="og:image:type" content="image/jpeg">\n'
    '<meta property="og:image:alt" content="Trimion Africa salon equipment: 1-year warranty, R150 delivery, order on WhatsApp 064 454 8506">')
rep('<meta name="twitter:image" content="https://trimionafrica.co.za/og.jpg?v=19">',
    '<meta name="twitter:image" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta name="twitter:title" content="Trimion Africa Shop | Salon Equipment – 162 machines">\n'
    '<meta name="twitter:description" content="1-year warranty, R150 delivery anywhere in SA, free online training. Order on WhatsApp 064 454 8506.">\n'
    '<link rel="image_src" href="https://trimionafrica.co.za/og.jpg?v=20">')

# ---------- 2. perks: warranty moves up to 2nd place ----------
rep('<div><b>Warranty</b>1 year on machines</div>', '')
rep('<div class="perks"><div><b>R150 delivery</b>Nationwide · 9–12 days</div>',
    '<div class="perks"><div><b>R150 delivery</b>Nationwide · 9–12 days</div><div class="pw"><b>🛡️ 1-year warranty</b>On the machine · handpieces 6 months</div>')


from urllib.parse import quote, unquote
def add_links(b, k):
    model = re.search(r'class="model">Model ([^<]*)<', b).group(1).strip()
    extra = f"\n\nMachine: {SITE}/p/m{k}\nBrochure (PDF): {SITE}/pdf/{quote(model)}.pdf"
    def fix(m):
        t = unquote(m.group(2))
        i = t.find('\n\nFull catalog')
        t = (t[:i] + extra + t[i:]) if i > -1 else t + extra
        return m.group(1) + quote(t, safe="-_.!~*()") + '"'
    return re.sub(r'(class="(?:btn|lb)" href="https://wa\.me/27644548506\?text=)([^"]*)"', fix, b)
# ---------- 3. cards: warranty line + static details ----------
def card_fix(m):
    sid = m.group(1)
    body = m.group(2)
    def one(c):
        k = int(c.group(1)); b = c.group(2)
        if sid == 'supplies':
            return f'<article class="card" data-k="{k}">{add_links(b, k)}</article>'
        short, full = SPECIAL.get(k, (W_MAIN, W_FULL if sid in HP_SECTIONS else '1-year warranty on the machine'))
        b = re.sub(r'(<div class="model">[^<]*</div>)', r'\1<div class="wty">✓ ' + short + '</div>', b, count=1)
        b = b.replace('<li>1-year warranty, confirmed on your invoice</li>', '<li>' + full + ', confirmed on your invoice</li>')
        b = add_links(b, k)
        return f'<article class="card" data-k="{k}">{b}</article>'
    body = re.sub(r'<article class="card" data-k="(\d+)">(.*?)</article>', one, body, flags=re.S)
    return f'<section id="{sid}">{body}</section>'
s = re.sub(r'<section id="([a-z]+)">(<h2>.*?)</section>', card_fix, s, flags=re.S)
assert s.count('<div class="wty">') == 162, s.count('<div class="wty">')
assert '1-year warranty, confirmed on your invoice</li><' not in s.replace("'<li>1-year warranty, confirmed on your invoice</li>'", '')

# ---------- 4. machine detail page ----------
rep("function sec(c){var s=c.closest('section'),h=s&&s.querySelector('h2');return h?h.firstChild.textContent.trim():''}",
    "function sec(c){var s=c.closest('section'),h=s&&s.querySelector('h2');return h?h.firstChild.textContent.trim():''}\n"
    "function W(i,c){var r=(SP[i]||[]).filter(function(x){return x[0]==='Warranty'})[0],s=(c.closest('section')||{}).id;"
    "if(r)return {h:r[1].replace(/^(\\d+) years? on the machine.*/,'$1-year warranty'),f:r[1].replace(/^(\\d+) years? on the machine/,'$1-year warranty on the machine'),s:'Machine '+r[1].replace(/^(\\d+ years?) on the machine, (\\d+ years?) on (.*)$/,'$1 · $3 $2')};"
    "var hp=" + json.dumps(sorted(HP_SECTIONS)) + ".indexOf(s)>-1;return {h:'" + W_MAIN + "',f:hp?'" + W_FULL + "':'1-year warranty on the machine',s:hp?'Machine 1 year · handpieces 6 months':'Covers the whole machine'}}")
rep("'<li>1-year warranty, confirmed on your invoice</li>'",
    "'<li>'+W(i,c).f+', confirmed on your invoice</li>'")
rep("""+e(pr?pr.textContent:'')+'</p><p class="ml">'+e(dd?dd.textContent:x.d)""",
    """+e(pr?pr.textContent:'')+'</p>'+(sec(c)==='Consumables'?'':'<div class="mwb"><i>🛡️</i><div><b>'+e(W(i,c).h)+' included</b><span>'+e(W(i,c).s)+' · '+(window.TA_PROMO?'FREE delivery this week':'R150 delivery')+' · free online training</span></div></div>')+'<p class="ml">'+e(dd?dd.textContent:x.d)""")

rep("'<p class=\"mn\">For professional salon and spa use.", "'<a class=\"mb mpdf\" href=\"/pdf/'+encodeURIComponent(m.replace('Model ','').trim())+'.pdf\" target=\"_blank\" rel=\"noopener\">📄 Download brochure (PDF)</a><p class=\"mn\">For professional salon and spa use.")
# ---------- 5. share: product share opens the share sheet ----------
rep("""if(a==='s'){var u=CAT+'#'+c.id,t=c.dataset.n+' ('+c.dataset.m+') from Trimion Africa';
  if(navigator.share)navigator.share({title:t,url:u}).catch(function(){});else window.open('https://wa.me/?text='+encodeURIComponent(t+': '+u),'_blank','noopener')}});""",
    """if(a==='s'){if(window.TA_share){window.TA_share(c);return}var u='https://trimionafrica.co.za/p/'+c.id,t=c.dataset.n+' ('+c.dataset.m+') from Trimion Africa';
  if(navigator.share)navigator.share({title:t,url:u}).catch(function(){});else window.open('https://wa.me/?text='+encodeURIComponent(t+': '+u),'_blank','noopener')}});""")
rep('https%3A%2F%2Ftrimionafrica.co.za%2F%3Fv%3D2" target="_blank" rel="noopener">Share catalog</a>',
    'https%3A%2F%2Ftrimionafrica.co.za%2F%3Fv%3D3" target="_blank" rel="noopener">Share catalog</a>')
rep("""navigator.share({title:'Trimion Africa catalog',url:"https://trimionafrica.co.za/?v=2"})""",
    """navigator.share({title:'Trimion Africa catalog',text:'Trimion Africa salon machines: 1-year warranty, R150 delivery anywhere in SA, free online training.',url:"https://trimionafrica.co.za/?v=3"})""")

# ---------- 6. cart + lay-by ----------
rep("<p>Free online training included. Delivery 9 to 12 business days.</p>",
    "<p>🛡️ 1-year warranty and free online training included. Delivery 9 to 12 business days.</p>")
rep("delivered within 9 to 12 business days, with free online training.",
    "delivered within 9 to 12 business days, with free online training and the full 1-year warranty.")

# ---------- 7. (install-app pop-up removed 16 Oct 2026: it rarely works in the Facebook/Instagram browsers most visitors use) ----------
rep("['pop','mp','acct','cmp','cart']","['pop','mp','acct','cmp','cart','shs']",1)
# ---------- 8. FAQ + legal ----------
FAQ_W = ('<details><summary>What warranty do I get?</summary><p>Every machine comes with a <b>1-year warranty on the machine itself</b> and '
         '<b>6 months on the handpieces and handles</b>, confirmed on your invoice. Some models carry longer cover, shown on that machine\'s page. '
         'If anything goes wrong, send us a WhatsApp with a short video and we help you straight away (many issues are settings). '
         'This is on top of your rights under the Consumer Protection Act.</p></details>')
rep('<details><summary>How does delivery work?</summary>', FAQ_W + '<details><summary>How does delivery work?</summary>')
rep('updated 7 October 2026', 'updated 24 October 2026 · Supplier: Trimion Africa Precision (Pty) Ltd, reg. 2026/806671/07, Durban, KwaZulu-Natal')
rep('<details><summary>Returns, refunds and warranty</summary><div class="lgb">\n',
    '<details><summary>Returns, refunds and warranty</summary><div class="lgb">\n'
    '<p>Warranty: every machine has a 1-year warranty on the machine (main unit) and 6 months on handpieces and handles, from the delivery date. '
    'Some models carry longer cover, shown on the machine page and your invoice. The warranty covers faults in materials and workmanship under normal salon use. '
    'It does not cover damage from misuse, wrong voltage, dropping, opening the machine yourself, or normal wear of consumables such as gels, membranes and cartridges.</p>\n')

# ---------- 9. share sheet (HTML + CSS + JS) ----------
SHEET = ('<div class="ih ipp" id="shs" hidden role="dialog" aria-modal="true" aria-labelledby="sht"><div>'
         '<div class="iph"><img id="shi" alt="" width="56" height="56"><div><h3 id="sht">Share this machine</h3><small id="shn"></small></div></div>'
         '<img class="shp" id="shp" alt="The picture people will see" width="1200" height="630">'
         '<p class="shh">This picture shows with your message, so friends see the machine, price and warranty straight away.</p>'
         '<button id="shf" type="button" hidden>📷 Send with the picture</button>'
         '<button id="shw" type="button">💬 Send on WhatsApp</button>'
         '<button id="shb" type="button">📄 Send PDF brochure</button>'
         '<button id="sho" type="button" class="sh2" hidden>↗ More apps</button>'
         '<div class="shr"><button id="shc" type="button" class="sh2">🔗 Copy link</button><a id="shd" class="sh2" download>⬇ Picture</a><a id="shpf" class="sh2" target="_blank" rel="noopener">⬇ PDF</a></div>'
         '<button id="shx" type="button" class="ipn">Close</button></div></div>\n')
rep('<section class="hs" aria-label="Featured">', SHEET + '<section class="hs" aria-label="Featured">')

CSS = ('.card .wty{font-size:.7rem;font-weight:700;color:#0b7a3e;margin:2px 0 1px;line-height:1.3}'
       '.perks .pw{border-color:#f8b73f;background:#fff8e8}'
       '.mwb{display:flex;gap:10px;align-items:flex-start;background:#eefaf2;border:1px solid #bfe7cd;border-radius:12px;padding:10px 12px;margin:10px 0 4px}'
       '.mwb i{font-style:normal;font-size:1.3rem;line-height:1}.mwb b{display:block;color:#0b5f31;font-size:.92rem}.mwb span{display:block;color:#3c5446;font-size:.78rem;line-height:1.45;margin-top:2px}'
       '.shp{display:block;width:100%;height:auto;aspect-ratio:1200/630;border-radius:12px;margin-top:14px;background:#0d2a5c;box-shadow:0 0 0 1px #e3e8f0}'
       '.ih p.shh{margin:8px 0 2px;font-size:.76rem}'
       '#shw{background:#1fa855}#shb{background:#0b84d8}.mpdf{background:var(--navy)!important;margin-top:4px}'
       '.ih .sh2{background:#eef3fa;color:var(--navy)}'
       '.shr{display:flex;gap:8px}.shr>*{flex:1}'
       '.shr a{margin-top:14px;display:block;text-align:center;border-radius:18px;padding:11px;font:700 .88rem system-ui,sans-serif;text-decoration:none}'
       '#shs>div{max-height:92vh;overflow:auto}')
rep('</style>', CSS + '</style>', count=s.count('</style>'))  # appended to each block is harmless but keep one:
# (keep only the first insertion)
first = s.find(CSS)
s = s[:first + len(CSS)] + s[first + len(CSS):].replace(CSS, '')

JS = open('/home/claude/trimion-site/tools/wa_clean.js', encoding='utf-8').read() + open('/home/claude/trimion-site/tools/share.js', encoding='utf-8').read()
rep('</body>', '<script>' + JS + '</script>\n</body>')

import sys; sys.path.insert(0, '/home/claude/trimion-site/tools'); import enhance; s = enhance.apply(s, OUT, rep)
def _kitcards(m):
    c = m.group(0); pm = re.search(r'class="price[^"]*">R([\d,]+)', c)
    if pm and int(pm.group(1).replace(',', '')) >= 50000:
        c = c.replace('<li>Certification available separately (R1,500)</li>', '<li>Certificate FREE with your <a href="/offers/#kit">Salon Starter Kit</a> (worth R1,500)</li>')
    return c
s = re.sub(r'<article class="card".*?</article>', _kitcards, s, flags=re.S)
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(s)

# ---------- 10. product pages /p/m{k}.html (full pages Google can read; also the share link) ----------
P = json.load(open('/home/claude/trimion-site/tools/products.json'))
DT = {x['k']: x for x in json.load(open('/home/claude/trimion-site/tools/details.json'))}
os.makedirs(f'{OUT}/p', exist_ok=True)
E = lambda t: html.escape(t, quote=True)
from urllib.parse import quote as _q
def _num(t):
    m = re.search(r'R([\d,]+)', t or ''); return int(m.group(1).replace(',', '')) if m else 0
PCSS = """*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f3f5f9;color:#14213d}
a{color:inherit}.top{background:#081a3d;color:#fff;padding:10px max(16px,env(safe-area-inset-left,0px));display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:5}
.top img{width:34px;height:34px;border-radius:50%}.top b{flex:1;letter-spacing:.12em;font-size:.95rem}.top a{text-decoration:none}
.top .wa{background:#1fa855;padding:7px 12px;border-radius:18px;font-weight:700;font-size:.85rem}
.wrap{max-width:760px;margin:0 auto;padding:12px 16px 40px}.crumb{font-size:.8rem;color:#5b6b86;margin:2px 0 10px}.crumb a{text-decoration:none}
.card{background:#fff;border-radius:14px;padding:14px;box-shadow:0 1px 3px rgba(8,26,61,.08);margin-bottom:12px}
.ph{width:100%;max-height:42vh;aspect-ratio:1/1;object-fit:contain;display:block;border-radius:10px;background:#fff}
h1{font-size:1.3rem;line-height:1.25;margin:4px 0 2px;text-wrap:balance}.mod{color:#5b6b86;font-size:.85rem}
.pr{font-size:1.8rem;font-weight:800;color:#d61f1f;margin:8px 0 0;letter-spacing:-.5px}.lb{font-size:.92rem;margin:2px 0 6px}
.chip{display:inline-block;background:#fff4f3;color:#d61f1f;border:1px solid #f6c4c0;border-radius:4px;font-size:.78rem;padding:2px 6px;margin:2px 4px 2px 0}
.chip.g{background:#ecf8f1;color:#157a3f;border-color:#bfe6cf}.chip.kit{background:#fff7d6;color:#7a5600;border-color:#f3d77a;text-decoration:none;font-weight:600}
.btns{display:grid;gap:8px;margin-top:12px}.btn{display:block;text-align:center;padding:13px;border-radius:24px;font-weight:700;text-decoration:none;border:0;font-size:1rem;cursor:pointer;width:100%;font-family:inherit}
.btn.w{background:#1fa855;color:#fff}.btn.n{background:#081a3d;color:#fff}.btn.o{background:#fff;color:#081a3d;border:1.5px solid #c9d3e6}
h2{font-size:1.02rem;margin:0 0 8px}ul{margin:0;padding-left:20px}li{margin:3px 0}p{margin:0 0 8px}
.rel{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.rel a{background:#fff;border-radius:10px;padding:8px;text-decoration:none;font-size:.82rem;line-height:1.3;min-width:0}
.rel img{width:100%;aspect-ratio:1/1;object-fit:contain;display:block}.rel b{display:block;color:#d61f1f;margin-top:3px}
@media(min-width:700px){.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.rel{grid-template-columns:repeat(4,1fr)}}
.ft{text-align:center;color:#5b6b86;font-size:.8rem;padding:20px 16px 30px}:focus-visible{outline:2px solid #1d6fe0;outline-offset:2px}"""
SECNAME = {}
for d in P: SECNAME[d['sid']] = d['sec']
smap = []
for d in P:
    k = d['k']; cid = f'm{k}'; dt = DT.get(k, {})
    cons = d['sid'] == 'supplies'
    por = 'request' in d['price'].lower()
    short = SPECIAL.get(k, (W_MAIN,))[0]
    title = f"{d['name']} – {d['price']}"
    bits = ([] if cons else [short]) + ['R150 delivery anywhere in SA'] + ([] if cons else ['free online training'])
    if d['lb']:
        bits.append(d['lb'].replace('Lay-by ', 'lay-by: '))
    desc = ', '.join(bits)
    desc = desc[0].upper() + desc[1:] + '. ' + ('Tap for a written quote on WhatsApp 064 454 8506.' if por else 'Order on WhatsApp 064 454 8506.')
    img = f'{SITE}/og/{cid}.jpg?v=3'
    url = f'{SITE}/p/{cid}'
    price = _num(d['price'])
    _ask = ('I would like information and a quote for the ' if por else 'I would like to order the ')
    wa = 'https://wa.me/27644548506?text=' + _q('Hi Trimion Africa, ' + _ask + d['name'] + ' (' + d['model'] + ').' + chr(10) + chr(10) + 'Machine: ' + url + chr(10) + 'Brochure (PDF): https://trimionafrica.co.za/pdf/' + d['model'] + '.pdf')
    paras = ''.join(f'<p>{E(t)}</p>' for t in dt.get('desc', []))
    specs = ''.join(f'<li>{E(t)}</li>' for t in dt.get('specs', []))
    kit = price >= 50000
    _g = [('Certificate included FREE with your Salon Starter Kit (worth R1,500)' if (kit and t.startswith('Certification available separately')) else t) for t in dt.get('get', [])]
    if kit: _g.append('Free Salon Starter Kit: treatment menu and price list, 10 ready-made social posts, Trimion Certified Salon feature')
    gets = ''.join(f'<li>{E(t)}</li>' for t in _g)
    rel = [x for x in P if x['sid'] == d['sid'] and x['k'] != k]
    rel = sorted(rel, key=lambda x: abs(_num(x['price']) - price))[:4]
    relh = ''.join(f'<a href="/p/m{x["k"]}"><img src="{x["img"]}" alt="" loading="lazy" width="200" height="200">{E(x["name"])}<b>{E(x["price"])}</b></a>' for x in rel)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": d['name'], "sku": d['model'], "mpn": d['model'],
          "image": [SITE + d['img'], img.split('?')[0]], "description": ' '.join(dt.get('desc', [])) or desc,
          "brand": {"@type": "Brand", "name": "Trimion Africa"}, "category": d['sec'], "url": url}
    if price:
        ld["offers"] = {"@type": "Offer", "price": str(price), "priceCurrency": "ZAR", "availability": "https://schema.org/InStock",
                        "itemCondition": "https://schema.org/NewCondition", "url": url,
                        "seller": {"@type": "Organization", "name": "Trimion Africa Precision (Pty) Ltd"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Shop", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": d['sec'], "item": SITE + "/#" + d['sid']},
        {"@type": "ListItem", "position": 3, "name": d['name'], "item": url}]}
    pricebox = (f'<div class="pr">{E(d["price"])}</div>' + (f'<div class="lb">💳 {E(d["lb"])}</div>' if d['lb'] else '')
                + '<span class="chip">10% off with code TRIMION10</span>' + ('' if cons else f'<span class="chip g">{E(short)}</span>')
                + '<span class="chip g">R150 delivery</span>' + ('<a class="chip kit" href="/offers/#kit">🎁 Free Salon Starter Kit</a>' if price >= 50000 else '')) if price else '<div class="pr" style="font-size:1.3rem">Price on request</div><p class="lb">Tap below for a written quote on WhatsApp.</p>'
    page = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)} | Trimion Africa</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Trimion Africa Shop">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:secure_url" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="420">
<meta property="og:image:alt" content="{E(d['name'])} from Trimion Africa">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#081a3d">
<link rel="icon" type="image/png" href="/img/4880f983c6.png"><link rel="manifest" href="/manifest.json">
<style>{PCSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
</head><body>
<header class="top"><a href="/"><img src="/img/4880f983c6.png" alt="Trimion Africa" width="34" height="34"></a><b><a href="/">TRIMION AFRICA</a></b><a class="wa" href="{wa}">WhatsApp</a></header>
<div class="wrap">
<nav class="crumb"><a href="/">Shop</a> › <a href="/#{d['sid']}">{E(d['sec'])}</a></nav>
<div class="grid">
<div class="card"><img class="ph" src="{d['img']}" alt="{E(d['name'])}" width="540" height="540" fetchpriority="high"></div>
<div class="card"><h1>{E(d['name'])}</h1><div class="mod">Model {E(d['model'])}</div>{pricebox}
<div class="btns"><a class="btn w" href="{wa}">{'Ask for a quote on WhatsApp' if por else 'Order on WhatsApp'}</a>
<button class="btn n" type="button" id="atc">Add to cart</button>
<a class="btn o" href="/pdf/{_q(d['model'])}.pdf">Brochure (PDF)</a></div></div>
</div>
{f'<div class="card"><h2>About this machine</h2>{paras}</div>' if paras else ''}
{f'<div class="card"><h2>Specifications</h2><ul>{specs}</ul></div>' if specs else ''}
{f'<div class="card"><h2>Included with your order</h2><ul>{gets}</ul></div>' if gets else ''}
{f'<div class="card"><h2>More {E(d["sec"].lower())}</h2><div class="rel">{relh}</div></div>' if relh else ''}
{'<div class="card"><h2>Know a salon owner?</h2><p>Refer a salon that buys a machine from R25,000 and we pay you <b>R2,000</b>. <a href="/offers/#refer">How it works</a></p></div>' if price >= 25000 else ''}
<div class="card"><h2>How to order</h2><p>Tap <b>Order on WhatsApp</b>. We confirm the price, delivery and lay-by option in writing and send your invoice. Pay in full by EFT or secure card link, or pay a deposit and the balance over 2 or 3 months.</p><p><a href="/">← Back to all machines</a></p></div>
</div>
<div class="ft">Trimion Africa Precision (Pty) Ltd · Durban, KwaZulu-Natal · WhatsApp 064 454 8506</div>
<script>(function(){{var b=document.getElementById('atc'),id='{cid}';function g(){{try{{return JSON.parse(localStorage.getItem('ta_quote')||'[]')}}catch(e){{return[]}}}}
function set(){{if(g().indexOf(id)>-1){{b.textContent='✓ In your cart – view cart';b.onclick=function(){{location.href='/#cart'}}}}}}
b.onclick=function(){{var q=g();if(q.indexOf(id)<0)q.push(id);try{{localStorage.setItem('ta_quote',JSON.stringify(q))}}catch(e){{}}set()}};set()}})();</script>
</body></html>
'''
    open(f'{OUT}/p/{cid}.html', 'w', encoding='utf-8').write(page)
    smap.append(url)
import datetime as _dt
_today = _dt.date.today().isoformat()
open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'<url><loc>{SITE}/</loc><lastmod>{_today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    f'<url><loc>{SITE}/offers/</loc><lastmod>{_today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    f'<url><loc>{SITE}/guide/</loc><lastmod>{_today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
    + ''.join(f'<url><loc>{u}</loc><lastmod>{_today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n' for u in smap) + '</urlset>\n')
open(f'{OUT}/robots.txt', 'w').write('User-agent: *\nAllow: /\nDisallow: /new/\n\nSitemap: https://trimionafrica.co.za/sitemap.xml\n')

# ---------- 11. service worker version + headers ----------
sw = open('/home/claude/trimion-site/tools/sw.js').read()
assert 'trimion-shop-v7' in sw
open(f'{OUT}/sw.js', 'w').write(sw)
open(f'{OUT}/_headers', 'w').write(open(f'{SRC}/_headers').read().rstrip('\n') + '\n'
    '/og/*\n  Cache-Control: public, max-age=86400\n  Access-Control-Allow-Origin: *\n'
    '/og.jpg\n  Cache-Control: public, max-age=86400\n'
    '/p/*\n  Cache-Control: public, max-age=3600\n'
    '/pdf/*\n  Cache-Control: public, max-age=86400\n')
print('built', len(s))
