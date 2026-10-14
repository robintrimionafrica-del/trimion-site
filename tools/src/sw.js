// Trimion Africa Shop service worker: makes the shop installable and opens it even with weak signal.
// Pages: always tries the internet first, so a new deploy shows straight away.
// Photos in /img/: named by their content, so once saved on the phone they never need downloading again.
var C='trimion-shop-v4',IMG='trimion-img-v1';
self.addEventListener('install',function(e){self.skipWaiting()});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==C&&n!==IMG}).map(function(n){return caches.delete(n)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener('fetch',function(e){var r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
 if(u.pathname.indexOf('/img/')===0){
  e.respondWith(caches.open(IMG).then(function(x){return x.match(r).then(function(m){return m||fetch(r).then(function(res){if(res.ok)x.put(r,res.clone());return res})})}));
  return}
 e.respondWith(fetch(r).then(function(res){if(res.ok&&r.mode==='navigate'){var c=res.clone();caches.open(C).then(function(x){x.put('/',c)})}return res})
 .catch(function(){return caches.match(r.mode==='navigate'?'/':r).then(function(m){return m||Response.error()})}))});
