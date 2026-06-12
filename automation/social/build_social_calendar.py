#!/usr/bin/env python3
"""Gera o calendario de posts sociais (GBP + Facebook/Instagram), 4x/semana cada.

Uso:
    py automation/social/build_social_calendar.py [semanas] [data-inicio YYYY-MM-DD]

Saida:
    automation/social/calendar-<inicio>.json   (fila pra agendar no Metricool/Make)
    automation/social/preview-<inicio>.html    (revisao visual de tudo)

Rotaciona servico x cidade x foto do banco (image_bank.json), com legendas
EN focadas em SEO/GEO/AEO: keyword servico+cidade na 1a frase, deep link pra
pagina do servico/cidade, hashtags locais no FB/IG (GBP sem spam de hashtag).
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK = json.loads((Path(__file__).parent / "image_bank.json").read_text(encoding="utf-8"))
SITE = "https://triangle-floor.com"
IMG_BASE = f"{SITE}/images/social"
PHONE = "(941) 402-6861"

CITIES = ["Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto", "Parrish",
          "Venice", "St. Petersburg", "Tampa"]

SERVICES = {
    "hardwood": {"name": "Hardwood Flooring", "kw": "hardwood flooring installation", "path": "/hardwood-flooring/"},
    "vinyl":    {"name": "Luxury Vinyl Plank", "kw": "luxury vinyl plank (LVP) installation", "path": "/vinyl-plank-flooring/"},
    "tile":     {"name": "Tile Installation", "kw": "porcelain tile installation", "path": "/tile-installation/"},
    "laminate": {"name": "Laminate Flooring", "kw": "laminate flooring installation", "path": "/laminate-flooring/"},
    "stairs":   {"name": "Stair Treads", "kw": "custom stair tread installation", "path": "/stair-treads/"},
}

# Paginas de cidade existentes no site (slug = cidade em kebab-case)
CITY_PATHS = {c: "/" + c.lower().replace(" ", "-").replace(".", "") + "/" for c in CITIES}
CITY_PATHS["St. Petersburg"] = "/st-petersburg/"

FBIG_TEMPLATES = [
    "{kw_title} in {city}, FL done right. {desc}. 300+ floors installed across {city} and the Tampa Bay area — 5.0★ rated on Google.\n\n📞 Free estimate in 24h: {phone}\n🔗 {link}\n\n{tags}",
    "Looking for {kw} in {city}, Florida? This is what our work looks like. {desc}. Licensed flooring contractor serving {city} homeowners with a 5.0★ Google rating.\n\n📞 {phone} — free in-home estimate\n🔗 {link}\n\n{tags}",
    "Another {svc_name} project completed near {city}, FL ✅ {desc}. From Bradenton to Tampa, we install floors built for Florida humidity.\n\n📞 Call {phone} for a free estimate\n🔗 {link}\n\n{tags}",
    "Before you choose a flooring contractor in {city}, FL — look at the work, not just the price. {desc}. 300+ projects, 5.0★ on Google, free estimates within 24 hours.\n\n📞 {phone}\n🔗 {link}\n\n{tags}",
]

GBP_TEMPLATES = [
    "{kw_title} in {city}, FL — {desc}. Triangle Flooring has completed 300+ projects across {city}, Bradenton, Sarasota and Tampa Bay, with a 5.0★ rating on Google. Free in-home estimate within 24 hours. Call {phone}.",
    "Recent project: {desc}. If you're comparing flooring contractors in {city}, Florida, ask for photos of real local work — this is ours. Licensed, 5.0★ Google rated, free estimates in 24h. {phone}.",
    "Why {city} homeowners choose us for {kw}: real local projects, honest pricing, and floors specified for Florida humidity. {desc}. Free estimate: {phone}.",
]

GENERIC_TAGS = ["#FloridaFlooring", "#TampaBay", "#FlooringContractor", "#HomeRenovation",
                "#FloorsOfInstagram", "#BeforeAndAfter", "#FloridaHomes", "#FlooringInstallation"]

SVC_TAGS = {
    "hardwood": ["#HardwoodFloors", "#HardwoodFlooring", "#WhiteOak", "#Herringbone"],
    "vinyl": ["#LuxuryVinylPlank", "#LVP", "#VinylPlankFlooring", "#WaterproofFlooring"],
    "tile": ["#TileInstallation", "#PorcelainTile", "#TileFloors", "#MarbleLook"],
    "laminate": ["#LaminateFlooring", "#LaminateFloors", "#WoodLookFloors"],
    "stairs": ["#StairRemodel", "#StairTreads", "#StaircaseDesign", "#CustomStairs"],
}


def city_tags(city: str) -> list[str]:
    compact = city.replace(" ", "").replace(".", "")
    return [f"#{compact}", f"#{compact}FL", f"#{compact}Flooring"]


def pick(seq, i):
    return seq[i % len(seq)]


def build(weeks: int, start: datetime) -> list[dict]:
    posts = []
    # banco ordenado: prioriza fotos com cidade (mais sinal GEO)
    bank = sorted(BANK, key=lambda b: b["city"] is None)
    fbig_days, gbp_days = [0, 2, 4, 5], [1, 3, 5, 6]  # seg/qua/sex/sab e ter/qui/sab/dom
    img_i = 0
    for w in range(weeks):
        for slot in range(4):
            img = pick(bank, img_i)
            svc = SERVICES[img["service"]]
            city = img["city"] or pick(CITIES, img_i)
            link = SITE + (CITY_PATHS.get(city, svc["path"]) if img["city"] else svc["path"])
            tags = " ".join(city_tags(city) + SVC_TAGS[img["service"]] + GENERIC_TAGS[:7])
            ctx = dict(kw=svc["kw"], kw_title=svc["kw"].capitalize(), svc_name=svc["name"],
                       city=city, desc=img["desc"], phone=PHONE, link=link, tags=tags)

            d_fb = start + timedelta(days=w * 7 + fbig_days[slot])
            posts.append({
                "date": d_fb.strftime("%Y-%m-%dT") + ("11:30:00" if slot % 2 == 0 else "18:00:00"),
                "channel": "fbig",
                "service": img["service"], "city": city,
                "image_url": f"{IMG_BASE}/{img['file']}",
                "caption": pick(FBIG_TEMPLATES, img_i).format(**ctx),
                "link": link,
            })
            d_g = start + timedelta(days=w * 7 + gbp_days[slot])
            posts.append({
                "date": d_g.strftime("%Y-%m-%dT") + "09:00:00",
                "channel": "gbp",
                "service": img["service"], "city": city,
                "image_url": f"{IMG_BASE}/{img['file']}",
                "caption": pick(GBP_TEMPLATES, img_i).format(**ctx),
                "link": link,
            })
            img_i += 1
    return posts


def preview_html(posts: list[dict]) -> str:
    cards = []
    for p in posts:
        cards.append(f"""<div class="card {p['channel']}">
<img src="{p['image_url'].replace(IMG_BASE, '../../images/social')}" loading="lazy">
<div class="body"><span class="ch">{'Google Posts' if p['channel'] == 'gbp' else 'Facebook + Instagram'}</span>
<span class="dt">{p['date'][:16].replace('T', ' ')}</span>
<pre>{p['caption']}</pre></div></div>""")
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>Preview — Calendário Social Triangle Flooring</title><style>
body{{font-family:'Segoe UI',sans-serif;background:#F7F9FC;padding:24px;color:#1B2939}}
h1{{color:#0F3A6E}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-top:18px}}
.card{{background:#fff;border-radius:12px;overflow:hidden;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(15,58,110,.08)}}
.card img{{width:100%;aspect-ratio:1/1;height:auto;object-fit:cover;display:block}}.body{{padding:14px}}
.ch{{font-size:.72rem;font-weight:700;text-transform:uppercase;padding:2px 10px;border-radius:20px}}
.gbp .ch{{background:#D1FAE5;color:#065F46}}.fbig .ch{{background:#E0E7FF;color:#3730A3}}
.dt{{float:right;font-size:.8rem;color:#5B6B7E}}
pre{{white-space:pre-wrap;font-family:inherit;font-size:.85rem;margin-top:10px;line-height:1.5}}
</style></head><body><h1>📅 Calendário Social — {len(posts)} posts</h1>
<p>GBP (verde) e FB+IG (azul), 4x/semana cada. Gerado por build_social_calendar.py.</p>
<div class="grid">{''.join(cards)}</div></body></html>"""


def main():
    weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    start = (datetime.strptime(sys.argv[2], "%Y-%m-%d") if len(sys.argv) > 2
             else datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7 or 7))
    posts = build(weeks, start)
    stamp = start.strftime("%Y-%m-%d")
    out = Path(__file__).parent / f"calendar-{stamp}.json"
    out.write_text(json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8")
    prev = Path(__file__).parent / f"preview-{stamp}.html"
    prev.write_text(preview_html(posts), encoding="utf-8")
    print(f"{len(posts)} posts -> {out.name} + {prev.name} (inicio {stamp}, {weeks} semanas)")


if __name__ == "__main__":
    main()
