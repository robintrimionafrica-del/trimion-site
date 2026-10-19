# Builds postt/posts.json: one entry per product for the social post bank (story/feed/square + videos).
import json, re, os, html
P = json.load(open('products.json')); D = {d['k']: d for d in json.load(open('details.json'))}
B = {b['code']: b for b in json.load(open('post_bank.json'))}
soc = '../public/social'
existing = {}
for f in os.listdir(soc):
    m = re.match(r'(Trimion_(\d+)_(.+?))(_m2)?\.(jpg|mp4)$', f)
    if m: existing[m.group(3)] = m.group(1)
KW = ['360° Cryo','Cryo','Electromagnetic','EMS','HIFU','Cavitation','Laser','Diode','RF','Radio Frequency','Ultrasonic','Hydra','Vacuum','Microcurrent','Pico','IPL','Oxygen','Plasma','Roller','LED']
def head(name):
    e = html.escape(name)
    for k in KW:
        m = re.search(r'(?<![\w])'+re.escape(html.escape(k))+r'(?![\w])', e)
        if m: return e[:m.start()]+'<em>'+m.group(0)+'</em>'+e[m.end():]
    return e
def short(s):
    s = re.split(r'[,(:;]', s)[0].strip()
    return s if (len(s) <= 24 and (' ' in s or re.search(r'\d', s))) else ''
out = []
for p in P:
    code = p['model']; d = D.get(p['k'], {})
    b = B.get(code)
    items = re.findall(r'✔ ([^\n]+)', b['text']) if b else []
    if not items: items = [x for x in (short(s) for s in d.get('specs', [])) if x][:3]
    sp = ' · '.join([code] + items[:3])
    sup = p['sid'] == 'supplies'
    m = re.search(r'R[\d,]+', p.get('lb', '') or '')
    lb = f'Lay-by from {m.group(0)} deposit' if (m and not sup) else 'R150 delivery nationwide'
    if code == 'TACRYOM': lb = 'R110 per membrane · minimum 30'
    chips = ['R150 delivery', 'Order on WhatsApp'] if sup else [('2-year warranty' if p['k'] == 1 else '1-year warranty'), 'Free training', 'Lay-by 2–3 months']
    name = existing.get(code) or f"Trimion_{p['k']:03d}_{code}"
    out.append(dict(k=p['k'], code=code, file=name, h=head(p['name']), hlen=len(p['name']), sp=sp,
                    img='/home/claude/trimion-site/public' + p['img'], price=p['price'], lb=lb, chips=chips, sid=p['sid']))
json.dump(out, open('postt/posts.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'posts;', sum(1 for o in out if o['code'] in existing), 'replace existing;', len(set(existing)-{o['code'] for o in out}), 'existing without product:', set(existing)-{o['code'] for o in out})
