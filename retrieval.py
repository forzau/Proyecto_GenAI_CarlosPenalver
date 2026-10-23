"""Embeddings y Chroma compartidos por el notebook y el futuro chat."""

import hashlib
import json
from pathlib import Path

from google.genai.types import EmbedContentConfig
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class GeminiRetrievalEmbeddings(GoogleGenerativeAIEmbeddings):
    """Mismo cliente de clase, adaptado a la búsqueda con Gemini Embedding 2."""

    model: str = "gemini-embedding-2"

    def _build_config(self, **kwargs):
        if self.model != "gemini-embedding-2":
            raise ValueError("Esta adaptación utiliza gemini-embedding-2.")
        # shortcut: 4.4.2 envía task_type, no admitido por Embedding 2; retirar al actualizar la integración.
        return EmbedContentConfig(
            output_dimensionality=kwargs.get("output_dimensionality") or self.output_dimensionality,
        )

    # shortcut: el MVP usa llamadas síncronas; adaptar aembed_* si el chat pasa a async.
    def embed_documents(self, texts, **kwargs):
        return super().embed_documents(
            [f"title: none | text: {text}" for text in texts], **kwargs
        )

    def embed_query(self, text, **kwargs):
        return super().embed_query(f"task: search result | query: {text}", **kwargs)


def index_documents(documents, embeddings, persist_directory):
    """Reutiliza la colección del mismo corpus, modelo y formato de embeddings."""
    if not documents:
        raise ValueError("El corpus está vacío.")
    ids = [doc.metadata["id"] for doc in documents]
    if len(set(ids)) != len(ids):
        raise ValueError("El corpus contiene identificadores duplicados.")
    if any(doc.metadata.get("simulator") not in {"lmu", "iracing", "acc"}
           or not doc.page_content.strip() for doc in documents):
        raise ValueError("Cada ficha necesita texto y un simulador válido.")
    configuration = {
        "model": embeddings.model,
        "dimensions": embeddings.output_dimensionality or 3072,
        "format": "embedding2-search-v1",
        "distance": "cosine",
        "documents": [(doc.metadata, doc.page_content) for doc in documents],
    }
    signature = hashlib.sha256(json.dumps(
        configuration, ensure_ascii=False, sort_keys=True
    ).encode("utf-8")).hexdigest()[:20]
    collection_name = f"simracing_{signature}"
    directory = str(Path(persist_directory).resolve())
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=directory,
        collection_metadata={"hnsw:space": "cosine"},
    )
    stored = set(vectorstore.get(include=[])["ids"])
    if stored - set(ids):
        raise ValueError("La colección contiene fichas ajenas al corpus.")
    missing = [doc for doc in documents if doc.metadata["id"] not in stored]
    if missing:
        vectorstore = Chroma.from_documents(
            missing,
            embedding=embeddings,
            ids=[doc.metadata["id"] for doc in missing],
            collection_name=collection_name,
            persist_directory=directory,
            collection_metadata={"hnsw:space": "cosine"},
        )
    if set(vectorstore.get(include=[])["ids"]) != set(ids):
        raise RuntimeError("El índice no contiene todas las fichas esperadas.")
    return vectorstore


def search(vectorstore, query, simulator, k=3):
    if simulator not in {"lmu", "iracing", "acc"}:
        raise ValueError("Selecciona lmu, iracing o acc antes de buscar.")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Escribe una consulta no vacía.")
    if not isinstance(k, int) or k < 1:
        raise ValueError("k debe ser un entero positivo.")
    return vectorstore.similarity_search(query, k=k, filter={"simulator": simulator})
