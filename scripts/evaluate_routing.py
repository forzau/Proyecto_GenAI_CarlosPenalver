"""Evaluación explícita del enrutamiento conversacional. Sin --run no usa API.

Un informe existente no se sobrescribe ni se repite. Para otra pasada deliberada,
indicar un --output nuevo. Todos los escenarios son ficticios, sin pruebas en pista.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Continuar solo los casos pendientes, conservando los intentos anteriores.")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/routing_evaluation_2026-10-26.json")
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    output = args.output.resolve()
    output.relative_to((ROOT / "outputs").resolve())
    if output.exists() and not args.resume:
        print("El informe ya existe; no se repiten llamadas. Usa otro --output para una pasada nueva.")
        return

    from dotenv import load_dotenv
    from langchain_chroma import Chroma
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.checkpoint.memory import InMemorySaver
    from agent import crear_grafo, sumar_uso
    from retrieval import GeminiRetrievalEmbeddings

    load_dotenv(ROOT / ".env", override=True)
    snapshots = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in
                 ("agent.py", "prompts/classify.md", "prompts/system.md", "prompts/other_simulator.md",
                  "prompts/source_quality.json", "data/corpus/mvp/preparado/corpus.jsonl")}
    report = {"executed_at": datetime.now(timezone.utc).isoformat(),
              "model": os.environ["GEMINI_MODEL"], "temperature": 1.0,
              "scenario_type": "synthetic_pilot_conversations", "turns": [],
              "snapshots": snapshots}
    if output.exists():
        report = json.loads(output.read_text(encoding="utf-8"))
        if report["model"] != os.environ["GEMINI_MODEL"]:
            raise ValueError("No se cambia automáticamente de modelo al continuar.")
        if report["snapshots"]["data/corpus/mvp/preparado/corpus.jsonl"] != snapshots["data/corpus/mvp/preparado/corpus.jsonl"]:
            raise ValueError("No se puede continuar con otro corpus.")

    class Accounting(BaseCallbackHandler):
        def __init__(self):
            self.calls, self.usages, self.errors = 0, [], []

        def on_llm_start(self, serialized, prompts, **kwargs):
            self.calls += 1

        def on_llm_end(self, response, **kwargs):
            self.usages.append(response.generations[0][0].message.usage_metadata or {})

        def on_llm_error(self, error, **kwargs):
            message = str(error).replace(os.environ["GOOGLE_API_KEY"], "[REDACTED]")
            self.errors.append({"type": type(error).__name__, "message": message[:1200]})

    class EvaluationEmbeddings(GeminiRetrievalEmbeddings):
        query_calls: int = 0

        def embed_query(self, text, **kwargs):
            self.query_calls += 1
            return super().embed_query(text, **kwargs)

        def embed_documents(self, texts, **kwargs):
            raise RuntimeError("Esta evaluación no puede reindexar el corpus.")

    accounting = Accounting()
    accounting.calls = report.get("model_calls", 0)
    accounting.usages = [report.get("usage", {})]
    accounting.errors = report.get("provider_errors", [])
    llm = ChatGoogleGenerativeAI(model=report["model"], api_key=os.environ["GOOGLE_API_KEY"], vertexai=False,
                               temperature=1.0, max_output_tokens=1800, max_retries=3, timeout=45,
                               callbacks=[accounting])
    embeddings = EvaluationEmbeddings(api_key=os.environ["GOOGLE_API_KEY"], vertexai=False,
        request_options={"timeout": 30000, "retry_options": {"attempts": 1}})
    embeddings.query_calls = report.get("embedding_query_calls", 0)
    retrieval_report = json.loads((ROOT / "outputs/retrieval_evaluation.json").read_text(encoding="utf-8"))
    store = Chroma(collection_name=retrieval_report["collection"], persist_directory=str(ROOT / "data/chroma"),
                   embedding_function=embeddings, create_collection_if_not_exists=False)
    corpus = [json.loads(s) for s in (ROOT / "data/corpus/mvp/preparado/corpus.jsonl").read_text(encoding="utf-8").splitlines()]
    if set(store.get(include=[])["ids"]) != {r["id"] for r in corpus}:
        raise ValueError("Índice diferente del corpus esperado")
    app = crear_grafo(store, llm, (ROOT / "prompts/system.md").read_text(encoding="utf-8"), checkpointer=InMemorySaver())
    configs = {name: {"configurable": {"thread_id": uuid4().hex}} for name in "abcdef"}
    completed = set()
    for turn in report["turns"]:
        if turn["status"] != "ok":
            continue
        completed.add(turn["id"])
        state = {"contexto": turn["context"], "contexto_pendiente": turn["pending_context"],
                 "requiere_confirmacion": turn["pending"],
                 "pregunta_pendiente": turn["question"] if turn["pending"] else None,
                 "historial": [(HumanMessage if m["role"] == "human" else AIMessage)(content=m["text"])
                               for m in turn["history"]],
                 "ultimo_intercambio": [{"rol": "human", "texto": turn["question"]},
                                         {"rol": "ai", "texto": turn["pilot_answer"]}],
                 "coche_sin_simulador": turn["classification"].get("coche") if not turn["context"] else None}
        app.update_state(configs[turn["conversation"]], state, as_node=turn["route"])
    # id, conversación, mensaje, ruta esperada, contexto vigente esperado, confirmación
    cases = [
        ("R01", "a", "Con mi Ferrari GT3 tengo sobreviraje al acelerar a la salida de curvas lentas.", "distinto", None, False),
        ("R02", "a", "Estoy conduciendo en Le Mans Ultimate.", "lmu", "lmu", False),
        ("R03", "a", "Todavía no he cambiado nada. ¿Qué debería observar si pruebo tu primera propuesta?", "lmu", "lmu", False),
        ("R04", "a", "Ahora estoy en Assetto Corsa Competizione, sin coche confirmado, y noto el coche incómodo al pasar por los pianos.", "acc", "lmu", True),
        ("R05", "a", "Sí, cambia al nuevo contexto.", "acc", "acc", False),
        ("R06", "a", "Quiero cambiar a iRacing porque bloqueo las ruedas delanteras al frenar.", "iracing", "acc", True),
        ("R07", "a", "No, cancela ese cambio; seguimos como antes.", "acc", "acc", False),
        ("R08", "a", "Escríbeme un poema sobre la luna.", "distinto", "acc", False),
        ("R09", "b", "En iRacing bloqueo a menudo los neumáticos delanteros al frenar. ¿Qué reparto de frenada probarías?", "iracing", "iracing", False),
        ("R10", "c", "En Automobilista 2 mi coche sobrevira al acelerar al salir de curvas lentas. ¿Cómo lo investigarías?", "distinto", "Automobilista 2", False),
        ("R11", "c", "Todavía no he tocado nada. ¿Qué debería observar primero?", "distinto", "Automobilista 2", False),
        ("R12", "d", "Estoy en Assetto Corsa original, no Competizione. Noto subviraje a mitad de curva. ¿Qué puedo comprobar?", "distinto", "Assetto Corsa", False),
        ("R13", "e", "Compara qué presión exacta debería usar en LMU y en ACC.", "distinto", None, False),
        ("R14", "f", "Conduzco un Ferrari 296 GT3 en Spa y se me va de atrás. ¿Qué ajusto?", "distinto", None, False),
        ("R15", "a", "No quiero cambiar a LMU, seguimos en ACC. ¿Qué ajustes de la guía podrían ayudar con los pianos?", "acc", "acc", False),
    ]

    def save():
        report.update(model_calls=accounting.calls, embedding_query_calls=embeddings.query_calls,
                      corpus_embedding_calls=0, usage=sumar_uso(*accounting.usages), provider_errors=accounting.errors,
                      model_call_unit="LangChain invocations; SDK may use up to three HTTP attempts each")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for identifier, conversation, question, expected_route, expected_context, expected_pending in cases:
        if identifier in completed:
            continue
        start = perf_counter()
        call_before, query_before = accounting.calls, embeddings.query_calls
        record = {"id": identifier, "conversation": conversation, "question": question,
                  "max_model_attempts": llm.max_retries,
                  "expected_route": expected_route, "expected_context": expected_context,
                  "expected_pending": expected_pending, "snapshots": snapshots,
                  "executed_at": datetime.now(timezone.utc).isoformat()}
        try:
            result = app.invoke({"pregunta": question}, config=configs[conversation])
            record.update(route=result["nodo_usado"], classification=result["clasificacion"],
                          context=result.get("contexto"), pending=result.get("requiere_confirmacion", False),
                          pending_context=result.get("contexto_pendiente"), answer=result["respuesta"],
                          pilot_answer=result["respuesta_piloto"], sources=result["fuentes"], usage=result["uso"],
                          history=[{"role": m.type, "text": m.content} for m in result.get("historial", [])],
                          retrieved_documents=[dict(d.metadata, text=d.page_content) for d in result["documentos_recuperados"]],
                          documents=[dict(d.metadata, text=d.page_content) for d in result["documentos"]],
                          excluded_sources=result["fuentes_excluidas"], error=result.get("error"))
            actual_context = (result.get("contexto") or {}).get("simulador")
            checks = {"route": record["route"] == expected_route, "context": actual_context == expected_context,
                      "pending": record["pending"] == expected_pending, "provider": not result.get("error")}
            if expected_route == "distinto" or expected_pending or identifier == "R07":
                checks["no_retrieval"] = embeddings.query_calls == query_before
            if identifier == "R05":
                checks["old_context_discarded"] = "Ferrari" not in str(record["history"]) and len(record["history"]) == 2
            if identifier in {"R10", "R11", "R12"}:
                checks["general_caveat"] = "podría no ajustarse" in record["answer"] and not record["sources"]
            record.update(checks=checks, status="ok" if all(checks.values()) else "failed",
                          technical_review="pending")
        except Exception as error:
            record.update(status="error", error_type=type(error).__name__,
                          error_message=str(error).replace(os.environ["GOOGLE_API_KEY"], "[REDACTED]")[:1200])
        record.update(elapsed_seconds=round(perf_counter() - start, 2),
                      model_calls=accounting.calls - call_before, embedding_query_calls=embeddings.query_calls - query_before)
        report["turns"].append(record)
        save()
        print(f"{identifier}: {record['status']}; ruta={record.get('route')}; llamadas={record['model_calls']}", flush=True)
        if record["status"] != "ok":
            raise SystemExit("Se conserva el informe parcial. Revisar antes de consumir más API.")
    report["completed"] = True
    save()
    print(f"Informe guardado: {output.name}. El enrutamiento no demuestra fidelidad técnica general.")


if __name__ == "__main__":
    main()
