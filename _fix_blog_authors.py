# -*- coding: utf-8 -*-
"""One-off maintenance: fix blog deformation + standardize author to Jose Mauricio.

Per post in blog/*/index.html:
  1. Remove duplicated CSS override that squashes the feature image to 240px.
  2. Ensure byline span "Jose Mauricio, Owner" in .article-meta.
  3. Article JSON-LD author: Organization -> Person Jose Mauricio (reviews untouched).
  4. Ensure the JM author-card before </article> (swap old TF card / insert if absent).
Reference card is read at runtime from an already-correct post so bytes match exactly.
"""
import io, glob, os, re

BLOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog")
REF = os.path.join(BLOG, "best-flooring-concrete-slab-florida", "index.html")

BAD_CSS = ".article-feature-img img{aspect-ratio:16/10;max-height:240px}"
OLD_AUTHOR = '"author": {"@type": "Organization", "name": "Triangle Flooring", "url": "https://triangle-floor.com/about/"}'
NEW_AUTHOR = ('"author": {"@type": "Person", "name": "Jose Mauricio", "jobTitle": "Owner & Lead Installer", '
              '"worksFor": {"@type": "Organization", "name": "Triangle Flooring", "url": "https://triangle-floor.com/about/"}}')
OLD_BYLINE = "<span>✍️ Triangle Flooring</span>"
NEW_BYLINE = "<span>✍️ Jose Mauricio, Owner</span>"
META_RE = re.compile(r'(<div class="article-meta"><span>\U0001f4c5 [^<]*</span>)')

def load(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()

def save(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

ref = load(REF)
cs = ref.index('<div class="author-card">')
ce = ref.index("</article>", cs)
NEW_CARD = ref[cs:ce]

stats = {"css": 0, "byline_swap": 0, "byline_ins": 0, "schema": 0, "card_swap": 0, "card_ins": 0, "skip": []}

for path in sorted(glob.glob(os.path.join(BLOG, "*", "index.html"))):
    c = load(path)
    orig = c

    if BAD_CSS in c:
        c = c.replace(BAD_CSS + "\n", "").replace(BAD_CSS, "")
        stats["css"] += 1

    if OLD_BYLINE in c:
        c = c.replace(OLD_BYLINE, NEW_BYLINE)
        stats["byline_swap"] += 1
    elif "Jose Mauricio, Owner" not in c:
        c2 = META_RE.sub(lambda m: m.group(1) + NEW_BYLINE, c, count=1)
        if c2 != c:
            c = c2
            stats["byline_ins"] += 1
        else:
            stats["skip"].append(("byline", path))

    if OLD_AUTHOR in c:
        c = c.replace(OLD_AUTHOR, NEW_AUTHOR)
        stats["schema"] += 1

    ci = c.find('<div class="author-card">')
    if ci >= 0:
        if "Jose Mauricio &mdash; Triangle Flooring" not in c:
            ei = c.index("</article>", ci)
            c = c[:ci] + NEW_CARD + c[ei:]
            stats["card_swap"] += 1
    else:
        ai = c.find("</article>")
        if ai > 0:
            c = c[:ai] + NEW_CARD + "  " + c[ai:]
            stats["card_ins"] += 1
        else:
            stats["skip"].append(("card", path))

    if c != orig:
        save(path, c)

for k in ("css", "byline_swap", "byline_ins", "schema", "card_swap", "card_ins"):
    print(k, "=", stats[k])
for item in stats["skip"]:
    print("SKIP:", item[0], os.path.relpath(item[1], BLOG))
print("done")
