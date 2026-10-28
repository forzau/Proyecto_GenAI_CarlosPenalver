"""Recursos de Streamlit por sesión, sin llamadas API durante el arranque."""

import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from agent import crear_grafo
from deployment import CORPUS, restaurar_paquete
from retrieval import GeminiRetrievalEmbeddings, open_existing_index

ROOT = Path(__file__).resolve().parent
MODELOS = {
    "gemini-3.5-flash-lite": "3.5 Flash-Lite · Más cuota",
    "gemini-3.1-flash-lite": "3.1 Flash-Lite",
    "gemini-3-flash-preview": "3 Flash · Preview",
    "gemini-3.6-flash": "3.6 Flash",
    "gemini-3.8-flash": "3.8 Flash",
}


def preparar_datos():
    if (ROOT / CORPUS).is_file() and (ROOT / "data/chroma/chroma.sqlite3").is_file():
        return
    st.title("Preparar BOX")
    st.info("Carga el paquete privado de datos de esta versión. Comprueba antes que la aplicación es privada en Streamlit.")
    paquete = st.file_uploader("Paquete privado de BOX", type=["gz"], max_upload_size=10)
    if paquete is not None:
        try:
            restaurar_paquete(paquete.getvalue(), ROOT)
        except Exception:
            st.error("No se ha podido cargar el paquete. Usa el archivo privado correspondiente a esta versión.")
        else:
            st.rerun()
    st.stop()


def modelo_inicial():
    load_dotenv(ROOT / ".env", override=True)
    modelo = os.environ.get("GEMINI_MODEL", "").strip()
    if modelo not in MODELOS:
        raise ValueError("Modelo no incluido en el selector.")
    return modelo


def cargar_agente(modelo=None):
    """Conserva el agente en session_state, sin compartir memoria con otra sesión."""
    modelo = modelo or modelo_inicial()
    if "agente" not in st.session_state or st.session_state.get("agente_modelo") != modelo:
        anterior = st.session_state.get("agente")
        agente = construir_agente(modelo, checkpointer=anterior.checkpointer if anterior else None)
        st.session_state.agente = agente
        st.session_state.agente_modelo = modelo
    return st.session_state.agente


def construir_agente(modelo=None, checkpointer=None):
    """Carga local, sin API ni reconstrucción automática del índice."""
    load_dotenv(ROOT / ".env", override=True)
    clave = os.environ.get("GOOGLE_API_KEY", "").strip()
    modelo = modelo or modelo_inicial()
    if modelo not in MODELOS:
        raise ValueError("Modelo no incluido en el selector.")
    modelo_embedding = os.environ.get("GEMINI_EMBEDDING_MODEL", "").strip()
    if not clave or not modelo or not modelo_embedding:
        raise ValueError("Configuración local incompleta.")
    records = [json.loads(line) for line in
               (ROOT / "data/corpus/mvp/preparado/corpus.jsonl").read_text(encoding="utf-8").splitlines()]
    documents = [Document(page_content=r["text"], metadata={k: v for k, v in r.items() if k != "text"})
                 for r in records]
    embeddings = GeminiRetrievalEmbeddings(
        model=modelo_embedding, api_key=clave, vertexai=False,
        request_options={"timeout": 30000, "retry_options": {"attempts": 1}},
    )
    store = open_existing_index(documents, embeddings, ROOT / "data/chroma")
    llm = ChatGoogleGenerativeAI(model=modelo, api_key=clave, vertexai=False, temperature=1.0,
                               max_output_tokens=1800, max_retries=3, timeout=45)
    return crear_grafo(store, llm, (ROOT / "prompts/system.md").read_text(encoding="utf-8"),
                       checkpointer=checkpointer if checkpointer is not None else InMemorySaver())
