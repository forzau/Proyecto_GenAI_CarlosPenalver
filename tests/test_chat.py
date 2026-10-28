import json
import unittest
from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4
from langchain_core.messages import AIMessage
from tests.fakes import decision, graph


def chat_function():
    n = json.loads((Path(__file__).resolve().parents[1] / "notebooks/proyecto.ipynb").read_text(encoding="utf-8"))
    cell = next(c for c in n["cells"] if c["id"] == "chat-functions")
    namespace = {"uuid4": uuid4}
    exec(compile("".join(cell["source"]), "chat-functions", "exec"), namespace)
    return namespace["iniciar_chat"]


class ChatTest(unittest.TestCase):
    def run_chat(self, inputs, decisiones=None, **kwargs):
        app, store, llm, classifier = graph(decisiones)
        output = []
        config = chat_function()(app, leer=Mock(side_effect=inputs), escribir=output.append, **kwargs)
        return app, store, llm, classifier, output, config

    def test_removed_commands_never_call_model(self):
        app, store, llm, classifier, output, config = self.run_chat(
            ["", "/simulador acc", "/coche Ferrari", "/confirmar", "/cancelar", "/desconocido", "/salir"])
        classifier.invoke.assert_not_called()
        store.similarity_search.assert_not_called()
        llm.invoke.assert_not_called()
        self.assertIn("Chat cerrado.", output)

    def test_missing_simulator_and_followup_use_normal_conversation(self):
        app, store, llm, _, output, config = self.run_chat(
            ["Tengo sobreviraje", "En LMU", "Todavía no he cambiado nada", "/salir"],
            [decision("distinto", "falta_simulador"), decision(), decision()])
        self.assertEqual(app.get_state(config).values["contexto"]["simulador"], "lmu")
        self.assertEqual(len(app.get_state(config).values["historial"]), 6)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertTrue(any("Fuentes para revisión" in text for text in output))

    def test_new_conversation_discards_previous_simulator(self):
        app, store, _, classifier, output, config = self.run_chat(
            ["En LMU, síntoma privado", "/nuevo", "Sobreviraje", "/salir"],
            [decision(), decision("distinto", "falta_simulador")])
        self.assertFalse(app.get_state(config).values.get("contexto"))
        payload = json.loads(classifier.invoke.call_args.args[0][-1].content)
        self.assertIsNone(payload["contexto_confirmado"])
        self.assertNotIn("privado", str(payload))
        self.assertEqual(store.similarity_search.call_count, 1)

    def test_simulator_change_is_confirmed_in_natural_language(self):
        app, store, llm, _, output, config = self.run_chat(
            ["En LMU mi Ferrari sobrevira", "Ahora en ACC salto en los pianos", "Sí, cambia", "/salir"],
            [decision(coche="Ferrari"), decision("acc"), decision("acc", accion="confirmar")])
        state = app.get_state(config).values
        self.assertEqual(state["contexto"], {"simulador": "acc", "coche": None})
        self.assertEqual(len(state["historial"]), 2)
        self.assertEqual(store.similarity_search.call_count, 2)
        self.assertEqual(llm.invoke.call_count, 2)

    def test_classifier_error_does_not_close_chat_or_reveal_provider_details(self):
        app, store, llm, _, output, config = self.run_chat(
            ["Ayuda", "En LMU", "/salir"], [RuntimeError("private-provider-detail"), decision()])
        self.assertNotIn("private-provider-detail", str(output))
        self.assertTrue(any("No he podido identificar" in text for text in output))
        self.assertEqual(llm.invoke.call_count, 1)

    def test_generation_error_does_not_close_chat_or_retry(self):
        app, store, llm, _ = graph()
        llm.invoke.side_effect = [RuntimeError("private-provider-detail"), AIMessage(content="Respuesta [LMU_USH_24].")]
        output = []
        config = chat_function()(app, leer=Mock(side_effect=["En LMU, pregunta A", "Pregunta B", "/salir"]), escribir=output.append)
        self.assertNotIn("private-provider-detail", str(output))
        self.assertEqual(llm.invoke.call_count, 2)
        self.assertTrue(any("No se ha podido completar" in text for text in output))
        self.assertEqual(app.get_state(config).values["respuesta_piloto"], "Respuesta.")

    def test_clean_view_keeps_internal_evidence_and_eof_exits(self):
        app, _, _, _, output, config = self.run_chat(["Sobreviraje en LMU", "/salir"], ver_fuentes=False)
        self.assertNotIn("LMU_USH_24", str(output))
        self.assertIn("LMU_USH_24", app.get_state(config).values["respuesta"])
        output = []
        chat_function()(app, leer=Mock(side_effect=EOFError), escribir=output.append)
        self.assertIn("Chat cerrado.", output)


if __name__ == "__main__":
    unittest.main()
