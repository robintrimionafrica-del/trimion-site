"""One-off (17 Oct 2026): add the G1 5-handle roller/vacuum/RF body shaping station from Weifang Mingliang (Domi) as k=167."""
import json, re, hashlib
from PIL import Image
from urllib.parse import quote
SRC = '/tmp/claude-0/-home-claude/a05a50a8-ddcf-5eab-9e5f-ba4d48daa54f/scratchpad/g1/g1_1.png'
GET = ["Brand new, straight from the factory",
       "1-year warranty on the machine, 6 months on handpieces, confirmed on your invoice",
       "Free online operational training",
       "In-person training at extra cost, with a male or female trainer (quoted on WhatsApp)",
       "Certification available separately (R1,500)",
       "R150 delivery anywhere in South Africa (9 to 12 business days)",
       "Ongoing support on WhatsApp"]
n = dict(k=167, name='5-Handle Roller, Vacuum and RF Body Shaping Station', model='TAVS5',
         desc=["Professional body shaping station combining mechanical roller massage, vacuum, bipolar RF and infrared warmth, for body contouring and massage treatments in salons and spas.",
               "Five handpieces for large body areas, smaller areas and the face, with a large touchscreen on a wheeled floor stand."],
         specs=["Handles: 5", "Power: 4500W",
                "Technology: mechanical roller massage, vacuum, bipolar RF and infrared warmth",
                "Screen: large touchscreen", "Type: Floor-standing, on wheels"])
s = open('src/index.html', encoding='utf-8').read()
P = json.load(open('products.orig.json')); D = json.load(open('details.orig.json'))
assert not any(x['k'] == 167 for x in P), 'already added'
# square product photo on the light-grey studio background
im = Image.open(SRC).convert('RGB'); bg = im.getpixel((5, 5))
side = max(im.size); sq = Image.new('RGB', (side, side), bg); sq.paste(im, ((side - im.width) // 2, 0))
sq = sq.resize((540, 540), Image.LANCZOS)
h = hashlib.sha1(sq.tobytes()).hexdigest()[:10]; img = f'/img/{h}.webp'
sq.save('src/img/' + h + '.webp', quality=82, method=6)
msg = (f"Hi Trimion Africa, please send me the price and an invoice for the {n['name']} ({n['model']}) so I can buy."
       "\n\nFull catalog (161 machines): https://trimionafrica.co.za/")
spec_li = ''.join(f'<li>{x}</li>' for x in n['specs'])
card = (f'<article class="card" data-k="{n["k"]}">\n'
    f'<div class="photo"><img src="{img}" alt="{n["name"]}" decoding="async" width="360" height="360" loading="lazy"></div>\n'
    f'<div class="body"><h3>{n["name"]}</h3><div class="model">Model {n["model"]}</div><div class="price por">Price on request</div>\n'
    f'<a class="btn" href="https://wa.me/27611185978?text={quote(msg, safe="")}" target="_blank" rel="noopener">Get price</a><details class="det"><summary>Full details</summary>\n'
    f'<div class="detb"><p class="dd">{n["desc"][0]}</p><div class="dh">Specifications</div><ul class="specs">{spec_li}</ul>\n'
    '<div class="dh">Included with your order</div><ul class="specs"><li>Free online operational training</li><li>In-person training at extra cost, with a male or female trainer</li><li>Certification available separately (R1,500)</li><li>1-year warranty, confirmed on your invoice</li><li>WhatsApp support</li></ul>\n'
    '<div class="dh">Delivery</div><ul class="specs"><li>Nationwide delivery R150, 9–12 business days</li><li>Final voltage and plug type confirmed on the invoice before dispatch</li></ul>\n'
    '</div></details></div></article>')
ld = (',{"@type":"ListItem","position":%d,"item":{"@type":"Product","name":%s,"sku":"%s","mpn":"%s","image":"https://trimionafrica.co.za%s","brand":{"@type":"Brand","name":"Trimion Africa"}}}'
      % (n['k'], json.dumps(n['name']), n['model'], n['model'], img))
P.append({'k': n['k'], 'sec': 'RF and cavitation', 'sid': 'rf', 'img': img, 'name': n['name'], 'model': n['model'], 'price': 'Price on request', 'lb': ''})
D.append({'k': n['k'], 'name': n['name'], 'model': n['model'], 'cat': 'RF and cavitation', 'price': 'Price on request',
          'desc': n['desc'], 'specs': n['specs'], 'get': GET, 'lb': '', 'img': img, 'wb': '1-year warranty included'})
# card goes right after the other vacuum RF roller station (k=117)
m = re.search(r'(<article class="card" data-k="117">.*?</article>)', s, re.S); assert m
s = s[:m.end()] + card + s[m.end():]
assert s.count('<h2>RF and cavitation <i>31</i></h2>') == 1
s = s.replace('<h2>RF and cavitation <i>31</i></h2>', '<h2>RF and cavitation <i>32</i></h2>')
end = '"brand":{"@type":"Brand","name":"Trimion Africa"}}}'
i = s.find('"position":166'); j = s.find(end, i); assert i > 0 and j > 0
j += len(end)
s = s[:j] + ld + s[j:]
open('src/index.html', 'w', encoding='utf-8').write(s)
json.dump(P, open('products.orig.json', 'w'), indent=0); json.dump(D, open('details.orig.json', 'w'), indent=1, ensure_ascii=False)
print('added', img)
