# Builds the Instagram posting plan: every post in order (1, 2, 3 ...) in batches of 10, with the
# Instagram caption (no clickable links, "link in bio"), price, lay-by and the video to post.
# Writes two copies of the same page:
#   ../public/instagram/index.html   (on the website; buttons download the videos)
#   argv[1]                          (the saved Claude artifact; buttons open the videos in a new tab)
import base64, html, json, os, re, sys
T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
SITE = 'https://trimionafrica.co.za'
N = '064 454 8506'
IGTAGS = '#salonequipment #spaequipment #beautysalon #salonowner #aestheticsbusiness #beautybusinesssa #durbansalon #southafricanbusiness #TrimionAfrica'

PR = {p['model']: p for p in json.load(open(f'{T}/products.json'))}
DT = {d['model']: d for d in json.load(open(f'{T}/details.json'))}
PO = {p['code']: p for p in json.load(open(f'{T}/postt/posts.json'))}
BANK = json.load(open(f'{T}/post_bank.json'))
CAT = {'ems': 'EMS', 'cryo': 'Cryo', 'rf': 'RF & cavitation', 'hifu': 'HIFU', 'face': 'Facial',
       'massage': 'Body massage', 'salon': 'Salon & wellness', 'supplies': 'Consumables'}
TAGS = {'ems': '#emsmachine #bodycare', 'cryo': '#cryo #bodycare', 'rf': '#rfmachine #cavitation',
        'hifu': '#HIFU #HIFUfacial', 'face': '#facialmachine #facialist', 'massage': '#bodymassage #spatreatment',
        'salon': '#salonlife #wellness', 'supplies': '#salonsupplies #spasupplies'}

# Day-1 posts (same as /media/today/), taken from today_page.py without running its page build
src = open(f'{T}/today_page.py', encoding='utf-8').read()
env = {'__file__': f'{T}/today_page.py'}; exec(src[:src.index('def cap_btn')], env); TODAY = env['POSTS']


def tags(*parts):
    seen, out = set(), []
    for t in ' '.join(parts).split():
        if t.lower() not in seen: seen.add(t.lower()); out.append(t)
    return ' '.join(out[:14])


def ig_from_bank(text, sid):
    out = []
    for ln in text.split('\n'):
        if ln.startswith('🔗'): continue
        if ln.startswith('🎁'): ln = '🎁 10% off with code TRIMION10'
        if ln.startswith('📲'): ln = f'📲 WhatsApp {N} · link in bio'
        if ln.startswith('📍'): ln = '📍 Durban · delivered nationwide'
        if ln.startswith('#'): ln = tags(ln.replace('#TrimionAfrica', ''), IGTAGS)
        out.append(ln)
    return '\n'.join(out)


def ig_new(code):
    p, d, o = PR[code], DT.get(code, {}), PO[code]
    sid = o['sid']; cons = sid == 'supplies'
    sp = d.get('specs', [])
    specs = (f"\n✔ {', '.join(sp)}" if sp else '') if cons else ''.join(f'\n✔ {s}' for s in sp[:3])
    hook = d.get('desc', [''])[0]
    lb = '' if cons or not p.get('lb') else f"\n💳 {p['lb']}"
    extra = '' if cons else '\n✅ 1-year warranty ✅ Free online training'
    return (f"{p['name']} ({code}) – {p['price']}\n\n{hook}{specs}\n\n💰 {p['price']}{lb}\n🚚 R150 delivery anywhere in South Africa{extra}"
            f"\n\n📲 WhatsApp {N} · link in bio\n📍 Durban · delivered nationwide\n\n{tags(TAGS.get(sid, ''), IGTAGS)}")


def thumb(path):
    f = os.path.join(PUB, path.lstrip('/'))
    return 'data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()


def machine(code, cap=None):
    p, o = PR[code], PO[code]; f = o['file']
    return dict(kind='m', title=p['name'], code=code, cat=CAT.get(o['sid'], ''), price=p['price'],
                lb='' if o['sid'] == 'supplies' else p.get('lb', ''), thumb=f'/social/thumb/{f}.jpg',
                feed=f'/social/feed/{f}.mp4', reel=f'/social/{f}_m2.mp4', cap=cap or (ig_from_bank(BANK_TXT[code], o['sid']) if code in BANK_TXT else ig_new(code)))


BANK_TXT = {b['code']: b['text'] for b in BANK}
REF_CAP = f"""Know a salon that needs a machine? Earn R2,000 💸

Refer a salon or spa to Trimion Africa. When they buy a machine from R25,000, you get R2,000.

✔ No limit on how many salons you refer
✔ They must name you before they order
✔ Valid until 31 December 2026

📲 WhatsApp {N} with your name and the salon's number · link in bio
T&Cs apply.

{IGTAGS}"""
DHAN_CAP = f"""Shubh Dhanteras from Trimion Africa 🪔

The best day to invest in your salon. Order by Friday 6 November for delivery in time for your new-season bookings.

💳 Diwali Special: lay-by deposit of only R5,000 (machines up to R60,000)
🏷️ 10% off with code TRIMION10
🚚 R150 delivery nationwide

📲 WhatsApp {N} · link in bio
T&Cs apply.

#Dhanteras #Diwali #DurbanDiwali {IGTAGS}"""
GREET_CAP = f"""Happy Diwali from all of us at Trimion Africa 🪔✨

May the festival of lights bring you, your family and your salon joy, health and a bright, busy year ahead.

📲 WhatsApp {N} · link in bio

#HappyDiwali #Diwali #DurbanDiwali #TrimionAfrica"""

items = []
for p in TODAY:
    m = re.search(r'\(([A-Z0-9-]+)\)$', p['title'])
    if m and m.group(1) in PR:
        it = machine(m.group(1), p['ig'])
    else:
        it = dict(kind='s', title=p['title'], code='', cat='Special', price='', lb='', thumb=p['thumb'],
                  feed=p['fb_vid'], reel=p['ig_vid'] if p['ig_vid'] != p['fb_vid'] else '', cap=p['ig'])
    items.append(it)
done = {i['code'] for i in items if i['code']}
rest = [b['code'] for b in BANK if b['code'] not in done]
rest += [c for c in PR if c not in done and c not in rest and c in PO]
for i, c in enumerate(rest):
    if i == 13:   # Refer & Earn as post 21
        items.append(dict(kind='s', title='Refer a salon, earn R2,000', code='', cat='Special', price='', lb='',
                          thumb='/social/thumb/Trimion_Offer_ref.jpg', feed='/social/Trimion_Offer_ref.mp4', reel='', cap=REF_CAP))
    items.append(machine(c))
dated = [dict(kind='d', title='Dhanteras', when='Post on or before Fri 6 Nov', code='', cat='Story', price='', lb='',
              thumb='/social/thumb/Trimion_Diwali_dhan.jpg', feed='', reel='/social/Trimion_Diwali_dhan.mp4', cap=DHAN_CAP),
         dict(kind='d', title='Happy Diwali', when='Post on Sun 8 Nov', code='', cat='Story', price='', lb='',
              thumb='/social/thumb/Trimion_Diwali_greet.jpg', feed='', reel='/social/Trimion_Diwali_greet.mp4', cap=GREET_CAP)]
for i, it in enumerate(items, 1): it['n'] = i
for it in items + dated: it['img'] = thumb(it['thumb'])
TOTAL = len(items)

E = html.escape


def page(site):
    def link(url, label, cls):
        if not url: return ''
        href = url if site else SITE + url
        extra = ' download' if site else ' target="_blank" rel="noopener"'
        return f'<a class="btn {cls}" href="{href}"{extra}>{label}</a>'

    def card(it, num):
        meta = ' · '.join(x for x in (it['code'], it['cat']) if x)
        price = f'<p class="price">{E(it["price"])}</p>' if it['price'] else ''
        lb = f'<p class="lb">{E(it["lb"])}</p>' if it['lb'] else ''
        when = f'<p class="when">{E(it["when"])}</p>' if it.get('when') else ''
        key = f"p{num}" if isinstance(num, int) else num
        badge = num if isinstance(num, int) else '★'
        btns = link(it['feed'], 'Feed video 4:5 ♪', 'pri') + link(it['reel'], 'Reel / Story 9:16 ♪' if it['feed'] else 'Story video 9:16 ♪', 'pri' if not it['feed'] else 'sec')
        return f'''<article class="post" id="{key}" data-key="{key}">
<div class="num" aria-hidden="true">{badge}</div>
<img class="th" src="{it['img']}" alt="" width="96" height="96" loading="lazy">
<div class="body"><h3>{E(it['title'])}</h3><p class="meta">{E(meta)}</p>{when}{price}{lb}
<div class="btns">{btns}<button class="btn cap" type="button">Copy caption</button>
<label class="done"><input type="checkbox" id="c-{key}"> Posted</label></div>
<details><summary>Show caption</summary><textarea readonly rows="12" aria-label="Instagram caption for {E(it['title'])}">{E(it['cap'])}</textarea></details></div></article>'''

    batches = [items[i:i + 10] for i in range(0, TOTAL, 10)]
    nav = ''.join(f'<a href="#b{k + 1}" data-b="b{k + 1}">{b[0]["n"]}–{b[-1]["n"]}</a>' for k, b in enumerate(batches))
    nav += '<a href="#dated" data-b="dated">Diwali</a>'
    secs = ''.join(f'<section class="batch" id="b{k + 1}"><header class="bh"><h2>Posts {b[0]["n"]}–{b[-1]["n"]}</h2><span class="prog" data-sec="b{k + 1}"></span></header>'
                   + ''.join(card(it, it['n']) for it in b) + '</section>' for k, b in enumerate(batches))
    secs += ('<section class="batch" id="dated"><header class="bh"><h2>Dated Stories</h2><span class="prog" data-sec="dated"></span></header>'
             '<p class="note">Post these as Instagram Stories on the day, not in the main sequence.</p>'
             + ''.join(card(it, f'd{i}') for i, it in enumerate(dated, 1)) + '</section>')
    how = ('Tap <b>Feed video 4:5</b> to download it, tap <b>Copy caption</b>, then post on Instagram.' if site else
           'Tap <b>Feed video 4:5</b> to open it, then save it to your phone (hold the video, or use the ⋮ menu). Tap <b>Copy caption</b> and post on Instagram.')
    return f'''<title>Trimion Instagram Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap">
<style>
/* Layout: navy brand band, sticky batch chips, one column of numbered post cards */
:root{{--bg:#eef1f8;--card:#ffffff;--fg:#0d1830;--muted:#56637e;--line:#d6dcea;--navy:#081a3d;--navy2:#0f2d66;--accent:#1f5fd6;--gold:#f8c43a;--ok:#14864a;--okbg:#e3f4ea;
 --display:"Poppins",system-ui,-apple-system,"Segoe UI",sans-serif;--body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0b1f4a;--navy2:#123272;--accent:#7aaaff;--gold:#f8c43a;--ok:#41c97c;--okbg:#12301f;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0b1f4a;--navy2:#123272;--accent:#7aaaff;--gold:#f8c43a;--ok:#41c97c;--okbg:#12301f;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body);margin:0}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}}
.wrap{{max-width:720px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.top{{background:linear-gradient(160deg,var(--navy2),var(--navy));color:#fff}}
.top .wrap{{padding-block:22px 20px}}
.brand{{font:700 12px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 8px}}
h1{{font:700 1.6rem/1.2 var(--display);margin:0 0 6px;text-wrap:balance}}
.top p{{margin:0;color:#c9d5f0;font-size:14px;max-width:60ch}}.top b{{color:#fff}}
.stats{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}
.stat{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:10px;padding:6px 10px;font-size:13px}}
.stat strong{{font:700 15px var(--display);font-variant-numeric:tabular-nums}}
nav{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;gap:6px;overflow-x:auto;padding-block:10px;scrollbar-width:none}}
nav a{{flex:0 0 auto;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:var(--card);border-radius:99px;padding:5px 11px;font-size:13px;font-weight:600;font-variant-numeric:tabular-nums}}
nav a.full{{background:var(--okbg);border-color:var(--ok);color:var(--ok)}}
.batch{{scroll-margin-top:64px;padding-top:8px}}
.bh{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:22px 0 10px}}
h2{{font:700 1.15rem var(--display);margin:0}}
.prog{{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}}
.note{{color:var(--muted);font-size:13px;margin:-4px 0 10px}}
.post{{display:grid;grid-template-columns:auto 96px 1fr;gap:12px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:10px;scroll-margin-top:64px}}
.post.is-done{{border-color:var(--ok);background:linear-gradient(var(--okbg),var(--okbg)) padding-box}}
.num{{font:700 15px/1 var(--display);color:var(--navy);background:var(--gold);border-radius:50%;width:32px;height:32px;display:grid;place-items:center;font-variant-numeric:tabular-nums}}
.th{{width:96px;height:96px;object-fit:contain;border-radius:10px;background:var(--navy);max-width:100%}}
.body{{min-width:0}}
h3{{font:600 15px/1.3 var(--display);margin:0;text-wrap:balance}}
.meta{{margin:2px 0 0;color:var(--muted);font-size:12.5px}}
.when{{margin:4px 0 0;font-weight:700;color:var(--accent);font-size:13px}}
.price{{margin:6px 0 0;font:700 1.25rem/1.1 var(--display);color:var(--accent);font-variant-numeric:tabular-nums}}
.lb{{margin:2px 0 0;font-size:12.5px;color:var(--muted)}}
.btns{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}}
.btn{{font:600 13px/1 var(--body);text-decoration:none;border-radius:9px;padding:9px 11px;cursor:pointer;border:1px solid var(--line);background:transparent;color:var(--fg)}}
.btn.pri{{background:var(--navy2);border-color:var(--navy2);color:#fff}}
.btn.cap{{color:var(--accent);border-color:var(--accent)}}
.btn:focus-visible,nav a:focus-visible,summary:focus-visible,.done input:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.done{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--ok);padding:6px 4px;cursor:pointer}}
.done input{{width:18px;height:18px;accent-color:var(--ok)}}
details{{margin-top:8px}}summary{{cursor:pointer;color:var(--muted);font-size:13px}}
textarea{{width:100%;margin-top:6px;font:13px/1.45 var(--body);color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:8px;resize:vertical}}
.foot{{color:var(--muted);font-size:12.5px;padding-block:20px 40px}}
.toast{{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--fg);color:var(--bg);padding:10px 16px;border-radius:10px;opacity:0;transition:opacity .2s;pointer-events:none;font-weight:600}}
.toast.on{{opacity:1}}
@media (max-width:480px){{.post{{grid-template-columns:auto 72px 1fr;gap:10px}}.th{{width:72px;height:72px}}}}
@media (prefers-reduced-motion:reduce){{.toast{{transition:none}}}}
</style>
<div class="top"><div class="wrap">
<p class="brand">Trimion Africa · Instagram</p>
<h1>Instagram posting plan</h1>
<p>Post in number order, one at a time. {how} The 4:5 feed video fits the Instagram grid with nothing cut off.</p>
<div class="stats"><span class="stat"><strong>{TOTAL}</strong> posts</span><span class="stat"><strong id="dn">0</strong> posted</span><span class="stat">Next: <strong id="nx">1</strong></span></div>
</div></div>
<nav aria-label="Batches"><div class="wrap">{nav}</div></nav>
<main class="wrap">{secs}
<p class="foot">Captions have no clickable links because Instagram doesn't allow them. Put trimionafrica.co.za in your Instagram bio so "link in bio" works. Prices and lay-by amounts match the website on {__import__("datetime").date.today():%d %B %Y}.</p></main>
<div class="toast" id="toast" role="status">Caption copied</div>
<script>
(function(){{
var K='trimion-ig-posted';var S={{}};
try{{S=JSON.parse(localStorage.getItem(K)||'{{}}')||{{}}}}catch(e){{S={{}}}}
function save(){{try{{localStorage.setItem(K,JSON.stringify(S))}}catch(e){{}}}}
var posts=[].slice.call(document.querySelectorAll('.post'));
function refresh(){{var n=0,next=null;
 posts.forEach(function(p){{var k=p.dataset.key,on=!!S[k];p.classList.toggle('is-done',on);p.querySelector('.done input').checked=on;
  if(k.charAt(0)==='p'){{if(on)n++;else if(next===null)next=k.slice(1);}}}});
 document.getElementById('dn').textContent=n;document.getElementById('nx').textContent=next||'all done';
 [].forEach.call(document.querySelectorAll('.prog'),function(el){{var sec=document.getElementById(el.dataset.sec);var ps=sec.querySelectorAll('.post'),d=0;
  [].forEach.call(ps,function(p){{if(S[p.dataset.key])d++}});el.textContent=d+' of '+ps.length+' posted';
  var a=document.querySelector('nav a[data-b="'+el.dataset.sec+'"]');if(a)a.classList.toggle('full',d===ps.length);}});}}
var t=document.getElementById('toast');function toast(m){{t.textContent=m;t.classList.add('on');setTimeout(function(){{t.classList.remove('on')}},1500)}}
document.addEventListener('change',function(e){{var i=e.target.closest('.done input');if(!i)return;var k=i.closest('.post').dataset.key;
 if(i.checked)S[k]=1;else delete S[k];save();refresh();}});
document.addEventListener('click',function(e){{var b=e.target.closest('.cap');if(!b)return;var p=b.closest('.post'),ta=p.querySelector('textarea');
 function fallback(){{p.querySelector('details').open=true;ta.focus();ta.select();toast('Caption selected, tap Copy')}}
 if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(ta.value).then(function(){{toast('Caption copied')}},fallback)}}else fallback();}});
refresh();
}})();
</script>'''


body = page(True)
os.makedirs(f'{PUB}/instagram', exist_ok=True)
open(f'{PUB}/instagram/index.html', 'w', encoding='utf-8').write(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    '<link rel="icon" href="/icon-192.png"><meta name="theme-color" content="#081a3d">'
    + body.replace('<style>', '<style>[hidden]{display:none!important}', 1).replace('<div class="top">', '</head><body><div class="top">', 1) + '</body></html>')
if len(sys.argv) > 1:
    open(sys.argv[1], 'w', encoding='utf-8').write(page(False))
print(TOTAL, 'posts +', len(dated), 'dated stories')
