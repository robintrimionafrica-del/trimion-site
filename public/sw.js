// Trimion Africa Shop service worker: makes the shop installable and opens it fast, even with weak signal.
// Home page: uses the internet if it answers within 0.8 seconds; otherwise opens the saved copy at once
// and quietly saves the newest version for next time. Only the real home page is ever saved as "/".
// Photos in /img/: named by their content, so once saved on the phone they never need downloading again.
var C='trimion-shop-v7',IMG='trimion-img-v1',WAIT=800,PRE=['/img/4880f983c6.png','/img/5d861a4924.webp','/img/9e644e33f3.png','/img/2f329d5478.png'];
self.addEventListener('install',function(e){e.waitUntil(Promise.all([caches.open(C).then(function(x){return fetch('/',{cache:'no-cache'}).then(function(r){if(r.ok)return x.put('/',r)})}),caches.open(IMG).then(function(x){return x.addAll(PRE)})]).catch(function(){}));self.skipWaiting()});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==C&&n!==IMG}).map(function(n){return caches.delete(n)}))}).then(function(){return self.clients.claim()}))});
function home(e){
 var net=fetch(e.request).then(function(res){if(res.ok&&res.type==='basic'){var c=res.clone();caches.open(C).then(function(x){x.put('/',c)})}return res});
 e.waitUntil(net.catch(function(){}));
 return caches.match('/').then(function(saved){
  if(!saved)return net;
  var late=new Promise(function(ok){setTimeout(function(){ok(saved)},WAIT)});
  return Promise.race([net.catch(function(){return saved}),late])})}
self.addEventListener('fetch',function(e){var r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
 if(u.pathname.indexOf('/img/')===0){
  e.respondWith(caches.open(IMG).then(function(x){return x.match(r).then(function(m){return m||fetch(r).then(function(res){if(res.ok)x.put(r,res.clone());return res})})}));
  return}
 if(r.mode==='navigate'&&(u.pathname==='/'||u.pathname==='/index.html')){e.respondWith(home(e));return}
 if(r.mode==='navigate')return;
 e.respondWith(fetch(r).catch(function(){return caches.match(r).then(function(m){return m||Response.error()})}))});
