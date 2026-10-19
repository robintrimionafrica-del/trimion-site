"""One-off (16 Oct 2026): add the two C2 HI-EMT machines from Weifang Mingliang (Domi) as k=165, 166."""
import json, re, hashlib
from PIL import Image
from urllib.parse import quote
S = '/tmp/claude-0/-home-claude/a05a50a8-ddcf-5eab-9e5f-ba4d48daa54f/scratchpad/c2img'
GET = ["Brand new, straight from the factory",
       "1-year warranty on the machine, 6 months on handpieces, confirmed on your invoice",
       "Free online operational training",
       "In-person training at extra cost, with a male or female trainer (quoted on WhatsApp)",
       "Certification available separately (R1,500)",
       "R150 delivery anywhere in South Africa (9 to 12 business days)",
       "Ongoing support on WhatsApp"]
NEW = [
 dict(k=165, src='dual', name='2-Handle HI-EMT Body Sculpting Machine with RF', model='TAC2-2H',
      desc=["Professional electromagnetic body sculpting machine with RF warming, for muscle toning treatments in salons and spas.",
            "Two independent handles let you treat two areas at once, with a 14-inch foldable 4K touchscreen."],
      specs=["Handles: 2, independently controlled", "Power: 2000W", "Technology: HI-EMT electromagnetic with RF warming",
             "Intensity: 16 levels", "Modes: 5, at 150Hz", "Sessions: 30 minutes", "Screen: 14-inch foldable 4K touchscreen",
             "Applicators: strap-on, for abdomen, arms, thighs and buttocks", "Type: Floor-standing, on wheels",
             "Material: ABS and stainless steel", "Power supply: 220V, 50Hz"]),
 dict(k=166, src='four', name='4-Handle HI-EMT Body Sculpting Machine with RF and Seat Applicator', model='TAC2-4H',
      desc=["Professional 4-handle electromagnetic body sculpting station with RF warming, for muscle toning treatments in busy salons and spas.",
            "Run up to four handles at once, or treat two clients side by side, plus a seat applicator for glute and core muscle toning."],
      specs=["Handles: 4, independently controlled, plus a seat applicator", "Power: 4000W (handles), 3500W (seat applicator)",
             "Technology: HI-EMT electromagnetic with RF warming", "Intensity: 16 levels", "Modes: 5, at 150Hz",
             "Sessions: 30 minutes", "Screen: 14-inch foldable 4K touchscreen",
             "Applicators: strap-on, for abdomen, arms, thighs and buttocks", "Type: Floor-standing, on wheels",
             "Material: ABS and stainless steel", "Power supply: 220V, 50Hz"]),
]
s = open('src/index.html', encoding='utf-8').read()
P = json.load(open('products.orig.json')); D = json.load(open('details.orig.json'))
assert not any(x['k'] in (165, 166) for x in P), 'already added'
cards = ''; ld = ''
for n in NEW:
    im = Image.open(f"{S}/{n['src']}.png").convert('RGB').resize((540, 540), Image.LANCZOS)
    h = hashlib.sha1(im.tobytes()).hexdigest()[:10]; img = f'/img/{h}.webp'
    im.save('src/img/' + h + '.webp', quality=82, method=6)
    n['img'] = img
    msg = (f"Hi Trimion Africa, please send me the price and an invoice for the {n['name']} ({n['model']}) so I can buy."
           "\n\nFull catalog (161 machines): https://trimionafrica.co.za/")
    spec_li = ''.join(f'<li>{x}</li>' for x in n['specs'])
    cards += (f'<article class="card" data-k="{n["k"]}">\n'
        f'<div class="photo"><img src="{img}" alt="{n["name"]}" decoding="async" width="360" height="360" loading="lazy"></div>\n'
        f'<div class="body"><h3>{n["name"]}</h3><div class="model">Model {n["model"]}</div><div class="price por">Price on request</div>\n'
        f'<a class="btn" href="https://wa.me/27644548506?text={quote(msg, safe="")}" target="_blank" rel="noopener">Get price</a><details class="det"><summary>Full details</summary>\n'
        f'<div class="detb"><p class="dd">{n["desc"][0]}</p><div class="dh">Specifications</div><ul class="specs">{spec_li}</ul>\n'
        '<div class="dh">Included with your order</div><ul class="specs"><li>Free online operational training</li><li>In-person training at extra cost, with a male or female trainer</li><li>Certification available separately (R1,500)</li><li>1-year warranty, confirmed on your invoice</li><li>WhatsApp support</li></ul>\n'
        '<div class="dh">Delivery</div><ul class="specs"><li>Nationwide delivery R150, 9–12 business days</li><li>Final voltage and plug type confirmed on the invoice before dispatch</li></ul>\n'
        '</div></details></div></article>')
    ld += (',{"@type":"ListItem","position":%d,"item":{"@type":"Product","name":%s,"sku":"%s","mpn":"%s","image":"https://trimionafrica.co.za%s","brand":{"@type":"Brand","name":"Trimion Africa"}}}'
           % (n['k'], json.dumps(n['name']), n['model'], n['model'], img))
    P.append({'k': n['k'], 'sec': 'EMS and electromagnetic', 'sid': 'ems', 'img': img, 'name': n['name'], 'model': n['model'], 'price': 'Price on request', 'lb': ''})
    D.append({'k': n['k'], 'name': n['name'], 'model': n['model'], 'cat': 'EMS and electromagnetic', 'price': 'Price on request',
              'desc': n['desc'], 'specs': n['specs'], 'get': GET, 'lb': '', 'img': img, 'wb': '1-year warranty included'})
# card goes at the end of the EMS grid (after k=99)
m = re.search(r'(<article class="card" data-k="99">.*?</article>)', s, re.S); assert m
s = s[:m.end()] + cards + s[m.end():]
assert s.count('<h2>EMS and electromagnetic <i>59</i></h2>') == 1
s = s.replace('<h2>EMS and electromagnetic <i>59</i></h2>', '<h2>EMS and electromagnetic <i>61</i></h2>')
end = '"brand":{"@type":"Brand","name":"Trimion Africa"}}}]}]}</script>'
i = s.find('"position":164'); j = s.find(end, i); assert i > 0 and j > 0
j += len('"brand":{"@type":"Brand","name":"Trimion Africa"}}}')
s = s[:j] + ld + s[j:]
open('src/index.html', 'w', encoding='utf-8').write(s)
json.dump(P, open('products.orig.json', 'w'), indent=0); json.dump(D, open('details.orig.json', 'w'), indent=1, ensure_ascii=False)
print('added', [n['img'] for n in NEW])
