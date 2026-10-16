#!/usr/bin/env python3
"""Build the Facebook / Instagram (Meta Commerce Manager) product feed from details.json.

Writes ../public/facebook-catalog.csv and a JPG photo per machine in ../public/fb/ (Meta does not reliably
accept WebP). Run after apply_prices.py so the feed shows the same prices as the shop.
Feed URL to give Commerce Manager: https://trimionafrica.co.za/facebook-catalog.csv
"""
import csv, json, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "public")
SITE = "https://trimionafrica.co.za"
D = json.load(open(os.path.join(HERE, "details.json")))

os.makedirs(os.path.join(PUB, "fb"), exist_ok=True)
rows = []
for d in D:
    price = int(re.sub(r"[^\d]", "", d["price"]))
    model = d["model"]
    jpg = f"fb/{model}.jpg"
    im = Image.open(os.path.join(PUB, d["img"].lstrip("/"))).convert("RGB")
    if min(im.size) < 600:
        im = im.resize((600, 600), Image.LANCZOS)
    im.save(os.path.join(PUB, jpg), "JPEG", quality=86, optimize=True, progressive=True)

    specs = [s for s in d.get("specs", []) if s.strip()]
    get = [g for g in d.get("get", []) if g.strip()]
    desc = " ".join(d["desc"])
    if specs:
        desc += "\n\nSpecifications:\n" + "\n".join("- " + s for s in specs)
    if get:
        desc += "\n\nIncluded:\n" + "\n".join("- " + g for g in get)
    if d.get("lb"):
        desc += f"\n\n{d['lb']} (balance over 2 or 3 months)."
    desc += "\n\nOrder on WhatsApp: 061 118 5978."

    rows.append({
        "id": model,
        "title": d["name"][:150],
        "description": desc[:9999],
        "availability": "in stock",
        "condition": "new",
        "price": f"{price}.00 ZAR",
        "link": f"{SITE}/p/m{d['k']}",
        "image_link": f"{SITE}/{jpg}",
        "brand": "Trimion Africa",
        "product_type": d["cat"],
        "shipping": "ZA::Standard:150.00 ZAR",
    })

out = os.path.join(PUB, "facebook-catalog.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"facebook catalog: {len(rows)} products")
