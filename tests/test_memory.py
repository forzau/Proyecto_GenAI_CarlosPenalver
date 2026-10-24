import unittest
from unittest.mock import Mock

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from agent import crear_grafo


def config(name):
    return {"configurable": {"thread_id": name}}


def doc(sim="lmu"):
    identifier = {"lmu": "LMU_USH_24", "acc": "ACC_DRIVER61_18"}[sim]
    return Document(page_content="Una ficha local de prueba.", metadata={
        "id": identifier, "simulator": sim, "url": "https://example.com/guia",
        "locator": "Celda de prueba", "game_version": "unknown",
    })


def graph():
    store, llm = Mock(), Mock()
    store.similarity_search.return_value = [doc()]
    llm.invoke.return_value = AIMessage(content="Prueba reducir la barra trasera [LMU_USH_24].")
    return crear_grafo(store, llm, "Reglas de memoria", checkpointer=InMemorySaver()), store, llm


class MemoryTest(unittest.TestCase):
    def test_followup_uses_history_before_retrieval_and_preserves_speakers(self):
        app, store, llm = graph()
        first = app.invoke({"pregunta": "Sobreviraje al salir de curva lenta", "simulador": "lmu",
                            "coche": "Ferrari GT3"}, config("a"))
        second = app.invoke({"pregunta": "Todavía no he cambiado nada. ¿Qué debo observar?"}, config("a"))
        query = store.similarity_search.call_args.args[0]
        for text in ("Sobreviraje", "Prueba reducir la barra", "Todavía no he cambiado nada"):
            self.assertIn(text, query)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertEqual(second["contexto"]["coche"], "Ferrari GT3")
        self.assertEqual([m.type for m in second["historial"]], ["human", "ai", "human", "ai"])
        self.assertNotIn("LMU_USH_24", first["historial"][1].content)
        messages = llm.invoke.call_args.args[0]
        self.assertIsInstance(messages[1], HumanMessage)
        self.assertIsInstance(messages[2], AIMessage)
        self.assertIn("Todavía no he cambiado nada", messages[-1].content)
        self.assertIn("Ferrari GT3", messages[-1].content)

    def test_applied_change_and_observation_remain_pilot_reports(self):
        app, _, llm = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu"}, config("a"))
        report = "He reducido la barra trasera. Ahora noto menos sobreviraje."
        result = app.invoke({"pregunta": report}, config("a"))
        self.assertEqual(result["historial"][2].content, report)
        self.assertIsInstance(result["historial"][2], HumanMessage)
        self.assertIn(report, llm.invoke.call_args.args[0][-1].content)

    def test_conversations_are_isolated_and_new_thread_has_no_history(self):
        app, store, llm = graph()
        app.invoke({"pregunta": "Síntoma privado A", "simulador": "lmu", "coche": "Ferrari"}, config("a"))
        store.similarity_search.return_value = [doc("acc")]
        llm.invoke.return_value = AIMessage(content="Prueba ACC [ACC_DRIVER61_18].")
        result = app.invoke({"pregunta": "Síntoma B", "simulador": "acc", "coche": "Porsche"}, config("b"))
        self.assertEqual(len(result["historial"]), 2)
        self.assertNotIn("Síntoma privado A", str(llm.invoke.call_args.args[0]))
        self.assertNotIn("Ferrari", str(llm.invoke.call_args.args[0]))
        self.assertEqual(app.get_state(config("a")).values["contexto"]["simulador"], "lmu")
        self.assertEqual(store.similarity_search.call_args.kwargs["filter"], {"simulator": "acc"})

    def test_simulator_change_waits_for_confirmation_without_api(self):
        app, store, llm = graph()
        first = app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu", "coche": "Ferrari"}, config("a"))
        result = app.invoke({"pregunta": "Pianos", "simulador": "acc"}, config("a"))
        self.assertTrue(result["requiere_confirmacion"])
        self.assertEqual(result["contexto"], first["contexto"])
        self.assertEqual(result["contexto_pendiente"], {"simulador": "acc", "coche": None})
        self.assertEqual(len(result["historial"]), 2)
        self.assertEqual(result["fuentes"], [])
        self.assertEqual(result["documentos"], [])
        self.assertEqual(store.similarity_search.call_count, 1)
        self.assertEqual(llm.invoke.call_count, 1)

    def test_confirmed_simulator_change_discards_old_car_history_and_sources(self):
        app, store, llm = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu", "coche": "Ferrari"}, config("a"))
        app.invoke({"pregunta": "Pianos", "simulador": "acc"}, config("a"))
        store.similarity_search.return_value = [doc("acc")]
        llm.invoke.return_value = AIMessage(content="Prueba ACC [ACC_DRIVER61_18].")
        result = app.invoke({"confirmar_contexto": True}, config("a"))
        self.assertEqual(result["contexto"], {"simulador": "acc", "coche": None})
        self.assertEqual(len(result["historial"]), 2)
        self.assertEqual(result["historial"][0].content, "Pianos")
        self.assertNotIn("Ferrari", str(llm.invoke.call_args.args[0]))
        self.assertNotIn("Sobreviraje", store.similarity_search.call_args.args[0])
        self.assertFalse(result["confirmar_contexto"])
        self.assertEqual(result["fuentes"][0]["id"], "ACC_DRIVER61_18")
        again = app.invoke({"pregunta": "Frenada", "simulador": "iracing"}, config("a"))
        self.assertTrue(again["requiere_confirmacion"])
        self.assertEqual(llm.invoke.call_count, 2)

    def test_car_change_requires_confirmation_and_filling_unknown_car_does_not_reset(self):
        app, store, llm = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu"}, config("a"))
        filled = app.invoke({"pregunta": "Es un Ferrari", "coche": "Ferrari"}, config("a"))
        self.assertFalse(filled["requiere_confirmacion"])
        self.assertEqual(len(filled["historial"]), 4)
        waiting = app.invoke({"pregunta": "Sobreviraje del Porsche", "coche": "Porsche"}, config("a"))
        self.assertTrue(waiting["requiere_confirmacion"])
        self.assertEqual(store.similarity_search.call_count, 2)
        result = app.invoke({"confirmar_contexto": True}, config("a"))
        self.assertEqual(result["contexto"]["coche"], "Porsche")
        self.assertEqual(len(result["historial"]), 2)
        self.assertNotIn("Ferrari", str(llm.invoke.call_args.args[0]))

    def test_cancel_by_reselecting_original_context_keeps_original_session(self):
        app, _, _ = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu", "coche": "Ferrari"}, config("a"))
        app.invoke({"pregunta": "Pianos", "simulador": "acc"}, config("a"))
        result = app.invoke({"pregunta": "Seguimos en LMU", "simulador": "lmu", "coche": "Ferrari"}, config("a"))
        self.assertFalse(result["requiere_confirmacion"])
        self.assertIsNone(result["contexto_pendiente"])
        self.assertEqual(len(result["historial"]), 4)

    def test_api_failure_does_not_keep_old_answer_or_duplicate_pilot_on_retry(self):
        app, _, llm = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu"}, config("a"))
        llm.invoke.side_effect = RuntimeError("Cuota agotada")
        for _ in range(2):
            with self.assertRaisesRegex(RuntimeError, "Cuota agotada"):
                app.invoke({"pregunta": "Todavía no he cambiado nada"}, config("a"))
        state = app.get_state(config("a")).values
        self.assertEqual(state["respuesta"], "")
        self.assertEqual(state["fuentes"], [])
        self.assertEqual(len(state["historial"]), 3)
        self.assertIsInstance(state["historial"][-1], HumanMessage)

    def test_no_documents_keeps_pilot_turn_and_limit_without_llm(self):
        app, store, llm = graph()
        store.similarity_search.return_value = []
        result = app.invoke({"pregunta": "Algo sin cobertura", "simulador": "lmu"}, config("a"))
        self.assertEqual(len(result["historial"]), 2)
        self.assertEqual(result["historial"][-1].content, result["respuesta_piloto"])
        llm.invoke.assert_not_called()

    def test_previous_answer_cannot_supply_a_citation_missing_this_turn(self):
        app, store, llm = graph()
        app.invoke({"pregunta": "Sobreviraje", "simulador": "lmu"}, config("a"))
        current = doc()
        current.metadata["id"] = "LMU_USH_22"
        store.similarity_search.return_value = [current]
        llm.invoke.return_value = AIMessage(content="La respuesta anterior lo decía [LMU_USH_24].")
        with self.assertRaisesRegex(ValueError, "no recuperados"):
            app.invoke({"pregunta": "¿Y ahora?"}, config("a"))
        self.assertNotIn("LMU_USH_24", str(llm.invoke.call_args.args[0]))


if __name__ == "__main__":
    unittest.main()
