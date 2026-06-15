#!/usr/bin/env python3
"""Esteira de fotos: jogue fotos cruas em automation/social/inbox/ e rode isto.

Para cada foto: Gemini classifica (servico + descricao + slug SEO), o arquivo
e convertido pra JPG 1080px com nome SEO/GEO (ex: luxury-vinyl-plank-living-
room-bradenton-fl.jpg), entra no image_bank.json e ja participa dos proximos
calendarios. Original vai pra inbox/processed/.

Cidade: inclua a cidade no nome do arquivo ao salvar no inbox (ex:
"tampa IMG_0123.jpg") — sem cidade no nome, entra como Florida (city null).

Uso:  py automation/social/ingest_photos.py
"""
import base64
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
INBOX = HERE / "inbox"
PROCESSED = INBOX / "processed"
DEST = ROOT / "images" / "social"
BANK = HERE / "image_bank.json"
MODEL = "gemini-2.5-flash"

SERVICES = ["hardwood", "vinyl", "tile", "laminate", "stairs"]
CITY_TOKENS = {
    "bradenton": "Bradenton", "sarasota": "Sarasota", "lakewood": "Lakewood Ranch",
    "palmetto": "Palmetto", "parrish": "Parrish", "venice": "Venice",
    "st-pete": "St. Petersburg", "stpete": "St. Petersburg", "st-petersburg": "St. Petersburg",
    "tampa": "Tampa",
}

PROMPT = (
    "You are tagging a flooring contractor's project photo for social media. "
    "Classify what the photo PRIMARILY shows. Respond ONLY with JSON: "
    '{"service": one of ["hardwood","vinyl","tile","laminate","stairs"], '
    '"desc": "8-14 word English description of what is visible (floor type, color, room)", '
    '"slug": "3-6 word kebab-case SEO filename slug, service keyword first, no city"} '
    "If stairs/treads are the main subject use stairs. Wood-look plank that may be "
    "vinyl or laminate: prefer vinyl unless clearly laminate."
)


def api_key() -> str:
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("GEMINI_API_KEY nao encontrada no .env")


def classify(img: Path) -> dict:
    mime = "image/png" if img.suffix.lower() == ".png" else "image/webp" if img.suffix.lower() == ".webp" else "image/jpeg"
    payload = {
        "contents": [{"parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": mime, "data": base64.b64encode(img.read_bytes()).decode()}},
        ]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.load(r)
    data = json.loads(resp["candidates"][0]["content"]["parts"][0]["text"])
    assert data["service"] in SERVICES, f"servico invalido: {data}"
    return data


def detect_city(filename: str):
    low = filename.lower().replace("_", "-").replace(" ", "-")
    for token, city in CITY_TOKENS.items():
        if token in low:
            return city
    return None


def unique_name(slug: str, city) -> str:
    base = f"{slug}-{(city or 'florida').lower().replace(' ', '-').replace('.', '')}-fl"
    base = re.sub(r"[^a-z0-9-]", "", base).strip("-")
    name, n = f"{base}.jpg", 2
    while (DEST / name).exists():
        name, n = f"{base}-{n}.jpg", n + 1
    return name


EXTS = (".jpg", ".jpeg", ".png", ".webp")


def convert(src: Path, dst: Path):
    subprocess.run(
        f'npx -y sharp-cli --input "{src}" --output "{dst}" --format jpeg --quality 82 resize 1080',
        shell=True, check=True, capture_output=True)


def process_before_after(bank) -> int:
    """Pareia inbox/antes/X.jpg com inbox/depois/X.jpg (mesmo nome de arquivo)."""
    a_dir, d_dir = INBOX / "antes", INBOX / "depois"
    if not a_dir.exists() or not d_dir.exists():
        return 0
    afters = {p.stem.lower().strip(): p for p in d_dir.iterdir() if p.suffix.lower() in EXTS}
    count = 0
    for before in [p for p in a_dir.iterdir() if p.suffix.lower() in EXTS]:
        after = afters.get(before.stem.lower().strip())
        if not after:
            print(f"AVISO: '{before.name}' em antes/ sem par em depois/ (mesmo nome) — pulado")
            continue
        try:
            tag = classify(after)
        except Exception as e:
            print(f"ERRO {after.name}: {e}")
            continue
        city = detect_city(after.name) or detect_city(before.name)
        base = unique_name(tag["slug"], city)[:-4]  # remove .jpg
        name_after, name_before = f"{base}-after.jpg", f"{base}-before.jpg"
        convert(after, DEST / name_after)
        convert(before, DEST / name_before)
        bank.append({"file": name_after, "before": name_before, "service": tag["service"],
                     "city": city, "desc": tag["desc"]})
        after.rename(PROCESSED / f"depois-{after.name}")
        before.rename(PROCESSED / f"antes-{before.name}")
        print(f"PAR {before.name}+{after.name} -> {base} [{tag['service']} | {city or 'Florida'}]")
        count += 1
    return count


def pull_remote():
    """Baixa fotos do worker de upload (KV) pro inbox local e apaga do remoto."""
    from urllib.parse import quote
    env = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l)
    base = env.get("WORKER_URL", "https://triangle-photo-upload.lucianodornfeld18.workers.dev").strip()
    tok = env["UPLOAD_TOKEN"].strip()

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) triangle-ingest/1.0"

    def get(path):
        sep = "&" if "?" in path else "?"
        req = urllib.request.Request(f"{base}{path}{sep}t={tok}", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()

    data = json.loads(get("/list"))
    done = []
    for k in data["singles"]:
        (INBOX / k.split("/", 1)[1]).write_bytes(get(f"/file?key={quote(k, safe='')}"))
        done.append(k)
    for p in data["pairs"]:
        (INBOX / "antes").mkdir(parents=True, exist_ok=True)
        (INBOX / "depois").mkdir(parents=True, exist_ok=True)
        (INBOX / "antes" / f"{p['id']}.jpg").write_bytes(get(f"/file?key={quote(p['before'], safe='')}"))
        (INBOX / "depois" / f"{p['id']}.jpg").write_bytes(get(f"/file?key={quote(p['after'], safe='')}"))
        done += [p["before"], p["after"]]
    if done:
        req = urllib.request.Request(f"{base}/delete?t={tok}",
                                     data=json.dumps({"keys": done}).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": UA},
                                     method="POST")
        urllib.request.urlopen(req, timeout=60)
    print(f"Remoto: {len(data['singles'])} fotos + {len(data['pairs'])} pares baixados")


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    (INBOX / "antes").mkdir(exist_ok=True)
    (INBOX / "depois").mkdir(exist_ok=True)
    if "--remote" in sys.argv:
        pull_remote()
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    ba = process_before_after(bank)
    photos = [p for p in INBOX.iterdir() if p.suffix.lower() in EXTS]
    if not photos and not ba:
        print(f"Inbox vazio: {INBOX}")
        return
    for img in photos:
        try:
            tag = classify(img)
        except Exception as e:
            print(f"ERRO {img.name}: {e}")
            continue
        city = detect_city(img.name)
        name = unique_name(tag["slug"], city)
        convert(img, DEST / name)
        bank.append({"file": name, "service": tag["service"], "city": city, "desc": tag["desc"]})
        img.rename(PROCESSED / img.name)
        print(f"{img.name} -> {name} [{tag['service']} | {city or 'Florida'}]")
    BANK.write_text(json.dumps(bank, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nBanco: {len(bank)} fotos. Proximo calendario ja usa as novas "
          f"(py automation/social/build_social_calendar.py + gen_creatives.py).")


if __name__ == "__main__":
    main()
