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


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    photos = [p for p in INBOX.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if not photos:
        print(f"Inbox vazio: {INBOX}")
        return
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    for img in photos:
        try:
            tag = classify(img)
        except Exception as e:
            print(f"ERRO {img.name}: {e}")
            continue
        city = detect_city(img.name)
        name = unique_name(tag["slug"], city)
        subprocess.run(
            f'npx -y sharp-cli --input "{img}" --output "{DEST / name}" --format jpeg --quality 82 resize 1080',
            shell=True, check=True, capture_output=True)
        bank.append({"file": name, "service": tag["service"], "city": city, "desc": tag["desc"]})
        img.rename(PROCESSED / img.name)
        print(f"{img.name} -> {name} [{tag['service']} | {city or 'Florida'}]")
    BANK.write_text(json.dumps(bank, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nBanco: {len(bank)} fotos. Proximo calendario ja usa as novas "
          f"(py automation/social/build_social_calendar.py + gen_creatives.py).")


if __name__ == "__main__":
    main()
