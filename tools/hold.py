#!/usr/bin/env python3
"""'Available on request' for machines whose SAHPRA status is not yet checked (owner decision 24/10/2026).
Nothing is deleted: every page, photo and link stays. For held machines:
  - no price, lay-by or discount is shown; the button becomes a WhatsApp enquiry
  - they are left out of the Google Shopping and Facebook/Instagram catalog feeds and the classifieds/posting packs
  - search-engine data carries no offer/price
To release a model once its documents are verified, add its model code to RELEASED below and rebuild.
  python3 hold.py data    -> products.json / details.json (run after apply_prices + safe_words data)
  python3 hold.py public  -> built pages and feeds (run near the end of rebuild.sh)
"""
import csv, io, json, os, re, sys
from urllib.parse import quote

T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, "..", "public")
HELD_SECTIONS = {"ems", "cryo", "rf", "hifu", "face", "massage"}
RELEASED = set()          # model codes cleared for promotion, e.g. {"TAXXXX"}
ONREQ = "Available on request"
WA = "https://wa.me/27644548506?text="

P = json.load(open(os.path.join(T, "products.orig.json")))
HELD = {p["k"]: p for p in P if p["sid"] in HELD_SECTIONS and p["model"] not in RELEASED}
HELD_MODELS = {p["model"] for p in HELD.values()}

def data():
    for f in ("products.json", "details.json"):
        path = os.path.join(T, f); L = json.load(open(path, encoding="utf-8"))
        for d in L:
            if d["k"] in HELD:
                d["price"] = "Price on request"; d["lb"] = ""; d["onreq"] = True
        json.dump(L, open(path, "w", encoding="utf-8"), indent=1)
    print(f"hold: {len(HELD)} machines set to on request in product data")

def enq(name, model):
    t = f"Hi Trimion Africa, I'd like information about the {name} ({model}). Is it available?"
    return f'<a class="btn" href="{WA}{quote(t, safe="")}" target="_blank" rel="noopener">Ask on WhatsApp</a>'

def home(s):
    def card(m):
        k = int(m.group(1)); b = m.group(2)
        if k not in HELD: return m.group(0)
        p = HELD[k]
        b = re.sub(r'<div class="price">R[\d,]+</div>(\s*<a class="lb" href="[^"]*"[^>]*>.*?</a>)?', f'<div class="price por">{ONREQ}</div>', b, count=1, flags=re.S)
        b = re.sub(r'<a class="btn" href="https://wa\.me/[^"]*"[^>]*>[^<]*</a>', lambda _: enq(p["name"], p["model"]), b, count=1)
        b = re.sub(r'<[^>]*class="[^"]*(?:was|save|disc|off|deal)[^"]*"[^>]*>[^<]*</[a-z]+>', '', b)   # strike-through / discount badges
        return m.group(0)[:m.start(2) - m.start(0)] + b + "</article>"
    return re.sub(r'<article class="card[^"]*" data-k="(\d+)"[^>]*>(.*?)</article>', card, s, flags=re.S)

def strip_offers(s):
    for model in HELD_MODELS:
        i = s.find(f'"sku":"{model}"')
        while i >= 0:
            end = s.find('"sku":', i + 6); end = len(s) if end < 0 else end
            j = s.find(',"offers":{', i)
            if 0 <= j < end:
                depth, q = 0, j + len(',"offers":')
                for q in range(q, len(s)):
                    if s[q] == "{": depth += 1
                    elif s[q] == "}":
                        depth -= 1
                        if depth == 0: break
                s = s[:j] + s[q + 1:]
            i = s.find(f'"sku":"{model}"', i + 6)
    return s

def feeds():
    n = 0
    for f, delim in (("google-products.tsv", "\t"), ("facebook-catalog.csv", ","), ("catalog.csv", ",")):
        p = os.path.join(PUB, f)
        if not os.path.exists(p): continue
        rows = list(csv.reader(open(p, encoding="utf-8", newline=""), delimiter=delim))
        idc = rows[0].index("id") if "id" in rows[0] else 0
        keep = [rows[0]] + [r for r in rows[1:] if r and r[idc] not in HELD_MODELS]
        out = io.StringIO(); csv.writer(out, delimiter=delim, lineterminator="\n").writerows(keep)
        open(p, "w", encoding="utf-8").write(out.getvalue()); n += len(rows) - len(keep)
    p = os.path.join(PUB, "google-products.xml")
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"<item>\s*<g:id>([^<]*)</g:id>.*?</item>\n?", lambda m: "" if m.group(1) in HELD_MODELS else m.group(0), s, flags=re.S)
        open(p, "w", encoding="utf-8").write(s)
    return n

def posting_pages():
    """Owner's posting pages (/media, /media/today): drop the held machines' post cards."""
    n = 0
    rx = re.compile("|".join(re.escape(m) for m in sorted(HELD_MODELS, key=len, reverse=True)))
    for rel in ("media/index.html", "media/today/index.html"):
        p = os.path.join(PUB, rel)
        if not os.path.exists(p): continue
        s = open(p, encoding="utf-8").read()
        def art(m):
            return "" if re.search(r"\b(" + rx.pattern + r")\b", m.group(0)) else m.group(0)
        t = re.sub(r"<article\b.*?</article>", art, s, flags=re.S)
        def sec(m):
            k = m.group(0).count("<article")
            if k == 0: return ""
            return re.sub(r"(<h2>[^<(]*)\(\d+\)", lambda h: f"{h.group(1)}({k})", m.group(0), count=1)
        t = re.sub(r"<section id=\"[^\"]+\">.*?</section>", sec, t, flags=re.S)
        if t != s: open(p, "w", encoding="utf-8").write(t); n += 1
    p = os.path.join(PUB, "vs.json")
    if os.path.exists(p):
        V = json.load(open(p, encoding="utf-8"))
        for v in V:
            if v.get("k") in HELD: v["p"] = ONREQ
        json.dump(V, open(p, "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    return n

def public():
    p = os.path.join(PUB, "index.html"); s = open(p, encoding="utf-8").read()
    s = strip_offers(home(s)); open(p, "w", encoding="utf-8").write(s)
    for k in HELD:
        f = os.path.join(PUB, "p", f"m{k}.html")
        if os.path.exists(f):
            t = open(f, encoding="utf-8").read(); open(f, "w", encoding="utf-8").write(strip_offers(t))
    print(f"hold: home cards + {len(HELD)} product pages on request; {feeds()} feed rows held back; {posting_pages()} posting pages trimmed")

if __name__ == "__main__":
    {"data": data, "public": public}[sys.argv[1] if len(sys.argv) > 1 else "public"]()
