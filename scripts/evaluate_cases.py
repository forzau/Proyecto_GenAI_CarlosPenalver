"""Completa D02, D03 y D05 explícitamente; conserva D01/D04 y resultados previos.

Sin --run no llama a ninguna API. --run reutiliza los casos ya completados.
Para repetir uno deliberadamente: --run --case D05 --repeat.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Autoriza las llamadas de evaluación pendientes.")
    parser.add_argument("--case", action="append", choices=["D02", "D03", "D05"])
    parser.add_argument("--repeat", action="store_true", help="Repetir solo los casos seleccionados.")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    if args.repeat and not args.case:
        parser.error("Para repetir, indica al menos un --case.")

    from dotenv import load_dotenv
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.checkpoint.memory import InMemorySaver
    from agent import crear_grafo
    from retrieval import GeminiRetrievalEmbeddings

    load_dotenv(ROOT / ".env", override=True)
    corpus_path = ROOT / "data/corpus/mvp/preparado/corpus.jsonl"
    corpus_hash = hashlib.sha256(corpus_path.read_bytes()).hexdigest()
    records = {r["id"]: r for r in (json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines())}
    retrieval = json.loads((ROOT / "outputs/retrieval_evaluation.json").read_text(encoding="utf-8"))
    if retrieval["corpus_sha256"] != corpus_hash:
        raise ValueError("El corpus no coincide con las búsquedas guardadas.")
    prompt = (ROOT / "prompts/system.md").read_text(encoding="utf-8")
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    output = ROOT / "outputs/evaluation_cases.json"
    archive = None
    if output.exists():
        report = json.loads(output.read_text(encoding="utf-8"))
        if report["corpus_sha256"] != corpus_hash:
            raise ValueError("El informe anterior corresponde a otro corpus; conservarlo antes de evaluar.")
        if args.repeat:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archive = output.with_name(f"evaluation_cases_before_{stamp}.json")
            shutil.copy2(output, archive)
    else:
        initial = json.loads((ROOT / "outputs/agent_style.json").read_text(encoding="utf-8"))
        memory = json.loads((ROOT / "outputs/memory_evaluation.json").read_text(encoding="utf-8"))
        followup = memory["turns"][0]
        report = {"corpus_sha256": corpus_hash, "cases": {
            "D01": {**initial, "question": initial["query"], "source_report": "outputs/agent_style.json",
                    "reused_generation": True},
            "D04": {**followup, "status": "ok", "model": memory["model"],
                    "simulator": followup["context"]["simulador"],
                    "executed_at": memory["executed_at"], "prompt_sha256": memory["prompt_sha256"],
                    "source_report": "outputs/memory_evaluation.json", "reused_generation": True,
                    "mode": "saved_initial_turn_and_live_followup"},
        }}

    def save():
        report["updated_at"] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    llm = ChatGoogleGenerativeAI(model=os.environ["GEMINI_MODEL"], api_key=os.environ["GOOGLE_API_KEY"],
                               vertexai=False, temperature=1.0, max_output_tokens=1800, max_retries=1, timeout=45)
    cached = {"D02": retrieval["results"][1], "D03": retrieval["results"][2]}
    cases = {
        "D02": {"simulator": "iracing", "question": cached["D02"]["query"]},
        "D03": {"simulator": "acc", "question": cached["D03"]["query"]},
        "D05": {"simulator": "lmu", "car": "Ferrari GT3",
                "question": "¿Qué presión exacta es óptima para mi Ferrari GT3 en la versión actual de LMU?"},
    }

    class SavedRetrieval:
        def __init__(self, entry):
            self.entry = entry

        def similarity_search(self, query, k, filter):
            if query != self.entry["query"] or filter != {"simulator": self.entry["simulator"]} or k != retrieval["k"]:
                raise ValueError("La consulta no coincide con la recuperación guardada.")
            selected = [records[hit["id"]] for hit in self.entry["hits"]]
            return [Document(page_content=r["text"], metadata={k: v for k, v in r.items() if k != "text"}) for r in selected]

    for identifier in args.case or list(cases):
        if report["cases"].get(identifier, {}).get("status") == "ok" and not args.repeat:
            print(identifier + ": resultado guardado reutilizado; sin API.", flush=True)
            continue
        case = cases[identifier]
        previous = report["cases"].get(identifier, {})
        result_record = {**case, "model": os.environ["GEMINI_MODEL"], "executed_at": datetime.now(timezone.utc).isoformat(),
                         "prompt_sha256": prompt_hash, "temperature": 1.0, "max_output_tokens": 1800, "k": 3,
                         "source_quality_sha256": hashlib.sha256((ROOT / "prompts/source_quality.json").read_bytes()).hexdigest(),
                         "reused_generation": False}
        start = perf_counter()
        try:
            if identifier in cached:
                store = SavedRetrieval(cached[identifier])
                result_record.update(mode="saved_retrieval_and_live_generation", embedding_calls=0,
                                     retrieved_at=retrieval["executed_at"])
            elif args.repeat and previous.get("documents") and previous.get("question") == case["question"]:
                entry = {"query": case["question"], "simulator": case["simulator"],
                         "hits": [{"id": d["id"]} for d in previous.get("retrieved_documents", previous["documents"])]}
                store = SavedRetrieval(entry)
                result_record.update(mode="saved_retrieval_and_live_generation", embedding_calls=0,
                                     retrieved_at=previous.get("retrieved_at", previous["executed_at"]),
                                     retrieval_source_report=str(archive.relative_to(ROOT)))
            else:
                embeddings = GeminiRetrievalEmbeddings(model=os.environ["GEMINI_EMBEDDING_MODEL"],
                    api_key=os.environ["GOOGLE_API_KEY"], vertexai=False,
                    request_options={"timeout": 30000, "retry_options": {"attempts": 1}})
                store = Chroma(collection_name=retrieval["collection"], persist_directory=str(ROOT / "data/chroma"),
                               embedding_function=embeddings, create_collection_if_not_exists=False)
                if set(store.get(include=[])["ids"]) != set(records):
                    raise ValueError("El índice existente no contiene exactamente el corpus esperado.")
                result_record.update(mode="live_retrieval_and_generation", embedding_calls=1)
            app = crear_grafo(store, llm, prompt, checkpointer=InMemorySaver())
            config = {"configurable": {"thread_id": uuid4().hex}}
            print(identifier + ": generando respuesta de evaluación.", flush=True)
            result = app.invoke({"pregunta": case["question"], "simulador": case["simulator"], "coche": case.get("car")}, config)
            result_record.update(status="ok", answer=result["respuesta"], pilot_answer=result["respuesta_piloto"],
                                 sources=result["fuentes"], usage=result["uso"], context=result["contexto"],
                                 documents=[dict(d.metadata, text=d.page_content) for d in result["documentos"]],
                                 retrieved_documents=[dict(d.metadata, text=d.page_content) for d in result["documentos_recuperados"]],
                                 excluded_sources=result["fuentes_excluidas"],
                                 manual_review={"status": "pending"})
            print(result["respuesta"], flush=True)
            print("Uso:", result["uso"], flush=True)
        except Exception as error:
            result_record.update(status="error", error=str(error).replace(os.environ["GOOGLE_API_KEY"], "[REDACTED]"))
            print(identifier + ": " + result_record["error"], flush=True)
        result_record["elapsed_seconds"] = round(perf_counter() - start, 2)
        report["cases"][identifier] = result_record
        save()
        if result_record["status"] == "error":
            raise SystemExit(1)
    save()
    print("Informe local guardado. Revisar fidelidad contra los fragmentos; status=ok solo indica ejecución.")


if __name__ == "__main__":
    main()
