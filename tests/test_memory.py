import json
import unittest
from langchain_core.messages import AIMessage, HumanMessage
from tests.fakes import config, decision, graph


class MemoryTest(unittest.TestCase):
    def test_followup_preserves_roles_context_and_retrieves_again(self):
        app, store, llm, classifier = graph([decision(coche="Ferrari GT3"), decision()])
        app.invoke({"pregunta": "En LMU, sobreviraje al salir con Ferrari GT3"}, config())
        result = app.invoke({"pregunta": "Todavía no he cambiado nada. ¿Qué debo observar?"}, config())
        self.assertEqual(result["contexto"], {"simulador": "lmu", "coche": "Ferrari GT3"})
        self.assertEqual([m.type for m in result["historial"]], ["human", "ai", "human", "ai"])
        self.assertIn("Todavía no", store.similarity_search.call_args.args[0])
        self.assertIn("sobreviraje", store.similarity_search.call_args.args[0])
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertNotIn("LMU_USH_24", str(result["historial"]))
        self.assertEqual(json.loads(classifier.invoke.call_args.args[0][-1].content)["contexto_confirmado"]["simulador"], "lmu")
        self.assertIsInstance(llm.invoke.call_args.args[0][1], HumanMessage)

    def test_applied_change_is_still_a_pilot_report(self):
        app, _, llm, _ = graph()
        app.invoke({"pregunta": "En LMU, sobreviraje"}, config())
        report = "He reducido la barra trasera. Ahora noto menos sobreviraje."
        result = app.invoke({"pregunta": report}, config())
        self.assertEqual(result["historial"][2].content, report)
        self.assertIn(report, llm.invoke.call_args.args[0][-1].content)

    def test_initial_clarification_keeps_symptom_and_car(self):
        app, store, _, _ = graph([decision("distinto", "falta_simulador", coche="Ferrari"), decision()])
        first = app.invoke({"pregunta": "Con Ferrari tengo sobreviraje al acelerar"}, config())
        self.assertFalse(first.get("contexto"))
        result = app.invoke({"pregunta": "Estoy en LMU"}, config())
        self.assertIn("sobreviraje al acelerar", store.similarity_search.call_args.args[0])
        self.assertEqual(result["contexto"]["coche"], "Ferrari")
        self.assertEqual(len(result["historial"]), 4)

    def test_simulator_change_requests_confirmation_without_retrieval_then_resets(self):
        app, store, llm, _ = graph([decision(coche="Ferrari"), decision("acc"), decision("acc", accion="confirmar")])
        initial = app.invoke({"pregunta": "En LMU mi Ferrari tiene sobreviraje"}, config())
        pending = app.invoke({"pregunta": "Ahora estoy en ACC y salto en los pianos"}, config())
        self.assertTrue(pending["requiere_confirmacion"])
        self.assertEqual(pending["contexto"], initial["contexto"])
        self.assertEqual(len(pending["historial"]), 2)
        self.assertEqual(pending["documentos"], [])
        self.assertEqual(store.similarity_search.call_count, 1)
        self.assertEqual(llm.invoke.call_count, 1)
        result = app.invoke({"pregunta": "Sí, cambia"}, config())
        self.assertEqual(result["contexto"], {"simulador": "acc", "coche": None})
        self.assertFalse(result["requiere_confirmacion"])
        self.assertIsNone(result["contexto_pendiente"])
        self.assertEqual(result["historial"][0].content, "Ahora estoy en ACC y salto en los pianos")
        self.assertEqual(len(result["historial"]), 2)
        self.assertNotIn("Ferrari", str(llm.invoke.call_args.args[0]))
        self.assertNotIn("sobreviraje", store.similarity_search.call_args.args[0])
        self.assertEqual(store.similarity_search.call_args.kwargs["filter"], {"simulator": "acc"})

    def test_car_change_and_fill_unknown_car_are_distinct(self):
        app, store, _, _ = graph([decision(), decision(coche="Ferrari"), decision(coche="Porsche"), decision(accion="confirmar")])
        app.invoke({"pregunta": "Sobreviraje en LMU"}, config())
        filled = app.invoke({"pregunta": "Mi coche es un Ferrari"}, config())
        self.assertFalse(filled["requiere_confirmacion"])
        self.assertEqual(len(filled["historial"]), 4)
        pending = app.invoke({"pregunta": "Ahora conduzco un Porsche y sobrevira"}, config())
        self.assertTrue(pending["requiere_confirmacion"])
        self.assertEqual(store.similarity_search.call_count, 2)
        result = app.invoke({"pregunta": "Confirmo el cambio"}, config())
        self.assertEqual(result["contexto"]["coche"], "Porsche")
        self.assertEqual(len(result["historial"]), 2)

    def test_cancel_preserves_context_and_does_not_generate(self):
        app, store, llm, _ = graph([decision(coche="Ferrari"), decision("acc"), decision(accion="cancelar"), decision()])
        app.invoke({"pregunta": "En LMU mi Ferrari sobrevira"}, config())
        app.invoke({"pregunta": "En ACC tengo un problema"}, config())
        result = app.invoke({"pregunta": "No, seguimos como antes"}, config())
        self.assertFalse(result["requiere_confirmacion"])
        self.assertIsNone(result["contexto_pendiente"])
        self.assertEqual(result["contexto"], {"simulador": "lmu", "coche": "Ferrari"})
        self.assertEqual(len(result["historial"]), 2)
        self.assertEqual(llm.invoke.call_count, 1)
        app.invoke({"pregunta": "Todavía no he cambiado nada"}, config())
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertTrue(all(c.kwargs["filter"] == {"simulator": "lmu"} for c in store.similarity_search.call_args_list))

    def test_other_simulator_change_and_followup_never_use_supported_corpus(self):
        other = lambda accion="continuar": decision("distinto", "otro_simulador", otro="AMS2", accion=accion)
        app, store, llm, _ = graph([decision(), other(), other("confirmar"), other()])
        app.invoke({"pregunta": "En LMU, sobreviraje"}, config())
        app.invoke({"pregunta": "Ahora estoy en AMS2 y sobrevira"}, config())
        llm.invoke.side_effect = None
        llm.invoke.return_value = AIMessage(content="Compara el síntoma en las mismas condiciones.")
        result = app.invoke({"pregunta": "Sí, cambia"}, config())
        self.assertEqual(result["contexto"]["simulador"], "AMS2")
        self.assertNotIn("LMU", str(result["historial"][0].content))
        self.assertEqual(result["fuentes"], [])
        app.invoke({"pregunta": "Ahora ocurre al frenar"}, config())
        self.assertEqual(store.similarity_search.call_count, 1)

    def test_threads_do_not_share_context_or_car(self):
        app, _, llm, _ = graph([decision(coche="Ferrari"), decision("acc")])
        app.invoke({"pregunta": "Síntoma privado en LMU"}, config("a"))
        result = app.invoke({"pregunta": "Pianos en ACC"}, config("b"))
        self.assertEqual(result["contexto"], {"simulador": "acc", "coche": None})
        self.assertNotIn("privado", str(llm.invoke.call_args.args[0]))
        self.assertEqual(len(result["historial"]), 2)
        self.assertEqual(app.get_state(config("a")).values["contexto"]["coche"], "Ferrari")

    def test_classifier_failure_and_generation_failure_clear_prior_answer(self):
        for where in ("clasificar", "responder"):
            app, _, llm, classifier = graph()
            first = app.invoke({"pregunta": "Sobreviraje en LMU"}, config())
            if where == "clasificar":
                classifier.invoke.side_effect = RuntimeError("private")
                result = app.invoke({"pregunta": "Ahora cambia el síntoma"}, config())
                self.assertEqual(result["error"], "clasificacion")
            else:
                llm.invoke.side_effect = RuntimeError("private")
                with self.assertRaises(RuntimeError):
                    app.invoke({"pregunta": "Ahora cambia el síntoma"}, config())
                result = app.get_state(config()).values
                self.assertEqual(result["respuesta"], "")
            self.assertEqual(result["fuentes"], [])
            self.assertNotEqual(result["respuesta"], first["respuesta"])
            self.assertEqual(result["contexto"], first["contexto"])

    def test_old_citations_cannot_support_new_turn(self):
        from tests.fakes import ficha
        app, store, llm, _ = graph()
        app.invoke({"pregunta": "En LMU, sobreviraje"}, config())
        store.similarity_search.side_effect = None
        store.similarity_search.return_value = [ficha(identifier="LMU_USH_22")]
        llm.invoke.side_effect = None
        llm.invoke.return_value = AIMessage(content="Lo anterior [LMU_USH_24].")
        with self.assertRaisesRegex(ValueError, "no recuperados"):
            app.invoke({"pregunta": "¿Y ahora?"}, config())
        self.assertNotIn("LMU_USH_24", str(llm.invoke.call_args.args[0]))


if __name__ == "__main__":
    unittest.main()
