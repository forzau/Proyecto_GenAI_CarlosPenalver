"""Tres consultas reales de recuperación. Ejecutar explícitamente: consume API."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from retrieval import GeminiRetrievalEmbeddings, index_documents, search

load_dotenv(ROOT / ".env", override=True)
import json
records = [json.loads(line) for line in
           (ROOT / "data/corpus/mvp/preparado/corpus.jsonl").read_text(encoding="utf-8").splitlines()]
documents = [Document(page_content=r["text"], metadata={k: v for k, v in r.items() if k != "text"})
             for r in records]
MODEL_EMBEDDING = os.environ["GEMINI_EMBEDDING_MODEL"]
llm_embedding = GeminiRetrievalEmbeddings(model=MODEL_EMBEDDING,
                                        api_key=os.environ["GOOGLE_API_KEY"], vertexai=False)
vectorstore = index_documents(documents, llm_embedding, ROOT / "data/chroma")

from datetime import datetime, timezone
import hashlib
import json

queries = [
    ("lmu", "En LMU, tengo sobreviraje al acelerar a la salida de una curva lenta. ¿Qué propone la guía?", "LMU_USH_24"),
    ("iracing", "En iRacing bloqueo a menudo los neumáticos delanteros al frenar. ¿Qué reparto de frenada sugiere la chuleta?", "IR_CHRIS_HAYE_02"),
    ("acc", "En ACC el coche resulta incómodo e inestable al pasar por los pianos. ¿Qué ajustes indica la guía?", "ACC_DRIVER61_18"),
]
retrieval_results = []
for simulator, query, expected_id in queries:
    results = search(vectorstore, query, simulator, k=3)
    isolated = bool(results) and all(doc.metadata["simulator"] == simulator for doc in results)
    found = expected_id in {doc.metadata["id"] for doc in results}
    retrieval_results.append({
        "simulator": simulator, "query": query, "expected_id": expected_id,
        "expected_in_top3": found, "correct_simulator": isolated,
        "hits": [{key: doc.metadata[key] for key in ("id", "source_id", "title", "locator", "url")}
                 for doc in results],
    })
    print(f"{simulator}: ficha esperada en top 3 = {found}; filtro correcto = {isolated}")
    for doc in results:
        print(" ", doc.metadata["id"], "—", doc.metadata["title"])

report = {
    "executed_at": datetime.now(timezone.utc).isoformat(),
    "embedding_model": MODEL_EMBEDDING, "dimensions": 3072, "k": 3,
    "corpus_sha256": hashlib.sha256((ROOT / "data/corpus/mvp/preparado/corpus.jsonl").read_bytes()).hexdigest(),
    "collection": vectorstore._collection.name,
    "results": retrieval_results,
}
report_path = ROOT / "outputs/retrieval_evaluation.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert all(result["correct_simulator"] for result in retrieval_results), "Se mezclaron simuladores."
assert all(result["expected_in_top3"] for result in retrieval_results), "Revisar la recuperación antes del agente."
print("Resultado local guardado en outputs/retrieval_evaluation.json")
