# Builds /media/today/: the first day of posts for the new Facebook page and Instagram (posted separately).
import html, os
T = os.path.dirname(os.path.abspath(__file__))
N = '064 454 8506'
IGTAGS = '#salonequipment #spaequipment #beautysalon #salonowner #aestheticsbusiness #beautybusinesssa #durbansalon #southafricanbusiness #TrimionAfrica'

POSTS = [
 dict(t='08:30', title='Our new number (first post)',
      fb_vid='/media/new-number-feed.mp4', ig_vid='/media/new-number-story.mp4', thumb='/media/new-number-feed.jpg',
      fb=f"""Welcome to the new Trimion Africa page! 👋

📲 Our new WhatsApp number is {N}. Save it now.

This is where you'll find our professional salon and spa machines: cryo, EMS, HIFU, RF, cavitation, facial machines and more, with prices, lay-by plans and delivery anywhere in South Africa.

✅ 1-year warranty
✅ Free online training
💳 Lay-by over 2–3 months
🚚 R150 delivery nationwide

Message us on WhatsApp: https://wa.me/27644548506
See every machine and price: https://trimionafrica.co.za

📍 Durban, KwaZulu-Natal

#TrimionAfrica #salonequipment #spaequipment""",
      ig=f"""Welcome to Trimion Africa 👋

📲 Our new WhatsApp number: {N}. Save it now.

Professional salon and spa machines: cryo, EMS, HIFU, RF, cavitation and facial machines, with prices, lay-by plans and delivery anywhere in South Africa.

✅ 1-year warranty
✅ Free online training
💳 Lay-by over 2–3 months
🚚 R150 delivery nationwide

👉 Prices and every machine: link in bio
📍 Durban · delivered nationwide

{IGTAGS}"""),
 dict(t='10:00', title='2-Handle Portable Electromagnetic + RF (TAEMC2R)',
      fb_vid='/social/feed/Trimion_140_TAEMC2R.mp4', ig_vid='/social/Trimion_140_TAEMC2R_m2.mp4', thumb='/social/feed/Trimion_140_TAEMC2R.jpg',
      fb=f"""Start offering electromagnetic body treatments for R34,600 ⚡

2-Handle Portable Electromagnetic + RF Body Sculpting Machine (TAEMC2R)
✔ Two handles with RF
✔ Up to 7 Tesla · 150Hz
✔ Compact, fits any treatment room

💰 R34,600
💳 Lay-by: R10,000 now, then 2 × R12,300
✅ 1-year warranty ✅ Free online training
🚚 R150 delivery anywhere in South Africa

🔗 Photos, specs and lay-by: https://trimionafrica.co.za/p/m74
📲 WhatsApp {N}

#TrimionAfrica #salonequipment #bodysculpting""",
      ig=f"""Start offering electromagnetic body treatments for R34,600 ⚡

2-Handle Portable Electromagnetic + RF (TAEMC2R)
✔ Two handles with RF
✔ Up to 7 Tesla · 150Hz
✔ Compact, fits any treatment room

💰 R34,600
💳 Lay-by: R10,000 now, then 2 × R12,300
✅ 1-year warranty ✅ Free online training
🚚 R150 delivery nationwide

📲 WhatsApp {N} · link in bio

#bodysculpting #emsculpt {IGTAGS}"""),
 dict(t='12:00', title='Diwali Special (until 15 Nov)',
      fb_vid='/social/Trimion_Diwali_offer.mp4', ig_vid='/social/Trimion_Diwali_offer.mp4', thumb='/social/thumb/Trimion_Diwali_offer.jpg',
      fb=f"""🪔 Diwali Special: light up your salon

Until 15 November 2026:
✨ FREE Salon Starter Kit with machines from R30,000
💳 Lay-by deposit of only R5,000 (machines up to R60,000)
🏷️ 10% off with code TRIMION10
🚚 R150 delivery nationwide

Full details: https://trimionafrica.co.za/promo
📲 WhatsApp {N} and tell us which machine you want.

T&Cs apply.
#Diwali #TrimionAfrica #salonequipment""",
      ig=f"""🪔 Diwali Special: light up your salon

Until 15 November 2026:
✨ FREE Salon Starter Kit with machines from R30,000
💳 Lay-by deposit of only R5,000 (machines up to R60,000)
🏷️ 10% off with code TRIMION10
🚚 R150 delivery nationwide

📲 WhatsApp {N} and tell us which machine you want.
T&Cs apply.

#Diwali #HappyDiwali #DurbanDiwali {IGTAGS}"""),
 dict(t='14:00', title='8-in-1 Water Dermabrasion Facial Station (TAWD8S)',
      fb_vid='/social/feed/Trimion_114_TAWD8S.mp4', ig_vid='/social/Trimion_114_TAWD8S_m2.mp4', thumb='/social/feed/Trimion_114_TAWD8S.jpg',
      fb=f"""8 facial tools in one station 💧

8-in-1 Water Dermabrasion Facial Station (TAWD8S)
✔ Cold hammer
✔ Bubble cleaner
✔ Skin scrubber and more

Add a deep-cleansing facial to your menu without buying eight separate devices.

💰 R29,250
💳 Lay-by: R10,000 now, then 2 × R9,625
✅ 1-year warranty ✅ Free online training
🚚 R150 delivery anywhere in South Africa

🔗 https://trimionafrica.co.za/p/m153
📲 WhatsApp {N}

#TrimionAfrica #facialmachine #hydrafacial""",
      ig=f"""8 facial tools in one station 💧

8-in-1 Water Dermabrasion Facial Station (TAWD8S)
✔ Cold hammer
✔ Bubble cleaner
✔ Skin scrubber and more

Add a deep-cleansing facial to your menu without buying eight separate devices.

💰 R29,250
💳 Lay-by: R10,000 now, then 2 × R9,625
✅ 1-year warranty ✅ Free online training

📲 WhatsApp {N} · link in bio

#facialmachine #hydrafacial #facialist {IGTAGS}"""),
 dict(t='16:00', title='4D HIFU Machine (TAUS4D)',
      fb_vid='/social/feed/Trimion_21_TAUS4D.mp4', ig_vid='/social/Trimion_21_TAUS4D_m2.mp4', thumb='/social/feed/Trimion_21_TAUS4D.jpg',
      fb=f"""Face and body HIFU in one machine ✨

4D HIFU Machine (TAUS4D)
✔ 4D technology
✔ 1–12 lines per shot
✔ 20,000 shots per cartridge

💰 R31,900
💳 Lay-by: R10,000 now, then 2 × R10,950
✅ 1-year warranty ✅ Free online training
🚚 R150 delivery anywhere in South Africa

🔗 https://trimionafrica.co.za/p/m128
📲 WhatsApp {N}

#TrimionAfrica #HIFU #salonequipment""",
      ig=f"""Face and body HIFU in one machine ✨

4D HIFU Machine (TAUS4D)
✔ 4D technology
✔ 1–12 lines per shot
✔ 20,000 shots per cartridge

💰 R31,900
💳 Lay-by: R10,000 now, then 2 × R10,950
✅ 1-year warranty ✅ Free online training

📲 WhatsApp {N} · link in bio

#HIFU #HIFUfacial #skincareclinic {IGTAGS}"""),
 dict(t='18:00', title='4-Handle 360° Cryo Station (TACRYO360-4)',
      fb_vid='/social/feed/Trimion_11_TACRYO360-4.mp4', ig_vid='/social/Trimion_11_TACRYO360-4_m2.mp4', thumb='/social/feed/Trimion_11_TACRYO360-4.jpg',
      fb=f"""Four clients at once. One station. ❄️

4-Handle 360° Cryo Body Contouring Station (TACRYO360-4)
✔ 4 handles running at the same time
✔ 360° surround cooling
✔ 7 applicator sizes

Built for busy salons and spas that want to book more clients a day.

💰 R157,200
💳 Lay-by: R40,000 now, then 2 × R58,600
✅ 1-year warranty ✅ Free online training
🚚 R150 delivery anywhere in South Africa

🔗 https://trimionafrica.co.za/p/m34
📲 WhatsApp {N}

#TrimionAfrica #cryo #spaequipment""",
      ig=f"""Four clients at once. One station. ❄️

4-Handle 360° Cryo Station (TACRYO360-4)
✔ 4 handles running at the same time
✔ 360° surround cooling
✔ 7 applicator sizes

💰 R157,200
💳 Lay-by: R40,000 now, then 2 × R58,600
✅ 1-year warranty ✅ Free online training

📲 WhatsApp {N} · link in bio

#cryo #bodycontouring #medspa {IGTAGS}"""),
 dict(t='19:30', title='Free Salon Starter Kit',
      fb_vid='/social/Trimion_Offer_kit.mp4', ig_vid='/social/Trimion_Offer_kit.mp4', thumb='/social/thumb/Trimion_Offer_kit.jpg',
      fb=f"""Buy the machine. Get the business. 💼

FREE Salon Starter Kit with every machine from R50,000:
✔ Certificate (worth R1,500)
✔ Treatment menu and price list
✔ 10 ready-made social media posts
✔ A "Trimion Certified Salon" feature on our page

Valid until 31 December 2026.
Details: https://trimionafrica.co.za/offers
📲 WhatsApp {N}

T&Cs apply.
#TrimionAfrica #salonowner #beautybusiness""",
      ig=f"""Buy the machine. Get the business. 💼

FREE Salon Starter Kit with every machine from R50,000:
✔ Certificate (worth R1,500)
✔ Treatment menu and price list
✔ 10 ready-made social media posts
✔ A "Trimion Certified Salon" feature on our page

Valid until 31 December 2026. T&Cs apply.
📲 WhatsApp {N} · link in bio

{IGTAGS}"""),
]

def cap_btn(txt, label):
    return f'<button class="b cap" type="button" data-cap="{html.escape(txt, quote=True)}">{label}</button>'
cards = []
for i, p in enumerate(POSTS, 1):
    cards.append(f'''<article class="it"><div class="hd"><span class="n">{i}</span><span class="tm">{p["t"]}</span><h3>{html.escape(p["title"])}</h3></div>
<img loading="lazy" src="{p["thumb"]}" alt="">
<div class="pl"><b>Facebook</b><div class="bs"><a class="b v" href="{p["fb_vid"]}" download>Video ♪</a>{cap_btn(p["fb"], "Copy caption")}</div></div>
<div class="pl"><b>Instagram</b><div class="bs"><a class="b v" href="{p["ig_vid"]}" download>Reel ♪</a>{cap_btn(p["ig"], "Copy caption")}</div></div>
<details><summary>Read captions</summary><pre>{html.escape(p["fb"])}</pre><pre>{html.escape(p["ig"])}</pre></details></article>''')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Trimion First Posts</title><meta name="robots" content="noindex">
<link rel="icon" href="/icon-192.png"><meta name="theme-color" content="#081a3d">
<style>
:root{{--bg:#f3f5fa;--card:#fff;--fg:#0d1830;--muted:#55627d;--line:#d9dfeb;--navy:#081a3d;--accent:#1f6feb;--wa:#128c4a;--gold:#f8c43a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0c2350;--accent:#6aa5ff;--wa:#2fbf6e;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
header{{background:var(--navy);color:#fff;padding:22px 16px 18px}}header h1{{margin:0 0 4px;font-size:1.5rem}}header p{{margin:0;opacity:.85}}
main{{max-width:620px;margin:0 auto;padding:12px 16px 40px}}
.it{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin-top:14px}}
.hd{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}.n{{background:var(--gold);color:#0a1f4d;font-weight:700;border-radius:50%;width:28px;height:28px;display:grid;place-items:center;flex:0 0 auto}}
.tm{{font-weight:700;color:var(--accent)}}h3{{margin:0;font-size:15px;line-height:1.3}}
.it>img{{width:100%;border-radius:10px;display:block;max-height:340px;object-fit:contain;background:#0a1f4d}}
.pl{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;flex-wrap:wrap}}
.bs{{display:flex;gap:6px;flex-wrap:wrap}}.b{{font:inherit;font-size:13px;font-weight:600;text-decoration:none;color:var(--fg);border:1px solid var(--line);background:transparent;border-radius:8px;padding:7px 11px;cursor:pointer}}
.b.v{{background:var(--wa);border-color:var(--wa);color:#fff}}.b.cap{{color:var(--accent)}}
details{{margin-top:10px;color:var(--muted);font-size:13px}}pre{{white-space:pre-wrap;font:inherit;border-top:1px solid var(--line);padding-top:8px}}
.toast{{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:#111;color:#fff;padding:10px 16px;border-radius:10px;opacity:0;transition:opacity .2s;pointer-events:none}}.toast.on{{opacity:1}}
</style></head><body>
<header><h1>Today's 7 posts</h1><p>Post 1 first. For each post: download the video, copy the caption, then post on Facebook and Instagram separately. Times are a guide.</p></header>
<main>{"".join(cards)}<p style="color:var(--muted);font-size:13px;margin-top:20px">All posts and videos: <a href="/media/" style="color:var(--accent)">trimionafrica.co.za/media</a></p></main>
<div class="toast" id="t">Caption copied</div>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('.cap');if(!b)return;var t=b.getAttribute('data-cap'),s=document.getElementById('t');
function ok(){{s.classList.add('on');setTimeout(function(){{s.classList.remove('on')}},1400)}}
if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,function(){{prompt('Copy:',t)}});else prompt('Copy:',t)}});</script>
</body></html>'''
os.makedirs(f'{T}/../public/media/today', exist_ok=True)
open(f'{T}/../public/media/today/index.html', 'w').write(page)
print('today page:', len(POSTS), 'posts')
