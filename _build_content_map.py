#!/usr/bin/env python3
"""
Build/refresh _content_map.json — the anti-cannibalization ledger.

Source of truth = sitemap.xml (live URL set) cross-referenced with the
city tier model and service taxonomy. Each entry records the primary
keyword / intent / city(+tier) / service so future blog automation runs
can enforce: one primary keyword+intent per URL.

Run:  py -3 _build_content_map.py
"""
import json, re, datetime
from pathlib import Path

ROOT = Path(__file__).parent
SITEMAP = ROOT / "sitemap.xml"
OUT = ROOT / "_content_map.json"

# --- City tier model (per business GEO strategy) -----------------------------
TIER1 = {"bradenton", "sarasota", "lakewood-ranch", "palmetto", "parrish", "venice"}
TIER2 = {"tampa", "st-petersburg"}
TIER3 = {"ellenton", "ruskin", "apollo-beach", "sun-city-center", "north-port", "nokomis"}
CITY_NAME = {
    "bradenton": "Bradenton", "sarasota": "Sarasota", "lakewood-ranch": "Lakewood Ranch",
    "palmetto": "Palmetto", "parrish": "Parrish", "venice": "Venice",
    "tampa": "Tampa", "st-petersburg": "St. Petersburg",
    "ellenton": "Ellenton", "ruskin": "Ruskin", "apollo-beach": "Apollo Beach",
    "sun-city-center": "Sun City Center", "north-port": "North Port", "nokomis": "Nokomis",
}
CITIES = list(CITY_NAME.keys())

# --- Service taxonomy --------------------------------------------------------
SERVICE_NAME = {
    "hardwood-flooring": "Hardwood Flooring",
    "vinyl-plank-flooring": "Luxury Vinyl Plank (LVP)",
    "tile-installation": "Tile Installation",
    "laminate-flooring": "Laminate Flooring",
    "stair-treads": "Stair Treads",
    "floor-repair": "Floor Repair / Replacement",
    "hardwood-refinishing": "Hardwood Refinishing",
}
# blog cost-post service prefixes -> canonical service key
COST_SVC = {
    "hardwood-flooring": "hardwood-flooring",
    "vinyl-plank-flooring": "vinyl-plank-flooring",
    "tile-installation": "tile-installation",
    "laminate-flooring": "laminate-flooring",
    "stair-treads": "stair-treads",
    "floor-repair": "floor-repair",
}

# --- Standalone blog posts (non cost-by-city) metadata -----------------------
STANDALONE_POSTS = {
    "best-flooring-florida-humidity": {
        "title": "Best Flooring for Florida Humidity (2026 Comparison)",
        "keyword": "best flooring for florida humidity", "intent": "informational-comparison",
        "service": None, "city": None, "date": "2026-05-03"},
    "hardwood-vs-vinyl-plank-lakewood-ranch": {
        "title": "Hardwood vs Vinyl Plank in Lakewood Ranch (Pros & Cons)",
        "keyword": "hardwood vs vinyl plank lakewood ranch", "intent": "informational-comparison",
        "service": "hardwood-flooring", "city": "lakewood-ranch", "date": "2026-05-03"},
    "flooring-vacation-rental-florida": {
        "title": "Best Flooring for Florida Vacation Rentals (2026 Guide)",
        "keyword": "best flooring for florida vacation rentals", "intent": "informational-investor",
        "service": None, "city": None, "date": "2026-04-15"},
    "hardwood-floor-refinishing-tampa-bay": {
        "title": "Hardwood Floor Refinishing in Tampa Bay (When & How)",
        "keyword": "hardwood floor refinishing tampa bay", "intent": "informational-howto",
        "service": "hardwood-refinishing", "city": None, "date": "2026-04-29"},
    "stair-tread-replacement-guide": {
        "title": "Stair Tread Replacement Guide: Hardwood vs LVP vs Tile",
        "keyword": "stair tread replacement", "intent": "informational-howto",
        "service": "stair-treads", "city": None, "date": "2026-04-08"},
    "water-damaged-hardwood-floor-repair-florida": {
        "title": "How to Fix Water-Damaged Hardwood Floors in Florida",
        "keyword": "how to fix water-damaged hardwood floors", "intent": "informational-howto",
        "service": "floor-repair", "city": None, "date": "2026-06-07"},
}

# --- Informational guides ----------------------------------------------------
GUIDES = {
    "engineered-vs-solid-hardwood-florida": ("engineered vs solid hardwood florida", "informational-comparison", "hardwood-flooring"),
    "hardwood-vs-vinyl-plank-florida": ("hardwood vs vinyl plank florida", "informational-comparison", "hardwood-flooring"),
    "pet-friendly-flooring-florida": ("pet friendly flooring florida", "informational-buyer", None),
    "waterproof-flooring-florida": ("waterproof flooring florida", "informational-buyer", None),
}

# --- Support / static pages --------------------------------------------------
SUPPORT = {
    "": "Home", "about": "About", "contact": "Contact", "faq": "FAQ",
    "glossary": "Glossary", "warranty": "Warranty", "directories": "Directories",
}


def tier_of(city):
    if city in TIER1: return 1
    if city in TIER2: return 2
    if city in TIER3: return 3
    return None


def classify(path):
    """path like '/blog/hardwood-flooring-cost-tampa/' -> entry dict."""
    p = path.strip("/")
    parts = p.split("/") if p else [""]

    # Home
    if p == "":
        return {"type": "home", "title": "Triangle Flooring — Home", "keyword": "flooring contractor bradenton",
                "intent": "brand/transactional", "service": None, "city": None, "tier": None, "language": "en"}

    # Blog
    if parts[0] == "blog":
        if len(parts) == 1:
            return {"type": "index", "title": "Flooring Blog", "keyword": "flooring blog tampa bay",
                    "intent": "index", "service": None, "city": None, "tier": None, "language": "en"}
        slug = parts[1]
        # cost-by-city pattern: {service}-cost-{city}[-2026]
        m = re.match(r"^(.*)-cost-([a-z-]+?)(?:-2026)?$", slug)
        if m and m.group(1) in COST_SVC:
            svc = COST_SVC[m.group(1)]
            # resolve city (handle multi-word like st-petersburg / lakewood-ranch)
            tail = m.group(2)
            city = next((c for c in CITIES if tail == c), None)
            if city:
                return {"type": "blog-cost", "title": f"{SERVICE_NAME[svc]} Cost in {CITY_NAME[city]} (2026)",
                        "keyword": f"{m.group(1).replace('-', ' ')} cost {city.replace('-', ' ')}",
                        "intent": "commercial-cost", "service": svc, "city": city,
                        "tier": tier_of(city), "language": "en"}
        if slug in STANDALONE_POSTS:
            d = STANDALONE_POSTS[slug]
            return {"type": "blog-standalone", "title": d["title"], "keyword": d["keyword"],
                    "intent": d["intent"], "service": d["service"], "city": d["city"],
                    "tier": tier_of(d["city"]), "language": "en"}
        return {"type": "blog-unknown", "title": slug, "keyword": slug.replace("-", " "),
                "intent": "unknown", "service": None, "city": None, "tier": None, "language": "en"}

    # Guides
    if parts[0] == "guides":
        if len(parts) == 1:
            return {"type": "index", "title": "Flooring Guides", "keyword": "flooring guides florida",
                    "intent": "index", "service": None, "city": None, "tier": None, "language": "en"}
        g = GUIDES.get(parts[1])
        if g:
            return {"type": "guide", "title": parts[1].replace("-", " ").title(), "keyword": g[0],
                    "intent": g[1], "service": g[2], "city": None, "tier": None, "language": "en"}

    # Service pages: /{service}/ or /{service}/{city}/
    if parts[0] in SERVICE_NAME:
        svc = parts[0]
        if len(parts) == 1:
            return {"type": "service-hub", "title": f"{SERVICE_NAME[svc]} — Tampa Bay",
                    "keyword": f"{svc.replace('-', ' ')} tampa bay", "intent": "commercial",
                    "service": svc, "city": None, "tier": None, "language": "en"}
        sub = parts[1]
        if sub in CITIES:
            return {"type": "service-city", "title": f"{SERVICE_NAME[svc]} in {CITY_NAME[sub]}",
                    "keyword": f"{svc.replace('-', ' ')} {sub.replace('-', ' ')}", "intent": "commercial-local",
                    "service": svc, "city": sub, "tier": tier_of(sub), "language": "en"}
        # special floor-repair subpages
        special = {"emergency": "Emergency Floor Repair", "water-damage": "Water Damage Floor Repair"}
        if sub in special:
            return {"type": "service-special", "title": special[sub],
                    "keyword": f"{sub.replace('-', ' ')} floor repair florida", "intent": "commercial",
                    "service": svc, "city": None, "tier": None, "language": "en"}

    # City landing pages: /{city}/
    if parts[0] in CITIES and len(parts) == 1:
        c = parts[0]
        return {"type": "city-landing", "title": f"Flooring in {CITY_NAME[c]}, FL",
                "keyword": f"flooring {c.replace('-', ' ')} fl", "intent": "commercial-local",
                "service": None, "city": c, "tier": tier_of(c), "language": "en"}

    # Support
    if parts[0] in SUPPORT and len(parts) == 1:
        return {"type": "support", "title": SUPPORT[parts[0]], "keyword": parts[0] or "home",
                "intent": "support", "service": None, "city": None, "tier": None, "language": "en"}

    return {"type": "other", "title": p, "keyword": p.replace("/", " ").replace("-", " "),
            "intent": "unknown", "service": None, "city": None, "tier": None, "language": "en"}


def main():
    locs = re.findall(r"<loc>https://triangle-floor\.com(/.*?)</loc>", SITEMAP.read_text(encoding="utf-8"))
    entries = []
    for path in locs:
        e = classify(path)
        e = {"url": path, **e}
        entries.append(e)
    entries.sort(key=lambda x: x["url"])

    by_type = {}
    for e in entries:
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1

    doc = {
        "_meta": {
            "generated": datetime.date.today().isoformat(),
            "source": "sitemap.xml + builder taxonomy",
            "rule": "Each primary keyword+intent belongs to exactly ONE url. Blog posts target informational/question intent and must NOT compete with /services/* or /{city}/* commercial pages for the same transactional query.",
            "city_tiers": {"tier1": sorted(TIER1), "tier2": sorted(TIER2), "tier3": sorted(TIER3)},
            "total_urls": len(entries),
            "counts_by_type": by_type,
        },
        "entries": entries,
    }
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT} with {len(entries)} entries")
    for t, n in sorted(by_type.items()):
        print(f"  {t:18} {n}")


if __name__ == "__main__":
    main()
