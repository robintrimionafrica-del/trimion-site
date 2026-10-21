"""Trust section (facts only), review invitation, category intro text, and richer search data
(FAQ, return policy, warranty). Called from enhance.apply()."""
import re, json
from urllib.parse import quote

INTRO = {
    'ems': 'Electromagnetic and EMS body sculpting machines with 1 to 6 handles, from compact tabletop units to tall floor stations, with or without RF.',
    'cryo': 'Cryo body contouring machines and stations with 360° cooling cups, plus combined cryo and electromagnetic units.',
    'rf': '448kHz CET/RET, vacuum, roller and cavitation machines for body and face contouring sessions.',
    'hifu': 'HIFU skin tightening machines from portable 4D units to 7D and 9D stations, with face and body cartridges.',
    'massage': 'Vacuum roller, vibration, cupping and pressotherapy systems for lymphatic and body massage sessions.',
    'face': 'Water dermabrasion, oxygen, CO2 bubble, RF and microcurrent facial machines and stations.',
    'salon': 'Massage chairs, sauna domes, hair dryers and body analysers to complete your salon or spa.',
    'supplies': 'Gels, solutions and cryo membranes for the machines in this catalog.',
}

TRUST = (
    '<div class="trust" id="trust" role="region" aria-labelledby="trh"><h2 id="trh">Why salons buy from Trimion Africa</h2>'
    '<div class="tg">'
    '<div><b>Registered South African company</b>Trimion Africa Precision (Pty) Ltd · CIPC 2026/806671/07 · 117 Stephen Dlamini Road, Durban</div>'
    '<div><b>1-year warranty</b>On the machine, 6 months on handpieces, written on your invoice. Plus your Consumer Protection Act rights.</div>'
    '<div><b>7-day cooling-off</b>Changed your mind? Cancel within 7 days of delivery under the ECT Act.</div>'
    '<div><b>Pay safely</b>EFT to the details on your Trimion invoice or a secure card link. We never ask for card numbers on WhatsApp.</div>'
    '<div><b>Trained to use it</b>Free online operational training with every machine. In-person training available.</div>'
    '<div><b>Real people on WhatsApp</b>064 454 8506 · robin.trimionafrica@gmail.com · replies within 2 business days for complaints</div>'
    '</div>'
    '<div class="rv"><b>Bought a machine from us?</b><span>Your review helps other salon owners choose with confidence.</span>'
    '<a href="https://wa.me/27644548506?text=' + quote('Hi Trimion Africa, I would like to leave a review for my machine.\n\nMachine:\nMy review:\nCan you show my salon name? Yes / No\n\nFull catalog (162 machines): https://trimionafrica.co.za/') +
    '" target="_blank" rel="noopener">Leave a review on WhatsApp</a></div>'
    '</div>\n')

CSS = ('.cintro{grid-column:1/-1;width:100%;max-width:none;font-size:.84rem;color:var(--muted);margin:-4px 0 10px;line-height:1.45}'
       '.trust{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 14px;margin:18px 0}'
       '.trust h2{margin:0 0 10px}'
       '.tg{display:grid;grid-template-columns:1fr;gap:8px}@media(min-width:700px){.tg{grid-template-columns:1fr 1fr 1fr}}'
       '.tg div{background:var(--bg);border-radius:10px;padding:10px 12px;font-size:.8rem;color:var(--muted);line-height:1.45}'
       '.tg b{display:block;color:var(--navy);font-size:.9rem;margin-bottom:2px}'
       '.rv{margin-top:12px;border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:4px}'
       '.rv b{color:var(--navy)}.rv span{font-size:.82rem;color:var(--muted)}'
       '.rv a{align-self:flex-start;margin-top:6px;background:#1fa855;color:#fff;font-weight:800;font-size:.86rem;border-radius:20px;padding:9px 16px;text-decoration:none}')


def apply(s):
    s = s.replace('</style>', CSS + '</style>', 1)
    # category intros under each heading (helps Google and buyers)
    for sid, text in INTRO.items():
        s, n = re.subn(r'(<section id="%s"><h2>.*?</h2>)' % sid, r'\1<p class="cintro">' + text + '</p>', s, count=1)
        assert n == 1, sid
    # trust section just before the questions
    anchor = '<div class="faq" id="faq">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, TRUST + anchor)
    # search data: FAQ page, return policy, description
    faq = re.search(r'<div class="faq" id="faq">(.*?)</div>\s*<p class="note">', s, re.S).group(1)
    qa = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', faq, re.S)
    strip = lambda t: re.sub(r'<[^>]+>', '', t).replace('&amp;', '&').replace('&quot;', '"').strip()
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
              'mainEntity': [{'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in qa]}
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    d = json.loads(m.group(2))
    store = next(x for x in d['@graph'] if x.get('@type') == 'Store')
    store['description'] = ('Professional salon and spa machines for South Africa: EMS and electromagnetic sculpting, cryo, RF and cavitation, '
                            'HIFU, massage and facial machines. 1-year warranty, R150 nationwide delivery, free online training and lay-by.')
    store['hasMerchantReturnPolicy'] = {'@type': 'MerchantReturnPolicy', 'applicableCountry': 'ZA',
                                        'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
                                        'merchantReturnDays': 14, 'returnMethod': 'https://schema.org/ReturnByMail',
                                        'returnFees': 'https://schema.org/ReturnShippingFees'}
    ship = {'@type': 'OfferShippingDetails', 'shippingRate': {'@type': 'MonetaryAmount', 'value': '150', 'currency': 'ZAR'},
            'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'ZA'},
            'deliveryTime': {'@type': 'ShippingDeliveryTime',
                             'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 3, 'unitCode': 'DAY'},
                             'transitTime': {'@type': 'QuantitativeValue', 'minValue': 8, 'maxValue': 9, 'unitCode': 'DAY'}}}
    for g in d['@graph']:
        if g.get('@type') == 'ItemList':
            for it in g['itemListElement']:
                o = it['item'].get('offers')
                if o:
                    o['shippingDetails'] = ship
    new = m.group(1) + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + m.group(3) + \
        '<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False, separators=(',', ':')) + '</script>'
    s = s[:m.start()] + new + s[m.end():]
    return s
