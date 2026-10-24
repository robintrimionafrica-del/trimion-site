#!/usr/bin/env bash
# Rebuild the whole Trimion website into ../public from the source in ./src.
# Needs: python3 with Pillow + reportlab, node with playwright (Chromium), Poppins fonts (in ./ogt).
# Steps: prices -> product data -> share pictures -> brochures -> site.
set -euo pipefail
cd "$(dirname "$0")"
python3 pricing.py                                   # prices.json from the estimates in pricing.py
cp products.orig.json products.json; cp details.orig.json details.json
python3 -c "import apply_prices as A; A.update_data()"   # put prices into product data
python3 hold.py data                                  # unchecked machines (EMS, cryo, RF, HIFU, facial, massage): price on request
python3 safe_words.py data                            # plain cosmetic wording in product data (no sculpting/tightening claims)
mkdir -p og-full ../public/og
node ogrender.js                                      # 1200x630 share pictures -> og-full/
python3 - <<'PY'
from PIL import Image; import glob, os
for f in glob.glob('og-full/*.jpg'):
    Image.open(f).resize((800, 420), Image.LANCZOS).save('../public/og/' + os.path.basename(f), quality=55, optimize=True, progressive=True, subsampling=2)
PY
rm -rf ../public/pdf && python3 brochure.py ../public/pdf   # one-page PDF brochures
mkdir -p ../public/img && cp -n src/img/* ../public/img/ 2>/dev/null || true
cp src/icon-*.png src/manifest.json ../public/ && mkdir -p ../public/app && cp src/app/* ../public/app/
mkdir -p ../public/media/brand && cp src/media_brand/* ../public/media/brand/
python3 build.py                                      # index.html, /p/ pages, sw.js, _headers, robots, sitemap
python3 visual_search.py                              # search by photo: /vs.js, /vs.json, camera button in the search bar
python3 shein_home.py                                 # shop-style layer: category circles, deal tiles, trending row, badges
python3 guide.py                                      # buyer's guide at /guide (all machines, prices, lay-by)
python3 fb_catalog.py                                 # Facebook/Instagram catalog feed at /facebook-catalog.csv + /fb/ photos
python3 xml_feed.py                                   # same feed as XML at /google-products.xml (WhatsApp sales assistant)
python3 promo.py                                      # promo-code page at /promo (TRIMION10)
python3 offers.py                                     # offers page at /offers (starter kit + R2,000 referral)
python3 subscribe.py                                  # email sign-up for specials at /subscribe + box on home and /offers
python3 flash.py                                      # 3 flash deals a day (R2,000 off) at /flash + banner on home page
python3 app_section.py                                # "Get the Trimion app" card above the footer (installs the site as an app)
python3 shop_preview.py                               # shop-style home page preview at /new/ (noindex, not linked)
python3 finalize_meta.py                              # home page count = live catalog, Google wording
python3 live_feed.py                                  # live feed on the home page: new machine video at 10, 12, 14, 16, 18, 19:30
python3 ig_page.py                                   # Instagram posting plan at /instagram (posts in order, batches of 10)
python3 gumtree_page.py                               # classifieds listing pack at /gumtree (Gumtree, Marketplace, Junkmail)
python3 meta_pixel.py                                 # Meta Pixel on every page (PageView, ViewContent, WhatsApp Lead)
python3 hold.py public                                # on-request cards, no offers in search data, held back from feeds
python3 speed.py                                      # lighter banner photos (.webp instead of .jpg)
python3 safe_words.py public                          # same plain wording across every public page and feed (keep last)
echo "Done. Commit and push to main; Cloudflare deploys in about a minute."
