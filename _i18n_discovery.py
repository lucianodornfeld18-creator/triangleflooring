#!/usr/bin/env python3
"""Make the PT/ES cluster discoverable + hreflang-reciprocal:
  1. Add the 16 PT/ES URLs to sitemap.xml.
  2. Add reciprocal hreflang (en/pt-BR/es/x-default) to the EN equivalent pages.
  3. Add a small language switcher link to the EN homepage footer.
Idempotent. Reversible via git.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://triangle-floor.com"
TODAY = "2026-06-10"

PAIRS = {
    "/": ("/pt/", "/es/"),
    "/hardwood-flooring/": ("/pt/pisos-de-madeira/", "/es/pisos-de-madera/"),
    "/vinyl-plank-flooring/": ("/pt/piso-vinilico/", "/es/piso-vinilico/"),
    "/tile-installation/": ("/pt/instalacao-de-azulejos/", "/es/instalacion-de-azulejos/"),
    "/laminate-flooring/": ("/pt/piso-laminado/", "/es/piso-laminado/"),
    "/stair-treads/": ("/pt/degraus-de-escada/", "/es/peldanos-de-escalera/"),
    "/floor-repair/": ("/pt/reparo-de-pisos/", "/es/reparacion-de-pisos/"),
    "/contact/": ("/pt/contato/", "/es/contato/"),
}

def en_file(en_path):
    rel = "index.html" if en_path == "/" else en_path.strip("/") + "/index.html"
    return os.path.join(ROOT, rel)

def hreflang_links(en, pt, es):
    return (f'\n<link rel="alternate" hreflang="en" href="{DOMAIN}{en}">'
            f'\n<link rel="alternate" hreflang="pt-BR" href="{DOMAIN}{pt}">'
            f'\n<link rel="alternate" hreflang="es" href="{DOMAIN}{es}">'
            f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en}">')

hreflang_done = []
for en, (pt, es) in PAIRS.items():
    fp = en_file(en)
    if not os.path.exists(fp):
        print("MISS", fp); continue
    raw = open(fp, encoding="utf-8").read()
    if re.search(r'hreflang=', raw):
        continue
    m = re.search(r'(<link rel="canonical"[^>]*>)', raw)
    if not m:
        continue
    raw = raw[:m.end()] + hreflang_links(en, pt, es) + raw[m.end():]
    open(fp, "w", encoding="utf-8", newline="").write(raw)
    hreflang_done.append(en)

# language switcher on EN homepage footer-bottom
home = en_file("/")
raw = open(home, encoding="utf-8").read()
if 'data-langswitch' not in raw:
    sw = '<span data-langswitch style="margin-left:10px">· <a href="/pt/" hreflang="pt-BR">Português</a> · <a href="/es/" hreflang="es">Español</a></span>'
    m = re.search(r'(<div class="footer-bottom">.*?)(</div>\s*</div>\s*</footer>)', raw, re.S)
    if m:
        raw = raw[:m.end(1)] + sw + raw[m.end(1):]
        open(home, "w", encoding="utf-8", newline="").write(raw)
        sw_done = True
    else:
        sw_done = False
else:
    sw_done = "already"

# sitemap
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
all_i18n = []
for en, (pt, es) in PAIRS.items():
    all_i18n += [pt, es]
added = 0
entries = ""
for u in all_i18n:
    full = DOMAIN + u
    if full in sm:
        continue
    entries += f"  <url>\n    <loc>{full}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    added += 1
if added:
    sm = sm.replace("</urlset>", entries + "</urlset>")
    open(sm_path, "w", encoding="utf-8", newline="").write(sm)

print(json.dumps({"hreflang_added_to": hreflang_done, "switcher": sw_done,
                  "sitemap_urls_added": added}, indent=2))
