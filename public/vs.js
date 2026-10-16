/* Trimion visual search: turns a photo into a small "fingerprint" (shape, outline and colour)
   so a client's photo can be matched against the catalogue photos. Runs in the browser and at
   build time (tools/vs_build.js runs this same file in headless Chromium), so both sides match. */
(function (root) {
  var N = 64;                 // working size of the cropped machine
  var SG = 12;                // silhouette grid
  var HC = 4, HB = 9;         // outline: 4x4 cells x 9 orientation bins
  var CB = 16;                // colour: 12 hues + 4 greys

  function draw(img, w, h) {
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    var x = c.getContext('2d', { willReadFrequently: true });
    x.fillStyle = '#fff'; x.fillRect(0, 0, w, h);
    var iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    var s = Math.min(w / iw, h / ih), dw = iw * s, dh = ih * s;
    var ox = Math.round((w - dw) / 2), oy = Math.round((h - dh) / 2);
    x.drawImage(img, ox, oy, dw, dh);
    var d = x.getImageData(0, 0, w, h);
    d.r = { x0: ox, y0: oy, x1: Math.min(w - 1, Math.round(ox + dw) - 1), y1: Math.min(h - 1, Math.round(oy + dh) - 1) };
    return d;
  }
  function med(a) { a.sort(function (p, q) { return p - q }); return a[a.length >> 1] }

  // 1. find the machine: everything that differs from the border colour
  function mask(d, w, h) {
    // only the area where the photo was drawn counts; its edges tell us the background colour
    var R = d.r, px = d.data, rs = [], gs = [], bs = [], i, x, y;
    function take(x, y) { i = (y * w + x) * 4; rs.push(px[i]); gs.push(px[i + 1]); bs.push(px[i + 2]) }
    for (x = R.x0; x <= R.x1; x++) { take(x, R.y0); take(x, R.y0 + 1); take(x, R.y1); take(x, R.y1 - 1) }
    for (y = R.y0; y <= R.y1; y++) { take(R.x0, y); take(R.x0 + 1, y); take(R.x1, y); take(R.x1 - 1, y) }
    var br = med(rs.slice()), bg = med(gs.slice()), bb = med(bs.slice()), m = new Uint8Array(w * h), dv = [];
    for (i = 0; i < rs.length; i++) dv.push(Math.abs(rs[i] - br) + Math.abs(gs[i] - bg) + Math.abs(bs[i] - bb));
    var th = Math.max(24, 3 * med(dv) + 12);   // plain backgrounds: low threshold; busy ones: higher
    var x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (y = R.y0 + 2; y <= R.y1 - 2; y++) for (x = R.x0 + 2; x <= R.x1 - 2; x++) {
      i = (y * w + x) * 4;
      var dd = Math.abs(px[i] - br) + Math.abs(px[i + 1] - bg) + Math.abs(px[i + 2] - bb);
      if (dd > th) { m[y * w + x] = 1; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y }
    }
    if (x1 < 0 || (x1 - x0) * (y1 - y0) < w * h * 0.01) { x0 = R.x0; y0 = R.y0; x1 = R.x1; y1 = R.y1; for (y = y0; y <= y1; y++) for (x = x0; x <= x1; x++) m[y * w + x] = 1 }
    return { m: m, x0: x0, y0: y0, x1: x1, y1: y1 };
  }

  function features(img) {
    var W = 192, d = draw(img, W, W), k = mask(d, W, W);
    // crop to the machine, keep its proportions, centre it in an N x N square
    var cw = k.x1 - k.x0 + 1, ch = k.y1 - k.y0 + 1, s = N / Math.max(cw, ch);
    var ox = (N - cw * s) / 2, oy = (N - ch * s) / 2;
    var g = new Float32Array(N * N), fm = new Uint8Array(N * N), col = new Float32Array(CB), px = d.data;
    for (var y = 0; y < N; y++) for (var x = 0; x < N; x++) {
      var sx = Math.floor((x - ox) / s) + k.x0, sy = Math.floor((y - oy) / s) + k.y0;
      if (sx < k.x0 || sx > k.x1 || sy < k.y0 || sy > k.y1) { g[y * N + x] = 1; continue }
      var i = (sy * W + sx) * 4, r = px[i] / 255, gg = px[i + 1] / 255, b = px[i + 2] / 255;
      g[y * N + x] = 0.299 * r + 0.587 * gg + 0.114 * b;
      if (!k.m[sy * W + sx]) { g[y * N + x] = 1; continue }
      fm[y * N + x] = 1;
      var mx = Math.max(r, gg, b), mn = Math.min(r, gg, b), v = mx, sat = mx ? (mx - mn) / mx : 0;
      if (sat < 0.25 || v < 0.2) col[12 + Math.min(3, Math.floor(v * 4))] += 1;
      else {
        var hh = mx === r ? ((gg - b) / (mx - mn)) % 6 : mx === gg ? (b - r) / (mx - mn) + 2 : (r - gg) / (mx - mn) + 4;
        hh = (hh * 60 + 360) % 360; col[Math.floor(hh / 30) % 12] += 1;
      }
    }
    // silhouette
    var sil = new Float32Array(SG * SG), c = N / SG;
    for (y = 0; y < N; y++) for (x = 0; x < N; x++) if (fm[y * N + x]) sil[Math.floor(y / c) * SG + Math.floor(x / c)] += 1;
    // outline (gradient orientation per cell)
    var hog = new Float32Array(HC * HC * HB), cc = N / HC;
    for (y = 1; y < N - 1; y++) for (x = 1; x < N - 1; x++) {
      var gx = g[y * N + x + 1] - g[y * N + x - 1], gy = g[(y + 1) * N + x] - g[(y - 1) * N + x];
      var mag = Math.sqrt(gx * gx + gy * gy); if (mag < 0.02) continue;
      var a = (Math.atan2(gy, gx) + Math.PI) % Math.PI, bin = Math.min(HB - 1, Math.floor(a / Math.PI * HB));
      hog[(Math.floor(y / cc) * HC + Math.floor(x / cc)) * HB + bin] += mag;
    }
    return { sil: norm(sil), hog: norm(hog), col: norm(col) };
  }
  function norm(v) { var s = 0, i; for (i = 0; i < v.length; i++) s += v[i] * v[i]; s = Math.sqrt(s) || 1; for (i = 0; i < v.length; i++) v[i] /= s; return v }
  function pack(f) {   // 0..1 floats -> one 0..255 byte each -> base64
    var a = [].concat([].slice.call(f.sil), [].slice.call(f.hog), [].slice.call(f.col)), b = '';
    for (var i = 0; i < a.length; i++) b += String.fromCharCode(Math.max(0, Math.min(255, Math.round(a[i] * 255))));
    return btoa(b);
  }
  function unpack(s) {
    var b = atob(s), a = new Float32Array(b.length); for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i) / 255;
    var n1 = SG * SG, n2 = n1 + HC * HC * HB;
    return { sil: norm(a.slice(0, n1)), hog: norm(a.slice(n1, n2)), col: norm(a.slice(n2)) };
  }
  function dot(p, q) { var s = 0; for (var i = 0; i < p.length; i++) s += p[i] * q[i]; return s }
  function score(a, b) { return 0.45 * dot(a.hog, b.hog) + 0.35 * dot(a.sil, b.sil) + 0.20 * dot(a.col, b.col) }
  root.TAVS = { features: features, pack: pack, unpack: unpack, score: score };
})(this);

/* Search by photo: camera button in the search bar -> pick or take a photo -> box the machine ->
   closest machines from the catalogue. Uses vs_core.js (bundled before this file) and /vs.json. */
(function () {
  var btn = document.getElementById('vsb'), fi = document.getElementById('vsf');
  if (!btn || !fi || !window.TAVS) return;
  var DATA = null, img = null, box = null;
  function load() {
    if (DATA) return Promise.resolve(DATA);
    return fetch('/vs.json').then(function (r) { return r.json() }).then(function (a) {
      DATA = a.map(function (x) { x.v = TAVS.unpack(x.f); return x }); return DATA;
    });
  }
  var P = document.createElement('div'); P.id = 'vsp'; P.setAttribute('role', 'dialog'); P.setAttribute('aria-modal', 'true'); P.setAttribute('aria-labelledby', 'vst');
  P.innerHTML = '<div class="ah"><button type="button" id="vsx" aria-label="Back to the shop">←</button><div><b id="vst">Search by photo</b><small>Find the machine in your picture</small></div></div>' +
    '<div class="vsw"><p class="vsh" id="vsh">Drag a box around the machine, then tap Find.</p>' +
    '<div class="vsc" id="vsc"><img id="vsi" alt="Your photo"><div class="vsr" id="vsr"></div></div>' +
    '<div class="vsa"><button type="button" class="vsg" id="vsg">Find matching machines</button><button type="button" class="vso" id="vso">Choose another photo</button></div>' +
    '<div id="vsres"></div></div>';
  document.body.appendChild(P);
  var I = P.querySelector('#vsi'), C = P.querySelector('#vsc'), R = P.querySelector('#vsr'), RES = P.querySelector('#vsres'), H = P.querySelector('#vsh');
  function open() { P.classList.add('open'); document.body.style.overflow = 'hidden' }
  function close() { P.classList.remove('open'); document.body.style.overflow = ''; fi.value = '' }
  P.querySelector('#vsx').addEventListener('click', close);
  P.querySelector('#vso').addEventListener('click', function () { fi.click() });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && P.classList.contains('open')) close() });
  btn.addEventListener('click', function () { load(); fi.click() });
  fi.addEventListener('change', function () {
    var f = fi.files && fi.files[0]; if (!f) return;
    var u = URL.createObjectURL(f); img = new Image();
    img.onload = function () { I.src = u; box = null; drawBox(); RES.innerHTML = ''; H.textContent = 'Drag a box around the machine, then tap Find. Or just tap Find.'; open() };
    img.onerror = function () { alert('That photo could not be opened. Please try a JPG or PNG screenshot.') };
    img.src = u;
  });
  // box drawing (mouse and touch)
  var st = null;
  function pt(e) { var r = I.getBoundingClientRect(), t = e.touches ? e.touches[0] : e; return { x: Math.max(0, Math.min(1, (t.clientX - r.left) / r.width)), y: Math.max(0, Math.min(1, (t.clientY - r.top) / r.height)) } }
  function drawBox() {
    if (!box) { R.style.display = 'none'; return }
    R.style.display = 'block'; R.style.left = box.x0 * 100 + '%'; R.style.top = box.y0 * 100 + '%';
    R.style.width = (box.x1 - box.x0) * 100 + '%'; R.style.height = (box.y1 - box.y0) * 100 + '%';
  }
  function down(e) { e.preventDefault(); st = pt(e); box = { x0: st.x, y0: st.y, x1: st.x, y1: st.y }; drawBox() }
  function move(e) { if (!st) return; e.preventDefault(); var p = pt(e); box = { x0: Math.min(st.x, p.x), y0: Math.min(st.y, p.y), x1: Math.max(st.x, p.x), y1: Math.max(st.y, p.y) }; drawBox() }
  function up() { if (box && (box.x1 - box.x0 < 0.05 || box.y1 - box.y0 < 0.05)) { box = null; drawBox() } st = null }
  C.addEventListener('mousedown', down); window.addEventListener('mousemove', move); window.addEventListener('mouseup', up);
  C.addEventListener('touchstart', down, { passive: false }); C.addEventListener('touchmove', move, { passive: false }); C.addEventListener('touchend', up);
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  P.querySelector('#vsg').addEventListener('click', function () {
    if (!img) return; H.textContent = 'Looking through ' + (DATA ? DATA.length : '') + ' machines…';
    var src = img;
    if (box) {   // cut out the boxed part
      var c = document.createElement('canvas'), w = img.naturalWidth, h = img.naturalHeight;
      c.width = Math.max(1, Math.round((box.x1 - box.x0) * w)); c.height = Math.max(1, Math.round((box.y1 - box.y0) * h));
      c.getContext('2d').drawImage(img, box.x0 * w, box.y0 * h, c.width, c.height, 0, 0, c.width, c.height); src = c;
    }
    load().then(function (D) {
      var q = TAVS.features(src);
      var top = D.map(function (x) { return [TAVS.score(q, x.v), x] }).sort(function (a, b) { return b[0] - a[0] }).slice(0, 6);
      H.textContent = 'Closest matches. Tap one to see it. Not quite right? Draw a tighter box around the machine and tap Find again.';
      var wa = 'https://wa.me/27611185978?text=' + encodeURIComponent("Hi Trimion Africa, I'm looking for a machine like the one in a photo I have. I'll send you the picture now.\n\nFull catalog: https://trimionafrica.co.za/");
      RES.innerHTML = '<div class="vsl">' + top.map(function (t) {
        var x = t[1]; return '<a href="#m' + x.k + '" data-k="' + x.k + '"><img src="' + x.i + '" alt="" loading="lazy" width="160" height="160"><b>' + esc(x.n) + '</b><small>' + esc(x.m) + '</small><span>' + esc(x.p) + '</span></a>'
      }).join('') + '</div><a class="vswa" href="' + wa + '" target="_blank" rel="noopener">Can’t find it? Send us the photo on WhatsApp</a>';
    }).catch(function () { H.textContent = 'Could not load the catalogue. Check your connection and try again.' });
  });
  RES.addEventListener('click', function (e) { var a = e.target.closest('a[data-k]'); if (!a) return; e.preventDefault(); close(); location.hash = 'm' + a.dataset.k });
})();
