#!/usr/bin/env python3
"""Offers page at /offers: (1) free Salon Starter Kit with every machine from R50,000,
(2) refer a salon, earn R2,000 when they buy a machine from R25,000. Runs in rebuild.sh."""
import os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "offers")
KIT_MIN, REF_MIN, REF_PAY, END = "R50,000", "R25,000", "R2,000", "31 December 2026"
q = urllib.parse.quote
WA_KIT = "https://wa.me/27611185978?text=" + q("Hi Trimion, I'd like the free Salon Starter Kit with my machine. The machine I want is: ")
WA_REF = "https://wa.me/27611185978?text=" + q("Hi Trimion, I'd like to refer a salon for the R2,000 reward.\n\nMy name: \nSalon I'm referring: \nTheir number: ")

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Trimion Salon Offers</title>
<meta name="description" content="Free Salon Starter Kit with every machine from {KIT_MIN}, and earn {REF_PAY} for every salon you refer. Trimion Africa, Durban.">
<meta property="og:title" content="Buy the machine. Get the business.">
<meta property="og:description" content="Free Salon Starter Kit with every machine from {KIT_MIN} · Refer a salon, earn {REF_PAY}.">
<meta property="og:image" content="https://trimionafrica.co.za/offers/kit.jpg">
<meta property="og:url" content="https://trimionafrica.co.za/offers/">
<link rel="canonical" href="https://trimionafrica.co.za/offers/">
<link rel="icon" href="/icon-192.png">
<meta name="theme-color" content="#081a3d">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Figtree:wght@400;500;600&display=swap">
<style>
:root{{--bg:#f3f5fa;--card:#fff;--fg:#0d1830;--muted:#55627d;--line:#d9dfeb;--navy:#081a3d;--accent:#1f6feb;--wa:#128c4a;--gold:#ffd23f;
  --display:"Sora",system-ui,sans-serif;--body:"Figtree",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0c2350;--accent:#6aa5ff;--wa:#2fbf6e;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--muted:#9aa7c2;--line:#26324d;--navy:#0c2350;--accent:#6aa5ff;--wa:#2fbf6e;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:620px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-right,0px)) 40px max(16px,env(safe-area-inset-left,0px))}}
header{{background:var(--navy);color:#fff}}
header .wrap{{padding-top:30px;padding-bottom:28px}}
.eyebrow{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin:0 0 8px}}
h1{{font:700 2rem/1.15 var(--display);margin:0 0 10px;text-wrap:balance}}
header p{{margin:0;opacity:.85}}
.hero{{width:100%;border-radius:14px;margin-top:18px;display:block}}
section{{margin-top:24px}}
h2{{font:600 1.25rem/1.3 var(--display);margin:0 0 4px}}
.tag{{display:inline-block;background:var(--gold);color:#3a2a00;font-weight:700;font-size:12px;border-radius:99px;padding:3px 10px;margin-bottom:8px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.card p{{margin:0 0 10px;color:var(--muted)}}
ul.kit{{list-style:none;padding:0;margin:0}} ul.kit li{{padding:9px 0;border-top:1px solid var(--line);display:flex;gap:12px}}
ul.kit li:first-child{{border-top:0}} ul.kit b{{display:block}} ul.kit span{{color:var(--muted);font-size:14px}}
ul.kit i{{font-style:normal;font-size:22px;line-height:1.2}}
ol{{margin:0;padding-left:20px}} ol li{{margin:6px 0}}
.btn{{display:block;text-align:center;text-decoration:none;font-weight:600;border-radius:12px;padding:14px 16px;margin-top:12px}}
.wa{{background:var(--wa);color:#fff}} .shop{{border:1px solid var(--line);color:var(--fg);background:var(--card)}}
.terms{{font-size:13px;color:var(--muted)}} .terms li{{margin:4px 0}}
a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
</style>
</head>
<body>
<header><div class="wrap">
  <p class="eyebrow">Trimion Africa · Salon equipment, Durban</p>
  <h1>Buy the machine. Get the business.</h1>
  <p>Two offers for salons and spas, valid until {END}.</p>
</div></header>
<main class="wrap">
<section id="diwali">
  <span class="tag">🪔 Diwali Special · until 15 November 2026</span>
  <h2>Light up your salon this Diwali</h2>
  <div class="card">
    <p>Happy Diwali from Trimion Africa. Until 15 November 2026:</p>
    <ul class="kit">
      <li><i>🎁</i><div><b>Free Salon Starter Kit from R30,000</b><span>Normally from R50,000. Certificate, treatment menu, 10 social posts and a Certified Salon feature.</span></div></li>
      <li><i>💳</i><div><b>Lay-by deposit only R5,000</b><span>On machines up to R60,000. Pay the balance over 2 or 3 months.</span></div></li>
      <li><i>🏷️</i><div><b>10% off with code TRIMION10</b><span>Works together with the Diwali Special.</span></div></li>
      <li><i>🚚</i><div><b>R150 delivery anywhere in South Africa</b><span>Order by Dhanteras, Friday 6 November, for delivery in time for your new-season bookings.</span></div></li>
    </ul>
    <a class="btn wa" href="https://wa.me/27611185978?text=Hi%20Trimion%2C%20I%27d%20like%20the%20Diwali%20Special.%20The%20machine%20I%20want%20is%3A%20" target="_blank" rel="noopener">Claim the Diwali Special on WhatsApp</a>
  </div>
</section>
<section id="kit">
  <span class="tag">With every machine from {KIT_MIN}</span>
  <h2>Free Salon Starter Kit</h2>
  <div class="card">
    <p>Everything you need to start booking clients the week your machine arrives.</p>
    <ul class="kit">
      <li><i>🎓</i><div><b>Certificate included free</b><span>Normally R1,500. Hang it in your treatment room.</span></div></li>
      <li><i>📋</i><div><b>Treatment menu and price list</b><span>Made for your salon, with your salon name, ready to print or post.</span></div></li>
      <li><i>📱</i><div><b>10 ready-made social media posts</b><span>Announce your new treatment on Instagram, Facebook and WhatsApp Status.</span></div></li>
      <li><i>⭐</i><div><b>Trimion Certified Salon</b><span>Window sticker, plus a feature on our Instagram so clients near you can find you.</span></div></li>
    </ul>
    <a class="btn wa" href="{WA_KIT}" target="_blank" rel="noopener">Claim my starter kit on WhatsApp</a>
    <a class="btn shop" href="/">Browse machines</a>
  </div>
</section>
<section id="refer">
  <span class="tag">No limit</span>
  <h2>Refer a salon, earn {REF_PAY}</h2>
  <div class="card">
    <p>Know a salon owner who needs a machine? Send them our way.</p>
    <ol>
      <li>Your friend tells us your name before she orders.</li>
      <li>She buys any machine from {REF_MIN}.</li>
      <li>Once her machine is paid in full and delivered, we pay you {REF_PAY} by EFT within 7 days.</li>
    </ol>
    <a class="btn wa" href="{WA_REF}" target="_blank" rel="noopener">Refer a salon on WhatsApp</a>
  </div>
</section>
<section>
  <h2>Terms</h2>
  <ul class="terms">
    <li>Starter kit: one kit per machine priced from {KIT_MIN}, including lay-by orders and orders using code TRIMION10. The kit is sent when the machine is paid in full.</li>
    <li>Referral reward: paid once per referred salon, for machines priced from {REF_MIN}. The referred salon must name you before placing the order. Not paid if the order is cancelled or refunded.</li>
    <li>You can't refer yourself or your own salon.</li>
    <li>Diwali Special: orders confirmed by 15 November 2026. The R5,000 lay-by deposit applies to machines priced up to R60,000; the balance is paid over 2 or 3 months as usual.</li>
    <li>Valid until {END}. Trimion Africa Precision (Pty) Ltd may change or end these offers at any time; offers already confirmed on your invoice are honoured.</li>
  </ul>
</section>
</main>
</body>
</html>
"""
os.makedirs(OUT, exist_ok=True)
import shutil; shutil.copy(os.path.join(HERE, "offers_kit.jpg"), os.path.join(OUT, "kit.jpg"))
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("offers page: /offers/")
