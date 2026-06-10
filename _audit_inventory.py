#!/usr/bin/env python3
"""Audit Phase 0 — full page inventory for Triangle Flooring.
Static analysis only. Parses every site HTML page and extracts SEO-relevant
fields. Outputs audit/00-inventory.csv + audit/00-inventory.md.
"""
import os, re, csv, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(ROOT, "audit")
os.makedirs(AUDIT, exist_ok=True)

# Internal-only docs / non-site pages to exclude from the inventory.
EXCLUDE_NAMES = {
    "PLANO-TOP1-2026-06.html", "GBP-COMPETITIVE-STRATEGY.html",
    "reviews-inspiracao.html", "diretorios-como-preencher.html",
    "offpage-checklist.html", "404.html",
}
EXCLUDE_DIRS = {".git", "__pycache__", "audit", "automation", "images"}

def file_to_url(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel

def strip_tags(s):
    s = re.sub(r"<script\b[^>]*>.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def attr(tag, name):
    m = re.search(name + r'\s*=\s*"([^"]*)"', tag, re.I)
    return m.group(1) if m else ""

def find_one(rx, text, flags=re.I | re.S):
    m = re.search(rx, text, flags)
    return m.group(1).strip() if m else ""

rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fn in filenames:
        if not fn.endswith(".html") or fn in EXCLUDE_NAMES:
            continue
        full = os.path.join(dirpath, fn)
        try:
            raw = open(full, encoding="utf-8", errors="replace").read()
        except Exception as e:
            print("ERR", full, e); continue

        url = file_to_url(full)
        head = raw[:raw.lower().find("</head>") + 7] if "</head>" in raw.lower() else raw

        lang = attr(find_one(r"(<html[^>]*>)", raw) or "<html>", "lang") or "?"
        title = strip_tags(find_one(r"<title[^>]*>(.*?)</title>", head))
        h1_raw = find_one(r"<h1[^>]*>(.*?)</h1>", raw)
        h1 = strip_tags(h1_raw)
        h1_count = len(re.findall(r"<h1\b", raw, re.I))
        meta_desc = ""
        for tag in re.findall(r"<meta\b[^>]*>", head, re.I):
            if re.search(r'name\s*=\s*"description"', tag, re.I):
                meta_desc = html.unescape(attr(tag, "content")); break
        canonical = ""
        for tag in re.findall(r"<link\b[^>]*>", head, re.I):
            if re.search(r'rel\s*=\s*"canonical"', tag, re.I):
                canonical = attr(tag, "href"); break
        robots_meta = ""
        for tag in re.findall(r"<meta\b[^>]*>", head, re.I):
            if re.search(r'name\s*=\s*"robots"', tag, re.I):
                robots_meta = attr(tag, "content"); break
        hreflang = len(re.findall(r'hreflang\s*=', head, re.I))

        body = strip_tags(raw)
        word_count = len(body.split())

        # schema types (explicit stack, no nested closure)
        schema_types = []
        for block in re.findall(r'<script[^>]*type\s*=\s*"application/ld\+json"[^>]*>(.*?)</script>', raw, re.S | re.I):
            try:
                data = json.loads(block.strip())
            except Exception:
                schema_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', block)
                continue
            stack = [data]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    t = o.get("@type")
                    if isinstance(t, str):
                        schema_types.append(t)
                    elif isinstance(t, list):
                        schema_types += [x for x in t if isinstance(x, str)]
                    stack.extend(o.values())
                elif isinstance(o, list):
                    stack.extend(o)
        schema_set = sorted(set(schema_types))

        # links
        hrefs = re.findall(r'<a\b[^>]*href\s*=\s*"([^"]+)"', raw, re.I)
        internal_out, external_out = set(), set()
        for h in hrefs:
            if h.startswith("#") or h.startswith("mailto:") or h.startswith("tel:") or h.startswith("javascript:"):
                continue
            if h.startswith("http"):
                if "triangle-floor.com" in h:
                    internal_out.add(re.sub(r"https?://(www\.)?triangle-floor\.com", "", h) or "/")
                else:
                    external_out.add(h)
            else:
                internal_out.add(h)

        # images
        imgs = re.findall(r"<img\b[^>]*>", raw, re.I)
        img_count = len(imgs)
        img_no_alt = sum(1 for t in imgs if not attr(t, "alt").strip())
        webp = len(re.findall(r'\.webp', raw, re.I))

        faq_q = len(re.findall(r'"@type"\s*:\s*"Question"', raw))
        ga4 = "G-7VP0F63NPC" in raw or "googletagmanager" in raw.lower()

        rows.append({
            "url": url, "lang": lang, "title": title, "title_len": len(title),
            "h1": h1, "h1_count": h1_count, "meta_desc": meta_desc,
            "meta_desc_len": len(meta_desc), "word_count": word_count,
            "schema_types": "|".join(schema_set), "n_schema": len(schema_set),
            "canonical": canonical, "robots_meta": robots_meta, "hreflang": hreflang,
            "int_links_out": len(internal_out), "ext_links_out": len(external_out),
            "img_count": img_count, "img_no_alt": img_no_alt, "faq_questions": faq_q,
            "ga4": int(bool(ga4)), "file": os.path.relpath(full, ROOT).replace("\\", "/"),
            "_int_targets": internal_out,
        })

# inbound internal links
def norm(u):
    u = u.split("#")[0].split("?")[0]
    if not u.startswith("/"): return None
    if not u.endswith("/") and not re.search(r"\.[a-z]+$", u):
        u = u + "/"
    return u
inbound = {r["url"]: 0 for r in rows}
for r in rows:
    seen = set()
    for t in r["_int_targets"]:
        n = norm(t)
        if n and n in inbound and n != r["url"]:
            seen.add(n)
    for n in seen:
        inbound[n] += 1
for r in rows:
    r["int_links_in"] = inbound[r["url"]]
    del r["_int_targets"]

rows.sort(key=lambda r: r["url"])

cols = ["url","lang","title","title_len","h1","h1_count","meta_desc","meta_desc_len",
        "word_count","schema_types","n_schema","canonical","robots_meta","hreflang",
        "int_links_in","int_links_out","ext_links_out","img_count","img_no_alt",
        "faq_questions","ga4","file"]
with open(os.path.join(AUDIT, "00-inventory.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in cols})

total = len(rows)
langs = {}
for r in rows: langs[r["lang"]] = langs.get(r["lang"], 0) + 1
all_schema = {}
for r in rows:
    for s in r["schema_types"].split("|"):
        if s: all_schema[s] = all_schema.get(s, 0) + 1
dup_titles = {}
for r in rows: dup_titles.setdefault(r["title"], []).append(r["url"])
dups = {t: u for t, u in dup_titles.items() if len(u) > 1}
no_canon = [r["url"] for r in rows if not r["canonical"]]
orphans = [r["url"] for r in rows if r["int_links_in"] == 0]
no_meta = [r["url"] for r in rows if not r["meta_desc"]]
multi_h1 = [(r["url"], r["h1_count"]) for r in rows if r["h1_count"] != 1]
no_ga = [r["url"] for r in rows if not r["ga4"]]
thin = [(r["url"], r["word_count"]) for r in rows if r["word_count"] < 600]
title_long = [(r["url"], r["title_len"]) for r in rows if r["title_len"] > 60]
md_long = [(r["url"], r["meta_desc_len"]) for r in rows if r["meta_desc_len"] > 160]
img_alt_issues = [(r["url"], r["img_no_alt"]) for r in rows if r["img_no_alt"] > 0]

def section(title, items, fmt=lambda x: f"- `{x}`"):
    out = [f"### {title} ({len(items)})", ""]
    out += [fmt(i) for i in items] if items else ["- _none_"]
    out.append("")
    return "\n".join(out)

with open(os.path.join(AUDIT, "00-inventory.md"), "w", encoding="utf-8") as f:
    f.write("# Phase 0 — Inventory & Ground Truth\n\n")
    f.write(f"**Total site pages inventoried:** {total} (excludes 404 + internal strategy docs)\n\n")
    f.write("**Languages (html lang attr):** " + ", ".join(f"`{k}`={v}" for k,v in sorted(langs.items())) + "\n\n")
    f.write(f"**Avg word count:** {sum(r['word_count'] for r in rows)//total} | "
            f"**Avg internal links out:** {sum(r['int_links_out'] for r in rows)//total} | "
            f"**Pages with GA4:** {sum(r['ga4'] for r in rows)}/{total}\n\n")
    f.write("**Schema @types across site:**\n\n")
    for s, c in sorted(all_schema.items(), key=lambda x: -x[1]):
        f.write(f"- `{s}` — {c} pages\n")
    f.write("\n## Flags\n\n")
    f.write(section("Duplicate titles", [f"{t}  ->  {', '.join(u)}" for t,u in dups.items()]))
    f.write(section("Pages missing canonical", no_canon))
    f.write(section("Pages missing meta description", no_meta))
    f.write(section("Orphan pages (0 inbound internal links)", orphans))
    f.write(section("Pages with !=1 H1", [f"{u} (h1count={c})" for u,c in multi_h1]))
    f.write(section("Pages missing GA4/GTM", no_ga))
    f.write(section("Hreflang present", [r["url"] for r in rows if r["hreflang"]>0]))
    f.write(section("Thin pages (<600 words)", [f"{u} ({c}w)" for u,c in sorted(thin, key=lambda x:x[1])]))
    f.write(section("Title >60 chars", [f"{u} ({c})" for u,c in title_long]))
    f.write(section("Meta desc >160 chars", [f"{u} ({c})" for u,c in md_long]))
    f.write(section("Pages with images missing alt", [f"{u} ({c} imgs)" for u,c in img_alt_issues]))

print(json.dumps({
    "total": total, "langs": langs, "schema_types": all_schema,
    "dup_titles": len(dups), "no_canonical": len(no_canon), "no_meta": len(no_meta),
    "orphans": len(orphans), "multi_h1": len(multi_h1), "no_ga4": len(no_ga),
    "hreflang_pages": sum(1 for r in rows if r["hreflang"]>0),
    "thin_pages": len(thin), "img_alt_issues": len(img_alt_issues),
    "avg_words": sum(r['word_count'] for r in rows)//total,
}, indent=2))
