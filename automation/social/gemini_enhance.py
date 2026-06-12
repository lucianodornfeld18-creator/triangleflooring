#!/usr/bin/env python3
"""Edita/melhora fotos do banco social com o Gemini (nano banana).

Uso:
    py automation/social/gemini_enhance.py images/social/foto.jpg "instrucao de edicao"

Le GEMINI_API_KEY do .env na raiz do projeto. Salva <nome>-enh.jpg ao lado.
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = "gemini-2.5-flash-image"


def api_key() -> str:
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("GEMINI_API_KEY nao encontrada no .env")


def enhance(img_path: Path, instruction: str) -> Path:
    payload = {
        "contents": [{
            "parts": [
                {"text": instruction},
                {"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_path.read_bytes()).decode(),
                }},
            ],
        }],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.load(r)
    for part in resp["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            out = img_path.with_name(img_path.stem + "-enh.jpg")
            out.write_bytes(base64.b64decode(part["inlineData"]["data"]))
            return out
    raise SystemExit(f"Sem imagem na resposta: {json.dumps(resp)[:400]}")


if __name__ == "__main__":
    img = ROOT / sys.argv[1] if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    instruction = sys.argv[2] if len(sys.argv) > 2 else (
        "Enhance this real estate photo: brighten and balance the lighting, fix white balance, "
        "remove wall clutter like posters and papers, keep the floor 100% identical and realistic. "
        "Professional interior photography look. Do not add furniture or change the room layout."
    )
    out = enhance(img, instruction)
    print(f"ok -> {out}")
