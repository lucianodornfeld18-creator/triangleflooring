# -*- coding: utf-8 -*-
"""Restore the mobile media rule wrongly emptied by _fix_blog_authors.py."""
import io, glob, os

BLOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog")
OLD = "@media(max-width:768px){}"
NEW = "@media(max-width:768px){.article-feature-img img{aspect-ratio:16/10;max-height:240px}}"

n = 0
for path in sorted(glob.glob(os.path.join(BLOG, "*", "index.html"))):
    with io.open(path, "r", encoding="utf-8") as f:
        c = f.read()
    if OLD in c:
        c = c.replace(OLD, NEW)
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(c)
        n += 1
print("restaurados:", n)
