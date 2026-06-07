#!/usr/bin/env python3
"""
validate_post.py <slug> [interlink1 interlink2 ...]

Parameterized port of the repo's _validate_post.py (which was hard-wired to the
water-damage slug). This is the SINGLE quality gate for the autonomous pipeline:
on autonomous push there is no human reviewer, so a non-zero exit here MUST abort
the commit (nothing gets published).

Exit 0 = pass (warnings allowed). Exit 1 = FAIL (do not publish).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def validate(slug, required_links=None):
    post = ROOT / "blog" / slug / "index.html"
    if not post.exists():
        print(f"FAIL: {post} does not exist")
        return False
    html = post.read_text(encoding="utf-8")
    errors, warns, oks = [], [], []

    # 1. Single DOCTYPE / single H1
    (oks if html.count("<!DOCTYPE html>") == 1 else errors).append("single <!DOCTYPE>")
    h1 = re.findall(r"<h1[ >]", html)
    (oks if len(h1) == 1 else errors).append(f"<h1> count = {len(h1)} (want 1)")

    # 2. Chrome present, no leftover slice markers
    for needed in ['<header class="site-header">', "</header>", "<footer>", "</footer>",
                   'class="whatsapp-float"', 'class="final-cta"', "getElementById('menuToggle')"]:
        (oks if needed in html else errors).append(f"chrome: {needed[:34]}")

    # 3. GA loader appears exactly once
    ga = html.count('googletagmanager.com/gtag/js?id=G-7VP0F63NPC')
    (oks if ga == 1 else errors).append(f"GA gtag loader x{ga} (want 1)")

    # 4. JSON-LD parses + required types
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
        if need not in types:
            errors.append(f"missing schema {need}")
    if not any("LocalBusiness" in t for t in types):
        warns.append("no LocalBusiness schema")

    # 5. FAQ schema == visible accordion
    faq_obj = next((json.loads(b) for b in blocks if '"FAQPage"' in b), None)
    schema_q = [q["name"] for q in faq_obj["mainEntity"]] if faq_obj else []
    vis_q = re.findall(r'<details class="faq-item"><summary>(.*?)</summary>', html)
    schema_a = [q["acceptedAnswer"]["text"] for q in faq_obj["mainEntity"]] if faq_obj else []
    vis_a = re.findall(r'<div class="faq-content"><p>(.*?)</p></div>', html)
    if schema_q == vis_q and schema_a == vis_a and len(vis_q) >= 6:
        oks.append(f"FAQPage schema == visible accordion ({len(vis_q)} Q&A)")
    else:
        errors.append(f"FAQ mismatch/short: schema {len(schema_q)}Q / visible {len(vis_q)}Q (want >=6, equal)")

    # 6. Internal links resolve
    links = set(re.findall(r'href="(/[^"#]*)"', html))
    for ln in sorted(links):
        p = ln.strip("/")
        if p == "":
            continue
        target = ROOT / p
        if target.is_dir() and (target / "index.html").exists():
            continue
        if target.exists():
            continue
        if (ROOT / (p + ".html")).exists():
            continue
        errors.append(f"broken internal link: {ln}")
    oks.append(f"checked {len(links)} internal links")

    # 7. Title / description uniqueness + length
    title = re.search(r"<title>(.*?)</title>", html).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', html).group(1)
    dup_t, dup_d = [], []
    for other in ROOT.rglob("index.html"):
        if other == post:
            continue
        o = other.read_text(encoding="utf-8", errors="ignore")
        mt = re.search(r"<title>(.*?)</title>", o)
        md = re.search(r'<meta name="description" content="(.*?)">', o)
        if mt and mt.group(1) == title:
            dup_t.append(str(other.relative_to(ROOT)))
        if md and md.group(1) == desc:
            dup_d.append(str(other.relative_to(ROOT)))
    (oks if not dup_t else errors).append("unique <title>" if not dup_t else f"title dup: {dup_t}")
    (oks if not dup_d else errors).append("unique meta description" if not dup_d else f"desc dup: {dup_d}")
    (oks if len(title) < 60 else errors).append(f"title {len(title)} chars (<60)")
    (oks if len(desc) < 155 else warns).append(f"description {len(desc)} chars (<155)")

    # 8. Answer-first / speakable, tables, required interlinks
    (oks if 'data-speakable="true"' in html else errors).append("answer-first speakable block")
    (oks if html.count("<table>") >= 1 else warns).append(f"{html.count('<table>')} tables (want >=2)")
    for must in (required_links or []):
        (oks if f'href="{must}"' in html else errors).append(f"required interlink {must}")

    # word count floor
    body = re.search(r'<article class="article-body">(.*?)</article>', html, re.S)
    words = len(re.sub(r"<[^>]+>", " ", body.group(1)).split()) if body else 0
    (oks if words >= 900 else errors).append(f"article ~{words} words (want >=900)")

    print(f"\n=== VALIDATION: blog/{slug}/index.html ===")
    for o in oks: print("  OK   ", o)
    for w in warns: print("  WARN ", w)
    for e in errors: print("  FAIL ", e)
    print(f"\n{len(oks)} ok / {len(warns)} warn / {len(errors)} fail")
    return not errors


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: validate_post.py <slug> [required_link ...]")
    ok = validate(sys.argv[1], sys.argv[2:])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
