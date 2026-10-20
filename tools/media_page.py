# Builds /media/: the download page for the social post bank (covers, new-number posts, specials,
# and every machine's Reel/Status video, feed video, story/feed/square pictures and caption).
import json, html, os
T = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(f'{T}/postt/posts.json'))
PR = {p['model']: p for p in json.load(open(f'{T}/products.json'))}
B = {b['code']: b['text'] for b in json.load(open(f'{T}/post_bank.json'))}
NUM = '064 454 8506'
SECS = [('ems', 'EMS & electromagnetic'), ('cryo', 'Cryo'), ('rf', 'RF & cavitation'), ('hifu', 'HIFU'),
        ('face', 'Facial & skin'), ('massage', 'Body massage'), ('salon', 'Wellness & salon'), ('supplies', 'Consumables')]

def caption(o):
    if o['code'] in B: return B[o['code']]
    p = PR[o['code']]
    lb = f"\n💳 {p['lb']}" if p.get('lb') and o['sid'] != 'supplies' else ''
    extra = '' if o['sid'] == 'supplies' else '\n✅ 1-year warranty ✅ Free online training'
    return (f"{p['name']} ({o['code']}) – {p['price']}\n\n💰 {p['price']}{lb}\n🚚 R150 delivery anywhere in South Africa{extra}\n\n"
            f"🔗 See it, price and lay-by: https://trimionafrica.co.za/p/m{o['k']}\n📲 WhatsApp {NUM}\n📍 Durban, KwaZulu-Natal · delivered nationwide\n\n#salonequipment #spaequipment #TrimionAfrica")

def btn(href, label, cls=''):
    return f'<a class="b {cls}" href="{href}" download>{label}</a>'

def card(thumb, title, sub, buttons, cap=None):
    c = f'<button class="b cap" type="button" data-cap="{html.escape(cap, quote=True)}">Copy caption</button>' if cap else ''
    return (f'<article class="it"><img loading="lazy" src="{thumb}" alt=""><div class="tx"><h3>{html.escape(title)}</h3>'
            f'<p>{html.escape(sub)}</p><div class="bs">{"".join(buttons)}{c}</div></div></article>')

NEW_CAP = (f"📲 We have a new WhatsApp number: {NUM}\n\nSave it now to chat, get prices, lay-by plans and order salon and spa machines.\n"
           "Our old number is no longer in use.\n\n🔗 trimionafrica.co.za\n📍 Durban · delivered nationwide\n\n#TrimionAfrica #salonequipment")
start = [
    card('/media/fb-cover.jpg', 'Facebook cover photo', '1640 × 924 · fits phone and computer', [btn('/media/fb-cover.jpg', 'Download')]),
    card('/media/whatsapp-cover.jpg', 'WhatsApp Business cover photo', '1920 × 1080', [btn('/media/whatsapp-cover.jpg', 'Download')]),
    card('/media/profile.jpg', 'Profile picture', 'WhatsApp, Facebook, Instagram · 1080 × 1080', [btn('/media/profile.jpg', 'Download')]),
    card('/media/new-number-story.jpg', 'New number: Status / Story / Reel', '9:16 · video with music', [btn('/media/new-number-story.mp4', 'Video ♪', 'v'), btn('/media/new-number-story.jpg', 'Picture')], NEW_CAP),
    card('/media/new-number-feed.jpg', 'New number: Facebook / Instagram post', '4:5 · video with music', [btn('/media/new-number-feed.mp4', 'Video ♪', 'v'), btn('/media/new-number-feed.jpg', 'Picture')], NEW_CAP),
]
SP = [('Trimion_Offer_kit', 'Free Salon Starter Kit', 'Until 31 Dec 2026'), ('Trimion_Offer_ref', 'Refer & earn R2,000', 'Until 31 Dec 2026'),
      ('Trimion_Diwali_offer', 'Diwali Special', 'Until 15 Nov 2026'), ('Trimion_Diwali_dhan', 'Dhanteras · 6 Nov', 'Post before 6 Nov'),
      ('Trimion_Diwali_greet', 'Happy Diwali greeting', 'Post on 8 Nov')]
specials = [card(f'/social/thumb/{f}.jpg', t, s + ' · video with music', [btn(f'/social/{f}.mp4', 'Video ♪', 'v')]) for f, t, s in SP]

groups = {}
for o in P:
    f = o['file']; p = PR[o['code']]
    groups.setdefault(o['sid'], []).append(card(
        f'/social/thumb/{f}.jpg', p['name'], f"{o['code']} · {p['price']}",
        [btn(f'/social/{f}_m2.mp4', 'Reel/Status ♪', 'v'), btn(f'/social/feed/{f}.mp4', 'Feed video ♪', 'v'),
         btn(f'/social/{f}.jpg', 'Story pic'), btn(f'/social/feed/{f}.jpg', 'Feed pic'), btn(f'/social/square/{f}.jpg', 'Square pic')],
        caption(o)))

tabs = [('start', 'Covers & new number', start), ('specials', 'Specials', specials)] + \
       [(sid, f'{name} ({len(groups.get(sid, []))})', groups.get(sid, [])) for sid, name in SECS]
nav = ''.join(f'<a href="#{k}">{html.escape(n)}</a>' for k, n, _ in tabs)
body = ''.join(f'<section id="{k}"><h2>{html.escape(n)}</h2>{"".join(items)}</section>' for k, n, items in tabs)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Trimion Media Kit</title><meta name="robots" content="noindex">
<link rel="icon" href="/icon-192.png"><meta name="theme-color" content="#081a3d">
<style>
:root{{--bg:#f3f5fa;--card:#fff;--fg:#0d1830;--muted:#55627d;--line:#d9dfeb;--navy:#081a3d;--accent:#1f6feb;--wa:#128c4a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0c2350;--accent:#6aa5ff;--wa:#2fbf6e;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
header{{background:var(--navy);color:#fff;padding:22px 16px 18px}}header h1{{margin:0 0 4px;font-size:1.5rem}}header p{{margin:0;opacity:.85}}
header b{{color:#7ee2a0}}
nav{{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:8px;overflow-x:auto;padding:10px 16px;scrollbar-width:none}}
nav a{{flex:0 0 auto;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:var(--card);border-radius:99px;padding:6px 12px;font-size:13px;font-weight:600}}
main{{max-width:760px;margin:0 auto;padding:0 16px 40px}}section{{scroll-margin-top:60px}}h2{{font-size:1.15rem;margin:26px 0 10px}}
.it{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px;margin-bottom:10px}}
.it img{{width:92px;height:92px;object-fit:contain;border-radius:10px;flex:0 0 auto;background:#0a1f4d}}
.tx{{min-width:0;flex:1}}h3{{margin:0;font-size:14px;line-height:1.3}}.tx p{{margin:2px 0 8px;color:var(--muted);font-size:13px}}
.bs{{display:flex;flex-wrap:wrap;gap:6px}}.b{{font:inherit;font-size:12.5px;font-weight:600;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:transparent;border-radius:8px;padding:6px 9px;cursor:pointer}}
.b.v{{background:var(--wa);border-color:var(--wa);color:#fff}}.b.cap{{color:var(--accent)}}
.toast{{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:#111;color:#fff;padding:10px 16px;border-radius:10px;opacity:0;transition:opacity .2s;pointer-events:none}}.toast.on{{opacity:1}}
</style></head><body>
<header><h1>Trimion media kit</h1><p>Everything with the new number <b>{NUM}</b>. Tap a button to download, then post. ♪ = instrumental music included.</p></header>
<nav>{nav}</nav><main>{body}
<p style="color:var(--muted);font-size:13px;margin-top:24px">Reel/Status = 9:16 for WhatsApp Status, Instagram & Facebook Reels and Stories. Feed = 4:5 for Facebook & Instagram posts. Square = 1:1 for WhatsApp catalog or Marketplace.</p></main>
<div class="toast" id="t">Caption copied</div>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('.cap');if(!b)return;var t=b.getAttribute('data-cap'),s=document.getElementById('t');
function ok(){{s.classList.add('on');setTimeout(function(){{s.classList.remove('on')}},1400)}}
if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,function(){{prompt('Copy:',t)}});else prompt('Copy:',t)}});</script>
</body></html>'''
os.makedirs(f'{T}/../public/media', exist_ok=True)
open(f'{T}/../public/media/index.html', 'w').write(page)
print('media page:', sum(len(i) for _, _, i in tabs), 'items')
