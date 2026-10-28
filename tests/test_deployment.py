"""Exportación y carga privada en un directorio vacío, sin Gemini."""

import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from shutil import copyfile
from unittest.mock import patch

import chromadb
from streamlit.testing.v1 import AppTest

from deployment import CONFIG_EMBEDDINGS, CORPUS, crear_paquete, restaurar_paquete
from retrieval import collection_name_for_documents
from tests.fakes import ficha

APP = Path(__file__).resolve().parents[1] / "app.py"


class DeploymentTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source, self.target = self.root / "source", self.root / "target"
        self.target.mkdir()
        corpus = self.source / CORPUS
        corpus.parent.mkdir(parents=True)
        self.docs = [ficha(sim) for sim in ("lmu", "iracing", "acc")]
        corpus.write_text("\n".join(json.dumps({**d.metadata, "text": d.page_content}) for d in self.docs), encoding="utf-8")
        self.collection_name = collection_name_for_documents(self.docs, CONFIG_EMBEDDINGS)
        client = chromadb.PersistentClient(path=str(self.source / "data/chroma"))
        collection = client.create_collection(self.collection_name, metadata={"hnsw:space": "cosine"})
        self.vectors = [[float(i == j) for i in range(3072)] for j in range(3)]
        collection.add(ids=[d.metadata["id"] for d in self.docs], embeddings=self.vectors,
                       documents=[d.page_content for d in self.docs], metadatas=[d.metadata for d in self.docs])
        self.package = self.root / "private.json.gz"
        crear_paquete(self.package, self.source)
        copyfile(self.source / "deployment_manifest.json", self.target / "deployment_manifest.json")

    def test_round_trip_keeps_corpus_vectors_and_simulator_filter_without_api(self):
        restaurar_paquete(self.package.read_bytes(), self.target)
        self.assertEqual((self.target / CORPUS).read_bytes(), (self.source / CORPUS).read_bytes())
        collection = chromadb.PersistentClient(path=str(self.target / "data/chroma")).get_collection(self.collection_name)
        stored = collection.get(ids=[d.metadata["id"] for d in self.docs], include=["embeddings"])
        vectors = dict(zip(stored["ids"], stored["embeddings"].tolist()))
        self.assertEqual(vectors, {d.metadata["id"]: v for d, v in zip(self.docs, self.vectors)})
        hits = collection.query(query_embeddings=[self.vectors[0]], n_results=1, where={"simulator": "acc"})
        self.assertEqual(hits["ids"], [[self.docs[2].metadata["id"]]])
        restaurar_paquete(self.package.read_bytes(), self.target)
        self.assertEqual(collection.count(), 3)

    def test_unrecognized_package_is_rejected_before_writing_data(self):
        with self.assertRaisesRegex(ValueError, "versión"):
            restaurar_paquete(b"not-the-private-package", self.target)
        self.assertFalse((self.target / "data").exists())

    def test_existing_different_corpus_is_never_overwritten(self):
        corpus = self.target / CORPUS
        corpus.parent.mkdir(parents=True)
        corpus.write_bytes(b"keep this corpus")
        with self.assertRaisesRegex(ValueError, "sobrescribe"):
            restaurar_paquete(self.package.read_bytes(), self.target)
        self.assertEqual(corpus.read_bytes(), b"keep this corpus")
        self.assertFalse((self.target / "data/chroma").exists())

    def test_incompatible_vectors_are_rejected_even_with_matching_package_hash(self):
        payload = json.loads(gzip.decompress(self.package.read_bytes()))
        payload["embeddings"][0] = [1.0]
        packed = gzip.compress(json.dumps(payload).encode())
        manifest_path = self.target / "deployment_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["sha256"] = hashlib.sha256(packed).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "incompatibles"):
            restaurar_paquete(packed, self.target)
        self.assertFalse((self.target / "data").exists())

    def test_empty_cloud_install_shows_private_upload_without_starting_agent(self):
        with patch("web_runtime.ROOT", self.target), patch("web_runtime.cargar_agente") as agent:
            page = AppTest.from_file(APP).run()
            self.assertFalse(page.exception)
            self.assertEqual(len(page.get("file_uploader")), 1)
            self.assertFalse(page.chat_input)
            agent.assert_not_called()


if __name__ == "__main__":
    unittest.main()
