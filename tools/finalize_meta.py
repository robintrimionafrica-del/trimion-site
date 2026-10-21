#!/usr/bin/env python3
"""Last build step: make the home page's machine count match the live catalog
(older steps hard-code 162) and drop the old 'Trimion Africa Shop' wording Google shows."""
import csv, os, re
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
n = sum(1 for _ in csv.DictReader(open(os.path.join(PUB, "google-products.tsv"), encoding="utf-8"), delimiter="\t"))
p = os.path.join(PUB, "index.html")
s = open(p, encoding="utf-8").read()
s = re.sub(r'\b162(?= (?:professional|salon|Salon|EMS|machines))', str(n), s)
s = re.sub(r'\(16[0-6] machines\)', f'({n} machines)', s)
s = re.sub(r'%2816[0-6]%20machines%29', f'%28{n}%20machines%29', s)
s = re.sub(r'\b162(%20(?:professional|salon))', rf'{n}\1', s)
s = re.sub(r'(?<![0-9])162(?=%20(?:machines|professional))', str(n), s)
s = re.sub(r'"merchantReturnDays": ?7\b', '"merchantReturnDays":14', s)
s = s.replace('content="Trimion Africa Shop: ', 'content="Trimion Africa: ')
s = s.replace('<meta property="og:site_name" content="Trimion Africa Shop">', '<meta property="og:site_name" content="Trimion Africa">')
open(p, "w", encoding="utf-8").write(s)
print(f"home meta: {n} machines")
