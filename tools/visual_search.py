"""Search by photo: bundle vs_core.js + vs_ui.js into ../public/vs.js, build ../public/vs.json
(one fingerprint per machine photo, via vs_build.js) and add the camera button to the search bar.
Runs after build.py (see rebuild.sh)."""
import subprocess, os
T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
subprocess.run(['node', os.path.join(T, 'vs_build.js')], check=True, cwd=T)
open(os.path.join(PUB, 'vs.js'), 'w').write(open(os.path.join(T, 'vs_core.js')).read() + '\n' + open(os.path.join(T, 'vs_ui.js')).read())

f = os.path.join(PUB, 'index.html'); s = open(f, encoding='utf-8').read()
assert 'id="vsb"' not in s, 'already added'
inp = '<input id="q" type="search"'
assert s.count(inp) == 1
CAM = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>')
btn = ('<button type="button" id="vsb" class="vsb" aria-label="Search by photo" title="Search by photo">' + CAM + '</button>'
       '<input id="vsf" type="file" accept="image/*" hidden>')
i = s.find('</div>', s.find(inp)); s = s[:i] + btn + s[i:]
CSS = '''<style>
/* search by photo */
.search input#q{padding-right:52px}
.vsb{position:absolute;right:6px;top:50%;margin-top:-19px;transform:none!important;width:38px;height:38px;border:0;border-radius:50%;background:#eef2fb;color:var(--navy);display:flex;align-items:center;justify-content:center;cursor:pointer}
.vsb svg{position:static;transform:none;width:20px;height:20px;stroke:currentColor;pointer-events:none}
.vsb.zap{position:absolute!important;left:auto!important;right:6px!important;top:50%!important}
.vsb:focus-visible{outline:2px solid #4f86ff;outline-offset:2px}
#vsp{position:fixed;inset:0;z-index:60;background:var(--bg);overflow-y:auto;display:none;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
#vsp.open{display:block}
.vsw{max-width:720px;margin:0 auto;padding:14px 16px 40px}
.vsh{color:var(--muted);font-size:.9rem;margin:0 0 10px;line-height:1.45}
.vsc{position:relative;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;touch-action:none;user-select:none;-webkit-user-select:none;cursor:crosshair}
.vsc img{display:block;width:100%;height:auto;max-height:60vh;object-fit:contain;pointer-events:none}
.vsr{position:absolute;border:2px solid var(--neon,#0a4dff);background:rgba(10,77,255,.12);box-shadow:0 0 0 9999px rgba(8,26,61,.35);display:none;pointer-events:none}
.vsa{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.vsa button{flex:1 1 160px;border-radius:22px;padding:12px 14px;font:600 .92rem system-ui,sans-serif;cursor:pointer}
.vsg{background:var(--navy);color:#fff;border:0}.vso{background:#fff;color:var(--navy);border:1px solid var(--line)}
.vsl{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.vsl a{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px;text-decoration:none;color:var(--ink);min-width:0}
.vsl img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:contain}
.vsl b{display:block;font-size:.84rem;line-height:1.3;margin:6px 0 2px}
.vsl small{display:block;color:var(--muted);font-size:.74rem}
.vsl span{display:block;font-weight:700;color:var(--navy);margin-top:4px}
.vswa{display:block;text-align:center;margin:16px 0 0;color:#1f9d55;font-weight:600}
</style>
'''
assert s.count('</body>') == 1 and s.count('</head>') == 1
s = s.replace('</head>', CSS + '</head>')   # styles in <head> so the camera button never flashes unstyled
s = s.replace('</body>', '<script src="/vs.js" defer></script>\n</body>')
open(f, 'w', encoding='utf-8').write(s)
print('search by photo added')
