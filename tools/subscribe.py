#!/usr/bin/env python3
"""Email sign-up for specials.
- /subscribe/ : a page you can share on WhatsApp ("subscribe to our specials").
- A small sign-up box on the home page (above Questions and answers) and on /offers.
Sign-ups are saved by worker/index.js (POST /api/subscribe) and listed on the private /subscribers page.
Each sign-up is also emailed to the Trimion Gmail inbox via FormSubmit once that form is activated.
Runs in rebuild.sh after offers.py and before meta_pixel.py."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "public")
INBOX = "robin.trimionafrica@gmail.com"
ENDPOINT = f"https://formsubmit.co/ajax/{INBOX}"
MARK = "<!--ta-subscribe-->"

# Shared form markup + script. Field ids are prefixed so they never clash with the shop's own ids.
FORM = """<form class="tasub-f" novalidate>
  <input type="text" name="_honey" class="tasub-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label class="tasub-l">Your name<input name="name" type="text" autocomplete="name" required></label>
  <label class="tasub-l">Email address<input name="email" type="email" inputmode="email" autocomplete="email" required></label>
  <label class="tasub-l">WhatsApp number <span>(optional)</span><input name="whatsapp" type="tel" inputmode="tel" autocomplete="tel"></label>
  <button type="submit" class="tasub-b">Subscribe to specials</button>
  <p class="tasub-m" role="status" aria-live="polite"></p>
  <p class="tasub-s">About 2 emails a month: new machines, flash deals and lay-by specials. Unsubscribe any time by replying STOP.</p>
</form>"""

JS = """<script>(function(){
var EP=%r;
document.querySelectorAll('.tasub-f').forEach(function(f){
  if(f.dataset.on)return;f.dataset.on=1;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var m=f.querySelector('.tasub-m'),b=f.querySelector('.tasub-b'),d=new FormData(f);
    var n=(d.get('name')||'').trim(),em=(d.get('email')||'').trim();
    if(d.get('_honey'))return;
    if(!n){m.textContent='Please add your name.';m.className='tasub-m err';return}
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em)){m.textContent='Please check your email address.';m.className='tasub-m err';return}
    b.disabled=true;b.textContent='Sending...';m.textContent='';m.className='tasub-m';
    var body={name:n,email:em,whatsapp:(d.get('whatsapp')||'').trim(),page:location.pathname};
    fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
    .then(function(r){return r.json().catch(function(){return{}}).then(function(j){if(!r.ok||!j.success)throw 0})})
    .then(function(){try{fetch(EP,{method:'POST',keepalive:true,headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify(Object.assign({_subject:'New specials subscriber: '+n,_template:'table',_captcha:'false'},body))}).catch(function(){})}catch(x){}})
    .then(function(){
      f.innerHTML='<p class="tasub-ok"><b>You are subscribed, '+n.replace(/[<>&"]/g,'')+'!</b><br>Watch your inbox for our next specials. Questions? WhatsApp us on <a href="https://wa.me/27644548506">064 454 8506</a>.</p>';
      try{if(window.fbq)fbq('track','CompleteRegistration',{content_name:'Specials email list'})}catch(x){}
    })
    .catch(function(){b.disabled=false;b.textContent='Subscribe to specials';
      m.innerHTML='Could not send right now. Please try again, or WhatsApp us on <a href="https://wa.me/27644548506">064 454 8506</a>.';m.className='tasub-m err'});
  });
});})();</script>""" % ENDPOINT

# Styles for the box inside existing pages: uses its own colours so it looks the same everywhere.
CSS = """<style>
.tasub{--tsbg:#ffffff;--tsfg:#0d1830;--tsmu:#55627d;--tsln:#d9dfeb;--tsin:#f6f8fc;--tsac:#128c4a;
  max-width:560px;margin:28px 16px;padding:20px;border:1px solid var(--tsln);border-radius:16px;background:var(--tsbg);color:var(--tsfg);font-family:inherit}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tasub{--tsbg:#121c33;--tsfg:#e8edf7;--tsmu:#9aa7c2;--tsln:#26324d;--tsin:#0a1122;--tsac:#2fbf6e}}
:root[data-theme="dark"] .tasub{--tsbg:#121c33;--tsfg:#e8edf7;--tsmu:#9aa7c2;--tsln:#26324d;--tsin:#0a1122;--tsac:#2fbf6e}
@media (min-width:592px){.tasub{margin:28px auto}}
.tasub h2{margin:0 0 4px;font-size:1.2rem;line-height:1.3}
.tasub>p{margin:0 0 14px;color:var(--tsmu)}
.tasub-l{display:block;font-size:14px;font-weight:600;margin:0 0 10px}
.tasub-l span{font-weight:400;color:var(--tsmu)}
.tasub-l input{display:block;width:100%;box-sizing:border-box;margin-top:4px;padding:12px;font:inherit;font-size:16px;color:var(--tsfg);
  background:var(--tsin);border:1px solid var(--tsln);border-radius:10px}
.tasub-l input:focus{outline:2px solid var(--tsac);outline-offset:1px}
.tasub-b{display:block;width:100%;margin-top:4px;padding:14px;border:0;border-radius:12px;background:var(--tsac);color:#fff;font:inherit;font-weight:700;font-size:16px;cursor:pointer}
.tasub-b:disabled{opacity:.7}
.tasub-m{min-height:1em;margin:8px 0 0;font-size:14px}
.tasub-m.err{color:#c0392b}
.tasub-s{margin:6px 0 0;font-size:12px;color:var(--tsmu)}
.tasub-ok{margin:0;font-size:15px}
.tasub a{color:var(--tsac)}
.tasub-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}
</style>"""

BOX = f"""{MARK}{CSS}<section class="tasub" id="subscribe" aria-labelledby="tasubh">
<h2 id="tasubh">Get our specials by email</h2>
<p>Be first to hear about new machines, flash deals and lay-by specials.</p>
{FORM}
</section>{JS}{MARK}"""

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Subscribe to Specials</title>
<meta name="description" content="Subscribe to Trimion Africa specials: new salon machines, flash deals and lay-by offers by email.">
<meta property="og:title" content="Get Trimion Africa specials by email">
<meta property="og:description" content="New salon and spa machines, flash deals and lay-by specials. Free to join, unsubscribe any time.">
<meta property="og:image" content="https://trimionafrica.co.za/og.jpg">
<meta property="og:url" content="https://trimionafrica.co.za/subscribe/">
<link rel="canonical" href="https://trimionafrica.co.za/subscribe/">
<link rel="icon" href="/icon-192.png">
<meta name="theme-color" content="#081a3d">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Figtree:wght@400;500;600;700&display=swap">
<style>
:root{{--bg:#f3f5fa;--fg:#0d1830;--muted:#55627d;--navy:#081a3d;--gold:#ffd23f;--display:"Sora",system-ui,sans-serif;--body:"Figtree",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1122;--fg:#e8edf7;--muted:#9aa7c2;--navy:#0c2350;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0a1122;--fg:#e8edf7;--muted:#9aa7c2;--navy:#0c2350;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
header{{background:var(--navy);color:#fff}}
.wrap{{max-width:560px;margin:0 auto;padding:0 16px}}
header .wrap{{padding-top:32px;padding-bottom:30px}}
.eyebrow{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin:0 0 8px}}
h1{{font:700 2rem/1.15 var(--display);margin:0 0 10px;text-wrap:balance}}
header p{{margin:0;opacity:.85}}
.perks{{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:16px 0 0}}
.perks li{{font-size:13px;border:1px solid rgba(255,255,255,.3);border-radius:99px;padding:4px 10px}}
main .tasub{{margin:-20px 16px 0;position:relative;box-shadow:0 6px 24px rgba(8,26,61,.10)}}
@media (min-width:592px){{main .tasub{{margin:-20px auto 0}}}}
.more{{text-align:center;margin:22px 0 40px;font-size:15px}}
.more a{{color:inherit;font-weight:600}}
</style>
{CSS}
</head>
<body>
<header><div class="wrap">
  <p class="eyebrow">Trimion Africa · Salon equipment, Durban</p>
  <h1>Get our specials first</h1>
  <p>Join our email list for new machines, flash deals and lay-by specials.</p>
  <ul class="perks"><li>Free to join</li><li>About 2 emails a month</li><li>Unsubscribe any time</li></ul>
</div></header>
<main>
<section class="tasub" id="subscribe" aria-label="Subscribe to specials">
{FORM}
</section>
<p class="more"><a href="/offers/">See today's offers</a> · <a href="/">Browse all machines</a></p>
</main>
{JS}
</body>
</html>
"""

os.makedirs(os.path.join(PUB, "subscribe"), exist_ok=True)
open(os.path.join(PUB, "subscribe", "index.html"), "w", encoding="utf-8").write(PAGE)

def inject(path, anchor_re, before=True):
    s = open(path, encoding="utf-8").read()
    s = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK), "", s, flags=re.S)  # replace an older copy
    m = re.search(anchor_re, s)
    if not m:
        print("  ! anchor not found in", os.path.relpath(path, PUB)); return
    i = m.start() if before else m.end()
    s = s[:i] + BOX + s[i:]
    open(path, "w", encoding="utf-8").write(s)
    print("  sign-up box added to", os.path.relpath(path, PUB))

print("subscribe page: /subscribe/ ->", INBOX)
inject(os.path.join(PUB, "index.html"), r'<div class="faq" id="faq">')
inject(os.path.join(PUB, "offers", "index.html"), r"</main>")
