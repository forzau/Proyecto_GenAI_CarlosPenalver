"""Pruebas de la web con el grafo real y respuestas locales controladas."""

import unittest
from itertools import product
from pathlib import Path
from unittest.mock import patch

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import GoogleAPIError
from langgraph.checkpoint.memory import InMemorySaver
from agent import crear_grafo
from retrieval import GeminiRetrievalEmbeddings
from streamlit.testing.v1 import AppTest

from tests.fakes import decision, graph

APP = Path(__file__).resolve().parents[1] / "app.py"


class WebTest(unittest.TestCase):
    def setUp(self):
        # Los casos controlados no necesitan las copias privadas del corpus.
        setup = patch("web_runtime.preparar_datos")
        setup.start()
        self.addCleanup(setup.stop)
        model = patch("web_runtime.modelo_inicial", return_value="gemini-3.5-flash-lite")
        model.start()
        self.addCleanup(model.stop)

    def test_model_switch_keeps_context_history_and_uses_new_model_for_next_turn(self):
        import web_runtime
        built = []

        def build(modelo, checkpointer=None):
            _, store, llm, classifier = graph([decision(coche="Ferrari")])
            app = crear_grafo(store, llm, "Reglas", clasificador=classifier,
                              checkpointer=checkpointer if checkpointer is not None else InMemorySaver())
            built.append((modelo, app, llm, classifier))
            return app

        with patch("web_runtime.construir_agente", side_effect=build):
            page = AppTest.from_file(APP).run()
            self.assertEqual(len(page.selectbox[0].options), 5)
            page.chat_input[0].set_value("En LMU mi Ferrari sobrevira").run()
            config = page.session_state["conversacion"]
            previous_model = page.selectbox[0].value
            target = next(model for model in web_runtime.MODELOS if model != previous_model)
            page.selectbox[0].select(target).run()
            self.assertEqual(len(page.exception), 0)
            self.assertEqual(len(page.chat_message), 2)
            self.assertEqual(page.session_state["contexto"], {"simulador": "lmu", "coche": "Ferrari"})
            self.assertEqual(page.session_state["conversacion"], config)
            self.assertIs(built[0][1].checkpointer, built[1][1].checkpointer)
            built[1][3].invoke.assert_not_called()
            page.chat_input[0].set_value("Sigue ocurriendo al acelerar").run()
            self.assertEqual(len(built[1][1].get_state(config).values["historial"]), 4)
            self.assertEqual(built[0][2].invoke.call_count, 1)
            self.assertEqual(built[1][2].invoke.call_count, 1)
            self.assertEqual(built[1][3].invoke.call_count, 1)
            self.assertEqual(page.session_state["trazas"][-1]["modelo"], target)
            page.button[0].click().run()
            self.assertEqual(page.selectbox[0].value, target)
            self.assertFalse(built[0][1].get_state(config).values)

    def test_unknown_model_is_rejected_before_loading_index_or_calling_api(self):
        import web_runtime
        with patch("web_runtime.open_existing_index") as store:
            with self.assertRaises(ValueError):
                web_runtime.construir_agente("modelo-ajeno")
            store.assert_not_called()

    def test_provider_limits_are_explained_and_manual_retry_does_not_duplicate_graph_invocations(self):
        for stage, code in product(("classification", "generation"), (503, 429)):
            with self.subTest(stage=stage, code=code):
                app, store, llm, classifier = graph()
                busy = GoogleAPIError(code, {"error": {"message": "private-provider-detail api-key-secret"}})
                if stage == "classification":
                    classifier.invoke.side_effect = [busy, decision()]
                else:
                    llm.invoke.side_effect = busy
                with patch("web_runtime.cargar_agente", return_value=app):
                    page = AppTest.from_file(APP).run()
                    page.chat_input[0].set_value("En LMU, sobreviraje").run()
                    self.assertEqual(len(page.error), 1)
                    self.assertIn("temporalmente saturado" if code == 503 else "Elige otro modelo", page.error[0].value)
                    self.assertNotIn("private-provider", page.error[0].value)
                    self.assertNotIn("api-key-secret", page.error[0].value)
                    self.assertFalse(page.chat_input[0].disabled)
                    self.assertFalse(page.selectbox[0].disabled)
                    page.run()
                    self.assertEqual(classifier.invoke.call_count, 1)
                    self.assertEqual(llm.invoke.call_count, 0 if stage == "classification" else 1)
                    llm.invoke.side_effect = None
                    llm.invoke.return_value = AIMessage(content="Prueba un cambio [LMU_USH_24].")
                    page.chat_input[0].set_value("En LMU, sobreviraje").run()
                    self.assertEqual(page.chat_message[-1].markdown[0].value, "Prueba un cambio.")
                    self.assertEqual(classifier.invoke.call_count, 2)

    @unittest.skipUnless((APP.parent / "data/corpus/mvp/preparado/corpus.jsonl").is_file(),
                         "Requiere el paquete privado para abrir los recursos reales.")
    def test_loads_real_resources_per_session_without_api_or_shared_checkpoints(self):
        import web_runtime
        build = web_runtime.crear_grafo
        graphs = []

        def record(*args, **kwargs):
            self.assertEqual(args[1].max_retries, 3)
            result = build(*args, **kwargs)
            graphs.append(result)
            return result

        with patch.object(ChatGoogleGenerativeAI, "invoke", side_effect=AssertionError("No API al arrancar")) as llm, \
             patch.object(GeminiRetrievalEmbeddings, "embed_documents", side_effect=AssertionError("No reindexar")) as embed, \
             patch.object(GeminiRetrievalEmbeddings, "embed_query", side_effect=AssertionError("No consultar")) as query, \
             patch("web_runtime.crear_grafo", side_effect=record):
            first = AppTest.from_file(APP, default_timeout=20).run()
            second = AppTest.from_file(APP, default_timeout=20).run()
            self.assertEqual(len(first.exception), 0)
            self.assertEqual(len(second.exception), 0)
            self.assertEqual(len(first.error), 0)
            self.assertEqual(len(second.error), 0)
            self.assertEqual(len(graphs), 2)
            self.assertIsNot(graphs[0].checkpointer, graphs[1].checkpointer)
            first.run()
            self.assertEqual(len(graphs), 2)
            target = next(model for model in web_runtime.MODELOS if model != first.selectbox[0].value)
            first.selectbox[0].select(target).run()
            self.assertEqual(len(first.exception), 0)
            self.assertEqual(len(graphs), 3)
            self.assertIs(graphs[0].checkpointer, graphs[2].checkpointer)
            self.assertIsNot(graphs[1].checkpointer, graphs[2].checkpointer)
            self.assertNotEqual(first.selectbox[0].value, second.selectbox[0].value)
            first.run()
            self.assertEqual(len(graphs), 3)
            self.assertNotEqual(first.session_state["conversacion"], second.session_state["conversacion"])
            llm.assert_not_called()
            embed.assert_not_called()
            query.assert_not_called()

    def test_submit_shows_clean_text_keeps_evidence_and_rerun_does_not_repeat_calls(self):
        app, store, llm, classifier = graph()
        with patch("web_runtime.cargar_agente", return_value=app):
            page = AppTest.from_file(APP).run()
            self.assertEqual(len(page.chat_message), 0)
            classifier.invoke.assert_not_called()
            page.chat_input[0].set_value("En LMU tengo sobreviraje").run()
            self.assertEqual(len(page.exception), 0)
            self.assertEqual(len(page.chat_message), 2)
            rendered = "\n".join(x.value for x in page.markdown)
            self.assertIn("Prueba un cambio.", rendered)
            self.assertNotIn("LMU_USH_24", rendered)
            self.assertNotIn("example.com", rendered)
            self.assertEqual(page.session_state["trazas"][0]["fuentes"][0]["id"], "LMU_USH_24")
            self.assertEqual(page.session_state["contexto"]["simulador"], "lmu")
            self.assertFalse(page.chat_input[0].disabled)
            self.assertIsNone(page.session_state["consulta_pendiente"])
            page.run()
            self.assertEqual(classifier.invoke.call_count, 1)
            self.assertEqual(llm.invoke.call_count, 1)
            self.assertEqual(store.similarity_search.call_count, 1)

    def test_natural_language_switch_waits_for_confirmation_and_preserves_session(self):
        app, store, _, _ = graph([decision(coche="Ferrari"), decision("acc"), decision("acc", accion="confirmar")])
        with patch("web_runtime.cargar_agente", return_value=app):
            page = AppTest.from_file(APP).run()
            page.chat_input[0].set_value("En LMU mi Ferrari sobrevira").run()
            config = page.session_state["conversacion"]
            page.chat_input[0].set_value("Ahora en ACC salto en los pianos").run()
            self.assertEqual(page.session_state["contexto"]["simulador"], "lmu")
            self.assertEqual(page.session_state["pendiente"]["simulador"], "acc")
            self.assertIn("Cambio pendiente", page.info[0].value)
            self.assertEqual(store.similarity_search.call_count, 1)
            page.chat_input[0].set_value("Sí, cambia").run()
            self.assertEqual(page.session_state["conversacion"], config)
            self.assertEqual(page.session_state["contexto"], {"simulador": "acc", "coche": None})
            self.assertIsNone(page.session_state["pendiente"])
            self.assertEqual(len(app.get_state(config).values["historial"]), 2)
            self.assertEqual(len(page.chat_message), 6)

    def test_new_conversation_clears_visible_history_evidence_and_graph_checkpoints(self):
        app, _, _, classifier = graph()
        with patch("web_runtime.cargar_agente", return_value=app):
            page = AppTest.from_file(APP).run()
            page.chat_input[0].set_value("En LMU, síntoma privado").run()
            previous = page.session_state["conversacion"]
            page.button[0].click().run()
            self.assertEqual(len(page.exception), 0)
            self.assertEqual(len(page.chat_message), 0)
            self.assertEqual(page.session_state["trazas"], [])
            self.assertIsNone(page.session_state["contexto"])
            self.assertNotEqual(page.session_state["conversacion"], previous)
            self.assertFalse(app.get_state(previous).values)
            self.assertEqual(classifier.invoke.call_count, 1)

    def test_generation_error_is_safe_and_does_not_repeat_graph_or_close_chat(self):
        app, _, llm, _ = graph()
        llm.invoke.side_effect = RuntimeError("private-provider-detail api-key-secret")
        with patch("web_runtime.cargar_agente", return_value=app):
            page = AppTest.from_file(APP).run()
            page.chat_input[0].set_value("En LMU, sobreviraje").run()
            self.assertEqual(len(page.exception), 0)
            self.assertEqual(len(page.error), 1)
            self.assertNotIn("private-provider", page.error[0].value)
            self.assertNotIn("api-key-secret", page.error[0].value)
            self.assertFalse(page.chat_input[0].disabled)
            page.run()
            self.assertEqual(llm.invoke.call_count, 1)

    def test_classifier_failure_is_presented_as_error_not_success(self):
        app, store, llm, _ = graph([RuntimeError("private-classifier")])
        with patch("web_runtime.cargar_agente", return_value=app):
            page = AppTest.from_file(APP).run()
            page.chat_input[0].set_value("Ayuda").run()
            self.assertEqual(len(page.error), 1)
            self.assertNotIn("private-classifier", page.error[0].value)
            self.assertEqual(page.session_state["trazas"][0]["error"], "clasificacion")
            store.similarity_search.assert_not_called()
            llm.invoke.assert_not_called()

    def test_startup_failure_never_displays_configuration_details(self):
        with patch("web_runtime.cargar_agente", side_effect=RuntimeError("private-api-key")):
            page = AppTest.from_file(APP).run()
            self.assertEqual(len(page.exception), 0)
            self.assertEqual(len(page.error), 1)
            self.assertNotIn("private-api-key", page.error[0].value)
            self.assertEqual(len(page.chat_input), 0)


if __name__ == "__main__":
    unittest.main()
