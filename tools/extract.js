const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
await p.goto('http://localhost:8766/',{waitUntil:'networkidle'});await p.waitForTimeout(800);
const n=await p.evaluate(()=>document.querySelectorAll('.card').length);const out=[];
for(let k=1;k<=n;k++){await p.evaluate(k=>{location.hash='m'+k},k);await p.waitForTimeout(60);
 out.push(await p.evaluate(k=>{const B=document.getElementById('mpb');const q=s=>B.querySelector(s);
  const mls=[...B.querySelectorAll('.mi .ml')].map(x=>x.textContent).filter(Boolean);
  const specs=[];B.querySelectorAll('.mx').forEach(mx=>{const h=mx.querySelector('h4');if(h&&/Spec/i.test(h.textContent))mx.querySelectorAll('li').forEach(li=>specs.push(li.textContent))});
  const get=[];B.querySelectorAll('.mx').forEach(mx=>{const h=mx.querySelector('h4');if(h&&/What you get/i.test(h.textContent))mx.querySelectorAll('li').forEach(li=>get.push(li.textContent))});
  const c=document.getElementById('m'+k);const lb=c.querySelector('.lb');
  return {k,name:q('#mpt').textContent,model:q('.mm').textContent.replace('Model ',''),cat:q('.mc').textContent,price:q('.mpr').textContent,desc:mls,specs,get,lb:lb?lb.textContent.trim():'',img:c.querySelector('.photo img').getAttribute('src'),wb:(q('.mwb b')||{}).textContent||''}},k));
 await p.evaluate(()=>{location.hash=''});}
fs.writeFileSync('/home/claude/trimion-site/tools/details.json',JSON.stringify(out,null,1));
console.log(out.length, JSON.stringify(out[2]).slice(0,900));console.log(out.filter(o=>!o.specs.length).length,'without specs');await b.close()})();
