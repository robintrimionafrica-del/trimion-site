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
