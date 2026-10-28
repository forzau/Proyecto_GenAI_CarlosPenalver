import unittest
from langchain_core.messages import AIMessage, SystemMessage
from pydantic import ValidationError
from agent import Clasificacion
from tests.fakes import config, decision, ficha, graph


class AgentTest(unittest.TestCase):
    def test_routes_and_filters_for_all_three_simulators(self):
        for sim in ("lmu", "iracing", "acc"):
            with self.subTest(sim=sim):
                app, store, llm, classifier = graph([decision(sim)])
                result = app.invoke({"pregunta": f"Síntoma en {sim}"}, config())
                self.assertEqual(result["nodo_usado"], sim)
                self.assertEqual(result["contexto"]["simulador"], sim)
                self.assertEqual(store.similarity_search.call_args.kwargs["filter"], {"simulator": sim})
                messages = llm.invoke.call_args.args[0]
                self.assertIsInstance(messages[0], SystemMessage)
                self.assertIn(result["fuentes"][0]["id"], messages[-1].content)
                self.assertIn("unknown", messages[-1].content)
                self.assertEqual(result["uso"]["total_tokens"], 21)
                self.assertEqual(result["llamadas_modelo"], 2)
                self.assertEqual(classifier.invoke.call_count, 1)

    def test_graph_has_exact_classroom_branches(self):
        app, *_ = graph()
        self.assertEqual(set(app.get_graph().nodes),
                         {"__start__", "clasificar", "lmu", "iracing", "acc", "distinto", "__end__"})
        edges = {(e.source, e.target) for e in app.get_graph().edges}
        for sim in ("lmu", "iracing", "acc", "distinto"):
            self.assertIn(("clasificar", sim), edges)
            self.assertIn((sim, "__end__"), edges)

    def test_missing_and_ambiguous_simulator_ask_without_retrieval_or_generation(self):
        for motivo in ("falta_simulador", "ambiguo"):
            app, store, llm, _ = graph([decision("distinto", motivo)])
            result = app.invoke({"pregunta": "Tengo sobreviraje"}, config())
            self.assertIn("simulador", result["respuesta_piloto"])
            self.assertFalse(result.get("contexto"))
            self.assertEqual(result["llamadas_modelo"], 1)
            store.similarity_search.assert_not_called()
            llm.invoke.assert_not_called()

    def test_unrelated_question_redirects_without_retrieval_or_generation(self):
        app, store, llm, _ = graph([decision("distinto", "fuera_tema")])
        result = app.invoke({"pregunta": "Escribe un poema"}, config())
        self.assertIn("simracing", result["respuesta"])
        store.similarity_search.assert_not_called()
        llm.invoke.assert_not_called()
        self.assertFalse(result.get("historial"))

    def test_other_simulator_uses_general_prompt_and_explicit_caveat_without_chroma(self):
        app, store, llm, _ = graph([decision("distinto", "otro_simulador", otro="rFactor 2")])
        llm.invoke.side_effect = None
        llm.invoke.return_value = AIMessage(content="Comprueba si el deslizamiento aparece al acelerar.")
        result = app.invoke({"pregunta": "En rFactor 2 desliza al acelerar"}, config())
        self.assertIn("Mi especialidad es LMU, iRacing y ACC", result["respuesta"])
        self.assertIn("podría no ajustarse", result["respuesta"])
        self.assertEqual(result["contexto"]["simulador"], "rFactor 2")
        self.assertEqual(result["fuentes"], [])
        self.assertEqual(result["documentos"], [])
        self.assertIn("No dispones de documentos", llm.invoke.call_args.args[0][0].content)
        store.similarity_search.assert_not_called()

    def test_general_branch_rejects_fake_corpus_citations(self):
        app, _, llm, _ = graph([decision("distinto", "otro_simulador", otro="AMS2")])
        llm.invoke.side_effect = None
        llm.invoke.return_value = AIMessage(content="Prueba [LMU_USH_24].")
        with self.assertRaisesRegex(ValueError, "sin respaldo"):
            app.invoke({"pregunta": "Consulta en AMS2"}, config())

    def test_invalid_classification_or_provider_error_never_defaults_to_lmu(self):
        for output in (RuntimeError("private-provider-detail"),
                       {"parsed": {"tipo": "inventado"}, "raw": None, "parsing_error": None},
                       {"parsed": None, "raw": None, "parsing_error": ValueError("private")}):
            app, store, llm, _ = graph([output])
            result = app.invoke({"pregunta": "Ayuda"}, config())
            self.assertEqual(result["error"], "clasificacion")
            self.assertNotIn("private", result["respuesta"])
            store.similarity_search.assert_not_called()
            llm.invoke.assert_not_called()

    def test_empty_input_never_calls_provider(self):
        app, store, llm, classifier = graph()
        with self.assertRaises(ValueError):
            app.invoke({"pregunta": " "}, config())
        classifier.invoke.assert_not_called()
        store.similarity_search.assert_not_called()
        llm.invoke.assert_not_called()

    def test_inconsistent_structured_categories_are_rejected(self):
        for fields in ({"tipo": "acc", "motivo": "otro_simulador", "otro_simulador": "AC"},
                       {"tipo": "distinto", "motivo": "otro_simulador"},
                       {"tipo": "distinto", "motivo": "consulta"}):
            with self.assertRaises(ValidationError):
                Clasificacion(**fields)

    def test_wrong_simulator_documents_stop_generation(self):
        app, store, llm, _ = graph()
        store.similarity_search.side_effect = None
        store.similarity_search.return_value = [ficha("acc")]
        with self.assertRaisesRegex(ValueError, "otro simulador"):
            app.invoke({"pregunta": "Sobreviraje en LMU"}, config())
        llm.invoke.assert_not_called()

    def test_empty_retrieval_does_not_generate(self):
        app, store, llm, _ = graph()
        store.similarity_search.side_effect = None
        store.similarity_search.return_value = []
        result = app.invoke({"pregunta": "Consulta LMU"}, config())
        self.assertIn("No he recuperado", result["respuesta"])
        self.assertEqual(len(result["historial"]), 2)
        llm.invoke.assert_not_called()

    def test_citation_presentation_and_group_validation(self):
        for refs in ("[LMU_USH_24, LMU_USH_22]", "[LMU_USH_24], [LMU_USH_22]", "[LMU_USH_24] y [LMU_USH_22]"):
            app, store, llm, _ = graph()
            store.similarity_search.side_effect = None
            store.similarity_search.return_value = [ficha(), ficha(identifier="LMU_USH_22")]
            llm.invoke.side_effect = None
            llm.invoke.return_value = AIMessage(content=f"Prueba un ajuste {refs}.\n\n**Fuentes:**\nEnlaces")
            result = app.invoke({"pregunta": "Consulta"}, config())
            self.assertEqual(result["respuesta_piloto"], "Prueba un ajuste.")
            self.assertEqual(len(result["fuentes"]), 2)
            self.assertIn(refs, result["respuesta"])

    def test_invalid_citations_and_empty_text_are_not_successful_answers(self):
        for answer in ("Prueba [INVENTADA_99].", "   "):
            app, _, llm, _ = graph()
            llm.invoke.side_effect = None
            llm.invoke.return_value = AIMessage(content=answer)
            with self.assertRaises(ValueError):
                app.invoke({"pregunta": "Consulta"}, config())

    def test_known_conflict_remains_excluded_and_auditable(self):
        app, store, llm, _ = graph()
        store.similarity_search.side_effect = None
        store.similarity_search.return_value = [ficha(identifier="LMU_USH_08"), ficha()]
        result = app.invoke({"pregunta": "Presiones en LMU"}, config())
        self.assertEqual(len(result["documentos_recuperados"]), 2)
        self.assertEqual([d.metadata["id"] for d in result["documentos"]], ["LMU_USH_24"])
        self.assertEqual(result["fuentes_excluidas"][0]["id"], "LMU_USH_08")
        self.assertIn("contradictorias", llm.invoke.call_args.args[0][0].content)
        store.similarity_search.return_value = [ficha(identifier="LMU_USH_08")]
        llm.reset_mock()
        result = app.invoke({"pregunta": "Presiones"}, config())
        self.assertIn("contradictorias", result["respuesta"])
        llm.invoke.assert_not_called()


if __name__ == "__main__":
    unittest.main()
