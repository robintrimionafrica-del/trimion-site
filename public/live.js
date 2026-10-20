(function(){
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
})();