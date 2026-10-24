# "Live feed" on the home page: a new machine video appears at 10:00, 12:00, 14:00, 16:00, 18:00 and 19:30
# (South African time) every day, newest first, with the post's music on tap. Writes /live.json and /live.js
# and inserts the section above the "Trending now" row of ../public/index.html. Runs after finalize_meta.py.
import json, os, random, subprocess
T = os.path.dirname(os.path.abspath(__file__)); PUB = f'{T}/../public'
P = json.load(open(f'{T}/postt/posts.json'))
PR = {p['model']: p for p in json.load(open(f'{T}/products.json'))}

def item(code):
    o = next(x for x in P if x['code'] == code); p = PR[code]; f = o['file']
    return dict(k=p['k'], n=p['name'], pr=p['price'], v=f'/social/feed/{f}.mp4', po=f'/social/feed/{f}.jpg', u=f"/p/m{p['k']}")

# Specials (9:16 videos; a 4:5 poster is cut from the middle of the last frame).
SPECIALS = [
    dict(id='Trimion_Diwali_offer', n='Diwali Special: FREE Starter Kit, R5,000 lay-by deposit', until='2026-11-15', u='/promo/'),
    dict(id='Trimion_Offer_kit', n='Buy the machine, get the business: FREE Salon Starter Kit', until='2026-12-31', u='/offers/'),
    dict(id='Trimion_Offer_ref', n='Know a salon? Earn R2,000 for every salon that buys', until='2026-12-31', u='/offers/'),
]
os.makedirs(f'{PUB}/social/poster', exist_ok=True)
for s in SPECIALS:
    out = f"{PUB}/social/poster/{s['id']}.jpg"
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.1', '-i', f"{PUB}/social/{s['id']}.mp4", '-frames:v', '1',
                        '-vf', 'crop=1080:1350:0:285,scale=540:675', '-q:v', '4', out], check=True)
    s.update(v=f"/social/{s['id']}.mp4", po=f"/social/poster/{s['id']}.jpg", sp=1)

# Day 0 (20 Oct 2026) matches the first day of posts on Facebook and Instagram.
first = [item('TAEMC2R'), dict(SPECIALS[0]), item('TAWD8S'), item('TAUS4D'), item('TACRYO360-4'), dict(SPECIALS[1])]
rest = [item(o['code']) for o in P if o['sid'] != 'supplies' and o['code'] not in ('TAEMC2R', 'TAWD8S', 'TAUS4D', 'TACRYO360-4')]
random.Random(20261020).shuffle(rest)
first = [x for x in first if x.get('sp') or not PR.get(next((c for c, q in PR.items() if q['k'] == x.get('k')), ''), {}).get('onreq')]   # on request (hold.py)
rest = [x for x in rest if not PR.get(next((c for c, q in PR.items() if q['k'] == x.get('k')), ''), {}).get('onreq')]
json.dump(dict(start='2026-10-20', slots=['10:00', '12:00', '14:00', '16:00', '18:00', '19:30'], first=first, items=rest,
               specials=SPECIALS, wa='27644548506'), open(f'{PUB}/live.json', 'w'), ensure_ascii=False, separators=(',', ':'))

JS = r"""(function(){
var box=document.getElementById('livefeed');if(!box)return;
var D=null,shown={},timer=null;
function sast(){var n=new Date();return new Date(n.getTime()+n.getTimezoneOffset()*60000+2*3600000)}
function dayNum(d){var s=D.start.split('-');return Math.floor((Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())-Date.UTC(+s[0],s[1]-1,+s[2]))/86400000)}
function ymd(d){return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
function postFor(day,i,date){
 if(day===0)return D.first[i];
 if(i===1&&day>0&&day%2===0){var live=D.specials.filter(function(s){return s.until>=date});if(live.length)return live[(day/2)%live.length]}
 var n=D.items.length;return D.items[(((day-1)*6+i)%n+n)%n]}
function posts(){var now=sast(),out=[];
 for(var back=0;back<3&&out.length<12;back++){var d=new Date(now.getTime()-back*86400000),dn=dayNum(d);
  for(var i=D.slots.length-1;i>=0;i--){var hm=D.slots[i].split(':'),t=new Date(d.getFullYear(),d.getMonth(),d.getDate(),+hm[0],+hm[1]);
   if(t>now)continue;var p=postFor(dn,i,ymd(d));if(p)out.push({p:p,t:t,key:ymd(d)+i})}}
 return out.slice(0,12)}
function next(){var now=sast();for(var i=0;i<D.slots.length;i++){var hm=D.slots[i].split(':');if(+hm[0]*60+ +hm[1]>now.getHours()*60+now.getMinutes())return 'today at '+D.slots[i]}return 'tomorrow at '+D.slots[0]}
function ago(t){var m=Math.round((sast()-t)/60000);if(m<60)return m<2?'Just now':m+' min ago';var h=Math.round(m/60);return h<24?h+'h ago':'Yesterday'}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function card(x,isNew){var p=x.p,live=(sast()-x.t)<7200000;
 var wa='https://wa.me/'+D.wa+'?text='+encodeURIComponent('Hi Trimion, I saw '+p.n+(p.pr?' ('+p.pr+')':'')+' on your live feed.');
 return '<article class="lv'+(isNew?' lvnew':'')+'" data-key="'+x.key+'"><div class="lvm"><video muted loop playsinline preload="none" poster="'+p.po+'" src="'+p.v+'"></video>'+
  '<span class="lvb'+(live?' on':'')+'">'+(live?'● LIVE':esc(ago(x.t)))+'</span><button class="lvs" type="button" aria-label="Sound on">🔇</button></div>'+
  '<a class="lvt" href="'+p.u+'">'+esc(p.n)+'</a>'+(p.pr?'<b class="lvp">'+esc(p.pr)+'</b>':'')+
  '<a class="lvw" href="'+wa+'" target="_blank" rel="noopener">WhatsApp</a></article>'}
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){v.play().catch(function(){})}else v.pause()})},{threshold:.5}):null;
function wire(el){var v=el.querySelector('video');if(io)io.observe(v);else v.setAttribute('controls','');
 el.querySelector('.lvs').addEventListener('click',function(){var on=v.muted;box.querySelectorAll('video').forEach(function(o){o.muted=true});box.querySelectorAll('.lvs').forEach(function(b){b.textContent='🔇'});
  v.muted=!on;this.textContent=on?'🔊':'🔇';if(on)v.play().catch(function(){})})}
function render(first){var ps=posts(),row=box.querySelector('.lvr');document.getElementById('lvnext').textContent='Next machine drops '+next();
 if(first){row.innerHTML=ps.map(function(x){return card(x,false)}).join('');ps.forEach(function(x){shown[x.key]=1});row.querySelectorAll('.lv').forEach(wire);return}
 ps.slice().reverse().forEach(function(x){if(shown[x.key])return;shown[x.key]=1;row.insertAdjacentHTML('afterbegin',card(x,true));wire(row.firstChild);row.scrollTo({left:0,behavior:'smooth'})});
 row.querySelectorAll('.lv').forEach(function(el){var x=ps.filter(function(y){return y.key===el.getAttribute('data-key')})[0];if(!x){el.remove();return}
  var b=el.querySelector('.lvb'),live=(sast()-x.t)<7200000;b.className='lvb'+(live?' on':'');b.textContent=live?'● LIVE':ago(x.t)})}
fetch('/live.json?d='+ymd(sast()),{cache:'no-cache'}).then(function(r){return r.json()}).then(function(j){D=j;render(true);box.hidden=false;timer=setInterval(function(){render(false)},60000)}).catch(function(){});
})();"""
open(f'{PUB}/live.js', 'w').write(JS)

CSS = """<style id="lv-css">#livefeed{margin:18px 0 6px}#livefeed .txh{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
#livefeed h2 .dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#e5243b;margin-right:6px;vertical-align:middle;animation:lvp 1.4s infinite}
@keyframes lvp{0%{box-shadow:0 0 0 0 rgba(229,36,59,.6)}70%{box-shadow:0 0 0 9px rgba(229,36,59,0)}100%{box-shadow:0 0 0 0 rgba(229,36,59,0)}}
#lvnext{font-size:12.5px;opacity:.7;margin:2px 0 10px}.lvr{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:6px;scrollbar-width:none}
.lv{flex:0 0 min(62vw,240px);scroll-snap-align:start;display:flex;flex-direction:column;gap:4px}.lvnew{animation:lvin .6s ease}@keyframes lvin{from{opacity:0;transform:translateX(-20px)}}
.lvm{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:4/5;background:#0a1f4d}.lvm video{width:100%;height:100%;object-fit:cover;display:block}
.lvb{position:absolute;left:8px;top:8px;background:rgba(0,0,0,.6);color:#fff;font:700 11px/1 system-ui,sans-serif;padding:5px 8px;border-radius:6px}.lvb.on{background:#e5243b}
.lvs{position:absolute;right:8px;bottom:8px;border:0;border-radius:50%;width:36px;height:36px;background:rgba(0,0,0,.6);color:#fff;font-size:16px;cursor:pointer}
.lvt{font-weight:600;font-size:13.5px;line-height:1.3;color:inherit;text-decoration:none;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.lvp{font-size:14px}.lvw{align-self:flex-start;background:#128c4a;color:#fff;text-decoration:none;font-weight:600;font-size:12.5px;border-radius:8px;padding:6px 12px}</style>"""
SEC = ('<section class="shs" id="livefeed" aria-label="Live feed" hidden><div class="txh"><h2><span class="dot"></span>Live feed</h2>'
       '<a href="/media/">All videos ›</a></div><p id="lvnext"></p><div class="lvr"></div></section>'
       '<script src="/live.js" defer></script>')
p = f'{PUB}/index.html'; s = open(p).read()
if 'id="livefeed"' not in s:
    anchor = '<section class="shs" aria-label="Trending now">'
    assert anchor in s
    s = s.replace(anchor, SEC + anchor, 1).replace('</head>', CSS + '</head>', 1)
    open(p, 'w').write(s)
print('live feed:', len(rest), 'machines in rotation,', len(SPECIALS), 'specials')
