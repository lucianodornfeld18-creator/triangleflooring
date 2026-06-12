#!/usr/bin/env python3
"""Gera criativos 1080x1080 com a marca pra cada slot do calendario social.

3 templates padrao rotativos (mesma linguagem visual das capas FB/GMB):
  T1 showcase  — foto full-bleed + faixa gradiente navy embaixo
  T2 panel     — painel navy a esquerda + foto a direita
  T3 frame     — moldura clara, foto em card + tipografia navy

Uso:
    py automation/social/gen_creatives.py [calendar-YYYY-MM-DD.json]

Pipeline: escreve creatives/<id>.html -> screenshot via Chrome headless (PNG)
-> (conversao p/ JPG feita fora, via sharp) -> atualiza image_url no calendar
-> regera o preview.
"""
import json
import subprocess
import sys
from pathlib import Path

from build_social_calendar import SERVICES, preview_html, IMG_BASE, SITE

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PHONE = "(941) 402-6861"

FONTS = "<link href='https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&display=swap' rel='stylesheet'>"
BASE_CSS = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden;font-family:'Outfit',sans-serif}
.stars{color:#FFC53D;letter-spacing:6px}"""


def t1_showcase(ctx):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.c{{position:relative;width:1080px;height:1080px;background:#0E2A4A}}
img.ph{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.ov{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,32,56,.30) 0%,rgba(14,32,56,0) 28%,rgba(13,26,46,0) 46%,rgba(13,26,46,.94) 100%)}}
.logo{{position:absolute;top:52px;left:56px;height:108px;mix-blend-mode:screen}}
.bt{{position:absolute;left:64px;right:64px;bottom:60px;color:#fff}}
.eyebrow{{font-size:30px;font-weight:700;letter-spacing:7px;text-transform:uppercase;color:#FF9D4D;margin-bottom:14px}}
h1{{font-size:88px;font-weight:800;line-height:1.04;letter-spacing:-2px;margin-bottom:26px}}
.row{{display:flex;align-items:center;gap:26px}}
.badge{{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.13);border:1.5px solid rgba(255,255,255,.3);border-radius:60px;padding:14px 28px;font-size:27px;font-weight:600;backdrop-filter:blur(6px)}}
.phone{{background:#E07A2B;border-radius:16px;padding:16px 30px;font-size:32px;font-weight:800;letter-spacing:.5px}}
.site{{position:absolute;right:64px;bottom:24px;font-size:24px;font-weight:600;color:rgba(255,255,255,.85);letter-spacing:1px}}
</style></head><body><div class="c">
<img class="ph" src="{ctx['photo']}"><div class="ov"></div>
<img class="logo" src="../../../images/logo-dark.png">
<div class="bt">
<div class="eyebrow">{ctx['svc']}</div>
<h1>{ctx['city']}, Florida</h1>
<div class="row">
<div class="badge"><span class="stars">★★★★★</span> 5.0 Google</div>
<div class="badge">300+ Projects</div>
<div class="phone">{PHONE}</div>
</div></div>
<div class="site">triangle-floor.com</div>
</div></body></html>"""


def t2_panel(ctx):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.c{{position:relative;width:1080px;height:1080px;display:flex;background:#0F2A4E}}
.panel{{position:relative;width:46%;background:linear-gradient(160deg,#143A66 0%,#0E2440 100%);color:#fff;padding:72px 56px;display:flex;flex-direction:column;z-index:2}}
.panel::after{{content:"";position:absolute;top:0;right:-70px;width:140px;height:100%;background:inherit;clip-path:polygon(0 0,100% 0,50% 100%,0 100%)}}
.ph-wrap{{position:relative;width:54%;z-index:1}}
img.ph{{width:100%;height:100%;object-fit:cover}}
.logo{{height:128px;mix-blend-mode:screen;align-self:flex-start;margin-left:-10px}}
.eyebrow{{margin-top:64px;font-size:27px;font-weight:700;letter-spacing:6px;text-transform:uppercase;color:#FF9D4D}}
h1{{font-size:78px;font-weight:800;line-height:1.05;letter-spacing:-2px;margin-top:14px}}
.sub{{margin-top:22px;font-size:30px;font-weight:500;color:#BCD7F2;line-height:1.4}}
.rate{{margin-top:38px;font-size:25px;font-weight:700;white-space:nowrap}}.rate .stars{{font-size:28px;letter-spacing:4px}}
.spacer{{flex:1}}
.phone{{align-self:flex-start;background:#E07A2B;border-radius:16px;padding:18px 32px;font-size:34px;font-weight:800}}
.site{{margin-top:18px;font-size:25px;font-weight:600;color:#9FC3E8;letter-spacing:1px}}
</style></head><body><div class="c">
<div class="panel">
<img class="logo" src="../../../images/logo-dark.png">
<div class="eyebrow">{ctx['svc']}</div>
<h1>{ctx['city']},<br>Florida</h1>
<div class="sub">Free in-home estimate within 24 hours</div>
<div class="rate"><span class="stars">★★★★★</span>&nbsp; 5.0 on Google</div>
<div class="spacer"></div>
<div class="phone">{PHONE}</div>
<div class="site">triangle-floor.com</div>
</div>
<div class="ph-wrap"><img class="ph" src="{ctx['photo']}"></div>
</div></body></html>"""


def t3_frame(ctx):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}<style>{BASE_CSS}
.c{{position:relative;width:1080px;height:1080px;background:#F4EFE6;padding:56px;display:flex;flex-direction:column}}
.ph-card{{position:relative;height:600px;border-radius:28px;overflow:hidden;box-shadow:0 30px 70px rgba(15,42,78,.35)}}
img.ph{{width:100%;height:100%;object-fit:cover}}
.chip{{position:absolute;top:28px;left:28px;background:rgba(13,26,46,.82);color:#fff;border-radius:60px;padding:12px 26px;font-size:25px;font-weight:700;backdrop-filter:blur(6px)}}
.chip .stars{{font-size:26px;letter-spacing:3px}}
.body{{flex:1;display:flex;flex-direction:column;padding:46px 12px 0}}
.eyebrow{{font-size:28px;font-weight:700;letter-spacing:7px;text-transform:uppercase;color:#C2611A}}
h1{{font-size:84px;font-weight:800;line-height:1.03;letter-spacing:-2px;color:#11335C;margin-top:12px}}
.rule{{width:130px;height:8px;background:#E07A2B;border-radius:6px;margin:26px 0 0}}
.foot{{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-bottom:6px}}
.brand{{display:flex;align-items:center;gap:18px}}
.brand img{{height:84px}}
.brand .nm{{font-size:30px;font-weight:800;color:#11335C;line-height:1.1}}
.brand .ar{{font-size:21px;font-weight:600;color:#5B6B7E;letter-spacing:1px}}
.phone{{background:#11335C;color:#fff;border-radius:16px;padding:18px 30px;font-size:31px;font-weight:800}}
</style></head><body><div class="c">
<div class="ph-card"><img class="ph" src="{ctx['photo']}">
<div class="chip"><span class="stars">★★★★★</span> 5.0 Google Rated</div></div>
<div class="body">
<div class="eyebrow">{ctx['svc']}</div>
<h1>{ctx['city']}, Florida</h1>
<div class="rule"></div>
<div class="foot">
<div class="brand"><img src="../../../images/logo.png">
<div><div class="nm">Triangle Flooring</div><div class="ar">triangle-floor.com</div></div></div>
<div class="phone">{PHONE}</div>
</div></div>
</div></body></html>"""


TEMPLATES = [t1_showcase, t2_panel, t3_frame]


def main():
    cal_name = sys.argv[1] if len(sys.argv) > 1 else sorted(HERE.glob("calendar-*.json"))[-1].name
    cal_path = HERE / cal_name
    posts = json.loads(cal_path.read_text(encoding="utf-8"))

    out_html = HERE / "creatives"
    out_html.mkdir(exist_ok=True)
    out_img = ROOT / "images" / "social" / "posts"
    out_img.mkdir(parents=True, exist_ok=True)

    # slots: pares fbig+gbp compartilham foto/cidade/servico -> 1 criativo por par
    seen = {}
    for i, p in enumerate(posts):
        key = (p["image_url"], p["city"], p["service"])
        if key not in seen:
            idx = len(seen)
            tpl = TEMPLATES[idx % len(TEMPLATES)]
            cid = f"c{idx + 1:02d}-{p['service']}-{p['city'].lower().replace(' ', '-').replace('.', '')}-t{idx % 3 + 1}"
            photo_rel = p["image_url"].replace(IMG_BASE, "../../../images/social")
            ctx = {"photo": photo_rel, "city": p["city"], "svc": SERVICES[p["service"]]["name"]}
            html_file = out_html / f"{cid}.html"
            html_file.write_text(tpl(ctx), encoding="utf-8")
            png = out_img / f"{cid}.png"
            subprocess.run([CHROME, "--headless=new", f"--screenshot={png}",
                            "--window-size=1080,1080", "--hide-scrollbars",
                            "--virtual-time-budget=8000", html_file.resolve().as_uri()],
                           check=True, capture_output=True)
            seen[key] = cid
            print(f"render {cid}")
        p["image_url"] = f"{IMG_BASE}/posts/{seen[key]}.jpg"

    cal_path.write_text(json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8")
    prev = HERE / cal_name.replace("calendar-", "preview-").replace(".json", ".html")
    prev.write_text(preview_html(posts), encoding="utf-8")
    print(f"{len(seen)} criativos -> images/social/posts/ | calendar + preview atualizados")


if __name__ == "__main__":
    main()
