// Trimion Africa website Worker.
// The shop pages are static files in ../public (served first by Cloudflare). This script only handles:
//   POST /api/subscribe   - saves a specials sign-up (name, email, WhatsApp) in a Durable Object.
//   GET  /subscribers/?key=...        - private list of sign-ups for the owner.
//   GET  /subscribers/?key=...&csv=1  - the same list as a CSV download.
// Anything else falls through to the static site.
import { DurableObject } from "cloudflare:workers";

// SHA-256 of the owner's private key. The key itself is not stored here.
const KEY_HASH = "c5f35b9b80dd79fbe7c021892024b0d298590c933f25c8c8a79a0d36c53c7aa9";

async function sha256(t) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const json = (o, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });

export class Subscribers extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`CREATE TABLE IF NOT EXISTS subs(
      email TEXT PRIMARY KEY, name TEXT, whatsapp TEXT, page TEXT, created TEXT, updated TEXT)`);
  }
  add(s) {
    const now = new Date().toISOString();
    this.sql.exec(
      `INSERT INTO subs(email,name,whatsapp,page,created,updated) VALUES(?,?,?,?,?,?)
       ON CONFLICT(email) DO UPDATE SET name=excluded.name,
         whatsapp=CASE WHEN excluded.whatsapp<>'' THEN excluded.whatsapp ELSE subs.whatsapp END, updated=excluded.updated`,
      s.email, s.name, s.whatsapp, s.page, now, now);
    return this.count();
  }
  count() { return this.sql.exec("SELECT COUNT(*) AS n FROM subs").one().n; }
  list() { return this.sql.exec("SELECT * FROM subs ORDER BY created DESC").toArray(); }
}

function store(env) { return env.SUBSCRIBERS.get(env.SUBSCRIBERS.idFromName("specials")); }

async function subscribe(request, env) {
  let d;
  try {
    d = await request.json();
  } catch {
    return json({ success: false, message: "Bad request" }, 400);
  }
  if (d._honey) return json({ success: true });
  const name = String(d.name || "").trim().slice(0, 100);
  const email = String(d.email || "").trim().toLowerCase().slice(0, 200);
  const whatsapp = String(d.whatsapp || "").replace(/[^\d+ ]/g, "").trim().slice(0, 30);
  const page = String(d.page || "").slice(0, 100);
  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ success: false, message: "Check name and email" }, 400);
  await store(env).add({ name, email, whatsapp, page });
  return json({ success: true });
}

async function adminPage(url, env) {
  const key = url.searchParams.get("key") || "";
  if (!key || (await sha256(key)) !== KEY_HASH)
    return new Response("Not found", { status: 404, headers: { "Cache-Control": "no-store" } });
  const rows = await store(env).list();
  const sast = (iso) => new Date(new Date(iso).getTime() + 2 * 3600e3).toISOString().slice(0, 16).replace("T", " ");
  if (url.searchParams.get("csv")) {
    const q = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
    const csv = ["Name,Email,WhatsApp,Signed up (SAST),Page"]
      .concat(rows.map((r) => [r.name, r.email, r.whatsapp, sast(r.created), r.page].map(q).join(",")))
      .join("\r\n");
    return new Response(csv, {
      headers: { "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": 'attachment; filename="trimion-subscribers.csv"', "Cache-Control": "no-store" },
    });
  }
  const wa = (n) => {
    let d = String(n || "").replace(/\D/g, "");
    if (d.startsWith("0")) d = "27" + d.slice(1);
    return d ? `<a href="https://wa.me/${d}">${esc(n)}</a>` : "";
  };
  const list = rows.length
    ? rows.map((r) => `<li><b>${esc(r.name)}</b><a href="mailto:${esc(r.email)}">${esc(r.email)}</a>${wa(r.whatsapp)}<small>${sast(r.created)}</small></li>`).join("")
    : `<li class="none">No sign-ups yet. Share trimionafrica.co.za/subscribe/ with customers.</li>`;
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Specials Subscribers</title><style>
:root{--bg:#f3f5fa;--card:#fff;--fg:#0d1830;--mu:#55627d;--ln:#d9dfeb;--ac:#128c4a}
@media (prefers-color-scheme:dark){:root{--bg:#0a1122;--card:#121c33;--fg:#e8edf7;--mu:#9aa7c2;--ln:#26324d;--ac:#2fbf6e}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
.w{max-width:560px;margin:0 auto;padding:20px 16px 40px}h1{font-size:1.5rem;margin:0 0 4px}p{margin:0 0 16px;color:var(--mu)}
.dl{display:block;text-align:center;background:var(--ac);color:#fff;text-decoration:none;font-weight:700;padding:13px;border-radius:12px;margin-bottom:16px}
ul{list-style:none;padding:0;margin:0}li{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:12px 14px;margin-bottom:10px;display:grid;gap:2px}
li a{color:var(--ac);word-break:break-all}small{color:var(--mu)}.none{color:var(--mu)}
</style></head><body><div class="w"><h1>Specials subscribers</h1><p>${rows.length} sign-up${rows.length === 1 ? "" : "s"}, newest first. Keep this link private.</p>
<a class="dl" href="?key=${encodeURIComponent(key)}&csv=1">Download list (CSV)</a><ul>${list}</ul></div></body></html>`;
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/subscribe") {
      if (request.method === "POST") return subscribe(request, env);
      return json({ success: false, message: "Use POST" }, 405);
    }
    if (url.pathname === "/subscribers" || url.pathname === "/subscribers/") return adminPage(url, env);
    return env.ASSETS.fetch(request);
  },
};
