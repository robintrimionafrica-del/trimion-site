#!/usr/bin/env python3
"""Build public/guide/index.html (the buyer's guide) from products.json and guide_template.html.

Run after apply_prices.py so the guide shows the same prices and lay-by plans as the shop.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
products = json.load(open(os.path.join(HERE, "products.json")))
tpl = open(os.path.join(HERE, "guide_template.html")).read()

def rand(s):
    return int(re.sub(r"[^\d]", "", s) or 0) if s else 0

def R(n):
    return "R" + f"{round(n):,}".replace(",", " ")

data, sections = [], {}
for p in products:
    price = rand(p.get("price", ""))
    if not price:
        continue
    dep = inst = 0
    m = re.match(r"Lay-by R([\d,]+) now, then 2 × R([\d,]+)", p.get("lb", ""))
    if m:
        dep, inst = rand(m.group(1)), rand(m.group(2))
    name = f'{p["name"]} ({p["model"]})'
    data.append([name, price, dep, inst, p["sec"]])
    sections.setdefault(p["sec"], []).append(len(data) - 1)

opts, rows = [], []
for sec, idx in sections.items():
    opts.append(f'<optgroup label="{html.escape(sec)}">')
    rows.append(f'<tr class="sec"><th colspan="3">{html.escape(sec)}</th></tr>')
    for i in idx:
        name, price, dep, inst, _ = data[i]
        n = html.escape(name)
        opts.append(f'<option value="{i}">{n} · {R(price)}</option>')
        lb = f"{R(dep)} + 2 × {R(inst)}" if dep else "Pay in full"
        rows.append(f'<tr><td>{n}</td><td class="n">{R(price)}</td><td class="n">{lb}</td></tr>')
    opts.append("</optgroup>")

out = (tpl.replace("{{OPTIONS}}", "".join(opts))
          .replace("{{ROWS}}", "".join(rows))
          .replace("{{DATA}}", json.dumps([d[:4] for d in data], ensure_ascii=False))
          .replace("{{COUNT}}", str(len(products))))
dest = os.path.join(HERE, "..", "public", "guide", "index.html")
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w").write(out)
print(f"guide: {len(data)} machines in {len(sections)} sections")
