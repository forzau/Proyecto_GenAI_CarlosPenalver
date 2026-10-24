import unittest
from unittest.mock import Mock

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, SystemMessage

from agent import crear_grafo


def ficha(simulador="lmu", identifier="LMU_USH_24"):
    return Document(page_content="Cambiar solo un ajuste por prueba.", metadata={
        "id": identifier, "simulator": simulador,
        "title": "Oversteer / Corner Exit / Low Speed", "locator": "Ruta / Low Speed",
        "url": "https://example.com/guia", "game_version": "unknown",
        "limitation": "Coche y versión no especificados.",
    })


class AgentTest(unittest.TestCase):
    def test_graph_retrieves_each_turn_and_passes_evidence_to_model(self):
        store, llm = Mock(), Mock()
        store.similarity_search.side_effect = [[ficha()], [ficha("acc", "ACC_DRIVER61_18")]]
        llm.invoke.side_effect = [
            AIMessage(content="Según la guía [LMU_USH_24], prueba un cambio.",
                      usage_metadata={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}),
            AIMessage(content=[{"type": "text", "text": "Guía histórica [ACC_DRIVER61_18]."}]),
        ]
        graph = crear_grafo(store, llm, "Reglas de sistema")
        first = graph.invoke({"pregunta": "Sobreviraje al salir", "simulador": "lmu"})
        messages = llm.invoke.call_args.args[0]
        self.assertIsInstance(messages[0], SystemMessage)
        self.assertEqual(messages[0].content, "Reglas de sistema")
        for expected in ("Sobreviraje al salir", "LMU_USH_24", "Ruta / Low Speed",
                         "unknown", "Coche y versión no especificados.", "Cambiar solo"):
            self.assertIn(expected, messages[1].content)
        self.assertEqual(first["fuentes"][0]["id"], "LMU_USH_24")
        self.assertEqual(first["uso"]["total_tokens"], 15)
        second = graph.invoke({"pregunta": "Pianos", "simulador": "acc"})
        self.assertEqual(second["fuentes"][0]["id"], "ACC_DRIVER61_18")
        self.assertNotIn("LMU_USH_24", llm.invoke.call_args.args[0][1].content)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertEqual(store.similarity_search.call_args.kwargs["filter"], {"simulator": "acc"})

    def test_invalid_input_and_cross_simulator_documents_never_call_llm(self):
        for question, simulator in (("", "lmu"), ("Ayuda", "general"), ("Ayuda", None)):
            with self.subTest(question=question, simulator=simulator):
                store, llm = Mock(), Mock()
                with self.assertRaises(ValueError):
                    crear_grafo(store, llm, "Reglas").invoke(
                        {"pregunta": question, "simulador": simulator})
                store.similarity_search.assert_not_called()
                llm.invoke.assert_not_called()
        store, llm = Mock(), Mock()
        store.similarity_search.return_value = [ficha("acc")]
        with self.assertRaisesRegex(ValueError, "otro simulador"):
            crear_grafo(store, llm, "Reglas").invoke({"pregunta": "Ayuda", "simulador": "lmu"})
        llm.invoke.assert_not_called()

    def test_no_results_returns_limit_without_calling_llm(self):
        store, llm = Mock(), Mock()
        store.similarity_search.return_value = []
        result = crear_grafo(store, llm, "Reglas").invoke({"pregunta": "Ayuda", "simulador": "lmu"})
        self.assertIn("No he recuperado", result["respuesta"])
        self.assertEqual(result["fuentes"], [])
        self.assertIn("no puedo recomendar", result["respuesta_piloto"])
        llm.invoke.assert_not_called()

    def test_pilot_text_hides_references_and_preserves_review_evidence(self):
        variants = [
            "Prueba un cambio [LMU_USH_24].\n\n**Fuentes:**\n[LMU_USH_24] https://example.com/guia",
            "Prueba un cambio [LMU_USH_24](https://example.com/guia).\n\n### Referencias\n- [LMU_USH_24] Ruta / Low Speed",
        ]
        for original in variants:
            with self.subTest(original=original):
                store, llm = Mock(), Mock()
                store.similarity_search.return_value = [ficha()]
                llm.invoke.return_value = AIMessage(content=original)
                result = crear_grafo(store, llm, "Reglas").invoke(
                    {"pregunta": "Ayuda", "simulador": "lmu"})
                self.assertEqual(result["respuesta_piloto"], "Prueba un cambio.")
                self.assertEqual(result["respuesta"], original)
                self.assertEqual(result["fuentes"][0]["id"], "LMU_USH_24")
                self.assertEqual(result["documentos"][0].metadata["id"], "LMU_USH_24")
                self.assertEqual(llm.invoke.call_count, 1)

    def test_fabricated_citation_and_empty_response_are_not_returned(self):
        for answer in ("Ajusta el coche [INVENTADA_99]", "   "):
            with self.subTest(answer=answer):
                store, llm = Mock(), Mock()
                store.similarity_search.return_value = [ficha()]
                llm.invoke.return_value = AIMessage(content=answer)
                with self.assertRaises(ValueError):
                    crear_grafo(store, llm, "Reglas").invoke(
                        {"pregunta": "Ayuda", "simulador": "lmu"})

    def test_api_error_is_not_reported_as_a_success_or_retried(self):
        store, llm = Mock(), Mock()
        store.similarity_search.return_value = [ficha()]
        llm.invoke.side_effect = RuntimeError("Cuota agotada")
        with self.assertRaisesRegex(RuntimeError, "Cuota agotada"):
            crear_grafo(store, llm, "Reglas").invoke({"pregunta": "Ayuda", "simulador": "lmu"})
        self.assertEqual(llm.invoke.call_count, 1)

    def test_grouped_citations_are_checked_and_hidden_in_pilot_text(self):
        store, llm = Mock(), Mock()
        store.similarity_search.return_value = [ficha(), ficha(identifier="LMU_USH_22")]
        graph = crear_grafo(store, llm, "Reglas")
        for refs in ("[LMU_USH_24, LMU_USH_22]", "[LMU_USH_24], [LMU_USH_22]", "[LMU_USH_24] y [LMU_USH_22]"):
            llm.invoke.return_value = AIMessage(content=f"Prueba un ajuste {refs}.")
            result = graph.invoke({"pregunta": "Ayuda", "simulador": "lmu"})
            self.assertEqual(result["respuesta_piloto"], "Prueba un ajuste.")
            self.assertEqual(len(result["fuentes"]), 2)
        llm.invoke.return_value = AIMessage(content="Prueba [LMU_USH_24, INVENTADA_99].")
        with self.assertRaisesRegex(ValueError, "no recuperados"):
            graph.invoke({"pregunta": "Ayuda", "simulador": "lmu"})

    def test_conflicting_source_is_kept_for_review_but_not_used_as_evidence(self):
        store, llm = Mock(), Mock()
        store.similarity_search.return_value = [ficha(identifier="LMU_USH_08"), ficha(identifier="LMU_USH_11")]
        llm.invoke.return_value = AIMessage(content="Falta una cifra exacta [LMU_USH_11].")
        graph = crear_grafo(store, llm, "Reglas")
        result = graph.invoke({"pregunta": "Presiones", "simulador": "lmu"})
        self.assertEqual(len(result["documentos_recuperados"]), 2)
        self.assertEqual([d.metadata["id"] for d in result["documentos"]], ["LMU_USH_11"])
        self.assertEqual(result["fuentes_excluidas"][0]["id"], "LMU_USH_08")
        self.assertIn("contradictorias", llm.invoke.call_args.args[0][0].content)
        llm.invoke.return_value = AIMessage(content="Cita excluida [LMU_USH_08].")
        with self.assertRaisesRegex(ValueError, "no recuperados"):
            graph.invoke({"pregunta": "Presiones", "simulador": "lmu"})
        store.similarity_search.return_value = [ficha(identifier="LMU_USH_08")]
        llm.reset_mock()
        result = graph.invoke({"pregunta": "Presiones", "simulador": "lmu"})
        self.assertIn("contradictorias", result["respuesta_piloto"])
        self.assertIn("contradictorias", result["respuesta"])
        llm.invoke.assert_not_called()

if __name__ == "__main__":
    unittest.main()
