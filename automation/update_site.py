#!/usr/bin/env python3
"""
update_site.py <slug> - wire a freshly-rendered post into the site.

Idempotent: skips work it has already done (safe to re-run).
  1. inject a blog card at the TOP of blog/index.html (.blog-list)
  2. add a <url> entry to sitemap.xml (and bump the blog index lastmod)
  3. mark the queue item status: "published" in _content_queue.json

Card meta (title/category/blurb/image/date) comes from automation/queue/<slug>.json.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOMAIN = "triangle-floor.com"
BLOG_INDEX = ROOT / "blog" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
QUEUE = ROOT / "_content_queue.json"
QUEUE_DIR = Path(__file__).parent / "queue"


def inject_card(data):
    slug = data["slug"]
    href = f"/blog/{slug}/"
    html = BLOG_INDEX.read_text(encoding="utf-8")
    if f'href="{href}"' in html:
        print("  blog index: card already present, skipping")
        return
    img = data.get("og_image", "card-repair.webp")
    cat = data.get("category", "Flooring Guides")
    date = data["date"]
    title = data.get("card_title", data.get("h1", data["title"]))
    blurb = data.get("card_blurb", data["meta_desc"])
    card = (
        f'<a href="{href}" class="blog-card">\n'
        f'          <div class="blog-card-photo"><img src="/images/{img}" alt="{title}" loading="lazy"></div>\n'
        f'          <div class="blog-card-body">\n'
        f'            <div class="blog-card-meta"><span>{cat}</span><span>{date}</span></div>\n'
        f'            <h2>{title}</h2>\n'
        f'            <p>{blurb}</p>\n'
        f'            <span class="blog-card-link">Read article →</span>\n'
        f'          </div>\n        </a>'
    )
    marker = '<div class="blog-list">'
    i = html.index(marker) + len(marker)
    html = html[:i] + card + html[i:]
    BLOG_INDEX.write_text(html, encoding="utf-8")
    print("  blog index: card inserted at top")


def add_to_sitemap(data):
    slug = data["slug"]
    loc = f"https://{DOMAIN}/blog/{slug}/"
    date = data["date"]
    xml = SITEMAP.read_text(encoding="utf-8")
    if loc in xml:
        print("  sitemap: url already present, skipping")
    else:
        entry = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{date}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n")
        xml = xml.replace("</urlset>", entry + "</urlset>")
        print("  sitemap: url added")
    # bump blog index lastmod so the listing change is seen
    xml = re.sub(
        r'(<loc>https://' + re.escape(DOMAIN) + r'/blog/</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
        r'\g<1>' + date + r'\g<2>', xml)
    SITEMAP.write_text(xml, encoding="utf-8")


def mark_published(slug):
    if not QUEUE.exists():
        return
    q = json.load(open(QUEUE, encoding="utf-8"))
    hit = False
    for item in q.get("backlog_new", []):
        if item.get("slug") == f"/blog/{slug}/" or item.get("slug") == slug:
            item["status"] = "published"
            hit = True
    if hit:
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  queue: marked {slug} as published")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: update_site.py <slug>")
    slug = sys.argv[1]
    data = json.load(open(QUEUE_DIR / f"{slug}.json", encoding="utf-8"))
    inject_card(data)
    add_to_sitemap(data)
    mark_published(slug)
    print(f"  site wired for {slug}")


if __name__ == "__main__":
    main()
