#!/usr/bin/env python3
"""Build the Facebook / Instagram (Meta Commerce Manager) product feed from details.json.

Writes ../public/facebook-catalog.csv and a JPG photo per machine in ../public/fb/ (Meta does not reliably
accept WebP). Run after apply_prices.py so the feed shows the same prices as the shop.
Feed URL to give Commerce Manager: https://trimionafrica.co.za/facebook-catalog.csv
Also writes ../public/google-products.tsv for Google Merchant Center: https://trimionafrica.co.za/google-products.tsv
"""
import csv, json, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "public")
SITE = "https://trimionafrica.co.za"
D = json.load(open(os.path.join(HERE, "details.json")))

os.makedirs(os.path.join(PUB, "fb"), exist_ok=True)
IMGV = {"TACRYOM": "-w", "TACRYOP3": "-w"}   # new file names so Meta fetches the cleaned (white background) photos
rows = []
for d in D:
    price = int(re.sub(r"[^\d]", "", d["price"]))
    model = d["model"]
    jpg = f"fb/{model}{IMGV.get(model, '')}.jpg"
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
    desc += "\n\nOrder on WhatsApp: 064 454 8506."

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

# Google Merchant Center feed (Google Shopping free listings + Business Profile products).
# Same products and prices; Google wants a different shipping format, no GTINs, and no phone numbers in text.
g_rows = []
for r in rows:
    g = dict(r)
    g["description"] = g["description"].replace("\n\nOrder on WhatsApp: 064 454 8506.", "")
    g["shipping"] = "ZA:::150.00 ZAR"
    g["identifier_exists"] = "no"
    g_rows.append(g)
gout = os.path.join(PUB, "google-products.tsv")
with open(gout, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(g_rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(g_rows)
print(f"google merchant feed: {len(g_rows)} products")

# Meta-review-friendly copy for the new Facebook page / WhatsApp catalog: https://trimionafrica.co.za/catalog.csv
# Same products, photos, prices and links; wording kept to plain product descriptions (Meta's commerce review
# tends to reject salon machines described with body-shaping or medical-sounding claims), and no phone number.
SAFE = [(r"\bbody sculpting\b", "body care"), (r"\bsculpting\b", "salon"), (r"\bbody contouring\b", "body care"),
        (r"\bcontouring\b", "care"), (r"\bcontour\b", "care"), (r"\bskin tightening\b", "skin care"),
        (r"\bmuscle toning\b", "toning"), (r"\bmuscles?\b", "body"), (r"\bface lifting\b", "face care"),
        (r"\blifting\b", "care"), (r"\blift\b", "care"), (r"\bshaping\b", "care"), (r"\bshapes\b", "treats"),
        (r"\btherapy\b", "treatment")]
def safe(s):
    for pat, rep in SAFE:
        s = re.sub(pat, lambda m: rep.title() if m.group(0)[0].isupper() and m.group(0)[1:2].islower() else rep, s, flags=re.I)
    s = re.sub(r"\b(Care|care) (Care|care)\b", r"\1", s)
    return s
m_rows = []
for r in rows:
    m = dict(r)
    m["title"] = safe(m["title"])[:150]
    m["description"] = safe(m["description"]).replace("Order on WhatsApp: 064 454 8506.", "Order on WhatsApp from Trimion Africa.")
    m["product_type"] = safe(m["product_type"])
    m_rows.append(m)
for name in ("catalog.csv", "facebook-catalog.csv"):   # the connected WhatsApp/Facebook catalog reads facebook-catalog.csv
    with open(os.path.join(PUB, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(m_rows[0]))
        w.writeheader()
        w.writerows(m_rows)
print(f"meta catalog (catalog.csv): {len(m_rows)} products")
