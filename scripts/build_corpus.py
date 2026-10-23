"""Reúne las tres fuentes locales del MVP; no llama a Gemini."""

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def markdown_cards(text):
    cards = []
    for section in text.split("\n## ")[1:]:
        title, _, body = section.partition("\n")
        if not title.strip() or not body.strip():
            raise ValueError("Ficha sin título o contenido")
        if title.strip() in {title for title, _ in cards}:
            raise ValueError("Título de ficha duplicado")
        cards.append((title.strip(), body.strip()))
    if not cards:
        raise ValueError("No hay fichas con encabezados ##")
    return cards


def build(root=ROOT):
    manifest = json.loads((root / "docs/corpus_mvp.json").read_text(encoding="utf-8"))
    records = []
    for source in manifest["sources"]:
        for asset in source["files"]:
            path = root / asset["path"]
            if hashlib.sha256(path.read_bytes()).hexdigest() != asset["sha256"]:
                raise ValueError(f"Archivo cambiado: {asset['path']}. Revisar y actualizar inventario.")
        path = root / source["input"]
        if source["simulator"] == "lmu":
            capture = json.loads(path.read_text(encoding="utf-8"))
            if capture["pending"] or capture["errors"]:
                raise ValueError("La captura de LMU está incompleta")
            cards = [(" / ".join(p["path"]), p["text"].strip(), p["url"])
                     for p in capture["pages"]]
            if len({url for _, _, url in cards}) != len(cards):
                raise ValueError("Hojas de LMU duplicadas")
        else:
            cards = [(title, body, source["url"]) for title, body in
                     markdown_cards(path.read_text(encoding="utf-8"))]
        if len(cards) != source["cards"]:
            raise ValueError(f"Número de fichas inesperado en {source['id']}")
        for index, (title, body, url) in enumerate(cards, 1):
            if not title or not body:
                raise ValueError("Ficha vacía")
            records.append({
                "id": f"{source['id']}_{index:02d}",
                "source_id": source["id"],
                "simulator": source["simulator"],
                "title": title,
                "locator": f"{source['locator']} / {title}",
                "url": url,
                "game_version": "unknown",
                "limitation": source["limitation"],
                "text": f"Simulador: {source['simulator']}\nCaso: {title}\n\n{body}",
            })
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("Identificadores duplicados")
    output = root / "data/corpus/mvp/preparado/corpus.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    temporary.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    temporary.replace(output)
    return records


if __name__ == "__main__":
    records = build()
    print(f"Corpus preparado: {len(records)} fichas; {dict(Counter(r['simulator'] for r in records))}")
