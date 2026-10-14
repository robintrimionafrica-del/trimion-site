# Build tools

Everything needed to regenerate `../public` (the live site) lives here.

- `src/` – the original v15 site (source of truth for cards, scripts and photos).
- `pricing.py` – estimated supplier prices (USD) per item, exchange rate, shipping %, markup. Edit here, then rebuild.
- `apply_prices.py` – turns prices into card prices, lay-by plans, Buy now messages and search data.
- `build.py` – applies warranty wording, share pages, share sheet, WhatsApp fixes, speed work (`enhance.py`) and writes `../public`.
- `ogrender.js` + `ogt/` – share pictures. `brochure.py` – PDF brochures.
- `trimion-price-estimates.xlsx` – the price list sent to Trimion for checking.

Run `./rebuild.sh`, check the site, then commit and push. Cloudflare Workers Builds deploys `main` automatically.
