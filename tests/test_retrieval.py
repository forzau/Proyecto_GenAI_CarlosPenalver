import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from retrieval import GeminiRetrievalEmbeddings, index_documents, open_existing_index, search


class LocalEmbeddings(Embeddings):
    """Vectores de prueba; no miden calidad semántica ni llaman a Gemini."""

    model = "local-test"
    output_dimensionality = 3

    def __init__(self):
        self.calls = 0

    def embed_documents(self, texts):
        self.calls += 1
        return [[1.0, 0.0, 0.0] for _ in texts]

    def embed_query(self, text):
        return [1.0, 0.0, 0.0]


class RetrievalTest(unittest.TestCase):
    def test_web_opens_existing_index_without_repairing_or_reembedding(self):
        documents = [Document(page_content="ficha", metadata={"id": sim, "simulator": sim})
                     for sim in ("lmu", "iracing", "acc")]
        embeddings = LocalEmbeddings()
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            with self.assertRaisesRegex(ValueError, "Falta el índice"):
                open_existing_index(documents, embeddings, directory)
            self.assertEqual(embeddings.calls, 0)
            store = index_documents(documents, embeddings, directory)
            reopened = open_existing_index(documents, embeddings, directory)
            self.assertEqual(set(reopened.get(include=[])["ids"]), {"lmu", "iracing", "acc"})
            self.assertEqual(embeddings.calls, 1)
            store.delete(ids=["lmu"])
            with self.assertRaisesRegex(ValueError, "exactamente el corpus"):
                open_existing_index(documents, embeddings, directory)
            self.assertEqual(embeddings.calls, 1)

    def test_embedding2_request_format_without_api(self):
        embeddings = GeminiRetrievalEmbeddings(
            api_key="test-only-not-a-key", vertexai=False,
            request_options={"timeout": 30000, "retry_options": {"attempts": 1}},
        )
        response = SimpleNamespace(embeddings=[SimpleNamespace(values=[0.1, 0.2])])
        with patch.object(embeddings.client.models, "embed_content", return_value=response) as call:
            self.assertEqual(embeddings.embed_documents(["diagnóstico"]), [[0.1, 0.2]])
            self.assertEqual(call.call_args.kwargs["contents"], [
                {"parts": [{"text": "title: none | text: diagnóstico"}]}
            ])
            self.assertIsNone(call.call_args.kwargs["config"].task_type)
            self.assertEqual(call.call_args.kwargs["config"].http_options.timeout, 30000)
            self.assertEqual(call.call_args.kwargs["config"].http_options.retry_options.attempts, 1)
            embeddings.embed_query("sobreviraje")
            self.assertEqual(call.call_args.kwargs["contents"],
                             "task: search result | query: sobreviraje")
            self.assertIsNone(call.call_args.kwargs["config"].task_type)

    def test_persistence_no_reembedding_and_simulator_filter(self):
        documents = [Document(page_content="mismo síntoma", metadata={"id": sim, "simulator": sim})
                     for sim in ("lmu", "iracing", "acc")]
        embeddings = LocalEmbeddings()
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            store = index_documents(documents, embeddings, directory)
            self.assertEqual(embeddings.calls, 1)
            reopened = index_documents(documents, embeddings, directory)
            self.assertEqual(embeddings.calls, 1)
            self.assertEqual(len(reopened.get(include=[])["ids"]), 3)
            for sim in ("lmu", "iracing", "acc"):
                hits = search(reopened, "mismo síntoma", sim)
                self.assertEqual([hit.metadata["simulator"] for hit in hits], [sim])
            changed = [Document(page_content="síntoma cambiado", metadata=doc.metadata)
                       for doc in documents]
            separate = index_documents(changed, embeddings, directory)
            self.assertNotEqual(store._collection.name, separate._collection.name)
            self.assertEqual(embeddings.calls, 2)

    def test_invalid_inputs_do_not_query_or_embed(self):
        store = Mock()
        for query, simulator in [("síntoma", "general"), ("", "acc")]:
            with self.assertRaises(ValueError):
                search(store, query, simulator)
        store.similarity_search.assert_not_called()
        with self.assertRaises(ValueError):
            index_documents([], LocalEmbeddings(), ".")


if __name__ == "__main__":
    unittest.main()
