
// Share sheet: send a machine with its picture, or as a link that shows the picture as a preview.
(function(){var S=document.getElementById('shs');if(!S)return;
var BASE='https://trimionafrica.co.za',cur=null,file=null,last=null,box=function(id){return document.getElementById(id)};
var lg=document.querySelector('.logo');if(lg)box('shi').src=lg.src;
var canFiles=false,canPdf=false,pdfFile=null;try{canPdf=!!(navigator.canShare&&window.File&&navigator.canShare({files:[new File(['x'],'t.pdf',{type:'application/pdf'})]}))}catch(e){}
try{canFiles=!!(navigator.canShare&&window.File&&navigator.canShare({files:[new File(['x'],'t.jpg',{type:'image/jpeg'})]}))}catch(e){}
function info(c){var pr=((c.querySelector('.price')||{}).textContent||'').trim(),lb=c.querySelector('.lb'),cons=!!c.closest('#supplies'),
 w=((c.querySelector('.wty')||{}).textContent||'✓ 1-year warranty').split('·')[0].replace('✓','').trim(),
 del=window.TA_PROMO?'FREE delivery this week':'R150 delivery',u=BASE+'/p/'+c.id,
 t='*'+c.dataset.n+'* ('+c.dataset.m+')\n'+pr+(lb?' · '+lb.textContent.replace(/\s+/g,' ').trim():'')+'\n'+(cons?del+' anywhere in SA':w+' · '+del+' · Free online training')+'\nTrimion Africa · WhatsApp 064 454 8506';
 var md=(c.dataset.m||c.id).trim();return {pdf:'/pdf/'+encodeURIComponent(md)+'.pdf',pfn:'Trimion-Africa-'+md.replace(/[^A-Za-z0-9]+/g,'-')+'.pdf',u:u,t:t,title:c.dataset.n+' | Trimion Africa',img:'/og/'+c.id+'.jpg?v=3',fn:'trimion-'+(c.dataset.m||c.id).toLowerCase().replace(/[^a-z0-9]+/g,'-')+'.jpg'}}
function loadPdf(c){var i=info(c);pdfFile=null;if(!canPdf||!window.fetch)return;
 fetch(i.pdf).then(function(r){return r.ok?r.blob():null}).then(function(b){if(b&&cur===c)pdfFile=new File([b],i.pfn,{type:'application/pdf'})}).catch(function(){})}
function load(c){var i=info(c);file=null;if(!canFiles||!window.fetch)return;
 fetch(i.img).then(function(r){return r.ok?r.blob():null}).then(function(b){if(b&&cur===c)file=new File([b],i.fn,{type:'image/jpeg'})}).catch(function(){})}
function toast(m){if(window.TA_toast)window.TA_toast(m,false)}
window.TA_share=function(c){cur=c;last=document.activeElement;var i=info(c);
 box('shn').textContent=c.dataset.n;box('shp').src=i.img;box('shd').href=i.img;box('shd').setAttribute('download',i.fn);box('shpf').href=i.pdf;box('shpf').setAttribute('download',i.pfn);loadPdf(c);
 box('shf').hidden=!canFiles;box('sho').hidden=!navigator.share;
 load(c);S.hidden=false;box(canFiles?'shf':'shw').focus()};
function close(){S.hidden=true;if(last&&last.focus)try{last.focus()}catch(e){}}
box('shf').addEventListener('click',function(){if(!cur)return;var i=info(cur);
 if(file&&navigator.canShare({files:[file]})){navigator.share({files:[file],title:i.title,text:i.t+'\n'+i.u}).then(close).catch(function(e){if(e&&e.name!=='AbortError')toast('Could not attach the picture. Try "Send on WhatsApp".')});return}
 toast('Getting the picture ready… tap again in a second');load(cur)});
box('shw').addEventListener('click',function(){if(!cur)return;var i=info(cur);window.open('https://wa.me/?text='+encodeURIComponent(i.t+'\n'+i.u+'\nBrochure (PDF): '+BASE+i.pdf),'_blank','noopener');close()});
box('shb').addEventListener('click',function(){if(!cur)return;var i=info(cur);
 if(pdfFile&&navigator.canShare({files:[pdfFile]})){navigator.share({files:[pdfFile],title:i.title,text:i.t+'\n'+i.u}).then(close).catch(function(e){if(e&&e.name!=='AbortError')toast('Could not attach the PDF. Sending the link instead.')});return}
 if(canPdf&&!pdfFile){toast('Getting the PDF ready… tap again in a second');loadPdf(cur);return}
 window.open('https://wa.me/?text='+encodeURIComponent('Brochure (PDF): '+BASE+i.pdf+'\n\n'+i.t+'\n'+i.u),'_blank','noopener');close()});
box('sho').addEventListener('click',function(){if(!cur)return;var i=info(cur);navigator.share({title:i.title,text:i.t,url:i.u}).then(close).catch(function(){})});
box('shc').addEventListener('click',function(){if(!cur)return;var i=info(cur),done=function(){toast('Link copied. Paste it in any chat to show the picture.')};
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(i.u).then(done).catch(function(){prompt('Copy this link:',i.u)});else prompt('Copy this link:',i.u)});
box('shx').addEventListener('click',close);
S.addEventListener('click',function(e){if(e.target===S)close()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!S.hidden)close()});
})();
