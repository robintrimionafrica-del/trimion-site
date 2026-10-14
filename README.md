# Trimion Africa Shop

Website for [trimionafrica.co.za](https://trimionafrica.co.za): 164 salon and spa machines, ordered on WhatsApp.

- `public/` is the website exactly as visitors get it (pages, photos, share pictures in `og/`, machine share pages in `p/`, PDF brochures in `pdf/`).
- `wrangler.jsonc` tells Cloudflare to serve `public/` from the Worker **trimion-catalog-v123**.
- Every change pushed to `main` goes live automatically through Cloudflare Workers Builds.
