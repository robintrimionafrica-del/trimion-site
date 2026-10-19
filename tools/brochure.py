"""Lightweight one-page brochures (built-in Helvetica, no embedded fonts)."""
import json, os, sys, io
from urllib.parse import quote
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/trimion-site/public/pdf'
ONLY = set(map(int, sys.argv[2].split(','))) if len(sys.argv) > 2 else None
DATE = '14 October 2026'
SITE = 'https://trimionafrica.co.za'
NAVY, NAVY2, BLUE, SKY = HexColor('#081a3d'), HexColor('#0d2a5c'), HexColor('#0b84d8'), HexColor('#9fc6ea')
INK, MUTED, LINE, AMBER = HexColor('#14213d'), HexColor('#5b6578'), HexColor('#e3e8f0'), HexColor('#f8b73f')
GREEN, GBG, GBD, GTX = HexColor('#1fa855'), HexColor('#eefaf2'), HexColor('#bfe7cd'), HexColor('#0b5f31')
W, H = A4
M = 40

def clean(t):
    t = t.replace('−', '-').replace('✓', '').replace('≤', '<=').replace('≥', '>=')
    return ''.join(ch if ch.encode('cp1252', 'ignore') else '' for ch in t)

def esc(t):
    return clean(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def P(size, color=INK, bold=False, lead=None):
    return ParagraphStyle('x', fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=size,
                          leading=lead or size * 1.3, textColor=color)

def para(c, html, style, x, y, w):
    """draw paragraph with top at y; return new y (bottom)"""
    p = Paragraph(html, style)
    _, h = p.wrap(w, 1000)
    if c: p.drawOn(c, x, y - h)
    return y - h

def jpg(path, maxpx, q):
    im = Image.open(path).convert('RGB'); im.thumbnail((maxpx, maxpx))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True); b.seek(0)
    return ImageReader(b), im.size

LOGO = None
def logo():
    global LOGO
    if LOGO is None:
        im = Image.open('/home/claude/trimion-site/tools/src/img/4880f983c6.png').convert('RGBA')
        bg = Image.new('RGB', im.size, (9, 30, 70)); bg.paste(im, mask=im.split()[3])
        b = io.BytesIO(); bg.save(b, 'JPEG', quality=80); b.seek(0); LOGO = ImageReader(b)
    return LOGO

def page(c, d, s):
    """draw (or measure when c is None). s = text scale for lower sections. returns bottom y of content"""
    cons = d['cat'] == 'Consumables'
    por = 'request' in d['price'].lower()
    url = f"{SITE}/p/m{d['k']}"
    wa = 'https://wa.me/27644548506?text=' + quote(
        f"Hi Trimion Africa, I have your brochure for the {d['name']} ({d['model']})" +
        ('. Please send me the price and an invoice.' if por else f" at {d['price']}. Please send my invoice.") + f"\n\n{url}")
    if c:
        # header band
        c.setFillColor(NAVY); c.rect(0, H - 74, W, 74, stroke=0, fill=1)
        c.setFillColor(NAVY2); c.rect(W * 0.62, H - 74, W * 0.38, 74, stroke=0, fill=1)
        c.drawImage(logo(), M, H - 60, 44, 44)
        c.setFillColor(white); c.setFont('Helvetica-Bold', 15); c.drawString(M + 54, H - 36, 'TRIMION AFRICA')
        c.setFillColor(SKY); c.setFont('Helvetica', 8.5); c.drawString(M + 54, H - 49, 'Professional salon & spa equipment  ·  Durban')
        c.setFillColor(white); c.setFont('Helvetica-Bold', 10); c.drawRightString(W - M, H - 36, 'Product brochure' if cons else 'Machine brochure')
        c.setFillColor(SKY); c.setFont('Helvetica', 8.5); c.drawRightString(W - M, H - 49, 'Prices as at ' + DATE)
    # photo
    top = H - 74 - 22; ph = 215
    if c:
        c.setStrokeColor(LINE); c.setFillColor(white); c.roundRect(M, top - ph, ph, ph, 10, stroke=1, fill=1)
        img, (iw, ih) = jpg('/home/claude/trimion-site/tools/src' + d['img'], 320, 50)
        sc = min((ph - 12) / iw, (ph - 12) / ih); dw, dh = iw * sc, ih * sc
        c.drawImage(img, M + (ph - dw) / 2, top - ph + (ph - dh) / 2, dw, dh)
    # right column
    x = M + ph + 22; w = W - M - x; y = top
    y = para(c, esc(d['cat'].upper()), P(7.5, BLUE, True), x, y, w) - 3
    ns = 18 if len(d['name']) < 34 else 15.5 if len(d['name']) < 52 else 13.5
    y = para(c, esc(d['name']), P(ns, NAVY, True, ns * 1.15), x, y, w) - 2
    y = para(c, 'Model ' + esc(d['model']), P(9, MUTED), x, y, w) - 6
    y = para(c, esc(d['price']), P(16 if por else 23, NAVY, True), x, y, w) - 2
    lb = d['lb'].replace('Lay-by', '').strip()
    if lb:
        y = para(c, f'<font color="#0b84d8"><b>Lay-by:</b></font> {esc(lb)}  ·  no interest, no fees', P(9), x, y, w)
    elif por:
        y = para(c, 'WhatsApp us for a written price and invoice.', P(9), x, y, w)
    y -= 8
    # warranty / delivery box
    if d.get('wb'):
        head, sub = d['wb'], d['wfull'] + '  ·  R150 delivery anywhere in SA  ·  free online training'
    else:
        head, sub = 'R150 delivery anywhere in South Africa', 'Order together with your machine to share one delivery.'
    st_h, st_s = P(10.5, GTX, True), P(8.3, HexColor('#3c5446'))
    hh = Paragraph(esc(head), st_h).wrap(w - 20, 500)[1] + Paragraph(esc(sub), st_s).wrap(w - 20, 500)[1] + 16
    if c:
        c.setFillColor(GBG); c.setStrokeColor(GBD); c.roundRect(x, y - hh, w, hh, 7, stroke=1, fill=1)
    yy = para(c, esc(head), st_h, x + 10, y - 8, w - 20) - 1
    para(c, esc(sub), st_s, x + 10, yy, w - 20)
    y -= hh + 10
    # buttons
    bw = (w - 8) / 2
    if c:
        for i, (lab, col, tc, link) in enumerate([('Order on WhatsApp', GREEN, white, wa), ('View online', HexColor('#eef3fa'), NAVY, url)]):
            bx = x + i * (bw + 8)
            c.setFillColor(col); c.roundRect(bx, y - 24, bw, 24, 12, stroke=0, fill=1)
            c.setFillColor(tc); c.setFont('Helvetica-Bold', 9.5); c.drawCentredString(bx + bw / 2, y - 15.5, lab)
            c.linkURL(link, (bx, y - 24, bx + bw, y), relative=0)
    y -= 24
    y = min(y, top - ph) - 20

    def heading(t, x0, y0):
        if c:
            c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 11 * s); c.drawString(x0, y0 - 11 * s, t)
            c.setFillColor(AMBER); c.rect(x0, y0 - 11 * s - 5, c.stringWidth(t, 'Helvetica-Bold', 11 * s), 1.6, stroke=0, fill=1)
        return y0 - 11 * s - 12

    # about
    y = heading('About this product' if cons else 'About this machine', M, y)
    for i, t in enumerate(d['desc']):
        y = para(c, esc(t), P(9.2 * s, INK if i == 0 else MUTED), M, y, W - 2 * M) - 3
    y -= 12
    # specs + what you get
    cw = (W - 2 * M - 24) / 2
    specs = d['specs'][:12]
    get = (['R150 delivery anywhere in South Africa (9 to 12 business days)', 'Order together with your machine to share one delivery',
            'Ongoing support on WhatsApp'] if cons else [g for g in d['get'] if not g.startswith('Brand new')])
    yl = y; yr = y
    if specs:
        yl = heading('Specifications', M, yl)
        for sp in specs:
            k, _, v = sp.partition(':')
            if v and len(k) < 40:
                st = P(8.4 * s); kp = Paragraph('<b>' + esc(k) + '</b>', st); vp = Paragraph(esc(v.strip()), st)
                kh = kp.wrap(cw * 0.38, 500)[1]; vh = vp.wrap(cw * 0.6, 500)[1]; rh = max(kh, vh)
                if c: kp.drawOn(c, M, yl - 3 - kh); vp.drawOn(c, M + cw * 0.4, yl - 3 - vh)
                yl -= rh + 6
            else:
                yl = para(c, esc(sp), P(8.4 * s), M, yl - 3, cw) - 3
            if c: c.setStrokeColor(HexColor('#eef1f6')); c.line(M, yl, M + cw, yl)
    xr = M + cw + 24
    yr = heading('What you get', xr, yr)
    for g in get:
        st = P(8.4 * s); pp = Paragraph(esc(g), st); gh = pp.wrap(cw - 14, 500)[1]
        if c:
            pp.drawOn(c, xr + 14, yr - 3 - gh)
            c.setStrokeColor(GREEN); c.setLineWidth(1.4); c.lines([(xr + 2, yr - 3 - 6, xr + 5, yr - 3 - 9), (xr + 5, yr - 3 - 9, xr + 10, yr - 3 - 2)]); c.setLineWidth(1)
            c.setStrokeColor(HexColor('#eef1f6')); c.line(xr, yr - gh - 6, xr + cw, yr - gh - 6)
        yr -= gh + 6
    y = min(yl, yr) - 16
    # how to order
    y = heading('How to order', M, y)
    steps = [('1. Choose', 'Pick your machine on trimionafrica.co.za or here'), ('2. WhatsApp us', '064 454 8506: we confirm price and delivery'),
             ('3. Pay', 'EFT or secure card link on your invoice, or lay-by'), ('4. Delivered', '9 to 12 business days, then online training')]
    sw = (W - 2 * M - 24) / 4; sh = 0
    for t, b in steps:
        sh = max(sh, Paragraph(f'<b>{t}</b><br/>{esc(b)}', P(8 * s)).wrap(sw - 14, 500)[1] + 12)
    for i, (t, b) in enumerate(steps):
        bx = M + i * (sw + 8)
        if c:
            c.setFillColor(HexColor('#f3f5f9')); c.roundRect(bx, y - 3 - sh, sw, sh, 6, stroke=0, fill=1)
        para(c, f'<font color="#081a3d"><b>{t}</b></font><br/>{esc(b)}', P(8 * s), bx + 7, y - 9, sw - 14)
    y -= sh + 3
    if c:
        # note + footer
        para(c, 'For professional salon and spa use. Not a medical device and not intended to diagnose, treat or cure any medical condition. '
                'Prices in South African rand; price, stock, voltage and plug type are confirmed in writing on your invoice. '
                'Photos show the actual machine model; colour and small details can differ.', P(7, MUTED), M, 84, W - 2 * M)
        c.setFillColor(NAVY); c.rect(0, 0, W, 44, stroke=0, fill=1)
        para(c, '<font color="#ffffff"><b>Trimion Africa Precision (Pty) Ltd</b></font>  ·  Reg. no. 2026/806671/07  ·  117 Stephen Dlamini Road, Durban, KwaZulu-Natal<br/>'
                'WhatsApp or call <font color="#ffffff">064 454 8506</font>  ·  <font color="#ffffff">info@trimionafrica.co.za</font>  ·  <font color="#ffffff">trimionafrica.co.za</font>',
             P(7.4, HexColor('#cfe3f7')), M, 34, W - 2 * M)
        c.linkURL('https://wa.me/27644548506', (0, 0, W / 2, 44), relative=0)
        c.linkURL(SITE, (W / 2, 0, W, 44), relative=0)
    return y

def build(d):
    s = 1.0
    while page(None, d, s) < 100 and s > 0.7:
        s -= 0.04
    path = f"{OUT}/{d['model']}.pdf"
    c = canvas.Canvas(path, pagesize=A4, pageCompression=1)
    c.setTitle(f"{d['name']} ({d['model']}) | Trimion Africa"); c.setAuthor('Trimion Africa'); c.setSubject('Machine brochure')
    page(c, d, s); c.showPage(); c.save()
    return s

D = json.load(open('/home/claude/trimion-site/tools/details.json'))
os.makedirs(OUT, exist_ok=True)
low = []
for d in D:
    if ONLY and d['k'] not in ONLY: continue
    w = next((g for g in d['get'] if 'warranty' in g.lower()), '')
    w = w.replace(', confirmed on your invoice', ''); d['wfull'] = w[:1].upper() + w[1:]
    d['wb'] = (d['wb'].replace(' included', '') + ' included') if d['wb'] else ''
    sc = build(d)
    if sc < 0.85: low.append((d['k'], round(sc, 2)))
print('scaled down:', low)
