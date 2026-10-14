const {chromium}=require('playwright');const fs=require('fs');
const P=JSON.parse(fs.readFileSync('/home/claude/trimion-site/tools/products.json'));
const only=process.argv[2]?process.argv[2].split(',').map(Number):null;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file:///home/claude/trimion-site/tools/ogt/t.html');
for(const d of P){if(only&&!only.includes(d.k))continue;
 const cons=d.sid==='supplies';
 d.chips=cons?[{t:'R150 delivery'},{t:'Order on WhatsApp'}]:[{t:(d.k===1?'✓ 2-year warranty':'✓ 1-year warranty'),w:true},{t:'R150 delivery'},{t:'Free online training'}];
 await p.evaluate(d=>window.render(d),d);
 await p.screenshot({path:`/home/claude/trimion-site/tools/og-full/m${d.k}.jpg`,type:'jpeg',quality:84});}
await b.close()})();
