"""Respuestas controladas para comprobar el grafo, no la precisión de Gemini."""

from unittest.mock import Mock

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from agent import Clasificacion, crear_grafo

IDS = {"lmu": "LMU_USH_24", "iracing": "IR_CHRIS_HAYE_02", "acc": "ACC_DRIVER61_18"}


def decision(tipo="lmu", motivo="consulta", coche=None, otro=None, accion="continuar"):
    return {"parsed": Clasificacion(tipo=tipo, motivo=motivo, coche=coche,
                                   otro_simulador=otro, accion=accion),
            "raw": AIMessage(content="Clasificación local", usage_metadata={
                "input_tokens": 4, "output_tokens": 2, "total_tokens": 6}),
            "parsing_error": None}


def ficha(sim="lmu", identifier=None):
    return Document(page_content="Cambiar solo un ajuste por prueba.", metadata={
        "id": identifier or IDS[sim], "simulator": sim,
        "title": "Ficha local", "locator": "Celda local", "url": "https://example.com/guia",
        "game_version": "unknown", "limitation": "Coche y versión no especificados."})


def graph(decisiones=None):
    store, llm, classifier = Mock(), Mock(), Mock()
    store.similarity_search.side_effect = lambda query, k, filter: [ficha(filter["simulator"])]
    llm.invoke.side_effect = lambda messages: AIMessage(content=(
        f"Prueba un cambio [{IDS[store.similarity_search.call_args.kwargs['filter']['simulator']]}]."),
        usage_metadata={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15})
    if decisiones is None:
        classifier.invoke.return_value = decision()
    else:
        classifier.invoke.side_effect = decisiones
    app = crear_grafo(store, llm, "Reglas de sistema", clasificador=classifier, checkpointer=InMemorySaver())
    return app, store, llm, classifier


def config(name="a"):
    return {"configurable": {"thread_id": name}}
