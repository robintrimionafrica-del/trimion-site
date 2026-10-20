// Home page banner slides (960x960), machines instead of a model, number 064 454 8506.
const {chromium}=require('playwright');const out=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:960,height:960}});
 await p.goto('file://'+__dirname+'/postt/slide.html');
 for(const k of ['ems','diwali','kit','refer','premium','why','own','ask']){await p.evaluate(k=>window.render(k),k);await p.screenshot({path:`${out}/${k}.png`});}
 await b.close()})();
