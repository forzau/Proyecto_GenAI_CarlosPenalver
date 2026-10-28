"""Paquete privado portable: reutiliza los vectores existentes, sin API."""

import gzip
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace

import chromadb
from langchain_core.documents import Document

from retrieval import collection_name_for_documents

ROOT = Path(__file__).resolve().parent
CORPUS = Path("data/corpus/mvp/preparado/corpus.jsonl")
CONFIG_EMBEDDINGS = SimpleNamespace(model="gemini-embedding-2", output_dimensionality=3072)


def crear_paquete(destino, root=ROOT):
    corpus = (root / CORPUS).read_bytes().decode("utf-8")
    records = [json.loads(line) for line in corpus.splitlines()]
    documents = [Document(page_content=r["text"], metadata={k: v for k, v in r.items() if k != "text"})
                 for r in records]
    collection = collection_name_for_documents(documents, CONFIG_EMBEDDINGS)
    client = chromadb.PersistentClient(path=str(root / "data/chroma"))
    stored = client.get_collection(collection).get(include=["embeddings"])
    vectors = dict(zip(stored["ids"], stored["embeddings"].tolist()))
    if set(vectors) != {r["id"] for r in records}:
        raise ValueError("El índice no coincide con el corpus.")
    payload = {"corpus": corpus, "embeddings": [vectors[r["id"]] for r in records]}
    packed = gzip.compress(json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8"), mtime=0)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(packed)
    manifest = {"sha256": hashlib.sha256(packed).hexdigest(), "collection": collection,
                "cards": len(records), "dimensions": 3072}
    (root / "deployment_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def restaurar_paquete(packed, root=ROOT):
    """Solo acepta el paquete de esta versión; no extrae rutas ni ejecuta objetos."""
    manifest = json.loads((root / "deployment_manifest.json").read_text(encoding="utf-8"))
    if len(packed) > 10_000_000 or hashlib.sha256(packed).hexdigest() != manifest["sha256"]:
        raise ValueError("El paquete no corresponde a esta versión.")
    payload = json.loads(gzip.decompress(packed))
    corpus = payload["corpus"].encode("utf-8")
    records = [json.loads(line) for line in payload["corpus"].splitlines()]
    vectors = payload["embeddings"]
    documents = [Document(page_content=r["text"], metadata={k: v for k, v in r.items() if k != "text"})
                 for r in records]
    if (len(records) != manifest["cards"] or len(vectors) != len(records)
            or collection_name_for_documents(documents, CONFIG_EMBEDDINGS) != manifest["collection"]
            or any(len(v) != manifest["dimensions"] or any(not math.isfinite(n) for n in v) for v in vectors)):
        raise ValueError("Corpus o vectores incompatibles.")
    target = root / CORPUS
    if target.exists() and target.read_bytes() != corpus:
        raise ValueError("No se sobrescribe un corpus diferente.")
    client = chromadb.PersistentClient(path=str(root / "data/chroma"))
    collection = client.get_or_create_collection(manifest["collection"], metadata={"hnsw:space": "cosine"})
    ids = [r["id"] for r in records]
    if set(collection.get(include=[])["ids"]) - set(ids):
        raise ValueError("El índice contiene fichas ajenas al paquete.")
    collection.upsert(ids=ids, embeddings=vectors, documents=[d.page_content for d in documents],
                      metadatas=[d.metadata for d in documents])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(corpus)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", required=True, type=Path, help="Destino privado .json.gz (fuera de Git).")
    args = parser.parse_args()
    manifest = crear_paquete(args.export)
    print(f"Paquete creado: {manifest['cards']} fichas, cero llamadas API.")
