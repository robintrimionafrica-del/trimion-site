# Builds the classifieds listing pack at /gumtree: every machine as a ready-to-post ad (photo, title,
# model, price, plain-text description) for Gumtree, Facebook Marketplace, Junkmail, Bob Shop and groups.
# Batches of 10, copy buttons, a "Posted" tick per ad (kept in the phone's browser), real photo files
# (600x600 JPG from /fb/) so they can be saved with one tap and uploaded anywhere.
import html, json, os, re
T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
N = '064 454 8506'
P = json.load(open(f'{T}/products.json'))
D = {d['model']: d for d in json.load(open(f'{T}/details.json'))}
CAT = {'ems': 'EMS & electromagnetic', 'cryo': 'Cryo', 'rf': 'RF & cavitation', 'hifu': 'HIFU', 'face': 'Facial',
       'massage': 'Body massage', 'salon': 'Salon & wellness', 'supplies': 'Consumables'}
E = html.escape


def title(p):
    t = f"{p['name']} ({p['model']})"
    return t if len(t) <= 100 else p['name'][:100]


def desc(p):
    d = D.get(p['model'], {}); cons = p['sid'] == 'supplies'
    specs = d.get('specs', [])
    warr = next((s.split(':', 1)[1].strip() for s in specs if s.lower().startswith('warranty')), '1 year')
    feats = [s for s in specs if not s.lower().startswith(('warranty', 'packaging'))][:6]
    out = [f"{p['name']} – Model {p['model']}", '', ' '.join(d.get('desc', [])[:2]).strip()]
    if feats: out += ['', 'Key features:'] + [f'• {s[:1].upper()}{s[1:]}' for s in feats]
    out += ['', f"Price: {p['price']}"]
    if not cons and p.get('lb'): out.append(p['lb'])
    out += ['', '✔ Brand new, straight from the factory']
    if not cons: out += [f'✔ Warranty: {warr}', '✔ Free online training on how to use it']
    out += ['✔ R150 delivery anywhere in South Africa', '✔ 10% off with code TRIMION10', '',
            'Trimion Africa, Durban', f'WhatsApp {N}', f"Photos, brochure and full specs: trimionafrica.co.za/p/m{p['k']}"]
    return '\n'.join(x for x in out if x is not None).replace('\n\n\n', '\n\n')


items = []
for p in P:
    items.append(dict(n=len(items) + 1, model=p['model'], title=title(p), price=p['price'],
                      num=re.sub(r'\D', '', p['price']), cat=CAT.get(p['sid'], ''), lb=p.get('lb', '') if p['sid'] != 'supplies' else '',
                      img=f"/fb/{p['model']}.jpg", desc=desc(p)))
TOTAL = len(items)


def card(it):
    k = f"g{it['n']}"
    lb = f'<p class="lb">{E(it["lb"])}</p>' if it['lb'] else ''
    return f'''<article class="post" id="{k}" data-key="{k}">
<a class="ph" href="{it['img']}" download="{it['model']}.jpg" aria-label="Save photo of {E(it['title'])}"><img src="{it['img']}" alt="{E(it['title'])}" width="600" height="600" loading="lazy" decoding="async"><span class="num">{it['n']}</span></a>
<div class="body"><h3>{E(it['title'])}</h3><p class="meta">{E(it['model'])} · {E(it['cat'])}</p><p class="price">{E(it['price'])}</p>{lb}
<div class="btns"><a class="btn pri" href="{it['img']}" download="{it['model']}.jpg">Save photo</a>
<button class="btn" type="button" data-copy="t">Copy title</button><button class="btn" type="button" data-copy="p">Copy price</button>
<button class="btn" type="button" data-copy="d">Copy description</button><button class="btn" type="button" data-copy="a">Copy all</button>
<label class="done"><input type="checkbox" id="c-{k}"> Posted</label></div>
<details><summary>Show description</summary><textarea readonly rows="14" aria-label="Description for {E(it['title'])}">{E(it['desc'])}</textarea></details>
<template data-t>{E(it['title'])}</template><template data-p>{it['num']}</template></div></article>'''


batches = [items[i:i + 10] for i in range(0, TOTAL, 10)]
nav = ''.join(f'<a href="#b{k + 1}" data-b="b{k + 1}">{b[0]["n"]}–{b[-1]["n"]}</a>' for k, b in enumerate(batches))
secs = ''.join(f'<section class="batch" id="b{k + 1}"><header class="bh"><h2>Ads {b[0]["n"]}–{b[-1]["n"]}</h2><span class="prog" data-sec="b{k + 1}"></span></header>'
               + ''.join(card(it) for it in b) + '</section>' for k, b in enumerate(batches))

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Trimion Listing Pack</title><meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico">
<style>
:root{{--bg:#eef1f8;--card:#fff;--fg:#0d1830;--muted:#56637e;--line:#d6dcea;--navy:#081a3d;--navy2:#0f2d66;--accent:#1f5fd6;--gold:#f8c43a;--ok:#14864a;--okbg:#e3f4ea}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--accent:#7aaaff;--ok:#41c97c;--okbg:#12301f;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;margin:0}}
.wrap{{max-width:720px;margin:0 auto;padding:0 16px}}
.top{{background:linear-gradient(160deg,var(--navy2),var(--navy));color:#fff}}.top .wrap{{padding-block:20px}}
.brand{{font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 6px}}
h1{{font-size:1.5rem;line-height:1.2;margin:0 0 6px}}.top p{{margin:4px 0 0;color:#c9d5f0;font-size:14px}}.top b{{color:#fff}}
nav{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;gap:6px;overflow-x:auto;padding-block:10px;scrollbar-width:none}}
nav a{{flex:0 0 auto;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:var(--card);border-radius:99px;padding:5px 11px;font-size:13px;font-weight:600}}
nav a.full{{background:var(--okbg);border-color:var(--ok);color:var(--ok)}}
.batch{{scroll-margin-top:60px}}.bh{{display:flex;align-items:baseline;justify-content:space-between;margin:22px 0 10px}}
h2{{font-size:1.1rem;margin:0}}.prog{{font-size:13px;color:var(--muted)}}
.post{{display:grid;grid-template-columns:120px 1fr;gap:12px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:10px;scroll-margin-top:60px}}
.post.is-done{{border-color:var(--ok);background:var(--okbg)}}
.ph{{position:relative;display:block}}.ph img{{width:120px;height:120px;object-fit:contain;border-radius:10px;background:#fff;display:block}}
.num{{position:absolute;top:-6px;left:-6px;font-weight:700;font-size:13px;color:var(--navy);background:var(--gold);border-radius:50%;width:28px;height:28px;display:grid;place-items:center}}
.body{{min-width:0}}h3{{font-size:15px;line-height:1.3;margin:0 0 2px}}.meta{{color:var(--muted);font-size:13px;margin:0}}
.price{{font-weight:700;font-size:16px;margin:4px 0 0}}.lb{{color:var(--muted);font-size:13px;margin:0}}
.btns{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}}
.btn{{font:600 13px system-ui,sans-serif;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:9px;padding:7px 10px;text-decoration:none;cursor:pointer}}
.btn.pri{{background:var(--accent);border-color:var(--accent);color:#fff}}.btn.ok{{background:var(--ok);border-color:var(--ok);color:#fff}}
.done{{display:flex;align-items:center;gap:5px;font-size:13px;font-weight:600;padding:0 4px}}
details{{margin-top:8px}}summary{{font-size:13px;color:var(--accent);cursor:pointer}}
textarea{{width:100%;margin-top:6px;font:13px/1.45 system-ui,sans-serif;border:1px solid var(--line);border-radius:9px;padding:8px;background:var(--bg);color:var(--fg)}}
@media (max-width:420px){{.post{{grid-template-columns:96px 1fr}}.ph img{{width:96px;height:96px}}}}
</style></head><body>
<header class="top"><div class="wrap"><p class="brand">Trimion Africa</p><h1>Listing pack: {TOTAL} ready-to-post ads</h1>
<p>For <b>Gumtree, Facebook Marketplace, Junkmail, Bob Shop</b> and salon groups. Tap <b>Save photo</b>, then copy the title, price and description into the ad. Tick <b>Posted</b> so you know where you are.</p>
<p>Post 10 a day. Ads with a clear price and photo get the most replies.</p></div></header>
<nav aria-label="Batches"><div class="wrap">{nav}</div></nav>
<main class="wrap">{secs}<p style="color:var(--muted);font-size:13px;margin:24px 0 40px">Prices and details match trimionafrica.co.za. WhatsApp {N}.</p></main>
<script>
(function(){{
 var S={{get:function(k){{try{{return localStorage.getItem(k)}}catch(e){{return null}}}},set:function(k,v){{try{{v?localStorage.setItem(k,v):localStorage.removeItem(k)}}catch(e){{}}}}}};
 function copy(txt,b){{var done=function(){{var o=b.textContent;b.textContent='Copied ✓';b.classList.add('ok');setTimeout(function(){{b.textContent=o;b.classList.remove('ok')}},1400)}};
  if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(txt).then(done,function(){{fb(txt);done()}})}}else{{fb(txt);done()}}}}
 function fb(t){{var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{{document.execCommand('copy')}}catch(e){{}}a.remove()}}
 document.addEventListener('click',function(e){{var b=e.target.closest('[data-copy]');if(!b)return;var c=b.closest('.post');
  var t=c.querySelector('template[data-t]').innerHTML.replace(/&amp;/g,'&'),p=c.querySelector('template[data-p]').innerHTML,d=c.querySelector('textarea').value;
  var m={{t:t,p:p,d:d,a:t+'\\n\\n'+d}};copy(m[b.dataset.copy],b)}});
 function prog(){{document.querySelectorAll('.batch').forEach(function(s){{var all=s.querySelectorAll('.post').length,n=s.querySelectorAll('.post.is-done').length;
  s.querySelector('.prog').textContent=n+' of '+all+' posted';var a=document.querySelector('nav a[data-b="'+s.id+'"]');if(a)a.classList.toggle('full',n===all)}})}}
 document.querySelectorAll('.post').forEach(function(c){{var k='tal-'+c.dataset.key,i=c.querySelector('input[type=checkbox]');
  if(S.get(k)){{i.checked=true;c.classList.add('is-done')}}i.addEventListener('change',function(){{S.set(k,i.checked?'1':'');c.classList.toggle('is-done',i.checked);prog()}})}});
 prog();
}})();
</script></body></html>'''

os.makedirs(f'{PUB}/gumtree', exist_ok=True)
open(f'{PUB}/gumtree/index.html', 'w', encoding='utf-8').write(PAGE)
print('listing pack:', TOTAL, 'ads at /gumtree')
