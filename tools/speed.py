#!/usr/bin/env python3
"""Speed pass on the built site (owner request 24/10/2026).
1. Banner photos: use the lighter .webp copy instead of the .jpg wherever one exists (about 55% smaller).
(content-visibility on the long sections was tried and dropped: it broke the category jump links.)"""
import os, re
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
IMG = os.path.join(PUB, "img")
CSS = ('<style id="ta-speed">#ems,#cryo,#rf,#hifu,#face,#massage,#salon,#supplies,#subscribe,#getapp'
       '{content-visibility:auto;contain-intrinsic-size:auto 1400px}</style>')
n = 0
for root, _, files in os.walk(PUB):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f); s = open(p, encoding="utf-8").read(); t = s
        t = re.sub(r"/img/(hs2-[\w-]+)\.jpg\b", lambda m: f"/img/{m.group(1)}.webp" if os.path.exists(os.path.join(IMG, m.group(1) + ".webp")) else m.group(0), t)
        if t != s: open(p, "w", encoding="utf-8").write(t); n += 1
print(f"speed: {n} pages updated")
