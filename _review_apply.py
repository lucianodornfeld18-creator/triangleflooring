#!/usr/bin/env python3
"""Inject real Google reviews (visible block + valid Review schema) into pages,
picking reviews relevant to each page's service/city. Makes the existing
aggregateRating legitimate (backed by visible, real reviews). Idempotent.
Source: _reviews.json. Reversible via git.
"""
import os, re, json, html as ihtml

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "_reviews.json"), encoding="utf-8"))
REVIEWS = DATA["reviews"]
AGG = DATA["_meta"]["aggregate"]
MARK = "<!--tf-reviews-->"

EXCLUDE_NAMES = {
    "PLANO-TOP1-2026-06.html", "GBP-COMPETITIVE-STRATEGY.html",
    "reviews-inspiracao.html", "diretorios-como-preencher.html",
    "offpage-checklist.html", "404.html",
}
ROOT_HOME = "index.html"  # only the site root home (has its own reviews block); NOT dir/index.html
EXCLUDE_DIRS = {".git", "__pycache__", "audit", "automation", "images"}

SERVICE_TOKENS = {
    "hardwood-flooring": ["hardwood"], "pisos-de-madeira": ["hardwood"], "pisos-de-madera": ["hardwood"],
    "vinyl-plank-flooring": ["vinyl", "lvp"], "piso-vinilico": ["vinyl", "lvp"],
    "tile-installation": ["tile"], "instalacao-de-azulejos": ["tile"], "instalacion-de-azulejos": ["tile"],
    "laminate-flooring": ["laminate"], "piso-laminado": ["laminate"],
    "stair-treads": ["stair-treads"], "degraus-de-escada": ["stair-treads"], "peldanos-de-escalera": ["stair-treads"],
    "floor-repair": ["floor-repair"], "reparo-de-pisos": ["floor-repair"], "reparacion-de-pisos": ["floor-repair"],
    "water-damage": ["water-damage", "floor-repair"],
    "hardwood-refinishing": ["refinishing", "hardwood"], "refinish": ["refinishing"],
}
CITY_TOKENS = ["bradenton", "sarasota", "lakewood-ranch", "palmetto", "parrish", "venice", "tampa", "st-petersburg"]

HEAD = {
    "en": ("What Our Customers Say", f'{AGG["ratingValue"]} ★ on Google · {AGG["reviewCount"]} reviews', "Verified Google review"),
    "pt": ("O Que Nossos Clientes Dizem", f'{AGG["ratingValue"].replace(".", ",")} ★ no Google · {AGG["reviewCount"]} avaliações', "Avaliação verificada do Google"),
    "es": ("Lo Que Dicen Nuestros Clientes", f'{AGG["ratingValue"].replace(".", ",")} ★ en Google · {AGG["reviewCount"]} reseñas', "Reseña verificada de Google"),
}

def page_lang(rel):
    r = rel.replace("\\", "/")
    if r.startswith("pt/"):
        return "pt"
    if r.startswith("es/"):
        return "es"
    return "en"

def page_tags(rel):
    tags = set()
    low = "/" + rel.replace("\\", "/").lower()
    for tok, tg in SERVICE_TOKENS.items():
        if tok in low:
            tags.update(tg)
    for c in CITY_TOKENS:
        if c in low:
            tags.add(c)
    return tags

GENERIC_FALLBACK = ["Carole Marinucci", "Maycon Bernardes", "Pablo Escobar", "Chavezito", "Lais Lana"]

def pick_reviews(tags, n=3):
    scored = []
    for r in REVIEWS:
        rt = set(r["tags"])
        score = 0
        for c in CITY_TOKENS:
            if c in tags and c in rt:
                score += 5
        score += 2 * len((tags & rt) - set(CITY_TOKENS))
        if len(r["text"]) > 60:
            score += 1
        scored.append((score, len(r["text"]), r))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    picked, seen = [], set()
    for s, _, r in scored:
        if r["author"] in seen:
            continue
        picked.append(r); seen.add(r["author"])
        if len(picked) >= n:
            break
    if len(picked) < n:
        for name in GENERIC_FALLBACK:
            for r in REVIEWS:
                if r["author"] == name and name not in seen:
                    picked.append(r); seen.add(name)
            if len(picked) >= n:
                break
    return picked[:n]

def initials(name):
    parts = [p for p in name.split() if p]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()

def review_section(reviews, lang):
    title, sub, badge = HEAD[lang]
    cards = []
    for r in reviews:
        stars = "★" * int(r["rating"])
        body = ihtml.escape(r["text"])
        cards.append(
            f'<div style="background:#F7F9FC;border:1px solid #E2E8F0;border-radius:16px;padding:1.4rem;display:flex;flex-direction:column">'
            f'<div style="color:#FFB534;font-size:1rem;letter-spacing:1.5px;margin-bottom:.6rem">{stars}</div>'
            f'<p style="font-size:.95rem;line-height:1.6;color:#1B2939;margin:0 0 1rem;font-style:italic">“{body}”</p>'
            f'<div style="display:flex;align-items:center;gap:10px;margin-top:auto;padding-top:.9rem;border-top:1px solid #E2E8F0">'
            f'<div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#2E8DD9,#1A4F8C);display:grid;place-items:center;color:#fff;font-weight:700;font-size:.9rem;flex-shrink:0">{initials(r["author"])}</div>'
            f'<div><div style="font-weight:700;font-size:.9rem;color:#1B2939">{ihtml.escape(r["author"])}</div>'
            f'<div style="font-size:.72rem;color:#5B6B7E">✔ {badge}</div></div></div></div>'
        )
    grid = "".join(cards)
    return (f'{MARK}<section style="background:#fff;padding:4rem 0"><div class="container">'
            f'<div style="text-align:center;max-width:740px;margin:0 auto 2rem">'
            f'<span class="eyebrow">★★★★★</span>'
            f'<h2 style="margin:.3rem 0">{title}</h2>'
            f'<p style="color:#5B6B7E;font-weight:600">{sub}</p></div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.3rem">{grid}</div>'
            f'</div></section>\n')

def review_schema_nodes(reviews):
    return [{
        "@type": "Review",
        "author": {"@type": "Person", "name": r["author"]},
        "datePublished": r["date"],
        "reviewRating": {"@type": "Rating", "ratingValue": str(r["rating"]), "bestRating": "5"},
        "reviewBody": r["text"],
    } for r in reviews]

def inject_schema(raw, reviews):
    LD = re.compile(r'(<script[^>]*type\s*=\s*"application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)
    done = {"ok": False}
    def is_lb(node):
        t = node.get("@type")
        return (t == "LocalBusiness") or (isinstance(t, list) and "LocalBusiness" in t)
    def walk(node):
        if done["ok"]:
            return
        if isinstance(node, dict):
            if is_lb(node) and "review" not in node:
                node["review"] = review_schema_nodes(reviews)
                if "aggregateRating" not in node:
                    node["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": AGG["ratingValue"], "reviewCount": AGG["reviewCount"], "bestRating": "5"}
                done["ok"] = True
                return
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    def repl(m):
        if done["ok"]:
            return m.group(0)
        try:
            data = json.loads(m.group(2).strip())
        except Exception:
            return m.group(0)
        walk(data)
        if done["ok"]:
            return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        return m.group(0)
    return LD.sub(repl, raw), done["ok"]

changed = 0
skipped = 0
no_schema = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fn in filenames:
        if not fn.endswith(".html") or fn in EXCLUDE_NAMES:
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        if rel.replace("\\", "/") == ROOT_HOME:
            continue
        raw = open(full, encoding="utf-8").read()
        if MARK in raw or "<footer" not in raw:
            skipped += 1
            continue
        lang = page_lang(rel)
        tags = page_tags(rel)
        picks = pick_reviews(tags, 3)
        sect = review_section(picks, lang)
        raw2 = raw.replace("<footer", sect + "<footer", 1)
        raw2, sch_ok = inject_schema(raw2, picks)
        if not sch_ok:
            no_schema.append(rel)
        open(full, "w", encoding="utf-8", newline="").write(raw2)
        changed += 1

print(json.dumps({"pages_with_reviews": changed, "skipped": skipped,
                  "reviews_available": len(REVIEWS), "no_lb_schema": len(no_schema)}, indent=2))
