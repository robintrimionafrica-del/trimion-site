// Builds ../public/vs.json: one visual fingerprint per machine photo, made with vs_core.js
// in headless Chromium so it matches what visitors' phones compute.
// Usage: node vs_build.js            (writes ../public/vs.json)
//        node vs_build.js test a.jpg b.jpg …   (prints the top matches for each test photo)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const T = __dirname, PUB = path.join(T, '..', 'public');
const P = JSON.parse(fs.readFileSync(path.join(T, 'products.json'))), PR = JSON.parse(fs.readFileSync(path.join(T, 'prices.json')));
const mime = f => f.endsWith('.webp') ? 'image/webp' : f.endsWith('.png') ? 'image/png' : 'image/jpeg';
const durl = f => 'data:' + mime(f) + ';base64,' + fs.readFileSync(f).toString('base64');

(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.setContent('<html><body></body></html>'); await pg.addScriptTag({ path: path.join(T, 'vs_core.js') });
  const fp = u => pg.evaluate(u => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(TAVS.pack(TAVS.features(i))); i.onerror = no; i.src = u }), u);
  const items = [];
  for (const p of P) {
    const price = PR[String(p.k)];
    items.push({ k: p.k, n: p.name, m: p.model, p: price ? 'R' + price.toLocaleString('en-US') : '', i: p.img, f: await fp(durl(path.join(PUB, p.img))) });
  }
  if (process.argv[2] === 'test') {
    for (const f of process.argv.slice(3)) {
      const q = await fp(durl(f));
      const top = await pg.evaluate(([q, items]) => { const a = TAVS.unpack(q); return items.map(x => [TAVS.score(a, TAVS.unpack(x.f)), x.k, x.m]).sort((p, q) => q[0] - p[0]).slice(0, 6) }, [q, items]);
      console.log(path.basename(f), top.map(t => t[2] + ' ' + t[0].toFixed(3)).join(' | '));
    }
  } else {
    fs.writeFileSync(path.join(PUB, 'vs.json'), JSON.stringify(items));
    console.log('vs.json:', items.length, 'machines,', fs.statSync(path.join(PUB, 'vs.json')).size, 'bytes');
  }
  await b.close();
})();
