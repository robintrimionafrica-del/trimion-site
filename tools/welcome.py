#!/usr/bin/env python3
"""Small reminder card on the home page (owner request 24/10/2026), not a blocking pop-up.
- First visit: welcome + save WhatsApp number + install app / email specials.
- Return visit with items in the cart: "Welcome back – you still have N items in your cart".
Shows at most once a day, 4 seconds after load, bottom of screen, closes with ✕ or after 12 s.
Everything is kept on the visitor's own phone (localStorage); nothing is sent anywhere."""
import os
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
MARK = 'id="tawel"'
CSS = ('<style>#tawel{position:fixed;left:12px;right:12px;bottom:78px;z-index:60;max-width:440px;margin:0 auto;background:#0b1f4d;color:#fff;'
       'border-radius:14px;padding:14px 40px 14px 14px;box-shadow:0 8px 30px rgba(0,0,0,.35);font-size:.9rem;line-height:1.4;'
       'transform:translateY(160%);transition:transform .35s ease}#tawel.on{transform:none}#tawel b{color:#f2c14e}'
       '#tawel .tw{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}#tawel .tw a{flex:1;min-width:120px;text-align:center;text-decoration:none;'
       'font-weight:700;font-size:.82rem;border-radius:18px;padding:8px 10px;background:#1fa855;color:#fff}#tawel .tw a.s{background:#fff;color:#0b1f4d}'
       '#tawel button{position:absolute;top:6px;right:8px;background:none;border:0;color:#fff;font-size:1.2rem;cursor:pointer;padding:4px}'
       '@media(prefers-reduced-motion:reduce){#tawel{transition:none}}</style>')
HTML = '<div id="tawel" role="status" aria-live="polite" hidden><button type="button" aria-label="Close">✕</button><div id="tawt"></div><div class="tw" id="tawa"></div></div>'
JS = r"""<script>(function(){var K='ta_welcome',now=Date.now(),s={};try{s=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
if(s.t&&now-s.t<864e5)return;var c=[];try{c=(window.TA_CART&&window.TA_CART.ids())||JSON.parse(localStorage.getItem('ta_cart')||'[]')}catch(e){}
var el=document.getElementById('tawel'),tx=document.getElementById('tawt'),ac=document.getElementById('tawa');if(!el)return;
var wa='https://wa.me/27644548506?text='+encodeURIComponent('Hi Trimion Africa, I would like some advice on salon equipment.');
if(c&&c.length){tx.innerHTML='👋 <b>Welcome back!</b> You still have '+c.length+' item'+(c.length>1?'s':'')+' in your cart.';
 ac.innerHTML='<a href="#" id="tawc">View my cart</a><a class="s" href="'+wa+'" target="_blank" rel="noopener">Ask us on WhatsApp</a>'}
else if(s.v){tx.innerHTML='👋 <b>Welcome back to Trimion Africa.</b> Need advice or a quote? We reply on WhatsApp.';
 ac.innerHTML='<a href="'+wa+'" target="_blank" rel="noopener">WhatsApp 064 454 8506</a><a class="s" href="#subscribe">Email me specials</a>'}
else{tx.innerHTML='👋 <b>Welcome to Trimion Africa Precision.</b> Save our WhatsApp number <b>064 454 8506</b>, or add our app to your home screen.';
 ac.innerHTML='<a href="#getapp">Install Trimion Africa</a><a class="s" href="'+wa+'" target="_blank" rel="noopener">WhatsApp us</a>'}
function hide(){el.classList.remove('on');setTimeout(function(){el.hidden=true},400)}
function busy(){var e=document.elementFromPoint(innerWidth/2,innerHeight/2);if(e&&e.closest('[role=dialog],[aria-modal=true]'))return true;return [].some.call(document.querySelectorAll('[aria-modal=true]'),function(d){return !d.hidden&&d.offsetParent!==null&&getComputedStyle(d).visibility!=='hidden'})}
var tries=0;function show(){if(busy()){if(++tries<30)setTimeout(show,2000);return}
 el.hidden=false;requestAnimationFrame(function(){el.classList.add('on')});
 try{localStorage.setItem(K,JSON.stringify({t:now,v:1}))}catch(e){}setTimeout(hide,12000);var w=setInterval(function(){if(el.hidden){clearInterval(w);return}if(busy()){hide();clearInterval(w)}},500)}
setTimeout(show,10000);
el.querySelector('button').addEventListener('click',hide);ac.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
 if(a.id==='tawc'){e.preventDefault();if(window.TA_openCart)window.TA_openCart()}hide()})})();</script>"""
p = os.path.join(PUB, 'index.html'); s = open(p, encoding='utf-8').read()
if MARK not in s:
    s = s.replace('</head>', CSS + '</head>', 1).replace('</body>', HTML + JS + '</body>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('welcome reminder added')
