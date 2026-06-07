#!/usr/bin/env python3
"""
render_post.py - Render ONE blog post to blog/<slug>/index.html.

Method (the proven one for this repo, ported from _build_water_damage_post.py):
slice the EXACT shared boilerplate (head styles + GA/Ads, blog CSS, header,
footer, whatsapp float, final-cta, closing scripts) from a recently-deployed
post so the new page is byte-identical chrome to the live site. _gen.py is
STALE vs deployed HTML, so we never use _gen.header()/footer().

The Claude API authors only CONTENT (a JSON object, schema = queue/_example.json).
This script does the deterministic structure/schema so the model can't break
the site.

Usage:  python automation/render_post.py <slug>
        (reads automation/queue/<slug>.json, writes blog/<slug>/index.html)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXEMPLAR = ROOT / "blog" / "best-flooring-florida-humidity" / "index.html"
QUEUE_DIR = Path(__file__).parent / "queue"

DOMAIN = "triangle-floor.com"
CITIES = ["Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto",
          "Parrish", "Venice", "St. Petersburg", "Tampa"]
# card images known to exist on the live site (render falls back to the first)
KNOWN_IMAGES = ["card-repair.webp", "card-tile.webp", "card-hardwood.webp",
                "card-vinyl.webp", "card-laminate.webp", "card-stairs.webp"]


def slc(src, start, end, inclusive_end=True):
    i = src.index(start)
    j = src.index(end, i)
    return src[i:(j + len(end)) if inclusive_end else j]


def safe_image(name):
    if name and (ROOT / "images" / name).exists():
        return name
    for k in KNOWN_IMAGES:
        if (ROOT / "images" / k).exists():
            return k
    return "card-repair.webp"


def faq_accordion(faqs):
    items = "".join(
        f'<details class="faq-item"><summary>{q}</summary>'
        f'<div class="faq-content"><p>{a}</p></div></details>'
        for q, a in faqs)
    return f'<div class="faq-list">{items}</div>'


def faqpage_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def card(href, img, cat, date, title, blurb):
    return (f'<a href="{href}" class="blog-card">\n'
            f'          <div class="blog-card-photo"><img src="/images/{safe_image(img)}" alt="{title}" loading="lazy"></div>\n'
            f'          <div class="blog-card-body">\n'
            f'            <div class="blog-card-meta"><span>{cat}</span><span>{date}</span></div>\n'
            f'            <h3>{title}</h3>\n'
            f'            <p>{blurb}</p>\n'
            f'            <span class="blog-card-link">Read article →</span>\n'
            f'          </div>\n        </a>')


def render(data):
    slug = data["slug"]
    url = f"https://{DOMAIN}/blog/{slug}/"
    title = data["title"]
    desc = data["meta_desc"]
    h1 = data.get("h1", title)
    category = data.get("category", "Flooring Guides")
    og_image = safe_image(data.get("og_image"))
    date = data["date"]
    read_min = data.get("read_min", 9)
    bc_short = data.get("breadcrumb_short", title)[:42]
    faqs = [(f["q"], f["a"]) for f in data["faqs"]]

    src = EXEMPLAR.read_text(encoding="utf-8")
    HEAD_STYLES_AND_GA = slc(src, "<style>\n:root", "</head>")
    BODY_CSS = slc(src, "<style>\n.blog-list", "</style>")
    HEADER = slc(src, '<header class="site-header">', "</header>")
    FOOTER = slc(src, "<footer>", "</footer>")
    FINAL_CTA = slc(src, '<section class="final-cta">', "</section>")
    WA_FLOAT = slc(src, '<a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring', "</a>")
    CLOSING_SCRIPTS = src[src.index("<script>\n(function(){var t=document.getElementById('menuToggle')"):
                          src.rindex("</html>") + len("</html>")]

    HEAD_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Palmetto, Florida">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://{DOMAIN}/images/{og_image}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Triangle Flooring">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://{DOMAIN}/images/{og_image}">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
"""

    BREADCRUMB = (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
                  f'<li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li>{bc_short}</li>'
                  f'</ol></div></nav>')

    ARTICLE_HERO = f"""<section class="article-hero">
  <div class="container">
    <span class="eyebrow">{category}</span>
    <h1>{h1}</h1>
    <div class="article-meta"><span>\U0001F4C5 Updated {date}</span><span>✍️ Jose Mauricio, Owner</span><span>\U0001F4D6 {read_min} min read</span></div>
  </div>
</section>"""

    toc = data.get("toc", [{"id": s["id"], "label": s["h2"]} for s in data["sections"]])
    toc_html = "".join(f'<li><a href="#{t["id"]}">{t["label"]}</a></li>' for t in toc)
    sections_html = "".join(
        f'\n<h2 id="{s["id"]}">{s["h2"]}</h2>\n{s["html"]}\n' for s in data["sections"])
    faq_h3s = "".join(f"<h3>{q}</h3>\n<p>{a}</p>\n\n" for q, a in faqs)
    knows = data.get("author_knows_about",
                     ["Flooring installation", "Floor repair", "Hardwood refinishing"])

    AUTHOR_CARD = """  <div class="author-card">
    <div style="width:64px;height:64px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--navy),var(--cerulean));color:#fff;display:grid;place-items:center;font-family:var(--font-head);font-weight:800;font-size:1.4rem">JM</div>
    <div>
      <strong>Jose Mauricio &mdash; Triangle Flooring</strong>
      <p>Owner and lead installer at Triangle Flooring, a licensed and insured Florida flooring contractor serving Bradenton, Sarasota, Lakewood Ranch, and Tampa Bay since 2023. 300+ projects completed. Every install backed by a 1-year written labor warranty.</p>
    </div>
  </div>"""

    ARTICLE = (
        '<article class="article-body">\n'
        '<div class="article-toc">\n  <strong>What\'s in this guide</strong>\n  <ol>'
        + toc_html + '</ol>\n</div>\n\n'
        + f'<p data-speakable="true">{data["answer_first"]}</p>\n'
        + sections_html
        + '\n<h2 id="faq">Frequently Asked Questions</h2>\n'
        + faq_h3s
        + AUTHOR_CARD + '\n</article>'
    )

    FAQ_SECTION = f"""<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">More Questions</span><h2>Frequently Asked</h2></div>
    {faq_accordion(faqs)}
  </div>
</section>"""

    rel = data.get("related_cards", [])
    RELATED = ""
    if rel:
        cards = "".join(card(c["href"], c.get("img"), c.get("cat", "Guides"),
                             c.get("date", date), c["title"], c.get("blurb", "")) for c in rel)
        RELATED = (f'<section class="related" style="background:var(--gray-light)">\n  <div class="container">\n'
                   f'    <div class="section-head"><span class="eyebrow">Continue Reading</span><h2>Related Guides</h2></div>\n'
                   f'    <div class="blog-list">{cards}</div>\n  </div>\n</section>')

    # JSON-LD
    plain_words = len(re.sub(r"<[^>]+>", " ", ARTICLE).split())
    breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://{DOMAIN}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://{DOMAIN}/blog/"},
        {"@type": "ListItem", "position": 3, "name": bc_short}]}
    author = {"@type": "Person", "name": "Jose Mauricio", "jobTitle": "Owner & Lead Installer",
              "worksFor": {"@type": "Organization", "name": "Triangle Flooring", "url": f"https://{DOMAIN}/about/"},
              "knowsAbout": knows}
    article_schema = {"@context": "https://schema.org", "@type": "Article",
                      "@id": f"{url}#article", "headline": h1, "description": desc,
                      "image": [f"https://{DOMAIN}/images/{og_image}"],
                      "datePublished": f"{date}T08:00:00-04:00", "dateModified": f"{date}T08:00:00-04:00",
                      "author": author,
                      "publisher": {"@type": "Organization", "name": "Triangle Flooring",
                                    "logo": {"@type": "ImageObject", "url": f"https://{DOMAIN}/images/logo.png",
                                             "width": 200, "height": 200}},
                      "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                      "articleSection": category, "wordCount": plain_words, "inLanguage": "en-US"}
    local_business = {"@context": "https://schema.org",
                      "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
                      "@id": f"https://{DOMAIN}/#business", "name": "Triangle Flooring",
                      "description": "Licensed and insured flooring contractor serving Bradenton, Sarasota, Lakewood Ranch and Tampa Bay, Florida.",
                      "url": f"https://{DOMAIN}/", "telephone": "+19414026861",
                      "image": f"https://{DOMAIN}/images/{og_image}",
                      "address": {"@type": "PostalAddress", "streetAddress": "8737 Royal Acacia Ave",
                                  "addressLocality": "Palmetto", "addressRegion": "FL",
                                  "postalCode": "34221", "addressCountry": "US"},
                      "geo": {"@type": "GeoCoordinates", "latitude": 27.5214, "longitude": -82.5723},
                      "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0",
                                          "reviewCount": "13", "bestRating": "5"},
                      "priceRange": "$$",
                      "areaServed": [{"@type": "City", "name": c} for c in CITIES],
                      "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                          "opens": "07:00", "closes": "19:00"}]}
    JSONLD = "\n".join([ld(breadcrumb_schema), ld(article_schema),
                        ld(faqpage_schema(faqs)), ld(local_business)])

    page = (HEAD_HTML + HEAD_STYLES_AND_GA + "\n<body>\n" + BODY_CSS + "\n" + HEADER + "\n"
            + BREADCRUMB + "\n\n" + ARTICLE_HERO + "\n\n" + ARTICLE + "\n\n" + FAQ_SECTION + "\n\n"
            + (RELATED + "\n\n" if RELATED else "") + FINAL_CTA + "\n\n" + FOOTER + "\n"
            + WA_FLOAT + "\n\n" + JSONLD + "\n\n" + CLOSING_SCRIPTS + "\n")

    out_dir = ROOT / "blog" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"  rendered blog/{slug}/index.html  ({plain_words} words, {len(faqs)} FAQ)")
    return out_dir / "index.html"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: render_post.py <slug>")
    slug = sys.argv[1]
    data = json.load(open(QUEUE_DIR / f"{slug}.json", encoding="utf-8"))
    render(data)


if __name__ == "__main__":
    main()
