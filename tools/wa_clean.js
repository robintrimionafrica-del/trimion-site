// WhatsApp links: strip emoji (some phones show them as boxes) and, on Android, open the WhatsApp app
// directly instead of going through wa.me web redirects. If WhatsApp is not installed, Chrome falls back to wa.me.
(function(){
var android=/Android/i.test(navigator.userAgent);
function clean(t){return String(t).replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{2300}-\u{23FF}\u{FE0F}\u{200D}\u{20E3}]/gu,'').replace(/[ \t]{2,}/g,' ').replace(/^[ \t]+/gm,'').replace(/ ·\s*$/gm,'')}
function isWa(u){return /^https:\/\/(wa\.me|api\.whatsapp\.com)\//.test(u)}
function fix(u){try{if(!isWa(u))return u;var i=u.indexOf('text=');if(i<0)return u;var a=u.slice(0,i+5),r=u.slice(i+5),j=r.indexOf('&'),q=j<0?r:r.slice(0,j),rest=j<0?'':r.slice(j);
 return a+encodeURIComponent(clean(decodeURIComponent(q)))+rest}catch(e){return u}}
function intent(u){try{var m=u.match(/^https:\/\/wa\.me\/(\d*)\/?\?text=([^&]*)/);if(!m)return null;
 return 'intent://send/?'+(m[1]?'phone='+m[1]+'&':'')+'text='+m[2]+'#Intent;scheme=whatsapp;S.browser_fallback_url='+encodeURIComponent(u)+';end'}catch(e){return null}}
function go(u){var f=fix(u),it=android?intent(f):null;if(it){location.href=it;return true}return false}
window.TA_waClean=fix;
var o=window.open;window.open=function(u){if(typeof u==='string'&&isWa(u)){if(go(u))return null;arguments[0]=fix(u)}return o.apply(window,arguments)};
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="wa.me"],a[href*="api.whatsapp.com"]');if(!a||e.defaultPrevented)return;
 if(go(a.href)){e.preventDefault();return}a.href=fix(a.href)});
})();
