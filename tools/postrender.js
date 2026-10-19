// Renders social post pictures: story 1080x1920, feed 1080x1350, square 1080x1080.
const {chromium}=require('playwright');const fs=require('fs');
const P=JSON.parse(fs.readFileSync(__dirname+'/postt/posts.json'));
const out=process.argv[2]; const only=process.argv[3]?process.argv[3].split(','):null;
const S={story:[1080,1920],feed:[1080,1350],square:[1080,1080]};
(async()=>{const b=await chromium.launch();
 for(const [sz,[w,h]] of Object.entries(S)){fs.mkdirSync(`${out}/${sz}`,{recursive:true});
  const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+__dirname+'/postt/t.html');
  for(const d of P){if(only&&!only.includes(d.code))continue;
   await p.evaluate(([d,sz])=>window.render(d,sz),[d,sz]);
   await p.screenshot({path:`${out}/${sz}/${d.file}.png`});}
  await p.close();}
 await b.close()})();
