#!/usr/bin/env python3
"""Consolidate all audit/*.md into one standalone HTML report.
Minimal markdown subset renderer (headings, tables, lists, bold, code, hr,
blockquote, paragraphs) — input markdown is controlled by this audit, so the
subset is sufficient. Output: audit/triangle-flooring-audit.html
"""
import os, re, html, json, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(ROOT, "audit")

ORDER = [
    ("README.md", "Executive Summary"),
    ("00-inventory.md", "Phase 0 — Inventory"),
    ("01-scored-audit.md", "Phase 1 — Scored Audit"),
    ("02-data-needed.md", "Phase 2 — Data Needed"),
    ("03-competitors.md", "Phase 3 — Competitors"),
    ("04-brechas.md", "Phase 4 — Brechas"),
    ("05-blind-spots.md", "Phase 5 — Blind Spots"),
    ("06-scorecard.md", "Phase 6a — Scorecard"),
    ("06-plan-60-days.md", "Phase 6b — 60-Day Plan"),
    ("fixes-applied.md", "Fixes Applied"),
]

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s

def render(md):
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i+1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div class="tw"><table><thead><tr>'] + [f"<th>{inline(c)}</th>" for c in header] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            lv = len(m.group(1))
            out.append(f"<h{lv}>{inline(m.group(2))}</h{lv}>")
            i += 1; continue
        if re.match(r"^\s*---\s*$", line):
            out.append("<hr>"); i += 1; continue
        if line.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>"); continue
        if re.match(r"^\s*[-*]\s+", line):
            buf = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                buf.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+','',lines[i]))}</li>"); i += 1
            out.append("<ul>" + "".join(buf) + "</ul>"); continue
        if re.match(r"^\s*\d+\.\s+", line):
            buf = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                buf.append(f"<li>{inline(re.sub(r'^\s*\d+\.\s+','',lines[i]))}</li>"); i += 1
            out.append("<ol>" + "".join(buf) + "</ol>"); continue
        if line.strip() == "":
            i += 1; continue
        buf = [line]; i += 1
        while i < n and lines[i].strip() != "" and not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|\s*\||>|\s*---\s*$)", lines[i]):
            buf.append(lines[i]); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)

sections, nav = [], []
for fn, title in ORDER:
    path = os.path.join(AUD, fn)
    if not os.path.exists(path):
        continue
    md = open(path, encoding="utf-8").read()
    sid = fn.replace(".", "-")
    nav.append(f'<a href="#{sid}">{html.escape(title)}</a>')
    sections.append(f'<section id="{sid}"><div class="card">{render(md)}</div></section>')

inv = list(csv.DictReader(open(os.path.join(AUD, "00-inventory.csv"), encoding="utf-8")))
total_pages = len(inv)
avg_words = sum(int(r["word_count"]) for r in inv)//total_pages if total_pages else 0

CSS = """
:root{--navy:#1A4F8C;--navy-dark:#0F3A6E;--navy-light:#E8F2FB;--cerulean:#2E8DD9;--orange:#E07A2B;--orange-dark:#C56619;--text:#1B2939;--gray:#5B6B7E;--gray-light:#F7F9FC;--border:#E2E8F0;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif;color:var(--text);background:var(--gray-light);line-height:1.6;font-size:15px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header.hero{background:linear-gradient(135deg,var(--navy-dark),var(--navy) 60%,var(--cerulean));color:#fff;padding:54px 0 40px}
header.hero h1{font-size:2.1rem;font-weight:800;letter-spacing:-.02em;margin-bottom:6px}
header.hero p{opacity:.9;max-width:760px}
.scorebar{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.score{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:12px 16px;min-width:120px}
.score .v{font-size:1.5rem;font-weight:800}
.score .l{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;opacity:.85}
.score.big{background:var(--orange);border-color:var(--orange)}
nav.toc{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--border);box-shadow:0 2px 8px rgba(15,58,110,.06)}
nav.toc .wrap{display:flex;gap:4px;overflow-x:auto;padding:10px 20px}
nav.toc a{white-space:nowrap;font-size:.82rem;font-weight:600;color:var(--navy);padding:7px 12px;border-radius:50px;text-decoration:none;transition:.2s}
nav.toc a:hover{background:var(--navy-light)}
main{padding:30px 0 60px}
section{margin-bottom:26px;scroll-margin-top:64px}
.card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:30px 34px;box-shadow:0 4px 14px rgba(15,58,110,.05)}
h1,h2,h3,h4{font-weight:800;letter-spacing:-.01em;line-height:1.25;color:var(--navy-dark)}
.card>h1{font-size:1.7rem;border-bottom:3px solid var(--orange);padding-bottom:10px;margin-bottom:16px;color:var(--navy)}
.card h2{font-size:1.3rem;margin:26px 0 10px;padding-top:6px;border-top:1px solid var(--border)}
.card h3{font-size:1.08rem;margin:18px 0 6px;color:var(--text)}
.card h4{font-size:.96rem;margin:12px 0 4px;color:var(--gray)}
p{margin:8px 0}
ul,ol{margin:8px 0 8px 22px}
li{margin:3px 0}
code{background:var(--navy-light);color:var(--navy-dark);padding:1px 6px;border-radius:5px;font-family:'Consolas',monospace;font-size:.86em}
strong{color:var(--navy-dark)}
hr{border:0;border-top:1px solid var(--border);margin:18px 0}
blockquote{border-left:4px solid var(--cerulean);background:var(--navy-light);padding:10px 16px;border-radius:0 8px 8px 0;margin:12px 0;color:var(--navy-dark)}
.tw{overflow-x:auto;margin:14px 0;border:1px solid var(--border);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.84rem}
th{background:var(--navy);color:#fff;text-align:left;padding:9px 11px;font-weight:600;white-space:nowrap}
td{padding:8px 11px;border-top:1px solid var(--border);vertical-align:top}
tr:nth-child(even) td{background:var(--gray-light)}
a{color:var(--cerulean)}
footer{text-align:center;color:var(--gray);font-size:.8rem;padding:24px 0 40px}
@media print{nav.toc{display:none}.card{box-shadow:none;break-inside:avoid}header.hero{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Triangle Flooring — SEO/GEO/AEO Domination Audit</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero"><div class="wrap">
<h1>Triangle Flooring — SEO / GEO / AEO Domination Audit</h1>
<p>Full technical, on-page, schema, AI-citation, local, off-page, social and conversion audit of triangle-floor.com. Generated 2026-06-09 from a static crawl of {total_pages} pages.</p>
<div class="scorebar">
<div class="score big"><div class="v">71/100</div><div class="l">Overall</div></div>
<div class="score"><div class="v">{total_pages}</div><div class="l">Pages</div></div>
<div class="score"><div class="v">{avg_words:,}</div><div class="l">Avg words</div></div>
<div class="score"><div class="v">8.0</div><div class="l">Technical</div></div>
<div class="score"><div class="v">5.1</div><div class="l">AEO</div></div>
<div class="score"><div class="v">2.5</div><div class="l">Off-page</div></div>
</div>
</div></header>
<nav class="toc"><div class="wrap">{''.join(nav)}</div></nav>
<main><div class="wrap">
{''.join(sections)}
</div></main>
<footer>Triangle Flooring SEO/GEO/AEO Audit · 2026-06-09 · generated by Claude Code from /audit/*.md</footer>
</body>
</html>"""

out_path = os.path.join(AUD, "triangle-flooring-audit.html")
open(out_path, "w", encoding="utf-8").write(HTML)
print(json.dumps({"out": out_path, "sections": len(sections), "bytes": len(HTML)}, indent=2))
