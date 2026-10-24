#!/usr/bin/env python3
"""Plain cosmetic wording across the whole site (owner request 24/10/2026).
Replaces results / body-shaping claims ("body sculpting", "skin tightening", "fat freezing", "firmer", trademark-style
hashtags) with neutral salon wording. Nothing is removed: product ids, links, prices and photos stay the same.
  python3 safe_words.py data    -> cleans tools/products.json + details.json (so share pictures and brochures use it)
  python3 safe_words.py public  -> cleans every text file in ../public (html, js, json, csv, tsv, xml, txt, webmanifest)
"""
import os, re, sys, json
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "public")

# Order matters: specific phrases first, single words last.
RULES = [
    # hashtags (also drops the trademark-style #emsculpt)
    (r"#emsculpt\b", "#emsmachine"), (r"#bodysculpting\b", "#bodycare"), (r"#bodycontouring\b", "#bodycare"),
    (r"#rfskintightening\b", "#rfmachine"), (r"#skintightening\b", "#skincare"), (r"#medspa\b", "#dayspa"),
    (r"#fatfreezing\b", "#cryomachine"), (r"#cryolipolysis\b", "#cryomachine"), (r"#weightloss\b", "#selfcare"),
    (r"#slimming\b", "#bodycare"), (r"#\w*sculpt\w*", "#bodycare"), (r"#\w*contour\w*", "#bodycare"),
    (r"\bbutt lift look\b", "glute care"), (r"\bbutt lift\b", "glute care"), (r"\bmicro lift\b", "microcurrent"), (r"#facelift(ing)?\b", "#facecare"), (r"#lipo\w*", "#bodycare"), (r"#fat\w*", "#bodycare"),
    (r"#hydra_?facials?\b", "#waterdermabrasion"), (r"\bhydra[ -]?facial machine\b", "water dermabrasion machine"), (r"\bhydra[ -]?facials?\b", "water dermabrasion facial"),
    # medical-device status is not yet confirmed per model (SAHPRA Rule 9), so never state "not a medical device"
    (r"\bThey are not medical devices and are not intended to\b", "They are for cosmetic use and are not intended to"),
    (r"\bthey are not medical devices and are not intended to\b", "they are for cosmetic use and are not intended to"),
    (r"\bnot medical devices and are not intended to\b", "for cosmetic use and are not intended to"),
    (r"\bNot medical devices and not intended to\b", "For cosmetic use only and not intended to"),
    (r"\bNot a medical device and not intended to\b", "For cosmetic use only and not intended to"),
    (r"<b>Salon and spa use</b>Not a medical device", "<b>Salon and spa use</b>Cosmetic treatments only"),
    (r"\bNot a medical device\b", "For cosmetic use only"),
    # throughput / income claims
    (r"Large double-coil handles cover more of the body per session, so you can book more clients a day\.", "Large double-coil applicators."),
    (r",? so you can book more clients a day", ""),
    (r"See how quickly a machine can pay for itself\. Enter your own session price and bookings; these are your figures, not a promise of results\.",
     "Work out your own numbers. Enter your session price, bookings and costs; these are your own estimates, not a promise of income or results."),
    (r"<h2>Salon earnings calculator</h2>", "<h2>Salon numbers calculator</h2>"),
    (r"See how fast a salon machine pays for itself, lay-by prices and answers to common questions\.", "Salon machine prices, lay-by options and answers to common questions."),
    (r"\bStart earning sooner\b", "Lay-by available"),
    # toning (results wording)
    (r"\belectromagnetic muscle applicators?\b", "electromagnetic applicators"),
    (r"\bfor body toning treatments\b", "for body treatments"), (r"\bglute and core (?:muscle |body )?toning\b", "glute and core sessions"),
    (r"\bmuscle toning station\b", "body station"), (r"\bbody toning station\b", "body station"),
    (r"\bmuscle toning\b", "body care"), (r"\babs and core toning\b", "abs and core sessions"), (r"\bbody toning\b", "body care"), (r"#\w*toning\w*", "#bodycare"),
    (r"\btoning\b", "care"),
    # fat / weight / cellulite
    (r"\bcryo fat freezing\b", "cryo machine"), (r"\bfat[- ]freezing\b", "cryo"), (r"\bfat (reduction|loss|burning)\b", "body care"),
    (r"\bweight[- ]loss\b", "body care"), (r"\bweight management\b", "body care"), (r"\bslimming\b", "body care"),
    (r"\bcellulite look\b", "smooth-looking skin"), (r"\bcellulite\b", "skin texture"),
    (r"\blymphatic and body massage\b", "body massage"), (r"\blymph(atic)? drainage\b", "relaxing massage"),
    (r"\blove handles\b", "sides"), (r"\bdouble chin\b", "chin area"), (r"\bstubborn areas\b", "selected areas"),
    # sculpting
    (r"\bEM sculpting\b", "EM body care"), (r"\bbody sculpting\b", "body care"), (r"\bface sculpting\b", "face care"),
    (r"\bsmooth & sculpt\b", "smooth & relax"), (r"\bsculpting (station|machine|system)\b", r"body \1"),
    (r"\bsculpting\b", "body care"), (r"\bsculpt\b", "care"),
    # contouring / shaping
    (r"\bbody and face contouring\b", "body and face"), (r"\bbody contouring\b", "body care"), (r"\bface contouring\b", "face care"),
    (r"\bcontouring\b", "body care"), (r"\bbody shaping\b", "body care"), (r"\bshaping\b", "care"),
    # tightening / lifting / firming
    (r"\bskin tightening\b", "skin care"), (r"\bHIFU tightening\b", "HIFU skin care"), (r"\btightening\b", "skin care"),
    (r"\bface lifting\b", "face care"), (r"\bface and jawline lift\b", "face and jawline care"),
    (r"\blifted, firmer skin\b", "refreshed-looking skin"), (r"\bfor a lifted, firmer look\b", "for a refreshed look"),
    (r"\blifted, firmer\b", "refreshed"), (r"\bneck firming\b", "neck care"), (r"\bfirm, toned look\b", "relaxing body sessions"),
    (r"(?<!contractions that )\btone and firm\b", "care for"), (r"\bfirming\b", "care"), (r"\bfirmer\b", "refreshed"),
    # muscle
    (r"\belectromagnetic muscle contractions that tone and firm\b", "electromagnetic stimulation sessions for"),
    (r"\belectromagnetic muscle contractions\b", "electromagnetic stimulation"), (r"\belectromagnetic muscle stimulation\b", "electromagnetic stimulation"),
    (r"\bmuscle toning\b", "body toning"),
]
COMP = [(re.compile(p, re.I), r) for p, r in RULES]

def _case(src, rep):
    if src[:1].isupper() and rep[:1].isalpha():
        if src.isupper() and len(src) > 3:
            return rep.upper()
        words_cap = all(w[:1].isupper() for w in re.findall(r"[A-Za-z]+", src))
        return rep.title() if words_cap and len(src.split()) > 1 else rep[:1].upper() + rep[1:]
    return rep

def clean(s):
    for rx, rep in COMP:
        s = rx.sub(lambda m: _case(m.group(0), m.expand(rep)), s)
    s = re.sub(r"\b(Body Care|body care) (Body Care|body care)\b", r"\1", s)
    s = re.sub(r"\b(Care|care) (Care|care)\b", r"\1", s)
    s = re.sub(r"\bbody body\b", "body", s, flags=re.I)
    s = re.sub(r"(#\w+)((?:\s+#\w+)*?)\s+\1\b", r"\1\2", s)
    s = re.sub(r"(#\w+)((?:\s+#\w+)*?)\s+\1\b", r"\1\2", s)
    return s

def clean_text(s):
    s = clean(s)
    # URL-encoded copies (WhatsApp pre-filled messages use %20 between words)
    def enc(m):
        raw = m.group(0)
        try:
            from urllib.parse import unquote
            dec = unquote(raw)
        except Exception:
            return raw
        new = clean(dec)
        return raw if new == dec else quote(new, safe="")
    return re.sub(r"(?:[A-Za-z0-9._~-]|%[0-9A-Fa-f]{2}){12,}", lambda m: enc(m) if "%20" in m.group(0) else m.group(0), s)

def walk(o):
    if isinstance(o, str): return clean(o)
    if isinstance(o, list): return [walk(x) for x in o]
    if isinstance(o, dict): return {k: (walk(v) if k not in ("img", "s", "sid", "slug", "url", "link") else v) for k, v in o.items()}
    return o

def data():
    for f in ("products.json", "details.json"):
        p = os.path.join(HERE, f)
        json.dump(walk(json.load(open(p, encoding="utf-8"))), open(p, "w", encoding="utf-8"), indent=1)
    print("safe words: product data cleaned")

EXT = (".html", ".js", ".json", ".csv", ".tsv", ".xml", ".txt", ".webmanifest")
def public():
    n = 0
    for root, _, files in os.walk(PUB):
        for f in files:
            if not f.endswith(EXT): continue
            p = os.path.join(root, f)
            try: s = open(p, encoding="utf-8").read()
            except UnicodeDecodeError: continue
            t = clean_text(s)
            if t != s:
                open(p, "w", encoding="utf-8").write(t); n += 1
    print(f"safe words: {n} public files updated")

if __name__ == "__main__":
    {"data": data, "public": public}[sys.argv[1] if len(sys.argv) > 1 else "public"]()
