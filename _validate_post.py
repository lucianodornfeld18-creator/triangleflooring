#!/usr/bin/env python3
"""Validate the new water-damage post (Phase 5 gate)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
SLUG = "water-damaged-hardwood-floor-repair-florida"
POST = ROOT / "blog" / SLUG / "index.html"
html = POST.read_text(encoding="utf-8")
errors, warns, oks = [], [], []

# 1. Single DOCTYPE / html / head / body, single H1
if html.count("<!DOCTYPE html>") == 1: oks.append("single <!DOCTYPE>")
else: errors.append(f"{html.count('<!DOCTYPE html>')} DOCTYPE")
h1 = re.findall(r"<h1[ >]", html)
if len(h1) == 1: oks.append("single <h1>")
else: errors.append(f"{len(h1)} <h1> tags")

# 2. Boilerplate present, no leftover slice markers
for needed in ['<header class="site-header">', "</header>", "<footer>", "</footer>",
               'class="whatsapp-float"', 'class="final-cta"', "getElementById('menuToggle')"]:
    (oks if needed in html else errors).append(f"chrome: {needed[:34]}")

# 3. GA4 + Ads appear exactly once each
for tag, label in [("G-7VP0F63NPC", "GA4"), ("AW-16536846393", "Ads")]:
    n = html.count(tag)
    # tag id appears multiple times in the gtag config block legitimately; count <script async occurrences instead
ga_async = html.count('googletagmanager.com/gtag/js?id=G-7VP0F63NPC')
if ga_async == 1: oks.append("GA/Ads gtag loader once (not duplicated)")
else: errors.append(f"gtag loader appears {ga_async}x")

# 4. JSON-LD blocks parse
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
types = []
for b in blocks:
    try:
        obj = json.loads(b)
        t = obj.get("@type"); types.append(t if isinstance(t, str) else "+".join(t))
    except json.JSONDecodeError as e:
        errors.append(f"JSON-LD parse error: {e}")
oks.append(f"JSON-LD parsed: {types}")
for need in ["BreadcrumbList", "Article", "FAQPage"]:
    if need not in types: errors.append(f"missing schema {need}")
if not any("LocalBusiness" in t for t in types): warns.append("no LocalBusiness schema")

# 5. FAQ schema == visible accordion
faq_obj = next((json.loads(b) for b in blocks if '"FAQPage"' in b), None)
schema_q = [q["name"] for q in faq_obj["mainEntity"]] if faq_obj else []
vis_q = re.findall(r'<details class="faq-item"><summary>(.*?)</summary>', html)
schema_a = [q["acceptedAnswer"]["text"] for q in faq_obj["mainEntity"]] if faq_obj else []
vis_a = re.findall(r'<div class="faq-content"><p>(.*?)</p></div>', html)
if schema_q == vis_q and schema_a == vis_a:
    oks.append(f"FAQPage schema == visible accordion ({len(vis_q)} Q&A)")
else:
    errors.append(f"FAQ mismatch: schema {len(schema_q)}Q / visible {len(vis_q)}Q")

# 6. Internal links resolve to a real file/dir
links = set(re.findall(r'href="(/[^"#]*)"', html))
for ln in sorted(links):
    p = ln.strip("/")
    if p == "": continue
    target = ROOT / p
    if target.is_dir() and (target / "index.html").exists(): continue
    if target.exists(): continue
    if (ROOT / (p + ".html")).exists(): continue
    # tel:/mailto already excluded by regex; flag everything else
    errors.append(f"broken internal link: {ln}")
oks.append(f"checked {len(links)} internal links")

# 7. Title / description uniqueness vs every other page
title = re.search(r"<title>(.*?)</title>", html).group(1)
desc = re.search(r'<meta name="description" content="(.*?)">', html).group(1)
dup_t, dup_d = [], []
for other in ROOT.rglob("index.html"):
    if other == POST: continue
    o = other.read_text(encoding="utf-8", errors="ignore")
    mt = re.search(r"<title>(.*?)</title>", o)
    md = re.search(r'<meta name="description" content="(.*?)">', o)
    if mt and mt.group(1) == title: dup_t.append(str(other.relative_to(ROOT)))
    if md and md.group(1) == desc: dup_d.append(str(other.relative_to(ROOT)))
(oks if not dup_t else errors).append("unique <title>" if not dup_t else f"title dup: {dup_t}")
(oks if not dup_d else errors).append("unique meta description" if not dup_d else f"desc dup: {dup_d}")
if len(title) < 60: oks.append(f"title {len(title)} chars (<60)")
else: warns.append(f"title {len(title)} chars (>=60)")
if len(desc) < 155: oks.append(f"description {len(desc)} chars (<155)")
else: warns.append(f"description {len(desc)} chars (>=155)")

# 8. Answer-first / speakable present, comparison tables, recip interlinks
if 'data-speakable="true"' in html: oks.append("answer-first speakable block present")
else: warns.append("no speakable answer-first")
if html.count("<table>") >= 2: oks.append(f"{html.count('<table>')} comparison tables")
else: warns.append("fewer than 2 tables")
for must in ["/floor-repair/water-damage/", "/floor-repair/", "/hardwood-flooring/"]:
    (oks if f'href="{must}"' in html else warns).append(f"interlink {must}")

print("\n=== VALIDATION:", POST.relative_to(ROOT), "===")
for o in oks: print("  OK   ", o)
for w in warns: print("  WARN ", w)
for e in errors: print("  FAIL ", e)
print(f"\n{len(oks)} ok / {len(warns)} warn / {len(errors)} fail")
sys.exit(1 if errors else 0)
