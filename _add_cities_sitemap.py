#!/usr/bin/env python3
"""One-off: add the 6 new expansion cities' URLs to sitemap.xml (idempotent)."""
import datetime
from pathlib import Path

ROOT = Path(__file__).parent
SM = ROOT / "sitemap.xml"
DOMAIN = "https://triangle-floor.com"
TODAY = datetime.date.today().isoformat()

NEW_CITIES = ["ellenton", "ruskin", "apollo-beach", "sun-city-center", "north-port", "nokomis"]
SERVICES = ["hardwood-flooring", "vinyl-plank-flooring", "tile-installation",
            "laminate-flooring", "stair-treads", "floor-repair"]

def entry(path, priority):
    return (f"  <url>\n    <loc>{DOMAIN}/{path}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n"
            f"    <priority>{priority}</priority>\n  </url>\n")

xml = SM.read_text(encoding="utf-8")
blocks, added = [], 0
for c in NEW_CITIES:
    candidates = [(f"{c}/", "0.85")]
    for s in SERVICES:
        candidates.append((f"{s}/{c}/", "0.80"))
        candidates.append((f"blog/{s}-cost-{c}/", "0.80"))
    for path, pri in candidates:
        loc = f"<loc>{DOMAIN}/{path}</loc>"
        if loc in xml:
            continue
        blocks.append(entry(path, pri))
        added += 1

if blocks:
    xml = xml.replace("</urlset>", "".join(blocks) + "</urlset>")
    SM.write_text(xml, encoding="utf-8")

print(f"Added {added} new URLs to sitemap.xml (TODAY={TODAY})")
total = xml.count("<loc>")
print(f"Total <loc> entries now: {total}")
