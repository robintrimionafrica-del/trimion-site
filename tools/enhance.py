"""Speed + landing text + WhatsApp share text. Used by build.py and build_lite.py."""
import os
from PIL import Image

HERO = ['5d861a4924', '823bb61a5b', '2ede239145', '191a91eb64']
SHARE_TXT = ('*Trimion Africa* | 162 professional salon & spa machines\n'
             'EMS, cryo, RF, HIFU, facial and massage machines\n'
             '1-year warranty · R150 delivery anywhere in SA · Free online training · Lay-by over 2 or 3 months\n'
             'Browse and order on WhatsApp: https://trimionafrica.co.za/?v=4')


def apply(s, out, rep):
    from urllib.parse import quote
    import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); import trust_seo; s = trust_seo.apply(s)
    # ---- 1. hero slider photos: JPEG -> WebP (about half the size) ----
    for h in HERO:
        src = f'/home/claude/trimion-site/tools/src/img/{h}.jpg'
        im = Image.open(src).convert('RGB')
        if h == HERO[0]:
            im.thumbnail((760, 760))
        im.save(f'{out}/img/{h}.webp', 'WEBP', quality=70 if h == HERO[0] else 72, method=6)
        jp = f'{out}/img/{h}.jpg'
        if os.path.exists(jp):
            os.remove(jp)
        rep(f'/img/{h}.jpg', f'/img/{h}.webp', s.count(f'/img/{h}.jpg') or 1) if False else None
        s = s.replace(f'/img/{h}.jpg', f'/img/{h}.webp')
    # preload the first slide (the biggest thing on screen), not a product card
    s = s.replace('<link rel="preload" as="image" href="/img/27d600c132.webp" fetchpriority="high">',
                  '<link rel="preload" as="image" href="/img/5d861a4924.webp" fetchpriority="high" type="image/webp">')
    s = s.replace('<img src="/img/5d861a4924.webp" alt="Brand model beside the EMS body sculpting machine" width="960" height="960" decoding="async" loading="eager">',
                  '<img src="/img/5d861a4924.webp" alt="Brand model beside the EMS body sculpting machine" width="960" height="960" decoding="async" loading="eager" fetchpriority="high">')
    # only the first product row loads straight away; the rest wait until scrolled to
    s = s.replace('loading="eager" fetchpriority="high"></div>', 'loading="eager"></div>')
    # skip layout work for sections far below the screen until they are needed
    css = (
           '.lead{margin:6px 0 10px;padding:14px 14px 12px;border-radius:12px;background:#fff;border:1px solid var(--line)}'
           '.lead h1{font-size:1.28rem;line-height:1.22;color:var(--navy);font-weight:800;margin:0 0 6px;letter-spacing:-.01em}'
           '.lead h1 em{font-style:normal;color:var(--blue)}'
           '.lead p{font-size:.86rem;color:var(--muted);line-height:1.45;margin:0}'
           '.lead ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 12px;padding:0}'
           '.lead li{font-size:.74rem;font-weight:700;color:var(--navy);background:#eef3fa;border-radius:20px;padding:5px 10px}'
           '.lead li.g{background:#fff8e8;box-shadow:inset 0 0 0 1px #f8b73f}'
           '.lead .lc{display:flex;gap:8px}.lead .lc a{flex:1;text-align:center;font-weight:800;font-size:.88rem;border-radius:22px;padding:11px 8px;text-decoration:none}'
           '.lead .l1{background:var(--blue);color:#fff}.lead .l2{background:#1fa855;color:#fff}'
           '@media(min-width:700px){.lead h1{font-size:1.6rem}.lead .lc{max-width:520px}}')
    s = s.replace('</style>', css + '</style>', 1)

    # slides 2-4 load straight away (low priority, ~180 KB together) so they're ready before the slider moves to them
    import re as _re
    for h in HERO[1:]:
        m = _re.search(r'<img src="/img/%s\.webp"[^>]*>' % h, s); assert m, h
        tag = m.group(0).replace(' loading="lazy"', '')
        tag = tag.replace('<img ', '<img loading="eager" fetchpriority="low" ', 1)
        s = s.replace(m.group(0), tag, 1)
    s = s.replace('</body>', "<script>(function(){var d=document.getElementById('ldl');if(d&&window.TA_PROMO)d.textContent='🚚 FREE delivery this week'})();</script>\n</body>", 1)
    # ---- 2. landing text (shows first, before the slider) ----
    lead = ('<section class="lead" aria-labelledby="lh"><h1 id="lh">Professional salon &amp; spa machines, <em>delivered anywhere in South Africa</em></h1>'
            '<p>161 EMS, cryo, RF, HIFU, facial and massage machines for salons and spas. Order on WhatsApp, pay in full or on lay-by, and get trained online for free.</p>'
            '<ul><li class="g">🛡️ 1-year warranty</li><li id="ldl">🚚 R150 delivery</li><li>🎓 Free online training</li><li>💳 Lay-by 2 or 3 months</li></ul>'
            '<div class="lc"><a class="l1" href="#ems">Shop machines</a>'
            '<a class="l2" href="https://wa.me/27611185978?text=' + quote('Hi Trimion Africa, I would like help choosing a machine for my salon.\n\nFull catalog (162 machines): https://trimionafrica.co.za/') +
            '" target="_blank" rel="noopener">Chat on WhatsApp</a></div></section>\n')
    anchor = '<section class="hs" aria-label="Featured">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, lead + anchor)

    # ---- 3. what WhatsApp shows when the site link is shared ----
    s = s.replace('<title>Trimion Africa Shop | Salon Equipment, Durban</title>',
                  '<title>Trimion Africa | Salon &amp; Spa Machines · 1-Year Warranty · R150 Delivery</title>')
    s = s.replace('<meta property="og:title" content="Trimion Africa Shop | Salon Equipment – 162 machines">',
                  '<meta property="og:title" content="Trimion Africa | 162 Salon &amp; Spa Machines">')
    s = s.replace('<meta name="twitter:title" content="Trimion Africa Shop | Salon Equipment – 162 machines">',
                  '<meta name="twitter:title" content="Trimion Africa | 162 Salon &amp; Spa Machines">')
    s = s.replace('content="Shop 162 salon machines online. 1-year warranty, R150 delivery anywhere in SA, free online training, lay-by over 2 or 3 months. Order on WhatsApp 061 118 5978."',
                  'content="EMS, cryo, RF, HIFU &amp; facial machines for salons and spas. 1-year warranty · R150 delivery anywhere in SA · free online training · lay-by over 2 or 3 months. Order on WhatsApp 061 118 5978."')
    s = s.replace('og.jpg?v=20', 'og.jpg?v=21')
    # "Share catalog" message
    s = s.replace('href="https://wa.me/?text=Trimion%20Africa%20salon%20machine%20catalog%3A%20https%3A%2F%2Ftrimionafrica.co.za%2F%3Fv%3D3"',
                  'href="https://wa.me/?text=' + quote(SHARE_TXT) + '"')
    s = s.replace("""navigator.share({title:'Trimion Africa catalog',text:'Trimion Africa salon machines: 1-year warranty, R150 delivery anywhere in SA, free online training.',url:"https://trimionafrica.co.za/?v=3"})""",
                  """navigator.share({title:'Trimion Africa | 162 salon & spa machines',text:'*Trimion Africa* | 162 professional salon & spa machines\\n1-year warranty · R150 delivery anywhere in SA · Free online training · Lay-by over 2 or 3 months\\nBrowse and order:',url:"https://trimionafrica.co.za/?v=4"})""")
    # ---- 4. first screen sooner: search-engine data moves to the end of the page, embedded icon becomes a file ----
    import re as _re
    m = _re.search(r'<script type="application/ld\+json">.*?</script>', s, _re.S)
    if m:
        ld = m.group(0); s = s.replace(ld, '', 1); s = s.replace('</body>', ld + '\n</body>', 1)
    s = _re.sub(r'<link rel="shortcut icon" href="data:image/x-icon;base64,[^"]*">', '<link rel="shortcut icon" href="/img/2f329d5478.png">', s)
    # ---- 5. the first picture gets the connection first; product photos wait their turn ----
    s = s.replace('<img src="/img/9e644e33f3.png" alt="" width="40" height="40">', '<img src="/img/4880f983c6.png" alt="" width="40" height="40">')
    s = _re.sub(r'(<div class="photo"><img [^>]*?)loading="eager"', r'\1loading="lazy"', s)
    s = _re.sub(r'(<div class="photo"><img )', r'\1fetchpriority="low" ', s)
    # ---- 6. search engines: robots.txt + sitemap ----
    import datetime as _dt
    open(f'{out}/robots.txt', 'w').write('User-agent: *\nAllow: /\nDisallow: /p/\n\nSitemap: https://trimionafrica.co.za/sitemap.xml\n')
    open(f'{out}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'<url><loc>https://trimionafrica.co.za/</loc><lastmod>{_dt.date.today().isoformat()}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n</urlset>\n')
    import shutil; shutil.copy('/home/claude/trimion-site/tools/sw.js', f'{out}/sw.js')
    for must in ['class="lead"', 'v=21', '%3Fv%3D4', '?v=4"})', '5d861a4924.webp" fetchpriority']:
        assert must in s, must
    return s
