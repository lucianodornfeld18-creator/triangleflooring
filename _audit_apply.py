#!/usr/bin/env python3
"""Idempotent in-place patcher for safe, site-wide audit fixes.
Operates on the committed HTML (the real deployed source — the _build_*.py
generators target a foreign OUT_DIR and do not regenerate in place).

Fixes applied:
  1. sameAs — add the canonical profile array to every LocalBusiness /
     Organization JSON-LD node that lacks it (was on 11/135 pages).

JSON-LD blocks are parsed as real JSON (json.loads) and re-serialized, never
regex-mutated. Re-running is a no-op once applied. Reversible via git.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# Canonical, verified public profiles (from footer + existing sameAs arrays).
SAME_AS = [
    "https://www.facebook.com/people/Triangle-Flooring/61567334333950/",
    "https://www.instagram.com/flooringtriangle",
    "https://share.google/TVRjAYdnZR3TS8Kzq",
    "https://www.yelp.com/biz/triangle-flooring-palmetto",
    "https://www.houzz.com/pro/trianglefloorus/__public",
    "https://nextdoor.com/pages/triangle-flooring/",
]
ENTITY_TYPES = {"LocalBusiness", "Organization", "HomeAndConstructionBusiness"}

EXCLUDE_NAMES = {
    "PLANO-TOP1-2026-06.html", "GBP-COMPETITIVE-STRATEGY.html",
    "reviews-inspiracao.html", "diretorios-como-preencher.html",
    "offpage-checklist.html",
}
EXCLUDE_DIRS = {".git", "__pycache__", "audit", "automation", "images"}

LD_RE = re.compile(r'(<script[^>]*type\s*=\s*"application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)

def node_is_entity(node):
    t = node.get("@type")
    if isinstance(t, str):
        return t in ENTITY_TYPES
    if isinstance(t, list):
        return any(x in ENTITY_TYPES for x in t)
    return False

def patch_node(node):
    """Add sameAs to entity nodes that lack it. Returns True if changed."""
    changed = False
    if isinstance(node, dict):
        if node_is_entity(node) and not node.get("sameAs"):
            node["sameAs"] = list(SAME_AS)
            changed = True
        for v in node.values():
            if patch_node(v):
                changed = True
    elif isinstance(node, list):
        for v in node:
            if patch_node(v):
                changed = True
    return changed

def process(path):
    raw = open(path, encoding="utf-8").read()
    blocks_changed = 0

    def repl(m):
        nonlocal blocks_changed
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(inner.strip())
        except Exception:
            return m.group(0)  # leave untouched if not parseable
        if patch_node(data):
            blocks_changed += 1
            new_inner = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            return open_tag + new_inner + close_tag
        return m.group(0)

    new_raw = LD_RE.sub(repl, raw)
    if blocks_changed:
        open(path, "w", encoding="utf-8", newline="").write(new_raw)
    return blocks_changed

changed_files = 0
changed_blocks = 0
scanned = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fn in filenames:
        if not fn.endswith(".html") or fn in EXCLUDE_NAMES:
            continue
        full = os.path.join(dirpath, fn)
        scanned += 1
        n = process(full)
        if n:
            changed_files += 1
            changed_blocks += n

print(json.dumps({
    "scanned_html": scanned,
    "files_changed": changed_files,
    "schema_blocks_patched": changed_blocks,
    "sameAs_entries": len(SAME_AS),
}, indent=2))
