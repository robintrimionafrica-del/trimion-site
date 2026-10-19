#!/usr/bin/env python3
"""Google Shopping RSS 2.0 XML copy of /google-products.tsv at /google-products.xml.
Read hourly by the WhatsApp/website sales assistant (MyChatBot), which can't parse TSV."""
import csv, os
from xml.sax.saxutils import escape as e

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
rows = list(csv.DictReader(open(os.path.join(PUB, "google-products.tsv"), encoding="utf-8"), delimiter="\t"))
items = []
for r in rows:
    items.append(f"""<item>
<g:id>{e(r['id'])}</g:id>
<title>{e(r['title'])}</title>
<description>{e(r['description'])}</description>
<link>{e(r['link'])}</link>
<g:image_link>{e(r['image_link'])}</g:image_link>
<g:price>{e(r['price'])}</g:price>
<g:availability>{e(r['availability'])}</g:availability>
<g:condition>{e(r['condition'])}</g:condition>
<g:brand>{e(r['brand'])}</g:brand>
<g:product_type>{e(r['product_type'])}</g:product_type>
</item>""")
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n<channel>\n'
       '<title>Trimion Africa Precision</title>\n<link>https://trimionafrica.co.za</link>\n'
       '<description>Professional salon and spa machines, South Africa</description>\n'
       + "\n".join(items) + "\n</channel>\n</rss>\n")
open(os.path.join(PUB, "google-products.xml"), "w", encoding="utf-8").write(xml)
print(f"xml feed: {len(items)} products")
