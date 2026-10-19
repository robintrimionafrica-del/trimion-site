"""Selling price = (Alibaba item price + shipping to SA) + customs/VAT -> tiered 35-50% markup.
Item price: Trimion's own 21 listed prices (Alibaba rand prices) or, for the other 143, estimated USD factory prices.
Real quotes in ACTUAL override the estimate.
Basis: Made-in-China.com listing ranges (14 Oct 2026), scaled to Alibaba factory level using
Trimion's own 21 listed prices (which work out to ~26x the USD factory price)."""
import json, math

RATE = 16.46          # USD->ZAR, currencyconvert.online, 14 Oct 2026 05:00 UTC (16.4573)
# Shipping China -> South Africa per unit (Alibaba Logistics / FedEx, DAP), by size of machine.
# Real quotes (15 Oct 2026): tabletop RF face machine R6,395, 6-in-1 cavitation R5,438.
SHIP = {'small': 1800, 'table': 5500, 'floor': 8500}
SHIP_C = 0.30         # consumables: shipping as a share of the item price
CUSTOMS = 0.15        # VAT/customs paid on arrival (DAP), on item + shipping

# Real Alibaba costs Trimion was quoted, item + shipping to SA in rand (customs added on top)
ACTUAL = {103: 10409 + 6395 + 502,   # TARFUS1: checkout R17,306 incl. fees
          73: round(900 * 16.46),    # TAEMC2: US$900 shipped to SA
          112: 21967 + 5438,         # TACAV6S: R21,967 + R5,438 Alibaba Logistics
          34: round((4700 + 1450) * 16.46),   # TACRYO360-4: US$4,700 + US$1,450 DHL (Maggie Hou)
          35: round((3800 + 750) * 16.46),    # TACRYO360-2: US$3,800 + US$750 DHL (Maggie Hou)
          7: round((5950 + 1450) * 16.46)}    # TACRYOEM: US$5,950 + US$1,450 DHL (Maggie Hou)
# Tiered markup on landed cost: 50% on cheaper machines, sliding down to 35% on the most expensive.
MARKUP_HI, MARKUP_LO = 0.50, 0.35
TIER_FROM, TIER_TO = 15000, 80000   # landed cost (R) where the slide starts and ends
ROUND = 50

# Trimion's own listed prices = the Alibaba item price in rand (before shipping, customs and markup)
OWN = {1: 143750, 2: 127650, 3: 43000, 4: 22000, 5: 20950, 6: 7500, 17: 44850, 31: 60399, 32: 17450, 33: 17000,
       41: 13199, 42: 101150, 43: 6450, 50: 18599, 51: 10999, 52: 6900, 58: 49950, 67: 35999, 68: 12899, 69: 39999, 70: 6999}

def markup(landed):
    if landed <= TIER_FROM: return MARKUP_HI
    if landed >= TIER_TO: return MARKUP_LO
    return MARKUP_HI - (MARKUP_HI - MARKUP_LO) * (landed - TIER_FROM) / (TIER_TO - TIER_FROM)

def sell(landed):
    return int(math.ceil(landed * (1 + markup(landed)) / ROUND) * ROUND)

# k: (usd, confidence, basis)
EMS = 'Made-in-China EM sculpting (Hiemt/Emslim) listings US$1,150-5,800; your 2-handle R20,950 and 4-handle R43,000 as anchors'
CRY = 'Made-in-China cryo listings: 360 4-handle US$2,130-5,000, 360 with chin handle US$1,330-1,600; your cryo station R17,450 as anchor'
RFC = 'Made-in-China cavitation/RF listings US$120-4,500; your 4-in-1 cavitation R6,450 and 448K RF R13,199 as anchors'
TEC = 'Made-in-China 448kHz / CET-RET (Tecar) listings US$350-3,300; your 448K RF R13,199 as anchor'
HIF = 'Made-in-China HIFU listings: 4D US$975-1,200, 7D/9D US$1,350-2,350, portable 9D US$1,367-1,563'
PRS = 'Made-in-China pressotherapy listings: 24 airbags US$699-999, EMS + far infrared US$439-599, suits US$800-1,300'
VRL = 'Made-in-China vacuum roller listings US$1,100-4,200; your 360 roller R18,599 as anchor'
HYD = 'Made-in-China hydra/oxygen facial listings US$389-4,000; your 8-in-1 dermabrasion R49,950 as anchor'
SML = 'Made-in-China small facial machines (CO2 bubble US$190-630, hydra 6-10 in 1 US$120-950, steamers US$24-52)'
P = {
 7: (2600, 'Medium', 'Cryo + EM combo; ' + CRY),
 8: (1650, 'High', EMS), 9: (1650, 'High', EMS), 10: (1900, 'Medium', EMS + '; seat pad adds ~US$250'),
 11: (1650, 'High', EMS), 12: (1900, 'Medium', EMS + '; seat pad adds ~US$250'),
 13: (1450, 'High', EMS), 14: (800, 'High', EMS), 15: (1650, 'High', EMS), 16: (850, 'High', EMS),
 18: (950, 'High', EMS), 19: (1750, 'High', EMS), 20: (1550, 'High', EMS), 21: (1450, 'High', EMS),
 22: (800, 'High', EMS), 23: (1850, 'Medium', EMS), 24: (750, 'High', EMS), 25: (1900, 'Medium', EMS),
 26: (1900, 'Medium', EMS + '; priced as 4-handle'), 27: (1000, 'Medium', EMS + '; water cooling'),
 28: (850, 'Medium', EMS + '; water cooling'), 29: (1900, 'Medium', EMS), 30: (2300, 'Medium', EMS + '; 6 handles'),
 71: (1650, 'High', EMS), 72: (450, 'Medium', EMS), 73: (780, 'High', EMS), 74: (900, 'High', EMS + '; +RF'),
 75: (780, 'High', EMS), 76: (900, 'High', EMS + '; +RF'), 77: (1400, 'High', EMS), 78: (1600, 'High', EMS + '; +RF'),
 79: (900, 'High', EMS), 80: (1600, 'High', EMS), 81: (1800, 'High', EMS + '; +RF'),
 82: (380, 'Medium', EMS), 83: (450, 'Medium', EMS + '; +RF'), 84: (800, 'High', EMS), 85: (920, 'High', EMS + '; +RF'),
 86: (1550, 'High', EMS), 87: (1750, 'High', EMS + '; +RF'), 88: (1050, 'High', EMS + '; +RF'), 89: (1850, 'High', EMS + '; +RF'),
 90: (1700, 'High', EMS), 91: (1900, 'High', EMS + '; +RF'), 92: (800, 'High', EMS), 93: (1500, 'High', EMS),
 94: (1650, 'High', EMS + '; +EMS'), 95: (900, 'High', EMS), 96: (1600, 'High', EMS), 97: (1750, 'High', EMS + '; +EMS'),
 98: (1900, 'Medium', EMS), 99: (950, 'High', EMS),
 34: (1500, 'Medium', CRY), 35: (850, 'Medium', CRY), 36: (2400, 'Medium', 'Cryo + EM combo; ' + CRY), 37: (800, 'High', CRY),
 38: (1300, 'Medium', CRY), 39: (900, 'Medium', CRY), 40: (650, 'Medium', CRY), 100: (750, 'Medium', CRY),
 44: (1900, 'Low', VRL + '; multi-applicator platform'), 45: (700, 'Medium', TEC), 46: (600, 'Medium', TEC),
 47: (1200, 'Low', 'Made-in-China EMS+RF face machines US$2,099-2,299'), 48: (350, 'Medium', RFC), 49: (220, 'Medium', RFC),
 101: (450, 'Medium', TEC), 102: (750, 'Medium', TEC), 103: (650, 'Low', RFC), 104: (700, 'Low', RFC), 105: (1100, 'Low', RFC),
 106: (450, 'Medium', RFC), 107: (120, 'Medium', RFC), 108: (160, 'Medium', RFC), 109: (380, 'Medium', RFC),
 110: (650, 'Medium', RFC), 111: (650, 'Medium', RFC), 112: (500, 'Medium', RFC), 113: (550, 'Medium', RFC), 114: (350, 'Medium', RFC),
 115: (1400, 'Medium', VRL), 116: (1250, 'Medium', VRL), 117: (1500, 'Medium', VRL),
 118: (1300, 'Low', 'Non-contact RF frame; Made-in-China RF body listings US$1,000-4,500'),
 119: (120, 'Medium', RFC), 120: (350, 'Medium', RFC), 121: (750, 'Medium', RFC),
 122: (900, 'Low', 'Made-in-China cartridge / fractional RF listings US$419-2,800'),
 123: (750, 'Medium', HIF), 124: (850, 'Medium', HIF), 125: (700, 'Medium', HIF), 126: (600, 'Medium', HIF), 127: (650, 'Medium', HIF),
 128: (800, 'Medium', HIF), 129: (1000, 'Medium', HIF), 130: (950, 'Medium', HIF), 131: (1100, 'Medium', HIF), 132: (950, 'Medium', HIF),
 133: (900, 'Medium', HIF),
 53: (1600, 'Medium', VRL), 54: (1450, 'Medium', VRL), 55: (1000, 'Medium', VRL),
 56: (380, 'Medium', PRS), 57: (480, 'Medium', PRS), 134: (380, 'Medium', PRS), 135: (380, 'Medium', PRS), 136: (520, 'Medium', PRS),
 137: (450, 'Medium', PRS), 138: (330, 'Medium', PRS), 139: (350, 'Medium', PRS), 140: (480, 'Medium', PRS), 141: (600, 'Medium', PRS),
 142: (680, 'Medium', PRS),
 59: (1200, 'Low', 'Ion + microcurrent floor platform; few comparable listings'), 60: (1100, 'Medium', HYD), 61: (1400, 'Medium', HYD),
 62: (1400, 'Medium', HYD), 63: (900, 'Medium', HYD), 64: (900, 'Medium', HYD), 65: (600, 'Medium', HYD),
 66: (1400, 'Low', 'EM + RF face patches (EMface type); Made-in-China EMS RF face US$2,099-2,299'),
 143: (90, 'Medium', SML), 144: (180, 'Medium', SML), 145: (180, 'Medium', SML), 146: (230, 'Medium', SML), 147: (230, 'Medium', SML),
 148: (200, 'Medium', SML), 149: (230, 'Medium', SML), 150: (260, 'Medium', SML), 151: (280, 'Medium', SML), 152: (450, 'Medium', SML),
 153: (520, 'Medium', SML), 154: (600, 'Medium', SML), 155: (480, 'Medium', SML), 156: (520, 'Medium', SML), 157: (420, 'Medium', SML),
 158: (350, 'Medium', SML),
 159: (800, 'Medium', 'Made-in-China body composition analysers US$499-1,500 (with printer US$800-1,500)'),
 160: (2.5, 'Medium', 'Made-in-China conductive / ultrasound gel US$0.30-6 per bottle'),
 161: (10, 'Low', 'Made-in-China aqua peel solution sets (AS1/SA2/AO3) US$8-9 per set'),
 162: (12, 'Low', 'Made-in-China aqua peel solution sets US$6-9; 4-bottle set'),
 163: (10, 'Low', 'CO2 bubble gel kits; few listings show prices'),
 164: (80, 'Medium', 'Made-in-China cryo membranes US$0.60-1.10 each; pack of 100'),
 165: (2600, 'High', 'Weifang Mingliang (Domi) dealer quote 16 Oct 2026: C2 dual-handle US$2,600'),
 166: (3100, 'High', 'Weifang Mingliang (Domi) dealer quote 16 Oct 2026: C2 four-handle US$3,100'),
 167: (3800, 'High', 'Weifang Mingliang (Domi) 2026 catalog: G1 5-handle body shaping US$3,800'),
}

def size(d):
    import re
    t = (d['name'] + ' ' + ' '.join(d['specs'])).lower()
    if d['cat'] == 'Consumables': return 'cons'
    m = re.search(r'(\d+(?:\.\d+)?)\s*kg', t)
    if m:
        w = float(m.group(1)); return 'small' if w <= 10 else 'table' if w <= 40 else 'floor'
    if re.search(r'tabletop|desktop|portable|compact', t): return 'table'
    if re.search(r'floor|station|tower|vertical|tall|cabinet|wheeled|trolley|platform|frame', t): return 'floor'
    if re.search(r'home|handheld|mini\b|pen\b|steamer|scrubber', t): return 'small'
    return 'table'

# Door-to-door quotes that already include customs and taxes (rand, nothing added)
ALL_IN = {8: round(1755 * 16.46),
          165: round((2600 + 760) * 16.46),   # TAC2-2H: US$2,600 + US$760 sea freight, customs clearance and taxes included (Domi)
          166: round((3100 + 760) * 16.46),
          167: round((3800 + 760) * 16.46)}   # TAVS5: US$3,800 + US$760 sea freight, customs clearance and taxes included (Domi)
         #   # TAC2-4H: US$3,100 + US$760 sea freight, customs clearance and taxes included (Domi)   # TAEM4: US$1,755 sea freight, double customs clearance and taxes included (Lyn Xie)

def landed(item_zar, d, k=None):
    """Item price in rand -> landed cost: + shipping to SA + customs/VAT."""
    if k in ALL_IN: return ALL_IN[k]
    if k in ACTUAL: return ACTUAL[k] * (1 + CUSTOMS)
    sz = size(d)
    ship = item_zar * SHIP_C if sz == 'cons' else SHIP[sz]
    return (item_zar + ship) * (1 + CUSTOMS)

def price(usd, d, k=None):
    l = landed(usd * RATE, d, k)
    return sell(l), l

if __name__ == '__main__':
    D = {d['k']: d for d in json.load(open('/home/claude/trimion-site/tools/details.orig.json'))}
    por = [k for k, d in D.items() if 'request' in d['price'].lower()]
    missing = set(por) - set(P); extra = set(P) - set(por)
    assert not missing and not extra, (missing, extra)
    out = {}
    for k in sorted(P):
        pr, _ = price(P[k][0], D[k], k); out[k] = pr
    assert not set(OWN) & set(P) and set(OWN) | set(P) == set(D), 'every item needs exactly one price source'
    for k, old in OWN.items():
        out[k] = sell(landed(old, D[k], k))
    FIXED = {164: 30 * 110}   # cryo membranes 110g: R110 each, minimum 30 (Robin, 19 Oct 2026)
    out.update(FIXED)
    out = dict(sorted(out.items()))
    json.dump(out, open('/home/claude/trimion-site/tools/prices.json', 'w'))
    print(len(out), 'priced; range', min(out.values()), '-', max(out.values()))
    for k in (8, 14, 34, 128, 60, 160, 164):
        print(k, D[k]['name'], 'R{:,}'.format(out[k]))
