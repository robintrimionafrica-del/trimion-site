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
rep('<meta name="description" content="Trimion Africa Shop: 159 professional salon and spa machines. R150 nationwide delivery, online training included. Order on WhatsApp 061 118 5978.">',
    '<meta name="description" content="Trimion Africa Shop: 159 professional salon and spa machines. 1-year warranty, R150 nationwide delivery, free online training and lay-by. Order on WhatsApp 061 118 5978.">')
rep('<meta property="og:type" content="website">',
    '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Trimion Africa Shop">\n<meta property="og:locale" content="en_ZA">')
rep('<meta property="og:description" content="Shop 159 salon machines online. R150 nationwide delivery, online training included. Order on WhatsApp 061 118 5978.">',
    '<meta property="og:description" content="Shop 159 salon machines online. 1-year warranty, R150 delivery anywhere in SA, free online training, lay-by over 2 or 3 months. Order on WhatsApp 061 118 5978.">')
rep('<meta property="og:image" content="https://trimionafrica.co.za/og.jpg?v=19">',
    '<meta property="og:image" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta property="og:image:secure_url" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta property="og:image:type" content="image/jpeg">\n'
    '<meta property="og:image:alt" content="Trimion Africa salon equipment: 1-year warranty, R150 delivery, order on WhatsApp 061 118 5978">')
rep('<meta name="twitter:image" content="https://trimionafrica.co.za/og.jpg?v=19">',
    '<meta name="twitter:image" content="https://trimionafrica.co.za/og.jpg?v=20">\n'
    '<meta name="twitter:title" content="Trimion Africa Shop | Salon Equipment – 159 machines">\n'
    '<meta name="twitter:description" content="1-year warranty, R150 delivery anywhere in SA, free online training. Order on WhatsApp 061 118 5978.">\n'
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
    return re.sub(r'(class="(?:btn|lb)" href="https://wa\.me/27611185978\?text=)([^"]*)"', fix, b)
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
assert s.count('<div class="wty">') == 159, s.count('<div class="wty">')
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
rep('updated 7 October 2026', 'updated 14 October 2026')
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
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(s)

# ---------- 10. product share pages /p/m{k}.html ----------
P = json.load(open('/home/claude/trimion-site/tools/products.json'))
os.makedirs(f'{OUT}/p', exist_ok=True)
E = lambda t: html.escape(t, quote=True)
for d in P:
    k = d['k']; cid = f'm{k}'
    cons = d['sid'] == 'supplies'
    por = 'request' in d['price'].lower()
    short = SPECIAL.get(k, (W_MAIN,))[0]
    title = f"{d['name']} – {d['price']}"
    bits = ([] if cons else [short]) + ['R150 delivery anywhere in SA'] + ([] if cons else ['free online training'])
    if d['lb']:
        bits.append(d['lb'].replace('Lay-by ', 'lay-by: '))
    desc = ', '.join(bits)
    desc = desc[0].upper() + desc[1:] + '. ' + ('Tap for a written quote on WhatsApp 061 118 5978.' if por else 'Order on WhatsApp 061 118 5978.')
    img = f'{SITE}/og/{cid}.jpg?v=3'
    page = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | Trimion Africa</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Trimion Africa Shop">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}/p/{cid}">
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
<link rel="icon" type="image/png" href="/img/4880f983c6.png">
<script>location.replace('/'+location.search+'#{cid}')</script>
<style>body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#081a3d;color:#fff;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}}main{{max-width:420px;text-align:center}}img{{width:100%;border-radius:14px}}a{{display:block;margin-top:12px;padding:12px;border-radius:22px;background:#1fa855;color:#fff;font-weight:700;text-decoration:none}}a.s{{background:#0b84d8}}</style>
</head><body><main>
<img src="/og/{cid}.jpg?v=3" alt="{E(d['name'])}" width="1200" height="630">
<h1 style="font-size:1.2rem">{E(d['name'])}</h1><p>{E(d['price'])}</p>
<a class="s" href="/#{cid}">View this machine</a>
<a class="s" href="/pdf/{quote(d['model'])}.pdf">Brochure (PDF)</a>
<a href="https://wa.me/27611185978?text={E(__import__('urllib.parse').parse.quote('Hi Trimion Africa, I am interested in the ' + d['name'] + ' (' + d['model'] + ').' + chr(10) + chr(10) + SITE + '/p/' + cid))}">Ask on WhatsApp</a>
</main></body></html>
'''
    open(f'{OUT}/p/{cid}.html', 'w', encoding='utf-8').write(page)

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
