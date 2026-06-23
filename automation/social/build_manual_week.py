#!/usr/bin/env python3
"""Gera a pagina de postagem MANUAL (Facebook + Instagram) da semana.

Enquanto o publisher do Facebook/Instagram nao esta ligado, esta pagina lista
os posts FB/IG da semana com botao de copiar legenda e baixar a arte — pratico
no celular. O Google ja publica sozinho, entao nao entra aqui.

Uso:
    py automation/social/build_manual_week.py [YYYY-MM-DD]
    (sem data = semana atual, segunda a domingo)

Saida: automation/social/manual-<segunda>.html  (abre no navegador)
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent

SERVICE_NAME = {"hardwood": "Hardwood", "vinyl": "Luxury Vinyl Plank",
                "tile": "Tile", "laminate": "Laminate", "stairs": "Stair Treads"}


def latest_calendar() -> Path:
    cals = sorted(HERE.glob("calendar-*.json"))
    if not cals:
        raise SystemExit("Nenhum calendar-*.json encontrado")
    return cals[-1]


def week_bounds(ref: datetime):
    monday = ref - timedelta(days=ref.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    return monday, monday + timedelta(days=7)


def main():
    ref = datetime.strptime(sys.argv[1], "%Y-%m-%d") if len(sys.argv) > 1 else datetime.now()
    start, end = week_bounds(ref)
    posts = json.loads(latest_calendar().read_text(encoding="utf-8"))

    week = []
    for p in posts:
        if p["channel"] not in ("fbig", "facebook", "instagram"):
            continue
        d = datetime.strptime(p["date"], "%Y-%m-%dT%H:%M:%S")
        if start <= d < end:
            week.append((d, p))
    week.sort(key=lambda x: x[0])

    cards = []
    for i, (d, p) in enumerate(week, 1):
        svc = SERVICE_NAME.get(p["service"], p["service"].title())
        day = d.strftime("%a %d/%m")
        cap = p["caption"]
        cards.append(f"""<div class="card">
  <div class="head"><span class="num">{i}</span><span class="day">{day}</span>
    <span class="tag">{svc} · {p['city']}</span></div>
  <img src="{p['image_url']}" alt="" loading="lazy">
  <div class="row">
    <a class="btn dl" href="{p['image_url']}" download target="_blank">⬇ Baixar imagem</a>
    <button class="btn cp" data-cap="cap{i}">📋 Copiar legenda</button>
  </div>
  <pre id="cap{i}">{cap}</pre>
</div>""")

    title_range = f"{start.strftime('%d/%m')} – {(end - timedelta(days=1)).strftime('%d/%m')}"
    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Posts manuais — semana {title_range}</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,sans-serif;background:#0F2A4E;color:#1B2939;padding:18px}}
.wrap{{max-width:520px;margin:0 auto}}
h1{{color:#fff;font-size:1.35rem;margin-bottom:2px}}
.sub{{color:#9FC3E8;font-size:.85rem;margin-bottom:8px}}
.note{{background:#173a63;color:#CFE3F7;border-radius:10px;padding:10px 13px;font-size:.82rem;margin-bottom:18px;line-height:1.5}}
.card{{background:#fff;border-radius:16px;overflow:hidden;margin-bottom:20px;box-shadow:0 10px 26px rgba(0,0,0,.28)}}
.head{{display:flex;align-items:center;gap:10px;padding:12px 14px 8px}}
.num{{background:#E07A2B;color:#fff;font-weight:800;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-size:.85rem}}
.day{{font-weight:700;color:#11335C;font-size:.9rem}}
.tag{{margin-left:auto;font-size:.74rem;font-weight:700;background:#E8F2FB;color:#1A4F8C;padding:3px 10px;border-radius:20px}}
.card img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}}
.row{{display:flex;gap:8px;padding:12px}}
.btn{{flex:1;text-align:center;border:none;border-radius:10px;padding:12px;font-size:.92rem;font-weight:700;cursor:pointer;text-decoration:none}}
.dl{{background:#E8F2FB;color:#1A4F8C}}
.cp{{background:#E07A2B;color:#fff}}
.cp.done{{background:#10B981}}
pre{{white-space:pre-wrap;font-family:inherit;font-size:.86rem;line-height:1.5;color:#1B2939;padding:0 14px 16px;margin:0}}
.foot{{color:#6f93bd;font-size:.78rem;text-align:center;margin-top:8px}}
</style></head><body><div class="wrap">
<h1>📲 Posts da semana — {title_range}</h1>
<div class="sub">Facebook + Instagram · {len(week)} posts</div>
<div class="note">Poste cada um no <b>Facebook</b> e no <b>Instagram</b> (@flooringtriangle): baixe a imagem, copie a legenda e cole. O Google já está saindo automático — não precisa postar lá.</div>
{''.join(cards) if cards else '<div class="note">Sem posts FB/IG nesta semana.</div>'}
<div class="foot">Triangle Flooring · uso interno</div>
</div>
<script>
document.querySelectorAll('.cp').forEach(b=>b.addEventListener('click',async()=>{{
  const t=document.getElementById(b.dataset.cap).innerText;
  try{{await navigator.clipboard.writeText(t);}}catch(e){{
    const r=document.createRange();r.selectNode(document.getElementById(b.dataset.cap));
    getSelection().removeAllRanges();getSelection().addRange(r);document.execCommand('copy');}}
  const o=b.textContent;b.textContent='✅ Copiado!';b.classList.add('done');
  setTimeout(()=>{{b.textContent=o;b.classList.remove('done');}},1500);
}}));
</script></body></html>"""

    out = HERE / f"manual-{start.strftime('%Y-%m-%d')}.html"
    out.write_text(html, encoding="utf-8")
    print(f"{len(week)} posts -> {out.name}")


if __name__ == "__main__":
    main()
