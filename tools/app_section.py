#!/usr/bin/env python3
"""'Get the Trimion app' card on the home page, just above the footer.
The app is the website installed to the home screen (manifest.json + sw.js): free, under 1 MB, Android and iPhone.
The button opens the site's own install flow (the #fia link), which shows the right steps for each phone.
Runs in rebuild.sh after flash.py and before meta_pixel.py."""
import os, re

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
MARK = "<!--ta-app-->"

BOX = MARK + """<style>
.taapp{max-width:560px;margin:24px 16px;padding:18px;border-radius:18px;background:linear-gradient(135deg,#081a3d,#0c2f6b);color:#fff;font-family:inherit}
@media (min-width:592px){.taapp{margin:24px auto}}
.taapp-h{display:flex;gap:14px;align-items:center}
.taapp-h img{width:64px;height:64px;border-radius:16px;box-shadow:0 4px 14px rgba(0,0,0,.35)}
.taapp-h b{display:block;font-size:18px;line-height:1.2}
.taapp-h span{display:block;font-size:13px;opacity:.8;margin-top:2px}
.taapp-st{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 0;padding:0;list-style:none}
.taapp-st li{font-size:12px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:99px;padding:4px 10px}
.taapp-sh{display:flex;gap:8px;margin:14px 0 0;overflow-x:auto}
.taapp-sh img{width:30%;min-width:96px;border-radius:12px;border:1px solid rgba(255,255,255,.2)}
.taapp-b{display:block;width:100%;margin-top:14px;padding:14px;border:0;border-radius:12px;background:#25d366;color:#05301a;font:inherit;font-weight:800;font-size:16px;cursor:pointer}
.taapp-n{margin:8px 0 0;font-size:12px;opacity:.75;text-align:center}
</style>
<section class="taapp" id="getapp" aria-labelledby="taapph">
 <div class="taapp-h"><img src="/icon-192.png" alt="Trimion app icon" width="64" height="64" loading="lazy">
  <div><b id="taapph">Get the Trimion app</b><span>Trimion Africa Precision · Shopping</span></div></div>
 <ul class="taapp-st"><li>Free</li><li>Under 1 MB</li><li>Android &amp; iPhone</li><li>Daily flash deals</li></ul>
 <div class="taapp-sh"><img src="/app/shot1.webp" alt="Shop screen" loading="lazy" width="108" height="192"><img src="/app/shot2.webp" alt="Flash deal screen" loading="lazy" width="108" height="192"><img src="/app/shot3.webp" alt="Specials sign-up screen" loading="lazy" width="108" height="192"></div>
 <button type="button" class="taapp-b" id="taappb">📲 Install the app</button>
 <p class="taapp-n">Installs straight from our website in seconds. No app store needed.</p>
</section>
<script>(function(){var b=document.getElementById('taappb'),s=document.getElementById('getapp');if(!b)return;
if(window.matchMedia('(display-mode: standalone)').matches||navigator.standalone){s.hidden=true;return}
b.addEventListener('click',function(){var l=document.getElementById('fia');if(l)l.click()});})();</script>""" + MARK

p = os.path.join(PUB, "index.html")
s = open(p, encoding="utf-8").read()
s = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK), "", s, flags=re.S)
anchor = '<div class="foot">'
if anchor in s:
    s = s.replace(anchor, BOX + anchor, 1); print("app card added to home page")
else:
    print("  ! footer anchor not found; app card not added")
open(p, "w", encoding="utf-8").write(s)
