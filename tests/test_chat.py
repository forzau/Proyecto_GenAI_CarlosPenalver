import json
import unittest
from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from agent import crear_grafo


def chat_function():
    notebook = json.loads((Path(__file__).resolve().parents[1] / "notebooks/proyecto.ipynb").read_text(encoding="utf-8"))
    cell = next(c for c in notebook["cells"] if c["id"] == "chat-functions")
    namespace = {"uuid4": uuid4}
    exec(compile("".join(cell["source"]), "chat-functions", "exec"), namespace)
    return namespace["iniciar_chat"]


def local_graph():
    ids = {"lmu": "LMU_USH_24", "acc": "ACC_DRIVER61_18", "iracing": "IR_CHRIS_HAYE_02"}
    store, llm = Mock(), Mock()

    def retrieve(query, k, filter):
        sim = filter["simulator"]
        return [Document(page_content="Texto ficticio local.", metadata={
            "id": ids[sim], "simulator": sim, "url": "https://example.com", "locator": "Celda local"})]

    def respond(messages):
        sim = store.similarity_search.call_args.kwargs["filter"]["simulator"]
        return AIMessage(content=f"Prueba un cambio [{ids[sim]}].")

    store.similarity_search.side_effect = retrieve
    llm.invoke.side_effect = respond
    return crear_grafo(store, llm, "Reglas", checkpointer=InMemorySaver()), store, llm


class ChatTest(unittest.TestCase):
    def run_chat(self, inputs, **kwargs):
        app, store, llm = local_graph()
        output = []
        config = chat_function()(app, leer=Mock(side_effect=inputs), escribir=output.append, **kwargs)
        return app, store, llm, output, config

    def test_exit_empty_and_invalid_commands_do_not_call_api(self):
        app, store, llm, output, config = self.run_chat(
            ["", "/desconocido", "/confirmar", "/simulador rf2", "/coche", "/salir"])
        store.similarity_search.assert_not_called()
        llm.invoke.assert_not_called()
        self.assertIn("Chat cerrado.", output)

    def test_followup_keeps_same_conversation_and_displays_review_sources(self):
        app, store, llm, output, config = self.run_chat(["Sobreviraje lento", "Todavía no he cambiado nada", "/salir"])
        self.assertEqual(len(app.get_state(config).values["historial"]), 4)
        self.assertIn("Sobreviraje lento", store.similarity_search.call_args.args[0])
        self.assertEqual(llm.invoke.call_count, 2)
        self.assertTrue(any("Fuentes para revisión" in text for text in output))

    def test_new_conversation_does_not_inherit_previous_pilot(self):
        app, store, llm, output, config = self.run_chat(["Mensaje privado anterior", "/nuevo", "Otro síntoma", "/salir"])
        self.assertEqual(len(app.get_state(config).values["historial"]), 2)
        self.assertNotIn("Mensaje privado anterior", str(llm.invoke.call_args.args[0]))
        self.assertEqual(store.similarity_search.call_count, 2)

    def test_simulator_selection_and_confirmation_process_pending_question_once(self):
        app, store, llm, output, config = self.run_chat(
            ["Sobreviraje", "/simulador acc", "Pianos", "/confirmar", "/salir"], coche="Ferrari")
        state = app.get_state(config).values
        self.assertEqual(state["contexto"], {"simulador": "acc", "coche": None})
        self.assertEqual(state["historial"][0].content, "Pianos")
        self.assertEqual(len(state["historial"]), 2)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertEqual(llm.invoke.call_count, 2)

    def test_car_name_with_spaces_can_be_confirmed(self):
        app, store, llm, output, config = self.run_chat(
            ["Sobreviraje", "/coche Porsche 911 GT3 R", "Consulta del nuevo coche", "/confirmar", "/salir"], coche="Ferrari")
        self.assertEqual(app.get_state(config).values["contexto"]["coche"], "Porsche 911 GT3 R")
        self.assertEqual(llm.invoke.call_count, 2)

    def test_cancel_restores_original_context_for_next_question(self):
        app, store, llm, output, config = self.run_chat(
            ["Sobreviraje", "/simulador acc", "Pianos", "/cancelar", "Seguimos en LMU", "/salir"], coche="Ferrari")
        self.assertEqual(app.get_state(config).values["contexto"], {"simulador": "lmu", "coche": "Ferrari"})
        self.assertEqual(len(app.get_state(config).values["historial"]), 4)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertTrue(all(c.kwargs["filter"] == {"simulator": "lmu"} for c in store.similarity_search.call_args_list))

    def test_api_failure_does_not_close_chat_or_show_raw_error(self):
        app, store, llm = local_graph()
        llm.invoke.side_effect = [RuntimeError("private-provider-detail"), AIMessage(content="Respuesta [LMU_USH_24].")]
        output = []
        config = chat_function()(app, leer=Mock(side_effect=["Pregunta A", "Pregunta B", "/salir"]), escribir=output.append)
        self.assertNotIn("private-provider-detail", str(output))
        self.assertEqual(llm.invoke.call_count, 2)
        self.assertTrue(any("No se ha podido completar" in text for text in output))
        self.assertEqual(app.get_state(config).values["respuesta_piloto"], "Respuesta.")

    def test_clean_presentation_keeps_internal_citations_and_eof_exits(self):
        app, store, llm, output, config = self.run_chat(["Sobreviraje", "/salir"], ver_fuentes=False)
        self.assertNotIn("LMU_USH_24", str(output))
        self.assertIn("LMU_USH_24", app.get_state(config).values["respuesta"])
        self.assertEqual(len(app.get_state(config).values["fuentes"]), 1)
        output = []
        chat_function()(app, leer=Mock(side_effect=EOFError), escribir=output.append)
        self.assertIn("Chat cerrado.", output)


if __name__ == "__main__":
    unittest.main()
