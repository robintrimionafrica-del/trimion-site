#!/usr/bin/env python3
"""Google Shopping RSS 2.0 XML copy of /google-products.tsv at /google-products.xml (the Merchant Center feed).
Wording uses the same plain, claim-free terms as the Facebook catalog (fb_catalog.py SAFE list), and every item
declares no barcode (identifier_exists=no) and the flat R150 South Africa delivery."""
import csv, os, re
from xml.sax.saxutils import escape as e

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
rows = list(csv.DictReader(open(os.path.join(PUB, "google-products.tsv"), encoding="utf-8"), delimiter="\t"))

# Same substitutions as fb_catalog.py: avoids body-shaping / medical-sounding claims that ad and listing reviews flag.
SAFE = [(r"\bbody sculpting\b", "body care"), (r"\bsculpting\b", "salon"), (r"\bbody contouring\b", "body care"),
        (r"\bcontouring\b", "care"), (r"\bcontour\b", "care"), (r"\bskin tightening\b", "skin care"),
        (r"\bmuscle toning\b", "toning"), (r"\bmuscles?\b", "body"), (r"\bface lifting\b", "face care"),
        (r"\blifting\b", "care"), (r"\blift\b", "care"), (r"\bshaping\b", "care"), (r"\bshapes\b", "treats"),
        (r"\btherapy\b", "treatment")]
def safe(s):
    for pat, rep in SAFE:
        s = re.sub(pat, lambda m: rep.title() if m.group(0)[0].isupper() and m.group(0)[1:2].islower() else rep, s, flags=re.I)
    return re.sub(r"\b(Care|care) (Care|care)\b", r"\1", s)

items = []
for r in rows:
    items.append(f"""<item>
<g:id>{e(r['id'])}</g:id>
<title>{e(safe(r['title']))}</title>
<description>{e(safe(r['description']))}</description>
<link>{e(r['link'])}</link>
<g:image_link>{e(r['image_link'])}</g:image_link>
<g:price>{e(r['price'])}</g:price>
<g:availability>{e(r['availability'])}</g:availability>
<g:condition>{e(r['condition'])}</g:condition>
<g:brand>{e(r['brand'])}</g:brand>
<g:product_type>{e(r['product_type'])}</g:product_type>
<g:identifier_exists>no</g:identifier_exists>
<g:shipping><g:country>ZA</g:country><g:price>150.00 ZAR</g:price></g:shipping>
</item>""")
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n<channel>\n'
       '<title>Trimion Africa Precision</title>\n<link>https://trimionafrica.co.za</link>\n'
       '<description>Professional salon and spa machines, South Africa</description>\n'
       + "\n".join(items) + "\n</channel>\n</rss>\n")
open(os.path.join(PUB, "google-products.xml"), "w", encoding="utf-8").write(xml)
print(f"xml feed: {len(items)} products")
