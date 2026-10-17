"""Set every card's price (the 143 'Price on request' cards and Trimion's own 21) from prices.json: price (price, lay-by link, Buy now), add offers to the
search data, and update products.json / details.json so share pictures, /p/ pages and brochures match."""
import re, json, math
from urllib.parse import quote, unquote

PRICES = {int(k): v for k, v in json.load(open('/home/claude/trimion-site/tools/prices.json')).items()}
CAT = '\n\nFull catalog (162 machines): https://trimionafrica.co.za/'
WA = 'https://wa.me/27611185978?text='

def R(n): return 'R{:,}'.format(n)

def layby(p):
    if p < 10000: return None
    dep = 5000 if p < 25000 else 10000 if p < 60000 else int(math.ceil(p * 0.25 / 1000) * 1000)
    inst = int(math.ceil((p - dep) / 2 / 25) * 25)
    return dep, inst

def enc(t): return quote(t, safe='')

def apply(s):
    n = [0]
    def card(m):
        k = int(m.group(1)); b = m.group(2)
        if k not in PRICES: return m.group(0)
        p = PRICES[k]
        name = re.search(r'<h3>(.*?)</h3>', b).group(1)
        from html import unescape
        nm = unescape(name); model = re.search(r'class="model">Model ([^<]*)<', b).group(1).strip()
        lb = layby(p); lbhtml = ''
        if lb:
            t = f"Hi Trimion Africa, I'd like the lay-by plan for the {nm} ({model}) at {R(p)}: {R(lb[0])} deposit, then the balance over 2 or 3 months. Please send my lay-by invoice." + CAT
            lbhtml = f'<a class="lb" href="{WA}{enc(t)}" target="_blank" rel="noopener"><b>Lay-by</b> {R(lb[0])} now, then 2 × {R(lb[1])}</a>'
        if '<div class="price por">Price on request</div>' in b:
            b = b.replace('<div class="price por">Price on request</div>', f'<div class="price">{R(p)}</div>{lbhtml}')
        else:   # Trimion's own listed price: replace price and any lay-by link with the re-priced ones
            b, c = re.subn(r'<div class="price">R[\d,]+</div>(\s*<a class="lb" href="[^"]*" target="_blank" rel="noopener">.*?</a>)?',
                           lambda _: f'<div class="price">{R(p)}</div>{lbhtml}', b, count=1, flags=re.S)
            assert c == 1, k
        buy = f"Hi Trimion Africa, I want to buy the {nm} ({model}) at {R(p)}. Please send my invoice." + CAT
        b, c = re.subn(r'<a class="btn" href="https://wa\.me/27611185978\?text=[^"]*" target="_blank" rel="noopener">(Get price|Buy now)</a>',
                       lambda _: f'<a class="btn" href="{WA}{enc(buy)}" target="_blank" rel="noopener">Buy now</a>', b)
        assert c == 1, k
        n[0] += 1
        return f'<article class="card" data-k="{k}">{b}</article>'
    s = re.sub(r'<article class="card" data-k="(\d+)">(.*?)</article>', card, s, flags=re.S)
    assert n[0] == len(PRICES), n[0]
    # search-engine data: add an offer for each newly priced product
    D = {d['k']: d for d in json.load(open('/home/claude/trimion-site/tools/details.json'))}
    added = 0
    for k, p in PRICES.items():
        sku = D[k]['model']
        i = s.find(f'"sku":"{sku}"'); assert i > 0, sku
        brand = '"brand":{"@type":"Brand","name":"Trimion Africa"}'
        j = s.find(brand, i); assert j > 0 and s.rfind('"sku":', 0, j) == i, sku
        e = j + len(brand)
        if s.startswith(',"offers":', e):   # already has an offer: update its price
            m = re.compile(r'"price":"\d+"').search(s, e); assert m, sku
            s = s[:m.start()] + '"price":"%d"' % p + s[m.end():]; added += 1; continue
        tail = brand + '}'; j = s.find(tail, i)
        assert j == e - len(brand) and s[j + len(tail)] == '}', sku
        offer = ',"offers":{"@type":"Offer","price":"%d","priceCurrency":"ZAR","url":"https://trimionafrica.co.za/","seller":{"@id":"https://trimionafrica.co.za/#org"}}' % p
        s = s[:j + len(tail) - 1] + offer + s[j + len(tail) - 1:]
        added += 1
    # no machines are on request any more
    s = s.replace('<option value="r">Price on request</option>', '')
    faq = '<details><summary>Why do some machines say "Price on request"?</summary><p>Prices for these machines depend on the configuration and current stock. Tap "Get price" and we\'ll send you a written price and invoice on WhatsApp.</p></details>\n'
    assert faq in s; s = s.replace(faq, '')
    assert s.count('price por') == 0
    return s

def update_data():
    for f in ('products.json', 'details.json'):
        path = '/home/claude/trimion-site/tools/' + f
        L = json.load(open(path))
        for d in L:
            if d['k'] in PRICES:
                p = PRICES[d['k']]; d['price'] = R(p); lb = layby(p)
                d['lb'] = f'Lay-by {R(lb[0])} now, then 2 × {R(lb[1])}' if lb else ''
        json.dump(L, open(path, 'w'), indent=1)
