#!/usr/bin/env python3
"""Promo-code page at /promo: code TRIMION10 = 10% off any machine, claimed on WhatsApp.
Used for the Meta email sign-up offer (Commerce Manager > Settings > Marketing) and for sharing."""
import os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "promo")
CODE, PCT = "TRIMION10", 10
WA = "https://wa.me/27611185978?text=" + urllib.parse.quote(
    f"Hi Trimion, I'd like to use code {CODE} ({PCT}% off). The machine I want is: ")

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{PCT}% Off Code</title>
<meta name="description" content="Use code {CODE} for {PCT}% off any Trimion Africa salon machine. Lay-by, 1-year warranty, R150 delivery nationwide.">
<meta property="og:title" content="{PCT}% off any Trimion machine · code {CODE}">
<meta property="og:description" content="Salon and spa machines with lay-by, 1-year warranty and R150 delivery anywhere in South Africa.">
<meta property="og:image" content="https://trimionafrica.co.za/og.jpg">
<meta property="og:url" content="https://trimionafrica.co.za/promo/">
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
.wrap{{max-width:560px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left,0px)) 40px}}
header{{background:var(--navy);color:#fff}}
header .wrap{{padding-top:32px;padding-bottom:30px}}
.eyebrow{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin:0 0 8px}}
h1{{font:700 2rem/1.15 var(--display);margin:0 0 10px;text-wrap:balance}}
header p{{margin:0;opacity:.85}}
.code{{margin-top:22px;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.08);border:2px dashed var(--gold);border-radius:14px;padding:12px 12px 12px 16px}}
.code strong{{flex:1;font:700 1.6rem/1 var(--display);letter-spacing:.06em;color:var(--gold)}}
.code button{{background:var(--gold);color:#3a2a00;border:0;border-radius:10px;font:600 15px var(--body);padding:10px 14px;cursor:pointer}}
section{{margin-top:26px}}
h2{{font:600 1.15rem/1.3 var(--display);margin:0 0 10px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
ol{{margin:0;padding-left:20px}} ol li{{margin:6px 0}}
.btn{{display:block;text-align:center;text-decoration:none;font-weight:600;border-radius:12px;padding:14px 16px;margin-top:12px}}
.wa{{background:var(--wa);color:#fff}}
.shop{{border:1px solid var(--line);color:var(--fg);background:var(--card)}}
.perks{{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:16px 0 0}}
.perks li{{font-size:13px;border:1px solid rgba(255,255,255,.3);border-radius:99px;padding:4px 10px}}
.terms{{font-size:13px;color:var(--muted)}} .terms li{{margin:4px 0}}
</style>
</head>
<body>
<header><div class="wrap">
  <p class="eyebrow">Trimion Africa · Salon equipment, Durban</p>
  <h1>{PCT}% off any machine</h1>
  <p>Use this code when you order on WhatsApp.</p>
  <div class="code"><strong id="c">{CODE}</strong><button id="cp" type="button">Copy</button></div>
  <ul class="perks"><li>1-year warranty</li><li>R150 delivery nationwide</li><li>Free online training</li><li>Lay-by available</li></ul>
</div></header>
<main class="wrap">
<section>
  <h2>How to use it</h2>
  <div class="card">
    <ol>
      <li>Pick your machine on our website.</li>
      <li>Send us a WhatsApp with the machine name and code <b>{CODE}</b>.</li>
      <li>We send your discounted price, then you pay in full or start a lay-by.</li>
    </ol>
    <a class="btn wa" href="{WA}" target="_blank" rel="noopener">Claim {PCT}% on WhatsApp</a>
    <a class="btn shop" href="/">Browse all machines</a>
  </div>
</section>
<section>
  <h2>Terms</h2>
  <ul class="terms">
    <li>{PCT}% off the listed price of one machine. Delivery is charged as normal.</li>
    <li>One use per customer. Use it within 7 days of receiving the code.</li>
    <li>Can't be combined with other offers or flash deals.</li>
    <li>Works with lay-by: we take {PCT}% off the total before working out your payments.</li>
    <li>Trimion Africa Precision (Pty) Ltd may end this offer at any time.</li>
  </ul>
</section>
</main>
<script>
document.getElementById('cp').addEventListener('click',function(){{
  var b=this,t='{CODE}';
  function done(){{b.textContent='Copied';setTimeout(function(){{b.textContent='Copy'}},1800)}}
  try{{navigator.clipboard.writeText(t).then(done,done)}}catch(e){{done()}}
}});
</script>
</body>
</html>
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("promo page: /promo/ code", CODE)
