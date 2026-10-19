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
      var wa = 'https://wa.me/27644548506?text=' + encodeURIComponent("Hi Trimion Africa, I'm looking for a machine like the one in a photo I have. I'll send you the picture now.\n\nFull catalog: https://trimionafrica.co.za/");
      RES.innerHTML = '<div class="vsl">' + top.map(function (t) {
        var x = t[1]; return '<a href="#m' + x.k + '" data-k="' + x.k + '"><img src="' + x.i + '" alt="" loading="lazy" width="160" height="160"><b>' + esc(x.n) + '</b><small>' + esc(x.m) + '</small><span>' + esc(x.p) + '</span></a>'
      }).join('') + '</div><a class="vswa" href="' + wa + '" target="_blank" rel="noopener">Can’t find it? Send us the photo on WhatsApp</a>';
    }).catch(function () { H.textContent = 'Could not load the catalogue. Check your connection and try again.' });
  });
  RES.addEventListener('click', function (e) { var a = e.target.closest('a[data-k]'); if (!a) return; e.preventDefault(); close(); location.hash = 'm' + a.dataset.k });
})();
