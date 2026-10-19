// Renders cover photos and the new-number announcement.
const {chromium}=require('playwright');const out=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1920}});
 await p.goto('file://'+__dirname+'/postt/cover.html');
 for(const k of ['fbcover','wacover','annstory','annfeed','profile']){const [w,h]=await p.evaluate(k=>window.render(k),k);
  await p.setViewportSize({width:w,height:h});await p.screenshot({path:`${out}/${k}.png`});}
 await b.close()})();
