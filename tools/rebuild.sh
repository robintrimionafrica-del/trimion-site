#!/usr/bin/env bash
# Rebuild the whole Trimion website into ../public from the source in ./src.
# Needs: python3 with Pillow + reportlab, node with playwright (Chromium), Poppins fonts (in ./ogt).
# Steps: prices -> product data -> share pictures -> brochures -> site.
set -euo pipefail
cd "$(dirname "$0")"
python3 pricing.py                                   # prices.json from the estimates in pricing.py
cp products.orig.json products.json; cp details.orig.json details.json
python3 -c "import apply_prices as A; A.update_data()"   # put prices into product data
mkdir -p og-full ../public/og
node ogrender.js                                      # 1200x630 share pictures -> og-full/
python3 - <<'PY'
from PIL import Image; import glob, os
for f in glob.glob('og-full/*.jpg'):
    Image.open(f).resize((800, 420), Image.LANCZOS).save('../public/og/' + os.path.basename(f), quality=55, optimize=True, progressive=True, subsampling=2)
PY
rm -rf ../public/pdf && python3 brochure.py ../public/pdf   # one-page PDF brochures
mkdir -p ../public/img && cp -n src/img/* ../public/img/ 2>/dev/null || true
cp src/icon-*.png src/manifest.json ../public/
python3 build.py                                      # index.html, /p/ pages, sw.js, _headers, robots, sitemap
python3 visual_search.py                              # search by photo: /vs.js, /vs.json, camera button in the search bar
python3 guide.py                                      # buyer's guide at /guide (all machines, prices, lay-by)
python3 fb_catalog.py                                 # Facebook/Instagram catalog feed at /facebook-catalog.csv + /fb/ photos
python3 promo.py                                      # promo-code page at /promo (TRIMION10)
echo "Done. Commit and push to main; Cloudflare deploys in about a minute."
