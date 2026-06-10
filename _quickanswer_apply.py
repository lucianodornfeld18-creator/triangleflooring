#!/usr/bin/env python3
"""Inject an answer-first 'Quick answer' block (40-60 words, AEO/snippet bait)
right after the H1 on EN commercial pages: cost posts, service hubs, and
service-city pages. Idempotent (marker). Reversible via git.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "tf-quickanswer"
WA = "free, itemized written quote within 24 hours"

SVC = {
    "hardwood-flooring": ("hardwood flooring", "$7.35–$20.70/sq ft installed", 7.35, 20.70),
    "vinyl-plank-flooring": ("luxury vinyl plank (LVP)", "$3.91–$11.11/sq ft installed", 3.91, 11.11),
    "tile-installation": ("porcelain & ceramic tile", "$7.50–$22.00/sq ft installed", 7.50, 22.00),
    "laminate-flooring": ("laminate flooring", "$3.50–$8.50/sq ft installed", 3.50, 8.50),
    "hardwood-refinishing": ("hardwood refinishing", "$3.50–$7.00/sq ft", 3.50, 7.00),
    "stair-treads": ("stair tread replacement", "$80–$220 per tread installed", None, None),
    "floor-repair": ("floor repair", "$250–$1,500+ per repair", None, None),
}
CITIES = {"bradenton":"Bradenton","sarasota":"Sarasota","lakewood-ranch":"Lakewood Ranch",
          "palmetto":"Palmetto","parrish":"Parrish","venice":"Venice","tampa":"Tampa",
          "st-petersburg":"St. Petersburg"}

def money(n):
    return f"${n:,.0f}"

def block(text):
    return (f'<div class="quick-answer" data-{MARK} style="background:#E8F2FB;border-left:4px solid #2E8DD9;'
            f'padding:16px 20px;border-radius:0 10px 10px 0;margin:1.4rem auto;max-width:820px;'
            f'font-size:1.02rem;line-height:1.6;color:#0F3A6E">'
            f'<strong>Quick answer:</strong> {text}</div>')

def svc_in(path):
    for tok in SVC:
        if tok in path:
            return tok
    return None

def city_in(path):
    for tok in CITIES:
        if f"-{tok}/" in path or f"/{tok}/" in path:
            return tok
    return None

def make_text(path):
    svc = svc_in(path)
    if not svc:
        return None
    name, price, lo, hi = SVC[svc]
    city = city_in(path)
    place = CITIES[city] if city else "the Bradenton–Sarasota–Tampa Bay area"
    is_cost = "/blog/" in path and "-cost-" in path
    room = ""
    if lo and hi:
        room = f" A typical 200 sq ft room runs {money(lo*200)}–{money(hi*200)}."
    if is_cost:
        return (f"Installing {name} in {place}, FL costs {price} in 2026.{room} "
                f"Final price depends on material grade, subfloor prep, and room layout. "
                f"Triangle Flooring provides a {WA}.")
    where = f"in {place}" if city else f"across {place}"
    return (f"{name.capitalize()} installation {where} costs {price} (2026, installed).{room} "
            f"Triangle Flooring is a licensed & insured local installer with 300+ Florida projects, "
            f"5.0★ on Google, and a {WA}.")

def eligible(rel):
    p = "/" + rel.replace("\\", "/")
    if p.startswith("/pt/") or p.startswith("/es/"):
        return False
    svc = svc_in(p)
    if not svc:
        return False
    if "/blog/" in p and "-cost-" in p:
        return True
    if re.match(rf"^/{svc}/(index\.html|[a-z-]+/index\.html)$", p):
        return True
    return False

changed = 0
skipped = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in {".git","__pycache__","audit","automation","images","pt","es"}]
    for fn in filenames:
        if fn != "index.html":
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        if not eligible(rel):
            continue
        raw = open(full, encoding="utf-8").read()
        if MARK in raw:
            skipped += 1
            continue
        text = make_text("/" + rel.replace("\\", "/"))
        if not text:
            continue
        m = re.search(r"</h1>", raw, re.I)
        if not m:
            continue
        raw2 = raw[:m.end()] + "\n" + block(text) + raw[m.end():]
        open(full, "w", encoding="utf-8", newline="").write(raw2)
        changed += 1

print(json.dumps({"quick_answers_added": changed, "already_had": skipped}, indent=2))
